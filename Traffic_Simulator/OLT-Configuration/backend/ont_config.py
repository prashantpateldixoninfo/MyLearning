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
    vlan_id: int

class ONTServiceRequest(BaseModel):
    ip: str
    serial_number: str
    ont_id: int
    vlan_id: int
    pon_port: int

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

    try:
        response = await asyncio.get_running_loop().run_in_executor(None, execute_telnet_commands_batch, config.ip, commands)

        # Handle different response scenarios
        if response["status"] == "success":
            return {"message": "ONT Profiles Created", "output": response["output"]}
        elif response["status"] == "error":
            raise HTTPException(
                status_code=400,
                detail={"message": response["message"], "output": response["output"]}
            )
        elif response["status"] == "critical":
            raise HTTPException(
                status_code=500,
                detail={"message": response["message"], "output": response["output"]}
            )
    except HTTPException as http_err:
        raise http_err  # Re-raise HTTP errors
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"message": f"Unexpected error: {str(e)}", "output": ""}
        )

@ont_router.post("/status_profile_details")
async def status_ont_profile_details(config: ONTProfileRequest):
    commands = [
            f"display dba-profile profile-id {config.profile_id}",
            f"display ont-lineprofile gpon profile-id {config.profile_id}",
            f"display ont-srvprofile gpon profile-id {config.profile_id}",
    ]
    try:
        response = await asyncio.get_running_loop().run_in_executor(None, execute_telnet_commands_batch, config.ip, commands)

        # Handle different response scenarios
        if response["status"] == "success":
            return {"message": "ONT Profiles Details Status", "output": response["output"]}
        elif response["status"] == "error":
            raise HTTPException(
                status_code=400,
                detail={"message": response["message"], "output": response["output"]}
            )
        elif response["status"] == "critical":
            raise HTTPException(
                status_code=500,
                detail={"message": response["message"], "output": response["output"]}
            )
    except HTTPException as http_err:
        raise http_err  # Re-raise HTTP errors
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"message": f"Unexpected error: {str(e)}", "output": ""}
        )

@ont_router.post("/status_profile_summary")
async def status_ont_profile_summary(config: ONTProfileRequest):
    commands = [
            f"display dba-profile all",
            f"display ont-lineprofile gpon all",
            f"display ont-srvprofile gpon all",
    ]
    try:
        response = await asyncio.get_running_loop().run_in_executor(None, execute_telnet_commands_batch, config.ip, commands)

        # Handle different response scenarios
        if response["status"] == "success":
            return {"message": "ONT Profiles Summary Status", "output": response["output"]}
        elif response["status"] == "error":
            raise HTTPException(
                status_code=400,
                detail={"message": response["message"], "output": response["output"]}
            )
        elif response["status"] == "critical":
            raise HTTPException(
                status_code=500,
                detail={"message": response["message"], "output": response["output"]}
            )
    except HTTPException as http_err:
        raise http_err  # Re-raise HTTP errors
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"message": f"Unexpected error: {str(e)}", "output": ""}
        )

@ont_router.post("/delete_profile")
async def delete_ont_profile(config: ONTProfileRequest):
    commands = [
        f"undo ont-srvprofile gpon profile-id {config.profile_id}",
        f"undo ont-lineprofile gpon profile-id {config.profile_id}",
        f"dba-profile delete profile-id {config.profile_id}"
    ]
    try:
        response = await asyncio.get_running_loop().run_in_executor(None, execute_telnet_commands_batch, config.ip, commands)

        # Handle different response scenarios
        if response["status"] == "success":
            return {"message": "ONT Profiles Deleted", "output": response["output"]}
        elif response["status"] == "error":
            raise HTTPException(
                status_code=400,
                detail={"message": response["message"], "output": response["output"]}
            )
        elif response["status"] == "critical":
            raise HTTPException(
                status_code=500,
                detail={"message": response["message"], "output": response["output"]}
            )
    except HTTPException as http_err:
        raise http_err  # Re-raise HTTP errors
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"message": f"Unexpected error: {str(e)}", "output": ""}
        )

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
