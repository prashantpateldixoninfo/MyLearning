import requests
import sys
import os
from enum import Enum

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from shared.config import BACKEND_URL

# Define Debug Mode Enum
class DebugMode(Enum):
    NO_DEBUG = "no-debug"
    DEBUG = "debug"
    SUMMARY = "summary"

def send_request(endpoint, data, output_box, debug_mode=DebugMode.NO_DEBUG):
    try:
        response = requests.post(f"{BACKEND_URL}/{endpoint}", json=data)
        if response.status_code == 200:  # Success
            message = response.json().get("message")
            formatted_text = f"""
                <p style="color: green; font-weight: bold;">Success | {message}</p>
            """
            output_box.setHtml(formatted_text)
            if debug_mode in {DebugMode.DEBUG, DebugMode.SUMMARY}:
                output_box.append(f"{response.json().get('output')}")
                output_box.setStyleSheet("color: blue;")
        elif response.status_code == 400:  # Command execution error
            error_details = response.json().get("detail", {})
            formatted_text = f"""
                <p style="color: orange; font-weight: bold;">Error | {error_details.get('message')}</p>
            """
            output_box.setHtml(formatted_text)
            if debug_mode in {DebugMode.DEBUG, DebugMode.SUMMARY}:
                output_box.append(f"{error_details.get('output')}")
                output_box.setStyleSheet("color: blue;")
        elif response.status_code == 500:  # Connection or unexpected failure
            error_details = response.json().get("detail", {})
            formatted_text = f"""
                <p style="color: red; font-weight: bold;">Critical | {error_details.get('message')}</p>
            """
            output_box.setHtml(formatted_text)
            if debug_mode in {DebugMode.DEBUG, DebugMode.SUMMARY}:
                output_box.append(f"{error_details.get('output')}")
                output_box.setStyleSheet("color: blue;")
    except requests.exceptions.RequestException as e:
        output_box.setText(f"Unknown Error Occurred | {e}")
        output_box.setStyleSheet("color: red; font-weight: bold;")

def send_telnet_request(endpoint, data, output_box):
    """
    Sends a POST request to the given API endpoint with provided data.
    Handles errors and updates the output box accordingly.
    """
    try:
        response = requests.post(f"{BACKEND_URL}/{endpoint}", json=data)
        if response.status_code == 200:
            output_box.setText(f"Success | {response.json().get('message')}")
            output_box.setStyleSheet("font-weight: bold; color: green;")
        else:
            output_box.setText(f"Error | {response.json().get('detail')}")
            output_box.setStyleSheet("font-weight: bold; color: red;")
    except requests.exceptions.RequestException as e:
        output_box.setText(f"Critical | {e}")
        output_box.setStyleSheet("font-weight: bold; color: red;")