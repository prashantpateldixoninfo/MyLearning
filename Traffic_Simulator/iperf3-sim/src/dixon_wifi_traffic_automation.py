# For Windows platform
# =============================
import subprocess
import time
import re
import os
import sys
from colorama import init, Fore, Style
from datetime import datetime
from pathlib import Path
import pyfiglet

iperf3_dir = Path().absolute()
iperf3_path = iperf3_dir / "iperf3.exe"


def test_automation_logo(log_filename):
    # Messages
    company_name = "Dixon Technology"
    banner_name = "Traffic Test Automation"

    # Create ASCII art for both lines separately
    fig1 = pyfiglet.Figlet(font="standard")  # You can use any compact font
    ascii_company_name = fig1.renderText(company_name).strip()

    fig2 = pyfiglet.Figlet(font="standard")  # You can use the same or different font
    ascii_banner_name = fig2.renderText(banner_name).strip()

    # Get terminal width to center the text
    terminal_width = os.get_terminal_size().columns

    # Center the first line
    ascii_company_name_centered = "\n".join(
        [line.ljust(terminal_width) for line in ascii_company_name.split("\n")]
    )

    # Make the second line full width
    ascii_banner_name_full = "\n".join(
        [line.center(terminal_width) for line in ascii_banner_name.split("\n")]
    )

    # Clear the screen
    # os.system('cls' if os.name == 'nt' else 'clear')

    # Display the banner in CYAN color
    with open(log_filename, "a") as log_file:
        print(Fore.CYAN + ascii_company_name_centered)
        log_file.write(ascii_company_name_centered + "\n")
        print(Fore.GREEN + ascii_banner_name_full)
        log_file.write(ascii_banner_name_full + "\n")


def refresh_networks(log_file):
    """Refreshes the list of available networks by disconnecting and rescanning."""
    try:
        print(Fore.MAGENTA + "Refreshing network list...")
        log_file.write(f"Refreshing network list..." + "\n")

        # Disconnect from any connected networks
        disconnect_command = "netsh wlan disconnect"
        subprocess.run(disconnect_command, shell=True)

        # Wait for a few seconds to ensure the network refresh happens
        time.sleep(2)

        # Scan for networks again
        print(Fore.MAGENTA + "Rescanning networks...")
        log_file.write(f"Rescanning networks..." + "\n")
        refresh_command = "netsh wlan show networks"
        refreshed_scan_result = subprocess.check_output(
            refresh_command, shell=True
        ).decode()

        return refreshed_scan_result

    except Exception as e:
        print(Fore.RED + f"Error while refreshing networks: {e}")
        log_file.write(f"Error while refreshing networks: {e}" + "\n")
        return ""


def scan_and_connect(ssid, password, log_filename):
    with open(log_filename, "a") as log_file:
        try:
            # Refresh and scan networks
            scan_result = refresh_networks(log_file)

            # Check if the target SSID is available after refresh
            if ssid in scan_result:
                print(Fore.CYAN + f"SSID '{ssid}' found. Attempting to connect...")
                log_file.write(f"SSID '{ssid}' found. Attempting to connect..." + "\n")

                # Create Wi-Fi profile
                profile = f"""
                <WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">
                    <name>{ssid}</name>
                    <SSIDConfig>
                        <SSID>
                            <name>{ssid}</name>
                        </SSID>
                    </SSIDConfig>
                    <connectionType>ESS</connectionType>
                    <connectionMode>auto</connectionMode>
                    <MSM>
                        <security>
                            <authEncryption>
                                <authentication>WPA2PSK</authentication>
                                <encryption>AES</encryption>
                                <useOneX>false</useOneX>
                            </authEncryption>
                            <sharedKey>
                                <keyType>passPhrase</keyType>
                                <protected>false</protected>
                                <keyMaterial>{password}</keyMaterial>
                            </sharedKey>
                        </security>
                    </MSM>
                </WLANProfile>
                """

                # Write the profile to an XML file
                profile_file = f"{ssid}.xml"
                log_file.write(f"{profile_file}" + "\n")

                # Add the profile to the system
                add_profile_command = (
                    f'netsh wlan add profile filename="{profile_file}"'
                )
                subprocess.run(add_profile_command, shell=True)

                # Connect to the network
                connect_command = f'netsh wlan connect name="{ssid}"'
                connection_result = subprocess.run(connect_command, shell=True)

                if connection_result.returncode == 0:
                    print(Fore.GREEN + f"Successfully connected to {ssid}")
                    log_file.write(f"Successfully connected to {ssid}" + "\n")
                else:
                    print(Fore.RED + f"Failed to connect to {ssid}")
                    log_file.write(f"Failed to connect to {ssid}" + "\n")
            else:
                print(
                    Fore.RED
                    + f"SSID '{ssid}' not found in the scan result after refresh."
                )
                log_file.write(
                    f"SSID '{ssid}' not found in the scan result after refresh." + "\n"
                )

        except Exception as e:
            print(Fore.RED + f"An error occurred: {e}")
            log_file.write(f"An error occurred: {e}" + "\n")


