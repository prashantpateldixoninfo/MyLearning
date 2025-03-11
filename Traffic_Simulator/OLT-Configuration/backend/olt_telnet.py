import telnetlib
import threading
import asyncio
import time
from fastapi import HTTPException

# Telnet session management
telnet_sessions = {}
session_timeout = 300  # 5-minute timeout

def cleanup_idle_sessions():
    """Remove idle Telnet sessions"""
    while True:
        current_time = time.time()
        for ip, (tn, last_active) in list(telnet_sessions.items()):
            if current_time - last_active > session_timeout:
                print(f"Closing idle session for {ip}")
                tn.close()
                del telnet_sessions[ip]
        time.sleep(10)

# Start cleanup thread
threading.Thread(target=cleanup_idle_sessions, daemon=True).start()

def connect_to_olt(ip: str, username: str, password: str):
    """Establish or reuse a Telnet connection"""
    try:
        if ip in telnet_sessions:
            telnet_sessions[ip] = (
                telnet_sessions[ip][0],
                time.time(),
            )  # Refresh session
            return telnet_sessions[ip][0], "Reusing existing session!"

        tn = telnetlib.Telnet(ip, timeout=5)

        # Step 1: Authenticate with Username
        tn.read_until(b"Username:", timeout=3)
        tn.write(username.encode("ascii") + b"\n")

        # Step 2: Authenticate with Password
        tn.read_until(b"Password:", timeout=3)
        tn.write(password.encode("ascii") + b"\n")

        # Step 3: Wait for initial login prompt (">")
        response = tn.read_until(b">", timeout=5).decode("ascii")

        if "invalid" in response.lower():
            tn.close()
            return None, f"Telnet connection failed for IP {ip} | Reason: Username or password invalid."

        # Step 4: Enter enable mode
        tn.write(b"enable\n")
        tn.read_until(b"#", timeout=5)  # Wait for prompt to change to privileged mode

        # Step 5: Enter configuration mode
        tn.write(b"config\n")
        tn.read_until(b"(config))#", timeout=5)  # Wait for prompt in config mode

        telnet_sessions[ip] = (tn, time.time())  # Store session with timestamp
        return tn, f"Connected to OLT {ip}"

    except Exception as e:
        return None, f"Telnet connection failed for IP {ip} | Reason: {str(e)}"

def close_telnet_session(ip: str):
    """Close a Telnet session"""
    tn_data = telnet_sessions.pop(ip, None)
    if tn_data:
        tn_data[0].close()
        return True
    return False

def check_telnet_status(ip: str):
    """Check if a Telnet session is active for a given IP."""
    if ip in telnet_sessions:
        return {"status": "Active", "message": f"Session is active for"}
    return {"status": "Inactive", "message": f"No active session found for"}

def execute_telnet_commands_batch(ip: str, commands: list):
    """Execute multiple commands on an active Telnet session step-by-step, ensuring prompt-based execution."""
    tn_data = telnet_sessions.get(ip)
    if not tn_data:
        return {
            "status": "critical",
            "message": f"No active session for OLT {ip}. Please connect first.",
            "output": ""
        }

    tn, _ = tn_data  # Retrieve session
    try:
        output = []
        error_patterns = [
            "% Parameter error",
            "% Too many parameters",
            "% Unknown command"
        ]
        expected_prompt = b")#"  # Huawei OLT prompt for command execution

        for cmd in commands:
            tn.write(cmd.encode("ascii") + b"\n")

            response = ""
            while True:
                chunk = tn.read_until(expected_prompt, timeout=5).decode("ascii")
                response += chunk

                # Handle pagination (Press 'Q' or ---- More ----)
                if "Press 'Q' to break" in chunk or "---- More ----" in chunk:
                    tn.write(b" ")  # Send Space to get next page
                    time.sleep(0.2)

                # Handle <cr> prompts (example: { <cr>|inner-vlan<K>|to<K> }:)
                elif "{ <cr>" in chunk:
                    tn.write(b"\n")  # Send Enter to continue execution
                    time.sleep(0.2)

                # Stop if we reach the expected prompt (meaning command execution is complete)
                elif ")#" in chunk:
                    # print(f"Command executed: {cmd}")
                    break # Exit loop when full output is received

            # Store executed command and its response
            output.append(f"{cmd} → {response.strip()}")

            # Check for error patterns in the response
            for error in error_patterns:
                if error in response:
                    return {
                        "status": "error",
                        "message": f"Command Execution Error: {error}",
                        "output": "\n".join(output)
                    }

        # Refresh session timestamp
        telnet_sessions[ip] = (tn, time.time())

        return {
            "status": "success",
            "message": "All commands executed successfully",
            "output": "\n".join(output)
        }

    except Exception as e:
        return {
            "status": "critical",
            "message": f"Batch command execution failed: {str(e)}",
            "output": "\n".join(output)
        }

async def handle_command_execution(ip: str, commands: list, success_message: str):
    """Executes Telnet commands and handles errors with a provided success message."""
    try:
        response = await asyncio.get_running_loop().run_in_executor(None, execute_telnet_commands_batch, ip, commands)

        # Handle different response scenarios
        if response["status"] == "success":
            return {"message": success_message, "output": response["output"]}
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
