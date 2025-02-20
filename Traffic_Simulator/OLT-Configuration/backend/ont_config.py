from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from olt_telnet import telnet_sessions

# Shared data store
shared_data = {}

ont_router = APIRouter()


class SubmitData(BaseModel):
    input: str


class ONTConfig(BaseModel):
    ip: str
    ont_id: str
    config_command: str


@ont_router.post("/configure")
async def configure_ont(config: ONTConfig):
    """Configure ONT using an active OLT session"""
    tn_data = telnet_sessions.get(config.ip)
    if not tn_data:
        raise HTTPException(
            status_code=400, detail="No active OLT session. Connect first."
        )

    tn, _ = tn_data  # Retrieve session
    try:
        tn.write(config.config_command.encode("ascii") + b"\n")
        response = tn.read_until(b">", timeout=5).decode("ascii")
        return {
            "message": f"ONT {config.ont_id} configured.",
            "output": response.strip(),
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"ONT configuration failed: {str(e)}"
        )


@ont_router.post("/submit")
async def submit_data(data: SubmitData):
    """Submit data to the shared store"""
    shared_data["input"] = data.input
    print(f"Received data: {shared_data['input']}")
    return {"status": "success", "received": shared_data["input"]}


@ont_router.get("/get_data")
async def get_data():
    """Retrieve stored data"""
    if "input" in shared_data:
        print(f"Sending data: {shared_data['input']}")
        return {"data": shared_data["input"]}
    raise HTTPException(status_code=404, detail="No data available")
