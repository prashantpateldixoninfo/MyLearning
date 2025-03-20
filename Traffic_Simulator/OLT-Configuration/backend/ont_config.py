from fastapi import APIRouter
from pydantic import BaseModel
import asyncio
from olt_telnet import handle_command_execution

ont_router = APIRouter()

class ONTCommand(BaseModel):
    ip: str

class ONTProfileRequest(BaseModel):
    ip: str
    profile_id: int
    tcont_id: int
    gemport_id: int
    vlan_id: int

class ONTServiceRequest(BaseModel):
    ip: str
    serial_number: str
    ont_id: int
    vlan_id: str
    pon_port: str
    gemport_id: int
    profile_id: int

@ont_router.post("/create_profile")
async def create_ont_profile(config: ONTProfileRequest):
    commands = [
        f"dba-profile add profile-id {config.profile_id} type4  max 1024000",
        f"ont-lineprofile gpon profile-id {config.profile_id}",
        f"tcont {config.tcont_id} dba-profile-id {config.profile_id}",
        f"gem add {config.gemport_id} eth tcont {config.tcont_id}",
        f"gem mapping {config.gemport_id} 1 vlan {config.vlan_id}",
        f"commit",
        f"quit",
        f"ont-srvprofile gpon profile-id {config.profile_id}",
        f"ont-port eth adaptive",
        f"port vlan eth 1-4 transparent",
        f"commit",
        f"quit"
    ]
    return await handle_command_execution(config.ip, commands, "ONT Profiles Created")

@ont_router.post("/status_profile_details")
async def status_ont_profile_details(config: ONTProfileRequest):
    commands = [
        f"display dba-profile profile-id {config.profile_id}",
        f"display ont-lineprofile gpon profile-id {config.profile_id}",
        f"display ont-srvprofile gpon profile-id {config.profile_id}",
    ]
    return await handle_command_execution(config.ip, commands, "ONT Profiles Details Status")

@ont_router.post("/status_profile_summary")
async def status_ont_profile_summary(config: ONTProfileRequest):
    commands = [
        f"display dba-profile all",
        f"display ont-lineprofile gpon all",
        f"display ont-srvprofile gpon all",
    ]
    return await handle_command_execution(config.ip, commands, "ONT Profiles Summary Status")

@ont_router.post("/delete_profile")
async def delete_ont_profile(config: ONTProfileRequest):
    commands = [
        f"undo ont-srvprofile gpon profile-id {config.profile_id}",
        f"undo ont-lineprofile gpon profile-id {config.profile_id}",
        f"dba-profile delete profile-id {config.profile_id}"
    ]
    return await handle_command_execution(config.ip, commands, "ONT Profiles Deleted")

@ont_router.post("/create_service")
async def create_ont_service(config: ONTServiceRequest):
    pon_slot, pon_port = config.pon_port.rsplit("/", 1)
    commands = [
        f"interface gpon {pon_slot}",
        f"ont confirm {pon_port} ontid {config.ont_id} sn-auth {config.serial_number} omci ont-lineprofile-id {config.profile_id} ont-srvprofile-id {config.profile_id}",
        "quit",
        f"service-port {config.ont_id} vlan {config.vlan_id} gpon {config.pon_port} ont {config.ont_id} gemport {config.gemport_id} multi-service user-vlan {config.vlan_id}"
    ]
    return await handle_command_execution(config.ip, commands, "ONT Service Created")

@ont_router.post("/status_service_details")
async def ont_service_status_details(config: ONTServiceRequest):
    pon_slot, pon_port = config.pon_port.rsplit("/", 1)
    commands = [
        f"interface gpon {pon_slot}",
        f"display ont info {pon_port} {config.ont_id}",
        "quit",
        f"display service-port vlan {config.vlan_id}",
        f"display service-port port {config.pon_port}"
    ]
    return await handle_command_execution(config.ip, commands, "ONT Service Details Status")

@ont_router.post("/status_service_summary")
async def ont_service_status_summary(config: ONTServiceRequest):
    pon_slot, pon_port = config.pon_port.rsplit("/", 1)
    commands = [
        f"interface gpon {pon_slot}",
        f"display ont info {pon_port} all",
        "quit",
        f"display service-port all",
        f"display mac-address vlan {config.vlan_id}"
    ]
    return await handle_command_execution(config.ip, commands, "ONT Service Summary Status")

@ont_router.post("/delete_service")
async def delete_ont_service(config: ONTServiceRequest):
    pon_slot, pon_port = config.pon_port.rsplit("/", 1)
    commands = [
        f"undo service-port {config.ont_id}",
        f"interface gpon {pon_slot}",
        f"ont delete {pon_port} {config.ont_id}",
        "quit",
    ]
    return await handle_command_execution(config.ip, commands, "ONT Service Deleted")

@ont_router.post("/save_configurations")
async def save_ont_configurations(ont: ONTCommand):
    """Save the ONT configuration."""
    commands = [
        "save"
    ]
    return await handle_command_execution(ont.ip, commands, "ALL Current Configurations saved successfully!")
