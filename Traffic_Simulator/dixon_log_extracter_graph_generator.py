import re
import sys
from pathlib import Path
from colorama import init, Fore, Style
from dixon_graph_generator_exp import (
    create_blank_excel,
    populate_data,
    add_chart,
    display_chart,
)


def extract_iperf_data_from_file(file_name):
    # Open the file and read the contents
    with open(file_name, "r") as file:
        log_data = file.read()

    bitrate_val = []
    pktlen_val = []
    time_val = []

    bitrate_loss = []
    pktlen_loss = []
    time_loss = []

    counting = 1

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

    variable_regexp = re.compile(r"\b(\d+)(?=\D*$)")
    print(
        f"{Fore.BLUE}--------------------------------------------------------------------------------------------------------------{Style.RESET_ALL}"
    )
    print(f"{Fore.CYAN}Log Extracted From :{Fore.GREEN} {file_name}{Style.RESET_ALL}")
    print(
        f"{Fore.BLUE}--------------------------------------------------------------------------------------------------------------{Style.RESET_ALL}"
    )
    print(
        f"{Fore.BLUE}--------------------------------------------------------------------------------------------------------------{Style.RESET_ALL}"
    )
    print(
        f"{Fore.CYAN}iperf3 executed commands count:{Style.RESET_ALL} [{len(commands)}]"
    )
    print(
        f"{Fore.BLUE}--------------------------------------------------------------------------------------------------------------{Style.RESET_ALL}"
    )
    for cmd in commands:
        if counting <= 10:
            print(f"{cmd}")
            bitrate_val.append(variable_regexp.search(cmd)[0])
            if counting == 10:
                print(
                    f"<===================={Fore.MAGENTA}Bit-Rate-Count{Style.RESET_ALL}[{counting}]==================================>"
                )
        elif counting > 10 and counting <= 20:
            print(f"{cmd}")
            pktlen_val.append(variable_regexp.search(cmd)[0])
            if counting == 20:
                print(
                    f"<===================={Fore.MAGENTA}Packet-Len-Count{Style.RESET_ALL}[{counting}]==================================>"
                )
        elif counting > 20 and counting <= 30:
            print(f"{cmd}")
            time_val.append(variable_regexp.search(cmd)[0])
            if counting == 30:
                print(
                    f"<===================={Fore.MAGENTA}Time-Duration-Count{Style.RESET_ALL}[{counting}]==================================>"
                )
        counting = counting + 1

    print(
        f"{Fore.BLUE}--------------------------------------------------------------------------------------------------------------{Style.RESET_ALL}"
    )
    print(
        f"{Fore.CYAN}iperf3 receiver statistics count:{Style.RESET_ALL} [{len(receiver_stats)}]"
    )
    print(
        f"{Fore.BLUE}--------------------------------------------------------------------------------------------------------------{Style.RESET_ALL}"
    )
    counting = 1
    for stats in receiver_stats:
        if counting <= 10:
            print(f"{stats[0]}")
            if counting == 10:
                print(
                    f"<===================={Fore.MAGENTA}Bit-Rate-Count{Style.RESET_ALL}[{counting}]==================================>"
                )
        elif counting > 10 and counting <= 20:
            print(f"{stats[0]}")
            if counting == 20:
                print(
                    f"<===================={Fore.MAGENTA}Packet-Len-Count{Style.RESET_ALL}[{counting}]==================================>"
                )
        elif counting > 20 and counting <= 30:
            print(f"{stats[0]}")
            if counting == 30:
                print(
                    f"<===================={Fore.MAGENTA}Time-Duration-Count{Style.RESET_ALL}[{counting}]==================================>"
                )
        counting = counting + 1

    print(
        f"{Fore.BLUE}--------------------------------------------------------------------------------------------------------------{Style.RESET_ALL}"
    )
    print(
        f"{Fore.CYAN}iperf3 traffic loss percentage count:{Style.RESET_ALL} [{len(receiver_stats)}]"
    )
    print(
        f"{Fore.BLUE}--------------------------------------------------------------------------------------------------------------{Style.RESET_ALL}"
    )
    counting = 1
    for stats in receiver_stats:
        if counting <= 10:
            print(f"{stats[5]}")
            bitrate_loss.append(stats[5])
            if counting == 10:
                print(
                    f"<===================={Fore.MAGENTA}Bit-Rate-Count{Style.RESET_ALL}[{counting}]==================================>"
                )
        elif counting > 10 and counting <= 20:
            print(f"{stats[5]}")
            pktlen_loss.append(stats[5])
            if counting == 20:
                print(
                    f"<===================={Fore.MAGENTA}Packet-Len-Count{Style.RESET_ALL}[{counting}]==================================>"
                )
        elif counting > 20 and counting <= 30:
            print(f"{stats[5]}")
            time_loss.append(stats[5])
            if counting == 30:
                print(
                    f"<===================={Fore.MAGENTA}Time-Duration-Count{Style.RESET_ALL}[{counting}]==================================>"
                )
        counting = counting + 1

    # Return the data therefore it can store in excel-sheet
    return bitrate_val, bitrate_loss, pktlen_val, pktlen_loss, time_val, time_loss


