from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from olt_telnet import connect_to_olt, telnet_sessions, close_telnet_session
import time

olt_router = APIRouter()


class OLTConnection(BaseModel):
    ip: str = Field(..., pattern=r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
    username: str = Field(..., min_length=1)
    password: str = Field(..., min_length=4)


class OLTCommand(BaseModel):
    ip: str
    command: str


@olt_router.post("/connect")
async def connect(olt: OLTConnection):
    """Connect to OLT"""
    tn, message = connect_to_olt(olt.ip, olt.username, olt.password)
    if tn:
        return {"message": message}
    raise HTTPException(status_code=400, detail=message)


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


@olt_router.post("/close")
async def close_session(ip: str):
    """Close OLT Telnet session"""
    if close_telnet_session(ip):
        return {"message": "Telnet session closed successfully."}
    raise HTTPException(status_code=400, detail="No active session found.")
