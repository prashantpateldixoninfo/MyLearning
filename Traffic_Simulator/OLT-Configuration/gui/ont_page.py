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
import sys
import os
import re

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from shared.config import BACKEND_URL


class ONTConfiguration(QWidget):
    def __init__(self, stack, olt_data):
        super().__init__()
        self.stack = stack
        self.debug_enabled = False
        self.olt_data = olt_data  # Store the received dictionary
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # === ONT Profile Configuration Block ===
        ont_profile_group = QGroupBox("ONT Profile Configuration")
        ont_profile_group.setStyleSheet("QGroupBox { font-weight: bold; font-size: 14px; }")
        ont_profile_layout = QVBoxLayout()

        self.profile_id_input = QLineEdit(placeholderText="Profile ID (0-8192)")
        self.profile_id_input.setText(self.olt_data.get('vlan_id'))
        self.tcont_id_input = QLineEdit(placeholderText="TCONT ID (0-127)")
        self.tcont_id_input.setText("1")
        self.gemport_id_input = QLineEdit(placeholderText="GEM Port ID (0-1023)")
        self.gemport_id_input.setText("1")

        ont_profile_layout.addWidget(self.profile_id_input)
        ont_profile_layout.addWidget(self.tcont_id_input)
        ont_profile_layout.addWidget(self.gemport_id_input)

        self.ont_profile_output = QTextEdit(placeholderText="ONT Profile Configuration Output...")
        self.ont_profile_output.setReadOnly(True)

        self.profile_checkbox = QCheckBox("Debug")
        self.profile_checkbox.setChecked(False)
        self.profile_checkbox.stateChanged.connect(self.on_checkbox_toggle)

        self.profile_create_btn = QPushButton("Create")
        self.profile_status_btn = QPushButton("Status")
        self.profile_delete_btn = QPushButton("Delete")
        self.profile_create_btn.clicked.connect(self.create_profile)
        self.profile_status_btn.clicked.connect(self.status_profile)
        self.profile_delete_btn.clicked.connect(self.delete_profile)

        profile_btn_layout = QHBoxLayout()
        profile_btn_layout.addWidget(self.profile_delete_btn)
        profile_btn_layout.addWidget(self.profile_status_btn)
        profile_btn_layout.addWidget(self.profile_create_btn)

        checkbox_layout = QHBoxLayout()
        checkbox_layout.addStretch()
        checkbox_layout.addWidget(self.profile_checkbox)

        ont_profile_layout.addWidget(self.ont_profile_output)
        ont_profile_layout.addLayout(checkbox_layout)
        ont_profile_layout.addLayout(profile_btn_layout)
        ont_profile_group.setLayout(ont_profile_layout)
        main_layout.addWidget(ont_profile_group)

        # === ONT Service Configuration Block ===
        ont_service_group = QGroupBox("ONT Service Configuration")
        ont_service_group.setStyleSheet("QGroupBox { font-weight: bold; font-size: 14px; }")
        ont_service_layout = QVBoxLayout()

        self.serial_number_input = QLineEdit(placeholderText="Serial Number (XXXX-XXXXXXXX or XXXXXXXXXXXX)")
        self.serial_number_input.setText("ZYOT-CE000292")
        self.ont_id_input = QLineEdit(placeholderText="ONT ID (0-127)")
        self.ont_id_input.setText("0")

        ont_service_layout.addWidget(self.serial_number_input)
        ont_service_layout.addWidget(self.ont_id_input)

        self.ont_service_output = QTextEdit(placeholderText="ONT Service Configuration Output...")
        self.ont_service_output.setReadOnly(True)

        self.service_checkbox = QCheckBox("Debug")
        self.service_checkbox.setChecked(False)
        self.service_checkbox.stateChanged.connect(self.on_checkbox_toggle)

        self.service_create_btn = QPushButton("Create")
        self.service_status_btn = QPushButton("Status")
        self.service_delete_btn = QPushButton("Delete")
        self.service_create_btn.clicked.connect(self.create_service)
        self.service_status_btn.clicked.connect(self.status_service)
        self.service_delete_btn.clicked.connect(self.delete_service)

        service_btn_layout = QHBoxLayout()
        service_btn_layout.addWidget(self.service_delete_btn)
        service_btn_layout.addWidget(self.service_status_btn)
        service_btn_layout.addWidget(self.service_create_btn)

        checkbox_layout = QHBoxLayout()
        checkbox_layout.addStretch()
        checkbox_layout.addWidget(self.service_checkbox)

        ont_service_layout.addWidget(self.ont_service_output)
        ont_service_layout.addLayout(checkbox_layout)
        ont_service_layout.addLayout(service_btn_layout)
        ont_service_group.setLayout(ont_service_layout)
        main_layout.addWidget(ont_service_group)

        back_button = QPushButton("← Back")
        back_button.setFixedSize(100, 30)
        back_button.setStyleSheet(
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
        back_button.clicked.connect(self.go_to_back)
        main_layout.addWidget(back_button, alignment=Qt.AlignRight)

        self.setLayout(main_layout)

    def go_to_back(self):
        self.stack.setCurrentIndex(0)

    def on_checkbox_toggle(self, state):
        self.debug_enabled = state == 2
        print(f"Checkbox State Updated: {self.debug_enabled}")

    def send_request(self, endpoint, data, output_box):
        try:
            response = requests.post(f"{BACKEND_URL}/ont/{endpoint}", json=data)
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
                    output_box.append(f"{error_details.get('output')}")
                    output_box.setStyleSheet("color: blue;")
        except requests.exceptions.RequestException as e:
            output_box.setText(f"Unknown Error Occurred | {e}")
            output_box.setStyleSheet("color: red; font-weight: bold;")

    def send_request_summary(self, endpoint, data, output_box):
        try:
            response = requests.post(f"{BACKEND_URL}/ont/{endpoint}", json=data)
            
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
                output_box.append(f"{error_details.get('output')}")
                output_box.setStyleSheet("color: blue;")
        except requests.exceptions.RequestException as e:
            output_box.setText(f"Unknown Error Occurred | {e}")
            output_box.setStyleSheet("color: red; font-weight: bold;")

    def validate_and_get_ont_profile_data(self):
        """Validate ONT Profile Inputs, Show Errors if Any, and Return Valid Data"""

        # Extract input values
        profile_id = self.profile_id_input.text().strip()
        tcont_id = self.tcont_id_input.text().strip()
        gemport_id = self.gemport_id_input.text().strip()

        # Validation Rules
        if not profile_id.isdigit() or not (0 <= int(profile_id) <= 8192):
            self.ont_profile_output.setText("Invalid Profile ID! Must be between 0-8192.")
            self.ont_profile_output.setStyleSheet("font-weight: bold; color: red;")
            return None

        if not tcont_id.isdigit() or not (0 <= int(tcont_id) <= 127):
            self.ont_profile_output.setText("Invalid TCONT ID! Must be between 0-127.")
            self.ont_profile_output.setStyleSheet("font-weight: bold; color: red;")
            return None

        if not gemport_id.isdigit() or not (0 <= int(gemport_id) <= 1023):
            self.ont_profile_output.setText("Invalid GEM Port ID! Must be between 0-1023.")
            self.ont_profile_output.setStyleSheet("font-weight: bold; color: red;")
            return None

        # Construct Valid Data Dictionary
        valid_data = {
            "ip": self.olt_data.get("ip"),
            "profile_id": profile_id,
            "tcont_id": tcont_id,
            "gemport_id": gemport_id,
            "vlan_id": self.olt_data.get("vlan_id"),
        }
        return valid_data

    def create_profile(self):
        data = self.validate_and_get_ont_profile_data()
        if data:
            self.send_request("create_profile", data, self.ont_profile_output)

    def status_profile(self):
        data = self.validate_and_get_ont_profile_data()
        if data:
            if self.debug_enabled:
                self.send_request("status_profile_details", data, self.ont_profile_output)
            else:
                self.send_request_summary("status_profile_summary", data, self.ont_profile_output)

    def delete_profile(self):
        data = self.validate_and_get_ont_profile_data()
        if data:
            self.send_request("delete_profile", data, self.ont_profile_output)

    def validate_and_get_ont_service_data(self):
        """Validate ONT Serivce Inputs, Show Errors if Any, and Return Valid Data"""
        serial_number = self.serial_number_input.text().strip()
        ont_id = self.ont_id_input.text().strip()

        serial_pattern = r"^(\w{12}|\w{14}|\w{16}|\w{4}-\w{8})$"
        if not re.match(serial_pattern, serial_number):
            self.ont_service_output.setText("Invalid Serial Number! Format: XXXXXXXXXXXX or XXXX-XXXXXXXX.")
            self.ont_service_output.setStyleSheet("font-weight: bold; color: red;")
            return None

        if not ont_id.isdigit() or not (0 <= int(ont_id) <= 127):
            self.ont_service_output.setText("Invalid ONT ID! Must be between 0-127.")
            self.ont_service_output.setStyleSheet("font-weight: bold; color: red;")
            return None

        # Construct Valid Data Dictionary
        valid_data = {
            "ip": self.olt_data.get("ip"),
            "serial_number": serial_number,
            "ont_id": ont_id,
            "vlan_id": self.olt_data.get("vlan_id"),
            "pon_port": self.olt_data.get("pon_port"),
            "gemport_id": self.gemport_id_input.text().strip(),
            "profile_id": self.profile_id_input.text().strip(),
        }
        return valid_data

    def create_service(self):
        data = self.validate_and_get_ont_service_data()
        if data:
            self.send_request("create_service", data, self.ont_service_output)

    def status_service(self):
        data = self.validate_and_get_ont_service_data()
        if data:
            if self.debug_enabled:
                self.send_request("status_service_details", data, self.ont_service_output)
            else:
                self.send_request_summary("status_service_summary", data, self.ont_service_output)

    def delete_service(self):
        data = self.validate_and_get_ont_service_data()
        if data:
            self.send_request("delete_service", data, self.ont_service_output)
