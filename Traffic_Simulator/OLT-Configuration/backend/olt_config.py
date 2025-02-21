from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from olt_telnet import connect_to_olt, telnet_sessions, close_telnet_session
import time

olt_router = APIRouter()


class OLTConnection(BaseModel):
    ip: str = Field(..., pattern=r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
    username: str = Field(..., min_length=1)
    password: str = Field(..., min_length=4)

class DisconnectRequest(BaseModel):
    ip: str

class OLTCommand(BaseModel):
    ip: str
    command: str


@olt_router.post("/connect")
async def connect(olt: OLTConnection):
    """Connect to OLT"""
    print("Connecting to OLT", olt.ip, olt.username, olt.password)
    tn, message = connect_to_olt(olt.ip, olt.username, olt.password)
    if tn:
        return {"message": message}
    raise HTTPException(status_code=400, detail=message)

@olt_router.post("/disconnect")
async def disconnect_olt(request: DisconnectRequest):
    """Disconnect the Telnet session for the given OLT IP."""
    ip = request.ip  # Extract the IP from the request body
    if close_telnet_session(ip):
        return {"message": f"Disconnected from OLT {ip} successfully."}
    raise HTTPException(status_code=400, detail=f"No active session found for OLT {ip}.")

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

