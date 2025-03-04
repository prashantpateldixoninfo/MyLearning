import asyncio
from concurrent.futures import ThreadPoolExecutor
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from olt_telnet import connect_to_olt, telnet_sessions, close_telnet_session, check_telnet_status
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
    command: str

class PortConfigRequest(BaseModel):
    ip: str
    uplink_port: str
    vlan_id: str
    pon_port: str


@olt_router.post("/connect_telnet")
async def connect(olt: OLTConnectionRequest):
    """Connect to OLT"""
    print("Connecting to OLT", olt.ip, olt.username, olt.password)
    tn, message = connect_to_olt(olt.ip, olt.username, olt.password)
    if tn:
        commands = [
            "enable",
            "config",
            "idle-timeout 240",
            "history-command max-size 100",
        ]
        # Run Telnet commands asynchronously
        loop = asyncio.get_running_loop()
        output = await loop.run_in_executor(executor, execute_telnet_commands_batch, olt.ip, commands)

        print(f"Backend Executed Commands Output: {output}")
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

@olt_router.post("/execute")
async def execute_command(command: OLTCommand):
    """Execute command on OLT"""
    tn_data = telnet_sessions.get(command.ip)
    if not tn_data:
        raise HTTPException(status_code=400, detail="No active session. Connect first.")

    tn, _ = tn_data  # Retrieve session
    try:
        tn.write(command.command.encode("ascii") + b"\n")
        response = tn.read_until(b">", timeout=5).decode("ascii")
        telnet_sessions[command.ip] = (tn, time.time())  # Refresh session timestamp
        return {"output": response.strip()}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Command execution failed: {str(e)}"
        )

def execute_telnet_commands_batch(ip: str, commands: list):
    """Execute multiple commands on an active Telnet session step-by-step with pagination & <cr> handling."""
    tn_data = telnet_sessions.get(ip)
    if not tn_data:
        raise HTTPException(status_code=400, detail=f"No active session for OLT {ip}. Please connect first.")

    tn, _ = tn_data  # Retrieve session
    try:
        output = []
        for cmd in commands:
            tn.write(cmd.encode("ascii") + b"\n")
            time.sleep(0.2)  # Small delay to allow OLT to process the command
            
            response = ""
            while True:
                chunk = tn.read_until(b">", timeout=2).decode("ascii")
                response += chunk
                
                # Check for pagination (Press 'Q' or ---- More)
                if "Press 'Q' to break" in chunk or "---- More" in chunk:
                    tn.write(b" ")  # Send Space to get next page
                    time.sleep(0.2)  # Allow time for more data
                # Check for <cr> prompts (example: { <cr>|inner-vlan<K>|to<K> }:)
                elif "{ <cr>" in chunk:
                    tn.write(b"\n")  # Send Enter to continue execution
                    time.sleep(0.2)
                else:
                    break  # Exit loop when full output is received

            output.append(f"{cmd} → {response.strip()}")  # Store command and response
        
        # Refresh session timestamp
        telnet_sessions[ip] = (tn, time.time())
        
        return "\n".join(output)  # Return all outputs as a formatted string
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch command execution failed: {str(e)}")

def execute_telnet_commands_batch_Fast(ip: str, commands: list):
    """Execute multiple commands on an active Telnet session as a batch."""
    tn_data = telnet_sessions.get(ip)
    if not tn_data:
        raise HTTPException(status_code=400, detail=f"No active session for OLT {ip}. Please connect first.")
    
    tn, _ = tn_data  # Retrieve session
    try:
        full_command = "\n".join(commands) + "\n"
        tn.write(full_command.encode("ascii"))
        time.sleep(.5)  # Small delay to ensure execution
        
        response = tn.read_very_eager().decode("ascii")
        telnet_sessions[ip] = (tn, time.time())  # Refresh session timestamp
        
        return response.strip()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch command execution failed: {str(e)}")

@olt_router.post("/configure_port_setting")
async def configure_olt_port(config: PortConfigRequest):
    """
    Configures the OLT port with VLAN and upstream port settings.
    """
    try:
        print(f"Backend Configure IP: {config.ip}, Uplink Port: {config.uplink_port}, VLAN: {config.vlan_id}, PON Port: {config.pon_port}")

        # Construct Huawei CLI commands
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

        print(f"Backend Executing commands: {commands}")
        
        # Run Telnet commands asynchronously
        loop = asyncio.get_running_loop()
        output = await loop.run_in_executor(executor, execute_telnet_commands_batch, config.ip, commands)

        print(f"Backend Executed Commands Output: {output}")
        return {"message": "Port configuration applied!", "output": output}
    
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=f"During port configuration | Reason: {e.detail}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"During port configuration | Reason: {str(e)}")