def get_excel_sheet_info(file_name_1, file_name_2):
    # Create the excel-sheet name based on file names
    vendor_name_1 = "First_File"
    vendor_name_2 = "Second_File"
    vendor_info_regexp = re.compile(r"_(5G|2\.4G)_(ZX|DXB)_")
    vendor_info = vendor_info_regexp.search(file_name_1)
    first_vendor_type = vendor_info.group(1)
    first_vendor_name = vendor_info.group(2)

    vendor_info = vendor_info_regexp.search(file_name_2)
    sec_vendor_type = vendor_info.group(1)
    sec_vendor_name = vendor_info.group(2)
    excel_sheet_name = f"Line_Chart_Of_{first_vendor_name}_{first_vendor_type}_{sec_vendor_name}_{sec_vendor_type}"

    return (
        excel_sheet_name,
        first_vendor_name,
        first_vendor_type,
        sec_vendor_name,
        sec_vendor_type,
    )


def find_file(filename):
    search_path = Path.cwd()  # Current directory
    for file_path in search_path.rglob(filename.name):
        return file_path  # Return the first match found
    return None  # File not found


def get_file_name_and_path(file_name):
    filename = Path(file_name)
    if filename.suffix == ".txt":
        filepath = find_file(filename)
        if filepath:
            print(f"{Fore.CYAN}File found:{Fore.GREEN} {filepath}{Style.RESET_ALL}")
            return filename.name, filepath
        else:
            print(
                f"{Fore.LIGHTBLUE_EX}{filename}{Fore.RED} file not found.{Style.RESET_ALL}"
            )
            sys.exit(0)
    else:
        filename = filename.with_suffix(".txt")
        filepath = find_file(filename)
        if filepath:
            print(f"{Fore.CYAN}File found:{Fore.GREEN} {filepath}{Style.RESET_ALL}")
            return filename.name, filepath
        else:
            print(
                f"{Fore.LIGHTBLUE_EX}{filename}{Fore.RED} file not found.{Style.RESET_ALL}"
            )
            sys.exit(0)


