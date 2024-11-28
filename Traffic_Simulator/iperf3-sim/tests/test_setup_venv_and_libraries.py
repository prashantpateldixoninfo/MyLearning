import os
import sys
import subprocess
from unittest import mock
import pytest

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

import setup_venv_and_libraries as setup_script  # type: ignore


@pytest.fixture
def mock_subprocess_check_call():
    """Mock subprocess.check_call."""
    with mock.patch("subprocess.check_call") as mock_call:
        yield mock_call


@pytest.fixture
def mock_subprocess_check_output():
    """Mock subprocess.check_output."""
    with mock.patch("subprocess.check_output") as mock_output:
        yield mock_output


@pytest.fixture
def mock_os_path_exists():
    """Mock os.path.exists."""
    with mock.patch("os.path.exists") as mock_exists:
        yield mock_exists


def test_create_virtualenv(mock_os_path_exists, mock_subprocess_check_call):
    """Test the creation of a virtual environment."""
    # Case 1: Virtual environment doesn't exist
    mock_os_path_exists.return_value = False
    setup_script.create_virtualenv("test_env")
    mock_subprocess_check_call.assert_called_once_with(
        [sys.executable, "-m", "venv", "test_env"]
    )

    # Case 2: Virtual environment already exists
    mock_os_path_exists.return_value = True
    setup_script.create_virtualenv("test_env")
    mock_subprocess_check_call.assert_called_once()  # No new calls


def test_get_installed_packages(mock_subprocess_check_output):
    """Test retrieving installed packages."""
    # Mock pip freeze output
    mock_subprocess_check_output.return_value = "package1==1.0.0\npackage2==2.0.0"
    installed_packages = setup_script.get_installed_packages("test_env")
    assert installed_packages == {"package1", "package2"}

    # Test exception handling
    mock_subprocess_check_output.side_effect = subprocess.CalledProcessError(
        returncode=1, cmd="pip freeze"
    )
    with pytest.raises(SystemExit):
        setup_script.get_installed_packages("test_env")


def test_check_and_install_dependencies(
    mock_os_path_exists, mock_subprocess_check_call, mock_subprocess_check_output
):
    """Test checking and installing dependencies."""
    # Mocking file and package data
    mock_os_path_exists.side_effect = lambda path: path == "requirements.txt"
    mock_subprocess_check_output.return_value = "package1==1.0.0"

    with mock.patch("builtins.open", mock.mock_open(read_data="package1\npackage2")):
        setup_script.check_and_install_dependencies("test_env", "requirements.txt")

    # Assert subprocess calls for missing packages
    mock_subprocess_check_call.assert_any_call(
        [
            (
                os.path.join("test_env", "Scripts", "pip")
                if os.name == "nt"
                else os.path.join("test_env", "bin", "pip")
            ),
            "install",
            "package2",
        ]
    )


def test_activate_virtualenv():
    """Test activating the virtual environment."""

    # Mocking print to capture output
    with mock.patch("builtins.print") as mock_print:
        setup_script.activate_virtualenv("test_env")  # Call the function to test

        # Construct the expected output
        activate_script = (
            os.path.join("test_env", "Scripts", "activate")
            if os.name == "nt"
            else os.path.join("test_env", "bin", "activate")
        )
        expected_print = f"To activate the virtual environment, run:\n {'source ' if os.name != 'nt' else ''}{activate_script}"
        deactivate_print = "To deactivate the virtual environment, run:\n deactivate"

        # Debug output for comparison
        print(f"expected_print = '{expected_print}'")
        print(f"mock_print.mock_calls = {mock_print.mock_calls}")

        # Assertions for print calls
        mock_print.assert_any_call(expected_print)
        mock_print.assert_any_call(deactivate_print)