@olt_router.post("/display_port_status_details")
async def display_port_status_details(config: PortConfigRequest):
    """
    Display the OLT port with VLAN and upstream port settings.
    """
    try:
        print(f"Backend Display Details IP: {config.ip}, Uplink Port: {config.uplink_port}, VLAN: {config.vlan_id}, PON Port: {config.pon_port}")

        # Construct Huawei CLI commands
        olt_slot, olt_port = config.pon_port.rsplit("/", 1)
        upstream_slot, upstream_port = config.uplink_port.rsplit("/", 1)
        commands = [
            f"display vlan {config.vlan_id}",
            f"display port vlan {config.uplink_port}",
            f"display ont autofind all"
        ]

        print(f"Backend Executing commands: {commands}")
        
        # Run Telnet commands asynchronously
        loop = asyncio.get_running_loop()
        output = await loop.run_in_executor(executor, execute_telnet_commands_batch, config.ip, commands)

        print(f"Backend Executed Commands Output: {output}")
        return {"message": "Displaying the port configurations in details!", "output": output}
  
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=f"During port status | Reason: {e.detail}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"During port status | Reason: {str(e)}")

def extract_port_information(output, user_pon_port):
    """
    Extract Uplink Port, Native VLAN, State, PON Port, and all ONT Serial Numbers belonging to the given PON Port.
    """

    # Pattern to extract OLT Port details
    olt_pattern = r"\s*(\d+ /\d+/\d+)\s+(\d+)\s+(\w+)"

    # Pattern to extract ONT Port and ONT Serial Number(s)
    ont_pattern = r"F/S/P\s*:\s*(\d+/\d+/\d+).*?Ont SN\s*:\s*([\w\d]+)\s*\((.*?)\)"

    # Extract OLT Port Information
    olt_match = re.search(olt_pattern, output)
    olt_port = olt_match.group(1).strip() if olt_match else "N/A"
    native_vlan = olt_match.group(2).strip() if olt_match else "N/A"
    state = olt_match.group(3).strip() if olt_match else "N/A"

    # Extract all ONT Port and ONT Serial Number(s)
    ont_matches = re.findall(ont_pattern, output, re.DOTALL)

    # Collect ONT SNs belonging to the user-specified PON Port
    ont_sn_list = [
        f"{ont_sn} ({ont_vendor})"
        for pon_port, ont_sn, ont_vendor in ont_matches
        if pon_port.strip() == user_pon_port.strip()
    ]

    # If no ONTs found for the specified PON Port, return default message
    ont_sn_result = ", ".join(ont_sn_list) if ont_sn_list else "No ONT found"

    return {
        "Uplink Port": olt_port,
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
    try:
        print(f"Backend Display Summary IP: {config.ip}, Uplink Port: {config.uplink_port}, VLAN: {config.vlan_id}, PON Port: {config.pon_port}")

        # Construct Huawei CLI commands
        olt_slot, olt_port = config.pon_port.rsplit("/", 1)
        upstream_slot, upstream_port = config.uplink_port.rsplit("/", 1)
        commands = [
            f"display vlan {config.vlan_id}",
            f"display port vlan {config.uplink_port}",
            f"display ont autofind all"
        ]

        print(f"Backend Executing commands: {commands}")
        
        # Run Telnet commands asynchronously
        loop = asyncio.get_running_loop()
        output = await loop.run_in_executor(executor, execute_telnet_commands_batch, config.ip, commands)

        print(f"Backend Executed Commands Output: {output}")
        # Extract information
        port_info = extract_port_information(output, config.pon_port)
        print(f"Extracted VLAN Info: {port_info}")

        if port_info:
            output_string = "\n".join([
                f"Uplink Port: {port_info.get('Uplink Port', 'N/A')}",
                f"Native VLAN: {port_info.get('Native VLAN', 'N/A')}",
                f"State: {port_info.get('State', 'N/A')}",
                f"PON Port: {port_info.get('PON Port', 'N/A')}",
                f"ONT Serial Num: {port_info.get('ONT Serial Num', 'No ONT found')}"
            ])
        else:
            output_string = "No Port information found."
        print(f"Output String:\n{output_string}")
        return {"message": "Displaying the port configurations as summary!", "output": output_string}
  
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=f"During port status | Reason: {e.detail}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"During port status | Reason: {str(e)}")

@olt_router.post("/delete_port_setting")
async def unconfig_olt_port(config: PortConfigRequest):
    """
    UnConfigures the OLT port with VLAN and upstream port settings.
    """
    try:
        print(f"Backend Delete IP: {config.ip}, Uplink Port: {config.uplink_port}, VLAN: {config.vlan_id}, PON Port: {config.pon_port}")

        # Construct Huawei CLI commands
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

        print(f"Backend Executing commands: {commands}")
        
        # Run Telnet commands asynchronously
        loop = asyncio.get_running_loop()
        output = await loop.run_in_executor(executor, execute_telnet_commands_batch, config.ip, commands)

        print(f"Backend Executed Commands Output: {output}")
        return {"message": "Port configuration deleted!", "output": output}
    
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=f"During port unconfiguration | Reason: {e.detail}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"During port unconfiguration | Reason: {str(e)}")
