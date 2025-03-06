from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import asyncio
from olt_telnet import execute_telnet_commands_batch

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
