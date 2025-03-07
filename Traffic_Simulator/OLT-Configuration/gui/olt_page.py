from qtpy.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QGroupBox,
    QCheckBox,
)
from qtpy.QtCore import Qt
import requests
import re
import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from shared.config import BACKEND_URL

class OLTConfiguration(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        self.debug_enabled = False 
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # === OLT Connection Block ===
        olt_connection_group = QGroupBox("OLT Connection")
        olt_connection_group.setStyleSheet("QGroupBox { font-weight: bold; font-size: 14px; }")
        olt_layout = QVBoxLayout()

        # Input Fields for OLT Connection
        self.ip_input = QLineEdit(placeholderText="IP Address")
        self.ip_input.setText("10.11.104.2")
        self.user_input = QLineEdit(placeholderText="User")
        self.user_input.setText("root")
        self.password_input = QLineEdit(placeholderText="Password")
        self.password_input.setEchoMode(QLineEdit.Password)  # Hide password input
        self.password_input.setText("admin")

        olt_layout.addWidget(self.ip_input)
        olt_layout.addWidget(self.user_input)
        olt_layout.addWidget(self.password_input)

        self.olt_output = QTextEdit(placeholderText="OLT Connection Output...")
        self.olt_output.setReadOnly(True)

        self.connect_telnet_btn = QPushButton("Connect")
        self.display_telnet_btn = QPushButton("Status")
        self.disconnect_telnet_btn = QPushButton("Disconnect")
        self.connect_telnet_btn.clicked.connect(self.connect_olt_session)
        self.display_telnet_btn.clicked.connect(self.display_olt_session)
        self.disconnect_telnet_btn.clicked.connect(self.disconnect_olt_session)

        olt_button_layout = QHBoxLayout()
        olt_button_layout.addWidget(self.disconnect_telnet_btn)
        olt_button_layout.addWidget(self.display_telnet_btn)
        olt_button_layout.addWidget(self.connect_telnet_btn)

        olt_layout.addWidget(self.olt_output)
        olt_layout.addLayout(olt_button_layout)
        olt_connection_group.setLayout(olt_layout)
        main_layout.addWidget(olt_connection_group)


        # === OLT Port Setting Block ===
        olt_port_group = QGroupBox("OLT Port Setting")
        olt_port_group.setStyleSheet("QGroupBox { font-weight: bold; font-size: 14px; }")
        olt_port_layout = QVBoxLayout()
  
        self.uplink_input = QLineEdit(placeholderText="Uplink Port (Frame/Slot/Port)")
        self.uplink_input.setText("0/16/5")
        self.vlan_input = QLineEdit(placeholderText="VLAN (1-65535)")
        self.vlan_input.setText("55")
        self.olt_port_input = QLineEdit(placeholderText="OLT PON Port (Frame/Slot/Port)")
        self.olt_port_input.setText("0/1/5")
        
        olt_port_layout.addWidget(self.uplink_input)
        olt_port_layout.addWidget(self.vlan_input)
        olt_port_layout.addWidget(self.olt_port_input)

        self.olt_port_output = QTextEdit(placeholderText="OLT Port Setting Output...")
        self.olt_port_output.setReadOnly(True)

        # Create Checkbox
        self.port_checkbox = QCheckBox("Debug")
        self.port_checkbox.setChecked(False)
        self.port_checkbox.stateChanged.connect(self.on_checkbox_toggle)

        self.port_config_btn = QPushButton("Config")
        self.port_display_btn = QPushButton("Status")
        self.port_delete_btn = QPushButton("Delete")
        self.port_config_btn.clicked.connect(self.config_port_settings)
        self.port_display_btn.clicked.connect(self.display_port_settings)
        self.port_delete_btn.clicked.connect(self.delete_port_settings)

        port_setting_btn_layout = QHBoxLayout()
        port_setting_btn_layout.addWidget(self.port_delete_btn)
        port_setting_btn_layout.addWidget(self.port_display_btn)
        port_setting_btn_layout.addWidget(self.port_config_btn)

        # Create a layout to position the checkbox at the bottom-right
        checkbox_layout = QHBoxLayout()
        checkbox_layout.addStretch()  # Push checkbox to the right
        checkbox_layout.addWidget(self.port_checkbox)

        olt_port_layout.addWidget(self.olt_port_output)
        olt_port_layout.addLayout(checkbox_layout)
        olt_port_layout.addLayout(port_setting_btn_layout)
        olt_port_group.setLayout(olt_port_layout)
        main_layout.addWidget(olt_port_group)

        # === Next Button ===
        self.next_button = QPushButton("Next →")
        self.next_button.setFixedSize(100, 30)
        self.next_button.setStyleSheet(
            """
            QPushButton {
                background-color: #A5D6A7;
                border: 2px solid #1e90ff;
                border-radius: 5px;
                color: white;
                font-weight: bold;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """
        )
        # self.next_button.clicked.connect(self.go_to_next)
        main_layout.addWidget(self.next_button, alignment=Qt.AlignRight)

        self.setLayout(main_layout)

    def go_to_next(self):
        """Switch to Second Page"""
        self.stack.setCurrentIndex(1)

    def on_checkbox_toggle(self, state):
        """Store checkbox state in a class variable."""
        self.debug_enabled = state == 2  # Qt.Checked = 2, Qt.Unchecked = 0
        print(f"Checkbox State Updated: {self.debug_enabled}")  # Prints True/False

    def get_olt_data(self):
        """Retrieve IP Address, VLAN, and OLT Port for ONT Page"""
        return {
            "ip": self.ip_input.text().strip(),
            "vlan": self.vlan_input.text().strip(),
            "olt_port": self.olt_port_input.text().strip(),
        }

    def validate_ip(self, ip):
        """Validate IP Address format and range."""
        ip_pattern = r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$"

        # Check if IP matches the pattern
        match = re.match(ip_pattern, ip)
        if not ip or not match:
            return "Invalid IP Address format!"

        # Ensure all octets are in the range 0-255
        if all(0 <= int(octet) <= 255 for octet in match.groups()):
            return None  # Valid IP, return None (no error)
        else:
            return "Invalid IP Address range!"

    def validate_and_get_credentials(self):
        """Extracts and validates IP, Username, and Password."""
        ip = self.ip_input.text().strip()
        username = self.user_input.text().strip()
        password = self.password_input.text().strip()

        # Validate IP
        ip_error = self.validate_ip(ip)
        if ip_error:
            self.olt_output.setText(ip_error)
            self.olt_output.setStyleSheet("font-weight: bold; color: red;")
            return ip_error, None  # Return error message if IP is invalid

        # Validate Username
        if not username:
            self.olt_output.setText("Username cannot be empty!")
            self.olt_output.setStyleSheet("font-weight: bold; color: red;")
            return "Username cannot be empty!", None

        # Validate Password
        if len(password) < 4:
            self.olt_output.setText("Password must be at least 4 characters long!")
            self.olt_output.setStyleSheet("font-weight: bold; color: red;")
            return "Password must be at least 4 characters long!", None

        validated_data = {"ip": ip, "username": username, "password": password}
        return None, validated_data        

    def send_telnet_request(self, endpoint, data):
        """
        Sends a POST request to the given API endpoint with provided data.
        Handles errors and updates the output box accordingly.
        """
        try:
            response = requests.post(endpoint, json=data)
            if response.status_code == 200:
                self.olt_output.setText(f"Success | {response.json().get('message')}")
                self.olt_output.setStyleSheet("font-weight: bold; color: green;")
            else:
                self.olt_output.setText(f"Error | {response.json().get('detail')}")
                self.olt_output.setStyleSheet("font-weight: bold; color: red;")
        except requests.exceptions.RequestException as e:
            self.olt_output.setText(f"Critical | {e}")
            self.olt_output.setStyleSheet("font-weight: bold; color: red;")

    def connect_olt_session(self):
        """Collect, validate, and send data to the backend"""
        error, data = self.validate_and_get_credentials()

        if data:
            self.send_telnet_request(f"{BACKEND_URL}/olt/connect_telnet", data)

    def display_olt_session(self):
        """Collect, validate, and send data to the backend"""
        error, data = self.validate_and_get_credentials()

        if data:
            self.send_telnet_request(f"{BACKEND_URL}/olt/display_telnet", data)

    def disconnect_olt_session(self):
        """Collect, validate, and send data to the backend"""
        error, data = self.validate_and_get_credentials()

        if data:
            self.send_telnet_request(f"{BACKEND_URL}/olt/disconnect_telnet", data)

    def send_request(self, endpoint, data, output_box):
        try:
            response = requests.post(f"{BACKEND_URL}/olt/{endpoint}", json=data)
            if response.status_code == 200:  # Success
                message = response.json().get("message")
                formatted_text = f"""
                    <p style="color: green; font-weight: bold;">Success | {message}</p>
                """
                output_box.setHtml(formatted_text)
                if self.debug_enabled:
                    output_box.append(f"{response.json().get('output')}")
                    output_box.setStyleSheet("color: blue;")
            elif response.status_code == 400:  # Command execution error
                error_details = response.json().get("detail", {})
                formatted_text = f"""
                    <p style="color: orange; font-weight: bold;">Error | {error_details.get('message')}</p>
                """
                output_box.setHtml(formatted_text)
                if self.debug_enabled:
                    output_box.append(f"{error_details.get('output')}")
                    output_box.setStyleSheet("color: blue;")
            elif response.status_code == 500:  # Connection or unexpected failure
                error_details = response.json().get("detail", {})
                formatted_text = f"""
                    <p style="color: red; font-weight: bold;">Critical | {error_details.get('message')}</p>
                """
                output_box.setHtml(formatted_text)
                if self.debug_enabled:
                    output_box.appendt(f"{error_details.get('output')}")
                    output_box.setStyleSheet("color: blue;")
        except requests.exceptions.RequestException as e:
            output_box.setText(f"Unknown Error Occurred | {e}")
            output_box.setStyleSheet("color: red; font-weight: bold;")

    def send_request_summary(self, endpoint, data, output_box):
        try:
            response = requests.post(f"{BACKEND_URL}/olt/{endpoint}", json=data)
            
            if response.status_code == 200:  # Success
                message = response.json().get("message")
                formatted_text = f"""
                    <p style="color: green; font-weight: bold;">Success | {message}</p>
                """
                output_box.setHtml(formatted_text)
                output_box.append(f"{response.json().get('output')}")
                output_box.setStyleSheet("color: blue;")
            elif response.status_code == 400:  # Command execution error
                error_details = response.json().get("detail", {})
                formatted_text = f"""
                    <p style="color: orange; font-weight: bold;">Error | {error_details.get('message')}</p>
                """
                output_box.setHtml(formatted_text)
                output_box.append(f"{error_details.get('output')}")
                output_box.setStyleSheet("color: blue;")
            elif response.status_code == 500:  # Connection or unexpected failure
                error_details = response.json().get("detail", {})
                formatted_text = f"""
                    <p style="color: red; font-weight: bold;">Critical | {error_details.get('message')}</p>
                """
                output_box.setHtml(formatted_text)
                output_box.appendt(f"{error_details.get('output')}")
                output_box.setStyleSheet("color: blue;")
        except requests.exceptions.RequestException as e:
            output_box.setText(f"Unknown Error Occurred | {e}")
            output_box.setStyleSheet("color: red; font-weight: bold;")

    def validate_port_settings(self, olt_port, vlan_id, uplink_port):
        port_pattern = r"^\d{1,2}/\d{1,2}/\d{1,2}$"
        vlan_pattern = r"^\d{1,5}$"

        if not re.match(port_pattern, olt_port):
            return "Invalid OLT Port format! Use Frame/Slot/Port."
        if not re.match(vlan_pattern, vlan_id) or not (1 <= int(vlan_id) <= 65535):
            return "Invalid VLAN ID! Range: 1-65535."
        if not re.match(port_pattern, uplink_port):
            return "Invalid Uplink Port format! Use Frame/Slot/Port."
        return None

    def get_validated_port_data(self):
        """Extract and validate port settings, returning errors or validated data."""
        olt_port = self.olt_port_input.text().strip()
        vlan_id = self.vlan_input.text().strip()
        uplink_port = self.uplink_input.text().strip()
        ip = self.ip_input.text().strip()

        validation_error = self.validate_port_settings(olt_port, vlan_id, uplink_port)
    
        if validation_error:
            self.olt_port_output.setText(validation_error)
            self.olt_port_output.setStyleSheet("color: red;")
            return validation_error, None  # Return error and no valid data

        validated_data = {
            "ip": ip,
            "uplink_port": uplink_port,
            "vlan_id": vlan_id,
            "pon_port": olt_port
        }

        return None, validated_data  # No error, return validated data

    def config_port_settings(self):
        error, data = self.get_validated_port_data()
        if data:
            print(f"Configuring IP: {data['ip']}, Uplink Port: {data['uplink_port']}, VLAN: {data['vlan_id']}, OLT Port: {data['pon_port']}")
            self.send_request("configure_port_setting", data, self.olt_port_output)

    def display_port_settings_details(self):
        error, data = self.get_validated_port_data()
        if data:
            print(f"Status Details IP: {data['ip']}, Uplink Port: {data['uplink_port']}, VLAN: {data['vlan_id']}, OLT Port: {data['pon_port']}")
            self.send_request("display_port_status_details", data, self.olt_port_output)

    def display_port_settings_summary(self):
        error, data = self.get_validated_port_data()
        if data:
            print(f"Status Summary IP: {data['ip']}, Uplink Port: {data['uplink_port']}, VLAN: {data['vlan_id']}, OLT Port: {data['pon_port']}")
            self.send_request_summary("display_port_status_details", data, self.olt_port_output)

    def display_port_settings(self):
        if self.debug_enabled:
            self.display_port_settings_details()
        else:
            self.display_port_settings_summary()
        

    def delete_port_settings(self):
        error, data = self.get_validated_port_data()
        if data:
            print(f"Deleting IP: {data['ip']}, Uplink Port: {data['uplink_port']}, VLAN: {data['vlan_id']}, OLT Port: {data['pon_port']}")
            self.send_request("display_port_status_details", data, self.olt_port_output)