def get_wifi_ip_address(log_filename):
    with open(log_filename, "a") as log_file:
        try:
            # Run the 'ipconfig' command and capture the output
            ipconfig_result = subprocess.check_output("ipconfig", shell=True).decode()

            # Look for the section related to 'Wireless LAN adapter Wi-Fi'
            wifi_section = re.search(
                r"Wireless LAN adapter Wi-Fi.*?:\s*(.*?)(?=\n\n|\Z)",
                ipconfig_result,
                re.DOTALL,
            )

            if wifi_section:
                wifi_info = wifi_section.group(1)

                # Search for the IPv4 Address using a regular expression
                ipv4_match = re.search(r"IPv4 Address.*?:\s*([0-9\.]+)", wifi_info)

                if ipv4_match:
                    wifi_ip_address = ipv4_match.group(1)
                    print(Fore.MAGENTA + f"Wi-Fi IPv4 Address: {wifi_ip_address}")
                    log_file.write(f"Wi-Fi IPv4 Address: {wifi_ip_address}" + "\n")
                    return wifi_ip_address
                else:
                    print(Fore.RED + f"IPv4 Address not found.")
                    log_file.write(f"IPv4 Address not found." + "\n")
                    return "IPv4 Address not found."
            else:
                print(Fore.RED + f"Wireless LAN adapter Wi-Fi not found.")
                log_file.write(f"Wireless LAN adapter Wi-Fi not found." + "\n")
                return "Wireless LAN adapter Wi-Fi not found."

        except Exception as e:
            print(Fore.RED + f"An error occurred: {e}")
            log_file.write(f"An error occurred: {e}" + "\n")
            return f"An error occurred: {e}"


def is_iperf3_server_running(log_file):
    # Check for running iperf3 server process using 'tasklist'
    try:
        output = subprocess.check_output("tasklist", shell=True, text=True)

        # Check if 'iperf3.exe' is present in the task list
        if "iperf3.exe" in output:
            print(Fore.CYAN + "iPerf3 server is already running.")
            log_file.write(f"iPerf3 server is already running." + "\n")
            return True
        else:
            print(Fore.MAGENTA + "iPerf3 server is not running.")
            log_file.write(f"iPerf3 server is not running." + "\n")
            return False

    except subprocess.CalledProcessError as e:
        print(Fore.RED + f"Error checking running processes: {e}")
        log_file.write(f"Error checking running processes: {e}" + "\n")
        return False


def run_iperf3_server(log_file):
    # Command to start iperf3 in server mode
    server_command = f'start cmd /k "{iperf3_path} -s"'

    # Run the command in a new terminal
    subprocess.run(server_command, shell=True)
    print(Fore.GREEN + "iPerf3 server started.")
    log_file.write(f"iPerf3 server started." + "\n")


