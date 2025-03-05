from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import asyncio

ont_router = APIRouter()

class ONTProfileRequest(BaseModel):
    ip: str
    profile_id: int
    tcont_id: int
    gemport_id: int

class ONTServiceRequest(BaseModel):
    ip: str
    serial_number: str
    ont_id: int

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

@ont_router.post("/create_profile")
async def create_ont_profile(config: ONTProfileRequest):
    commands = [
        f"ont-profile create {config.profile_id} tcont {config.tcont_id} gemport {config.gemport_id}"
    ]
    output = await asyncio.get_running_loop().run_in_executor(None, execute_telnet_commands_batch, config.ip, commands)
    return {"message": "ONT Profile Created", "output": output}

@ont_router.post("/status_profile")
async def status_ont_profile(config: ONTProfileRequest):
    commands = [
        f"display ont-profile {config.profile_id}"
    ]
    output = await asyncio.get_running_loop().run_in_executor(None, execute_telnet_commands_batch, config.ip, commands)
    return {"message": "ONT Profile Status Retrieved", "output": output}

@ont_router.post("/delete_profile")
async def delete_ont_profile(config: ONTProfileRequest):
    commands = [
        f"undo ont-profile {config.profile_id}"
    ]
    output = await asyncio.get_running_loop().run_in_executor(None, execute_telnet_commands_batch, config.ip, commands)
    return {"message": "ONT Profile Deleted", "output": output}

@ont_router.post("/create_service")
async def create_ont_service(config: ONTServiceRequest):
    commands = [
        f"interface gpon 0/0",
        f"ont add {config.ont_id} sn {config.serial_number} profile {config.ont_id}"
    ]
    output = await asyncio.get_running_loop().run_in_executor(None, execute_telnet_commands_batch, config.ip, commands)
    return {"message": "ONT Service Created", "output": output}

@ont_router.post("/status_service")
async def status_ont_service(config: ONTServiceRequest):
    commands = [
        f"display ont info {config.ont_id}"
    ]
    output = await asyncio.get_running_loop().run_in_executor(None, execute_telnet_commands_batch, config.ip, commands)
    return {"message": "ONT Service Status Retrieved", "output": output}

@ont_router.post("/delete_service")
async def delete_ont_service(config: ONTServiceRequest):
    commands = [
        f"interface gpon 0/0",
        f"ont delete {config.ont_id}"
    ]
    output = await asyncio.get_running_loop().run_in_executor(None, execute_telnet_commands_batch, config.ip, commands)
    return {"message": "ONT Service Deleted", "output": output}