# Example usage:
if __name__ == "__main__":
    # Initialize colorama for colored output on Windows
    if sys.platform == "win32":
        init(autoreset=True)

    # Get the log files name from user
    # file_name_1 = 'C:\Dixon_Project\Softwares\IPerf-3.17.1\Logs\log_2024-10-23_13-11-28_Airtel_Zerotouch_5G_ZX_6_PP.txt'  # Replace with the actual log file name
    # file_name_2 = 'C:\Dixon_Project\Softwares\IPerf-3.17.1\Logs\log_2024-10-23_11-42-04_Airtel_Zerotouch_5G_DXB_6_PP.txt'

    # Get the log files name from user
    file_name = (
        input(Fore.YELLOW + "Enter your first filename : " + Style.RESET_ALL)
        or "log_2024-10-23_13-11-28_Airtel_Zerotouch_5G_ZX_6_PP.txt"
    )
    first_file_name, first_file_path = get_file_name_and_path(file_name)

    file_name = (
        input(Fore.YELLOW + "Enter your second filename : " + Style.RESET_ALL)
        or "log_2024-10-23_11-42-04_Airtel_Zerotouch_5G_DXB_6_PP.txt"
    )
    sec_file_name, sec_file_path = get_file_name_and_path(file_name)

    # Get excel-sheet name based on files name
    (
        excel_sheet_name,
        first_vendor_name,
        first_vendor_type,
        sec_vendor_name,
        sec_vendor_type,
    ) = get_excel_sheet_info(first_file_name, sec_file_name)

    # Create the excel-sheet
    excel_file_path = Path.cwd() / "Logs" / f"{excel_sheet_name}.xlsx"
    create_blank_excel(excel_file_path)
    print(
        f"{Fore.CYAN}Excel file created at: {Fore.GREEN}{excel_file_path}{Style.RESET_ALL}"
    )

    # Extract the data from provided log files
    (
        bitrate_val_1,
        bitrate_loss_1,
        pktlen_val_1,
        pktlen_loss_1,
        time_val_1,
        time_loss_1,
    ) = extract_iperf_data_from_file(first_file_path)
    (
        bitrate_val_2,
        bitrate_loss_2,
        pktlen_val_2,
        pktlen_loss_2,
        time_val_2,
        time_loss_2,
    ) = extract_iperf_data_from_file(sec_file_path)

    # ============================================
    # Update Bitrate info in excel-sheet
    # ============================================
    bitrate_graph_info = {
        "sheet_num": 0,  # First sheet in the workbook
        "sheet_name": "Bitrate",
        "x_axis": "Bitrate",
        "first_header": f"{first_vendor_name}_{first_vendor_type}",
        "sec_header": f"{sec_vendor_name}_{sec_vendor_type}",
        "x_axis_value": bitrate_val_1,
        "first_header_value": bitrate_loss_1,
        "sec_header_value": bitrate_loss_2,
    }
    print(f"{Fore.GREEN}Updating the Bitrate Data in Excel{Style.RESET_ALL}")
    populate_data(excel_file_path, bitrate_graph_info)

    if first_vendor_type == sec_vendor_type:
        chart_title = f"{first_vendor_type}-Bitrate"
    else:
        chart_title = f"{first_vendor_type}-{sec_vendor_type}-Bitrate"
    add_chart(excel_file_path, bitrate_graph_info["sheet_num"], chart_title)

    # ============================================
    # Update Packet Length info in excel-sheet
    # ============================================
    pktlen_graph_info = {
        "sheet_num": 1,  # Second sheet in the workbook
        "sheet_name": "Packet-Len",
        "x_axis": "Packet-Len",
        "first_header": f"{first_vendor_name}_{first_vendor_type}",
        "sec_header": f"{sec_vendor_name}_{sec_vendor_type}",
        "x_axis_value": pktlen_val_1,
        "first_header_value": pktlen_loss_1,
        "sec_header_value": pktlen_loss_2,
    }
    print(f"{Fore.GREEN}Updating the Packet Length Data in Excel{Style.RESET_ALL}")
    populate_data(excel_file_path, pktlen_graph_info)

    if first_vendor_type == sec_vendor_type:
        chart_title = f"{first_vendor_type}-Packet-Len"
    else:
        chart_title = f"{first_vendor_type}-{sec_vendor_type}-Packet-Len"

    add_chart(excel_file_path, pktlen_graph_info["sheet_num"], chart_title)

    # ============================================
    # Update Time Variation info in excel-sheet
    # ============================================
    time_graph_info = {
        "sheet_num": 2,  # Third sheet in the workbook
        "sheet_name": "Time-Var",
        "x_axis": "Time-Var",
        "first_header": f"{first_vendor_name}_{first_vendor_type}",
        "sec_header": f"{sec_vendor_name}_{sec_vendor_type}",
        "x_axis_value": time_val_1,
        "first_header_value": time_loss_1,
        "sec_header_value": time_loss_2,
    }
    print(f"{Fore.GREEN}Updating the Time Variation Data in Excel{Style.RESET_ALL}")
    populate_data(excel_file_path, time_graph_info)

    if first_vendor_type == sec_vendor_type:
        chart_title = f"{first_vendor_type}-Time-Var"
    else:
        chart_title = f"{first_vendor_type}-{sec_vendor_type}-Time-Var"

    add_chart(excel_file_path, time_graph_info["sheet_num"], chart_title)

    # ============================================
    # Finally Display the Chart
    # ============================================
    print(f"{Fore.GREEN}Excel-Sheet is launched now{Style.RESET_ALL}")
    display_chart(excel_file_path)
