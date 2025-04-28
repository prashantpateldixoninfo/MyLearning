from fastapi import APIRouter
from pydantic import BaseModel
import asyncio
from olt_telnet import handle_command_execution

debug_router = APIRouter()

class DebugCommand(BaseModel):
    ip: str
    cmd: str

@debug_router.post("/execute_commands")
async def execute_cmds(config: DebugCommand):
    print(config.cmd)
    command_list = [line.strip() for line in config.cmd.splitlines() if line.strip()]
    if not command_list:
        return {"message": "No commands to execute"}
    # Add commands to the list for execution
    return await handle_command_execution(config.ip, command_list, "Commands Executed Successfully")
