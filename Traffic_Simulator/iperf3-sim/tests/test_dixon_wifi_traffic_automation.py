import os
import sys
import re
import subprocess
import pytest
from unittest.mock import patch, mock_open, MagicMock

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from dixon_wifi_traffic_automation import (  # type: ignore
    refresh_networks,
    scan_and_connect,
    get_wifi_ip_address,
    is_iperf3_server_running,
    run_iperf3_server,
)


@pytest.fixture
def log_file():
    # Fixture to create a dummy log file for testing
    return mock_open()


def test_refresh_networks(log_file):
    """Test refresh_networks function with mocked subprocess output."""

    # Mock the file object with read and write capabilities
    m = mock_open()

    with patch("builtins.open", m):
        with open("dummy.log", "w") as log_file:
            with patch("subprocess.run") as mock_run, patch(
                "subprocess.check_output"
            ) as mock_check_output:
                mock_run.return_value = MagicMock(returncode=0)
                mock_check_output.return_value = b"Network SSID: Test_Network"

                result = refresh_networks(log_file)

                assert "Test_Network" in result
                mock_run.assert_called_once_with("netsh wlan disconnect", shell=True)
                mock_check_output.assert_called_once_with(
                    "netsh wlan show networks", shell=True
                )


def test_scan_and_connect_success(log_file):
    """Test scan_and_connect function when SSID is found and connection is successful."""
    with patch("builtins.open", log_file):
        with patch("subprocess.run") as mock_run, patch(
            "subprocess.check_output"
        ) as mock_check_output:
            mock_check_output.return_value = b"Network SSID: Test_Network"
            mock_run.return_value = MagicMock(returncode=0)

            scan_and_connect("Test_Network", "Test_Password", "test_log.txt")

            mock_run.assert_any_call("netsh wlan disconnect", shell=True)
            mock_run.assert_any_call(
                'netsh wlan connect name="Test_Network"', shell=True
            )


def test_get_wifi_ip_address(log_file):
    """Test get_wifi_ip_address function with mocked subprocess output."""
    ipconfig_output = """
    Wireless LAN adapter Wi-Fi:
       IPv4 Address. . . . . . . . . . . : 192.168.1.101
    """
    with patch("builtins.open", log_file):
        with patch("subprocess.check_output", return_value=ipconfig_output.encode()):
            result = get_wifi_ip_address("test_log.txt")
            assert result == "192.168.1.101"


def test_is_iperf3_server_running(log_file):
    """Test is_iperf3_server_running function when iperf3 is running."""
    tasklist_output = """
    iperf3.exe                    1234 Console                    1     2,048 K
    """
    # Mock the file object with read and write capabilities
    m = mock_open()

    with patch("builtins.open", m):
        with open("dummy.log", "w") as log_file:
            with patch("subprocess.check_output", return_value=tasklist_output):
                assert is_iperf3_server_running(log_file) is True


def test_is_iperf3_server_not_running(log_file):
    """Test is_iperf3_server_running function when iperf3 is not running."""
    tasklist_output = """
    No tasks running...
    """

    # Mock the file object with read and write capabilities
    m = mock_open()

    with patch("builtins.open", m):
        with open("dummy.log", "w") as log_file:
            with patch("subprocess.check_output", return_value=tasklist_output):
                assert is_iperf3_server_running(log_file) is False


def test_run_iperf3_server(log_file):
    """Test run_iperf3_server function."""

    # Mock the file object with read and write capabilities
    m = mock_open()

    with patch("builtins.open", m):
        with open("dummy.log", "w") as log_file:
            with patch("subprocess.run") as mock_run:
                run_iperf3_server(log_file)
                mock_run.assert_called_once()
