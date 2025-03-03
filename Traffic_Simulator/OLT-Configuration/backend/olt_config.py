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
    olt_port: str
    vlan_id: str
    upstream_port: str
    ip: str  # OLT IP address

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
                
                # Check for pagination (Press 'Q' or ---- More ----)
                if "Press 'Q' to break" in chunk or "---- More ----" in chunk:
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
        print(f"Backend Configuring OLT Port: {config.olt_port}, VLAN: {config.vlan_id}, Upstream: {config.upstream_port}, IP: {config.ip}")

        # Construct Huawei CLI commands
        olt_slot, olt_port = config.olt_port.rsplit("/", 1)
        upstream_slot, upstream_port = config.upstream_port.rsplit("/", 1)
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
        print(f"Backend Display OLT Port: {config.olt_port}, VLAN: {config.vlan_id}, Upstream: {config.upstream_port}")

        # Construct Huawei CLI commands
        olt_slot, olt_port = config.olt_port.rsplit("/", 1)
        upstream_slot, upstream_port = config.upstream_port.rsplit("/", 1)
        commands = [
            f"display vlan {config.vlan_id}",
            f"display port vlan {config.upstream_port}",
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

def extract_vlan_info(output):
    """Extract F/S/P, Native VLAN, and State from the given text."""
    pattern = r"\s*(\d+ /\d+/\d+)\s+(\d+)\s+(\w+)"
    
    match = re.search(pattern, output)
    if match:
        olt_port, native_vlan, state = match.groups()
        return {
            "F/S/P": olt_port.strip(),
            "Native VLAN": native_vlan.strip(),
            "State": state.strip()
        }
    return None

@olt_router.post("/display_port_status_summary")
async def display_port_status_summary(config: PortConfigRequest):
    """
    Display the OLT port with VLAN and upstream port settings.
    """
    try:
        print(f"Backend Display OLT Port: {config.olt_port}, VLAN: {config.vlan_id}, Upstream: {config.upstream_port}")

        # Construct Huawei CLI commands
        olt_slot, olt_port = config.olt_port.rsplit("/", 1)
        upstream_slot, upstream_port = config.upstream_port.rsplit("/", 1)
        commands = [
            f"display vlan {config.vlan_id}",
            f"display port vlan {config.upstream_port}",
            f"display ont autofind all"
        ]

        print(f"Backend Executing commands: {commands}")
        
        # Run Telnet commands asynchronously
        loop = asyncio.get_running_loop()
        output = await loop.run_in_executor(executor, execute_telnet_commands_batch, config.ip, commands)

        print(f"Backend Executed Commands Output: {output}")
        # Extract information
        vlan_info = extract_vlan_info(output)
        print(f"Extracted VLAN Info: {vlan_info}")

        if vlan_info:
            output_string = "\n".join([
                f"F/S/P: {vlan_info.get('F/S/P', 'N/A')}",
                f"Native VLAN: {vlan_info.get('Native VLAN', 'N/A')}",
                f"State: {vlan_info.get('State', 'N/A')}"
            ])
        else:
            output_string = "No VLAN information found."
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
        print(f"Backend UnConfiguring OLT Port: {config.olt_port}, VLAN: {config.vlan_id}, Upstream: {config.upstream_port}")

        # Construct Huawei CLI commands
        olt_slot, olt_port = config.olt_port.rsplit("/", 1)
        upstream_slot, upstream_port = config.upstream_port.rsplit("/", 1)
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
