import os
import sys
import pytest
from unittest.mock import patch, mock_open
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from dixon_log_extracter_graph_generator import (  # type: ignore
    extract_iperf_data_from_file,
    get_excel_sheet_info,
    get_file_name_and_path,
    find_file,
)

# Sample data simulating the contents of a log file
MOCK_LOG_DATA = """
Running iperf3 [iperf3.exe -c 192.168.0.1 -t 10 -i 1 -b 100M]
0.00-1.00 sec  12.5 MBytes  100 Mbits/sec  0.1 ms  0/100 (0%)  receiver
Running iperf3 [iperf3.exe -c 192.168.0.2 -t 10 -i 1 -b 200M]
1.00-2.00 sec  25.0 MBytes  200 Mbits/sec  0.2 ms  0/200 (0%)  receiver
"""


# Test function for extract_iperf_data_from_file
def test_extract_iperf_data_from_file():
    # Mock the open function to simulate reading from a file
    m = mock_open(read_data=MOCK_LOG_DATA)

    with patch("builtins.open", m):
        # Call the function under test
        bitrate_val, bitrate_loss, pktlen_val, pktlen_loss, time_val, time_loss = (
            extract_iperf_data_from_file("dummy.log")
        )

        # Assertions for the extracted data
        assert bitrate_val == [
            "100",
            "200",
        ]  # Command bit rates extracted from the logs
        assert bitrate_loss == ["0", "0"]  # Loss values extracted from the logs
        assert pktlen_val == []  # No extra data in the mock
        assert pktlen_loss == []  # No extra data in the mock
        assert time_val == []  # No extra data in the mock
        assert time_loss == []  # No extra data in the mock


# Test get_excel_sheet_info function
def test_get_excel_sheet_info():
    file_name_1 = "log_2024-10-23_13-11-28_Airtel_5G_ZX_6_PP.txt"
    file_name_2 = "log_2024-10-23_11-42-04_Airtel_5G_DXB_6_PP.txt"

    (
        excel_sheet_name,
        first_vendor_name,
        first_vendor_type,
        sec_vendor_name,
        sec_vendor_type,
    ) = get_excel_sheet_info(file_name_1, file_name_2)

    assert excel_sheet_name == "Line_Chart_Of_ZX_5G_DXB_5G"
    assert first_vendor_name == "ZX"
    assert first_vendor_type == "5G"
    assert sec_vendor_name == "DXB"
    assert sec_vendor_type == "5G"


# Test get_file_name_and_path function
def test_get_file_name_and_path():
    # Mocking file system behavior
    with patch.object(Path, "rglob", return_value=[Path("test_dir/log.txt")]):
        file_name, file_path = get_file_name_and_path("log.txt")

    assert file_name == "log.txt"
    assert file_path == Path("test_dir/log.txt")


def test_get_file_name_and_path_not_found():
    with patch.object(Path, "rglob", return_value=[]):
        with pytest.raises(SystemExit):
            get_file_name_and_path("nonexistent_file.txt")


# Test find_file function
def test_find_file():
    with patch.object(Path, "rglob", return_value=[Path("test_dir/log.txt")]):
        result = find_file(Path("log.txt"))
        assert result == Path("test_dir/log.txt")


def test_find_file_not_found():
    with patch.object(Path, "rglob", return_value=[]):
        result = find_file(Path("nonexistent_file.txt"))
        assert result is None
