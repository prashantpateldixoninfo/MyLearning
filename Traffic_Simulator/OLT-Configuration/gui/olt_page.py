from qtpy.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QGroupBox,
    QCheckBox,
)
from qtpy.QtCore import Qt
from request_handler import send_request, send_telnet_request, DebugMode
import re

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

        # Function to create a row with Label + Input
        def add_labeled_input(label_text, input_widget):
            row_layout = QHBoxLayout()
            label = QLabel(label_text)
            label.setFixedWidth(70)  # Set fixed width for alignment
            row_layout.addWidget(label)
            row_layout.addWidget(input_widget)
            return row_layout

        # Input Fields for OLT Connection
        self.ip_input = QLineEdit(placeholderText="Enter IP Address")
        self.ip_input.setText("10.11.104.2")

        self.user_input = QLineEdit(placeholderText="Enter Username")
        self.user_input.setText("root")

        self.password_input = QLineEdit(placeholderText="Enter Password")
        self.password_input.setEchoMode(QLineEdit.Password)  # Hide password input
        self.password_input.setText("admin")

        # Add labeled input fields
        olt_layout.addLayout(add_labeled_input("IP Address:", self.ip_input))
        olt_layout.addLayout(add_labeled_input("Username:", self.user_input))
        olt_layout.addLayout(add_labeled_input("Password:", self.password_input))

        # Output & Buttons
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

        # Input Fields for OLT Port Setting
        self.uplink_input = QLineEdit(placeholderText="Uplink Port (Frame/Slot/Port)")
        self.uplink_input.setText("0/16/1")

        self.vlan_input = QLineEdit(placeholderText="VLAN (1-65535)")
        self.vlan_input.setText("222")

        self.olt_port_input = QLineEdit(placeholderText="OLT PON Port (Frame/Slot/Port)")
        self.olt_port_input.setText("0/1/1")

        # Add labeled input fields
        olt_port_layout.addLayout(add_labeled_input("Uplink Port:", self.uplink_input))
        olt_port_layout.addLayout(add_labeled_input("VLAN ID:", self.vlan_input))
        olt_port_layout.addLayout(add_labeled_input("OLT PON Port:", self.olt_port_input))

        # Output & Buttons
        self.olt_port_output = QTextEdit(placeholderText="OLT Port Setting Output...")
        self.olt_port_output.setReadOnly(True)

        # Checkbox Layout (Bottom-Right)
        self.port_checkbox = QCheckBox("Debug")
        self.port_checkbox.setChecked(False)
        self.port_checkbox.stateChanged.connect(self.on_checkbox_toggle)

        checkbox_layout = QHBoxLayout()
        checkbox_layout.addStretch()
        checkbox_layout.addWidget(self.port_checkbox)

        # Buttons for Port Settings
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

        olt_port_layout.addWidget(self.olt_port_output)
        olt_port_layout.addLayout(checkbox_layout)
        olt_port_layout.addLayout(port_setting_btn_layout)
        olt_port_group.setLayout(olt_port_layout)
        main_layout.addWidget(olt_port_group)

        # === Control Buttons ===
        control_button_layout = QHBoxLayout()
        self.save_button = QPushButton("Save")
        self.save_button.setFixedSize(100, 30)
        self.save_button.clicked.connect(self.save_configurations)

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
        control_button_layout.addStretch(2)
        control_button_layout.addWidget(self.save_button, alignment=Qt.AlignCenter)
        control_button_layout.addStretch(1)
        control_button_layout.addWidget(self.next_button, alignment=Qt.AlignRight)
        main_layout.addLayout(control_button_layout)

        self.setLayout(main_layout)

    def go_to_next(self):
        """Switch to Second Page"""
        self.stack.setCurrentIndex(1)

    def on_checkbox_toggle(self, state):
        """Store checkbox state in a class variable."""
        self.debug_enabled = state == 2  # Qt.Checked = 2, Qt.Unchecked = 0

    def get_olt_data(self):
        """Retrieve IP Address, VLAN, and OLT Port for ONT Page"""
        return {
            "ip": self.ip_input.text().strip(),
            "vlan_id": self.vlan_input.text().strip(),
            "pon_port": self.olt_port_input.text().strip(),
        }

    def validate_ip(self, ip):
        """Validate IP Address format and range."""
        ip_pattern = r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$"

        if not ip:
            return "No IP Address provided!"

        match = re.match(ip_pattern, ip)
        if not match:
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
            return None

        # Validate Username
        if not username:
            self.olt_output.setText("Username cannot be empty!")
            self.olt_output.setStyleSheet("font-weight: bold; color: red;")
            return None

        # Validate Password
        if len(password) < 4:
            self.olt_output.setText("Password must be at least 4 characters long!")
            self.olt_output.setStyleSheet("font-weight: bold; color: red;")
            return None

        validated_data = {"ip": ip, "username": username, "password": password}
        return validated_data        

    def connect_olt_session(self):
        """Collect, validate, and send data to the backend"""
        data = self.validate_and_get_credentials()
        if data:
            send_telnet_request("olt/connect_telnet", data, self.olt_output)

    def display_olt_session(self):
        """Collect, validate, and send data to the backend"""
        data = self.validate_and_get_credentials()
        if data:
            send_telnet_request("olt/display_telnet", data, self.olt_output)

    def disconnect_olt_session(self):
        """Collect, validate, and send data to the backend"""
        data = self.validate_and_get_credentials()
        if data:
            send_telnet_request("olt/disconnect_telnet", data, self.olt_output)

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
            return None  # Return error and no valid data

        validated_data = {
            "ip": ip,
            "uplink_port": uplink_port,
            "vlan_id": vlan_id,
            "pon_port": olt_port
        }

        return validated_data  # No error, return validated data

    def config_port_settings(self):
        data = self.get_validated_port_data()
        if data:
            send_request("olt/configure_port_setting", data, self.olt_port_output, DebugMode.DEBUG if self.debug_enabled else DebugMode.NO_DEBUG)

    def display_port_settings(self):
        data = self.get_validated_port_data()
        if self.debug_enabled:
            send_request("olt/display_port_status_details", data, self.olt_port_output, DebugMode.DEBUG if self.debug_enabled else DebugMode.NO_DEBUG)
        else:
            send_request("olt/display_port_status_summary", data, self.olt_port_output, DebugMode.SUMMARY)

    def delete_port_settings(self):
        data = self.get_validated_port_data()
        if data:
            send_request("olt/delete_port_setting", data, self.olt_port_output, DebugMode.DEBUG if self.debug_enabled else DebugMode.NO_DEBUG)

    def save_configurations(self):
        data = {"ip": self.ip_input.text().strip()}
        send_request("olt/save_configurations", data, self.olt_port_output, DebugMode.DEBUG if self.debug_enabled else DebugMode.NO_DEBUG)