def execute_iper3_client_cmds(ip_address):
    with open(log_filename, "a") as log_file:
        # Launch the iperf3 server
        if not is_iperf3_server_running(log_file):
            # Step 2: If not running, start the iperf3 server
            run_iperf3_server(log_file)
            time.sleep(20)
        else:
            print(Fore.CYAN + f"Server already running, skipping launch.")
            log_file.write(f"Server already running, skipping launch." + "\n")

        # List of commands with varying time durations, with the 30-second command first
        iperf_commands = [
            # Varing Bitrate Commands
            {
                "command": ["iperf3.exe", "-c", ip_address, "-u", "-b", "50M"],
                "duration": 10,
            },
            {
                "command": ["iperf3.exe", "-c", ip_address, "-u", "-b", "80M"],
                "duration": 10,
            },
            # {
            #     "command": [
            #         "iperf3.exe", "-c", ip_address, "-u", "-b", "120M"
            #     ],
            #     "duration": 10
            # },
            # {
            #     "command": [
            #         "iperf3.exe", "-c", ip_address, "-u", "-b", "200M"
            #     ],
            #     "duration": 10
            # },
            # {
            #     "command": [
            #         "iperf3.exe", "-c", ip_address, "-u", "-b", "300M"
            #     ],
            #     "duration": 10
            # },
            # {
            #     "command": [
            #         "iperf3.exe", "-c", ip_address, "-u", "-b", "400M"
            #     ],
            #     "duration": 10
            # },
            # {
            #     "command": [
            #         "iperf3.exe", "-c", ip_address, "-u", "-b", "500M"
            #     ],
            #     "duration": 10
            # },
            # {
            #     "command": [
            #         "iperf3.exe", "-c", ip_address, "-u", "-b", "700M"
            #     ],
            #     "duration": 10
            # },
            # {
            #     "command": [
            #         "iperf3.exe", "-c", ip_address, "-u", "-b", "800M"
            #     ],
            #     "duration": 10
            # },
            # {
            #     "command": [
            #         "iperf3.exe", "-c", ip_address, "-u", "-b", "1000M"
            #     ],
            #     "duration": 10
            # },
            # # Varing Packet Length Commands
            # {
            #     "command": [
            #         "iperf3.exe", "-c", ip_address, "-u", "-b", "100M", "-l", "1400"
            #     ],
            #     "duration": 10
            # },
            # {
            #     "command": [
            #         "iperf3.exe", "-c", ip_address, "-u", "-b", "100M", "-l", "1300"
            #     ],
            #     "duration": 10
            # },
            # {
            #     "command": [
            #         "iperf3.exe", "-c", ip_address, "-u", "-b", "100M", "-l", "1200"
            #     ],
            #     "duration": 10
            # },
            # {
            #     "command": [
            #         "iperf3.exe", "-c", ip_address, "-u", "-b", "100M", "-l", "1100"
            #     ],
            #     "duration": 10
            # },
            # {
            #     "command": [
            #         "iperf3.exe", "-c", ip_address, "-u", "-b", "100M", "-l", "900"
            #     ],
            #     "duration": 10
            # },
            # {
            #     "command": [
            #         "iperf3.exe", "-c", ip_address, "-u", "-b", "100M", "-l", "700"
            #     ],
            #     "duration": 10
            # },
            # {
            #     "command": [
            #         "iperf3.exe", "-c", ip_address, "-u", "-b", "100M", "-l", "500"
            #     ],
            #     "duration": 10
            # },
            # {
            #     "command": [
            #         "iperf3.exe", "-c", ip_address, "-u", "-b", "100M", "-l", "300"
            #     ],
            #     "duration": 10
            # },
            # {
            #     "command": [
            #         "iperf3.exe", "-c", ip_address, "-u", "-b", "100M", "-l", "100"
            #     ],
            #     "duration": 10
            # },
            # {
            #     "command": [
            #         "iperf3.exe", "-c", ip_address, "-u", "-b", "100M", "-l", "50"
            #     ],
            #     "duration": 10
            # },
            # # Varing Time Duration Commands
            # {
            #     "command": [
            #         "iperf3.exe", "-c", ip_address, "-u", "-b", "100M", "-t", "10"
            #     ],
            #     "duration": 10
            # },
            # {
            #     "command": [
            #         "iperf3.exe", "-c", ip_address, "-u", "-b", "100M", "-t", "20"
            #     ],
            #     "duration": 20
            # },
            # {
            #     "command": [
            #         "iperf3.exe", "-c", ip_address, "-u", "-b", "100M", "-t", "30"
            #     ],
            #     "duration": 30
            # },
            # {
            #     "command": [
            #         "iperf3.exe", "-c", ip_address, "-u", "-b", "100M", "-t", "40"
            #     ],
            #     "duration": 40
            # },
            # {
            #     "command": [
            #         "iperf3.exe", "-c", ip_address, "-u", "-b", "100M", "-t", "50"
            #     ],
            #     "duration": 50
            # },
            # {
            #     "command": [
            #         "iperf3.exe", "-c", ip_address, "-u", "-b", "100M", "-t", "60"
            #     ],
            #     "duration": 60
            # },
            # {
            #     "command": [
            #         "iperf3.exe", "-c", ip_address, "-u", "-b", "100M", "-t", "120"
            #     ],
            #     "duration": 120
            # },
            # {
            #     "command": [
            #         "iperf3.exe", "-c", ip_address, "-u", "-b", "100M", "-t", "180"
            #     ],
            #     "duration": 180
            # },
            #             {
            #     "command": [
            #         "iperf3.exe", "-c", ip_address, "-u", "-b", "100M", "-t", "240"
            #     ],
            #     "duration": 240
            # },
            # {
            #     "command": [
            #         "iperf3.exe", "-c", ip_address, "-u", "-b", "100M", "-t", "300"
            #     ],
            #     "duration": 300
            # }
        ]

        # Iterate over the commands and run them
        for iperf_case in iperf_commands:
            duration = iperf_case["duration"]
            command = iperf_case["command"]
            formatted_command = " ".join(command)

            # Display and log message before running the command in red
            message = (
                f"\nRunning iperf3 [{formatted_command}] for {duration} seconds..."
            )
            print(Fore.GREEN + message)
            log_file.write(message + "\n")

            # Execute the iperf3 command
            try:
                result = subprocess.run(
                    command, capture_output=True, text=True, check=True
                )
                output_message = f"iperf3 [{formatted_command}] output ({duration} seconds):\n{result.stdout}"
                print(Fore.WHITE + output_message)
                log_file.write(output_message + "\n")
            except subprocess.CalledProcessError as e:
                error_message = f"An error occurred during the {duration - 1} seconds test:\n{e.stderr}"
                print(Fore.RED + error_message)
                log_file.write(error_message + "\n")


