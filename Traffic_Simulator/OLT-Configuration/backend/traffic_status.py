from fastapi import APIRouter
from pydantic import BaseModel
import asyncio
from olt_telnet import handle_command_execution

traffic_router = APIRouter()

class OLTStatusCommand(BaseModel):
    ip: str

class OLTTrafficStatusCommand(BaseModel):
    ip: str
    pon_port: str
    ont_id: int

class EthPortTrafficStatusCommand(BaseModel):
    ip: str
    uplink_port: str


@traffic_router.post("/olt_port_statistics")
async def olt_port_statistics(config: OLTTrafficStatusCommand):
    pon_slot, pon_port = config.pon_port.rsplit("/", 1)
    commands = [
        f"interface gpon {pon_slot}",
        f"display statistics ont {pon_port} {config.ont_id}",
        f"quit",
    ]
    return await handle_command_execution(config.ip, commands, "OLT Port Statistics")

@traffic_router.post("/eth_port_statistics")
async def eth_port_statistics(config: EthPortTrafficStatusCommand):
    upstream_slot, upstream_port = config.uplink_port.rsplit("/", 1)
    commands = [
        f"interface eth {upstream_slot}",
        f"display statistics performance {upstream_port} current-15minutes",
        f"quit",
    ]
    return await handle_command_execution(config.ip, commands, "Ethernet Port Statistics")


@traffic_router.post("/save_configurations")
async def save_olt_configurations(ont: OLTStatusCommand):
    """Save the OLT configuration."""
    commands = [
        "save"
    ]
    return await handle_command_execution(ont.ip, commands, "ALL Current Configurations saved successfully!")
