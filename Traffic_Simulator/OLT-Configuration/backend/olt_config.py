import asyncio
from concurrent.futures import ThreadPoolExecutor
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from olt_telnet import (
    connect_to_olt,
    telnet_sessions,
    close_telnet_session,
    check_telnet_status,
    execute_telnet_commands_batch,
    handle_command_execution,
)
import time
import re

olt_router = APIRouter()
executor = ThreadPoolExecutor()

class OLTConnectionRequest(BaseModel):
    ip: str = Field(..., pattern=r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
    username: str = Field(..., min_length=1)
    password: str = Field(..., min_length=4)

class SessionStatusRequest(BaseModel):
    ip: str

class DisconnectRequest(BaseModel):
    ip: str

class OLTCommand(BaseModel):
    ip: str

class PortConfigRequest(BaseModel):
    ip: str
    uplink_port: str
    vlan_id: str
    pon_port: str

@olt_router.post("/connect_telnet")
async def connect(olt: OLTConnectionRequest):
    """Connect to OLT"""
    tn, message = connect_to_olt(olt.ip, olt.username, olt.password)
    if tn:
        commands = [
            "idle-timeout 240",
            "history-command max-size 100",
        ]
        # Run Telnet commands asynchronously
        loop = asyncio.get_running_loop()
        output = await loop.run_in_executor(executor, execute_telnet_commands_batch, olt.ip, commands)

        return {"message": message, "output": output}
    raise HTTPException(status_code=400, detail=message)

@olt_router.post("/display_telnet")
async def display_olt_connection(session: SessionStatusRequest):
    """Display the Telnet session for the given OLT IP."""
    ip = session.ip
    status, msg = (lambda d: (d["status"], d["message"]))(check_telnet_status(ip))
    if status == "Active":
        return {"message": f"{msg} {ip} OLT"}
    elif status == "Inactive":
        raise HTTPException(status_code=400, detail=f"{msg} {ip} OLT")

@olt_router.post("/disconnect_telnet")
async def disconnect_olt(request: DisconnectRequest):
    """Disconnect the Telnet session for the given OLT IP."""
    ip = request.ip  # Extract the IP from the request body
    if close_telnet_session(ip):
        return {"message": f"Disconnected from OLT {ip}"}
    raise HTTPException(status_code=400, detail=f"No active session found for OLT {ip}. Unable to Delete")

@olt_router.post("/configure_port_setting")
async def configure_olt_port(config: PortConfigRequest):
    """
    Configures the OLT port with VLAN and upstream port settings.
    """
    olt_slot, olt_port = config.pon_port.rsplit("/", 1)
    upstream_slot, upstream_port = config.uplink_port.rsplit("/", 1)
    commands = [
        f"interface gpon {olt_slot}",
        f"port {olt_port} ont-auto-find enable",
        "quit",
        f"vlan {config.vlan_id} smart",
        f"port vlan {config.vlan_id} {upstream_slot} {upstream_port}",
        f"interface eth {upstream_slot}",
        f"native-vlan {upstream_port} vlan {config.vlan_id}",
        "quit",
    ]
    return await handle_command_execution(config.ip, commands, "Port configuration applied!")

@olt_router.post("/display_port_status_details")
async def display_port_status_details(config: PortConfigRequest):
    """
    Display the OLT port with VLAN and upstream port settings.
    """
    commands = [
        f"display vlan {config.vlan_id}",
        f"display port vlan {config.uplink_port}",
        f"display ont autofind all"
    ]
    return await handle_command_execution(config.ip, commands, "Displaying the port configurations in details!")

def extract_port_information(output, user_uplink_port, user_pon_port):
    """
    Extracts Native VLAN from 'Native VLAN:' key, State for the given Uplink Port,
    and all ONT Serial Numbers for the given PON Port.
    """
    # Extract Native VLAN from "Native VLAN:" key
    native_vlan_match = re.search(r"Native VLAN:\s*(\d+)", output)
    native_vlan = native_vlan_match.group(1).strip() if native_vlan_match else "N/A"

    # Extract State for the given Uplink Port
    state_pattern = r"\s*(\d+ /\d+/\d+)\s+(\d+)\s+(\w+)"
    state_match = re.search(state_pattern, output)
    state = state_match.group(3).strip() if state_match else "N/A"

    # Extract ONT Port and ONT Serial Number(s)
    ont_pattern = r"F/S/P\s*:\s*(\d+/\d+/\d+).*?Ont SN\s*:\s*([\w\d]+)\s*\((.*?)\)"
    ont_matches = re.findall(ont_pattern, output, re.DOTALL)

    # Filter ONT Serial Numbers belonging to the specified PON Port
    ont_sn_list = [
        f"{ont_sn} ({ont_vendor})"
        for pon_port, ont_sn, ont_vendor in ont_matches
        if pon_port.strip() == user_pon_port.strip()
    ]

    # If no ONTs found, return default message
    ont_sn_result = ", ".join(ont_sn_list) if ont_sn_list else "No ONT found"

    return {
        "Uplink Port": user_uplink_port,
        "Native VLAN": native_vlan,
        "State": state,
        "PON Port": user_pon_port,
        "ONT Serial Num": ont_sn_result
    }

@olt_router.post("/display_port_status_summary")
async def display_port_status_summary(config: PortConfigRequest):
    """
    Display the OLT port with VLAN and upstream port settings.
    """
    commands = [
        f"display vlan {config.vlan_id}",
        f"display port vlan {config.uplink_port}",
        f"display ont autofind all"
    ]
    result =  await handle_command_execution(config.ip, commands, "Displaying the port configurations in summary!")
    try:
        port_info = extract_port_information(result['output'], config.uplink_port, config.pon_port)
        if port_info:
            filter_output = "\n".join([
                "------------------Uplink Info------------------\n"
                f"Uplink Port: {port_info.get('Uplink Port', 'N/A')}",
                f"Native VLAN: {port_info.get('Native VLAN', 'N/A')}",
                f"State: {port_info.get('State', 'N/A')}",
                "------------------OLT PON Info------------------\n"
                f"PON Port: {port_info.get('PON Port', 'N/A')}",
                f"ONT Serial Num: {port_info.get('ONT Serial Num', 'No ONT found')}"
            ])
        else:
            filter_output = "No Port information found."
        return {"message": result['message'], "output": filter_output}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=f"During port status summary | Reason: {e.detail}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"During port status summary| Reason: {str(e)}")

@olt_router.post("/delete_port_setting")
async def unconfig_olt_port(config: PortConfigRequest):
    """
    UnConfigures the OLT port with VLAN and upstream port settings.
    """
    olt_slot, olt_port = config.pon_port.rsplit("/", 1)
    upstream_slot, upstream_port = config.uplink_port.rsplit("/", 1)
    commands = [
        f"interface eth {upstream_slot}",
        f"native-vlan {upstream_port} vlan 1",
        "quit",
        f"undo port vlan {config.vlan_id} {upstream_slot} {upstream_port}",
        f"undo vlan {config.vlan_id}",
        f"interface gpon {olt_slot}",
        f"port {olt_port} ont-auto-find disable",
        "quit"
    ]
    return await handle_command_execution(config.ip, commands, "Port configuration deleted!")

@olt_router.post("/save_configurations")
async def save_olt_configurations(olt: OLTCommand):
    """Save the OLT configuration."""
    commands = [
        "save"
    ]
    return await handle_command_execution(olt.ip, commands, "ALL Current Configurations saved successfully!")