def extract_iperf_data_from_file(file_name):
    # Open the file and read the contents
    with open(file_name, "r") as file:
        log_data = file.read()

    # Regular expressions for the command and receiver stats
    command_regex = r"Running iperf3 \[(iperf3.exe .*?)\]"
    receiver_stats_regex = r"(\d+\.\d+\-\d+\.\d+\s+sec\s+(\d+\.\d+|\d+)\s+(MBytes|GBytes|KBytes)\s+(\d+\.\d+|\d+)\s+(Mbits|Kbits)\/sec\s+\d+\.\d+\sms\s+\d+\/\d+\s+\((\d+|\d+\.\d+)\%\)\s+receiver)"

    # Find all matches for the commands
    commands = re.findall(command_regex, log_data)

    # Find all matches for the receiver stats
    receiver_stats = re.findall(receiver_stats_regex, log_data)

    # Display the results
    # for cmd, stats in zip(commands, receiver_stats):
    #    print(f"Extracted command: {cmd}")
    #    print(f"Extracted receiver stats: {stats[0]}")
    print(
        f"--------------------------------------------------------------------------------------------------------------"
    )
    print(f"{Fore.CYAN}Log Extracted From :{Fore.GREEN}{file_name}{Style.RESET_ALL}")
    print(
        f"--------------------------------------------------------------------------------------------------------------"
    )
    print(
        f"--------------------------------------------------------------------------------------------------------------"
    )
    print(f"iperf3 executed commands count: [{len(commands)}]")
    print(
        f"--------------------------------------------------------------------------------------------------------------"
    )
    for cmd in commands:
        print(f"{cmd}")
    print(
        f"--------------------------------------------------------------------------------------------------------------"
    )
    print(f"iperf3 receiver statistics count: [{len(receiver_stats)}]")
    print(
        f"--------------------------------------------------------------------------------------------------------------"
    )
    for stats in receiver_stats:
        print(f"{stats[0]}")
    print(
        f"--------------------------------------------------------------------------------------------------------------"
    )
    print(f"iperf3 traffic loss percentage count: [{len(receiver_stats)}]")
    print(
        f"--------------------------------------------------------------------------------------------------------------"
    )
    for stats in receiver_stats:
        print(f"{stats[5]}")


def cal_time_duration(start_time, log_filename, task_name):
    with open(log_filename, "a") as log_file:
        stop_time = datetime.now()
        duration = stop_time - start_time

        # Extract hours, minutes, and seconds
        hours, remainder = divmod(duration.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        print(
            Fore.CYAN
            + f"Your {task_name} Took : {int(hours)} hrs, {int(minutes)} mins, {int(seconds)} secs"
        )
        log_file.write(
            f"Your {task_name} Took : {int(hours)} hrs, {int(minutes)} mins, {int(seconds)} secs"
            + "\n"
        )


if __name__ == "__main__":
    # Initialize colorama for colored output on Windows
    if sys.platform == "win32":
        init(autoreset=True)

    # Get the input from users
    target_ssid = (
        input(
            Fore.YELLOW
            + "Enter your SSID like {Airtel_Zerotouch_2.4G_DXB_6_PP}: "
            + Style.RESET_ALL
        )
        or "Airtel_Zerotouch_2.4G_DXB_6_PP"
    )
    password = (
        input(Fore.YELLOW + "Enter your SSID Password: " + Style.RESET_ALL)
        or "Airtel@123"
    )

    # Start Time of Session
    session_con_time_start = datetime.now()

    # Create the log file name based on timestamp and append the SSID to it.

    # Specify the folder where log files will be saved
    log_folder = os.path.join(
        os.path.expanduser(f"{iperf3_dir}"), "Logs"
    )  # Saves in user's home directory

    # Check if the folder exists; if not, create it
    os.makedirs(
        log_folder, exist_ok=True
    )  # Automatically create the folder if it doesn't exist

    # Create a timestamp for log file name
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_filename = os.path.join(
        log_folder, f"log_{timestamp}_{target_ssid}.txt"
    )  # Save in the specified folder

    # Step-01 print the company logo
    test_automation_logo(log_filename)

    # Print the user informatiion
    with open(log_filename, "a") as log_file:
        print(
            Fore.BLUE
            + f"------------------------------------------------------------------------------------------------------------------------------"
        )
        log_file.write(
            "------------------------------------------------------------------------------------------------------------------------------"
            + "\n"
        )
        print(Fore.GREEN + f"Your Information:")
        log_file.write(f"Your Information:" + "\n")
        print(
            Fore.BLUE
            + f"------------------------------------------------------------------------------------------------------------------------------"
        )
        log_file.write(
            "------------------------------------------------------------------------------------------------------------------------------"
            + "\n"
        )
        print(Fore.YELLOW + "SSID: " + Fore.CYAN + f"{target_ssid}")
        log_file.write(f"SSID: " + f"{target_ssid}" + "\n")
        print(Fore.YELLOW + "Password : " + Fore.CYAN + f"{password}")
        log_file.write(f"Password: " + f"{password}" + "\n")
        print(Fore.YELLOW + "Current Directory : " + Fore.CYAN + f"{iperf3_dir}")
        log_file.write(f"Current Directory : " + f"{iperf3_dir}" + "\n")
        print(Fore.YELLOW + "Iperf3 Executable Path : " + Fore.CYAN + f"{iperf3_path}")
        log_file.write(f"Iperf3 Executable Path : " + f"{iperf3_path}" + "\n")
        print(Fore.YELLOW + "Log File Path : " + Fore.CYAN + f"{log_filename}")
        log_file.write(f"Log File Path : " + f"{log_filename}" + "\n")
        print(
            Fore.BLUE
            + f"------------------------------------------------------------------------------------------------------------------------------"
        )
        log_file.write(
            "------------------------------------------------------------------------------------------------------------------------------"
            + "\n"
        )

    # sys.exit(0)
    # Step-02 Call the function to scan and connect
    scan_and_connect(target_ssid, password, log_filename)

    # Step-03 Get and display the IP address for Wi-Fi
    time.sleep(1)
    wifi_ip_address = get_wifi_ip_address(log_filename)
    if wifi_ip_address == "IPv4 Address not found.":
        time.sleep(7)
        wifi_ip_address = get_wifi_ip_address(log_filename)  # Try once more time

    cal_time_duration(session_con_time_start, log_filename, "Session")

    # Step-04 Execute the iperf3 client commands and write into log file
    command_exec_time_start = datetime.now()
    execute_iper3_client_cmds(wifi_ip_address)
    cal_time_duration(command_exec_time_start, log_filename, "iperf3 Execution")

    # Total Session and Command execution time
    cal_time_duration(session_con_time_start, log_filename, "Script")

    # Step-05 Extract the Logfile and display the summary on console
    # extract_iperf_data_from_file(log_filename)
