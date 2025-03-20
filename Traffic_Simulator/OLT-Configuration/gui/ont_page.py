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

class ONTConfiguration(QWidget):
    def __init__(self, stack, olt_data):
        super().__init__()
        self.stack = stack
        self.debug_enabled = False
        self.olt_data = olt_data  # Store the received dictionary
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # Function to create a row with Label + Input
        def add_labeled_input(label_text, input_widget):
            row_layout = QHBoxLayout()
            label = QLabel(label_text)
            label.setFixedWidth(70)  # Set fixed width for alignment
            row_layout.addWidget(label)
            row_layout.addWidget(input_widget)
            return row_layout

        # === ONT Profile Configuration Block ===
        ont_profile_group = QGroupBox("ONT Profile Configuration")
        ont_profile_group.setStyleSheet("QGroupBox { font-weight: bold; font-size: 14px; }")
        ont_profile_layout = QVBoxLayout()

        # Input Fields
        self.profile_id_input = QLineEdit(placeholderText="0-8192")
        self.profile_id_input.setText(self.olt_data.get('vlan_id'))

        self.tcont_id_input = QLineEdit(placeholderText="0-127")
        vlan_id = int(self.olt_data.get('vlan_id', 0))
        default_tcont_id = vlan_id % 10
        self.tcont_id_input.setText(str(default_tcont_id))

        self.gemport_id_input = QLineEdit(placeholderText="0-1023")
        self.gemport_id_input.setText("1")

        # Add labeled inputs using function
        ont_profile_layout.addLayout(add_labeled_input("Profile ID:", self.profile_id_input))
        ont_profile_layout.addLayout(add_labeled_input("TCONT ID:", self.tcont_id_input))
        ont_profile_layout.addLayout(add_labeled_input("GEM Port ID:", self.gemport_id_input))

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

        # Input Fields
        self.serial_number_input = QLineEdit(placeholderText="XXXX-XXXXXXXX or XXXXXXXXXXXX")
        self.serial_number_input.setText("DPDP-C1000168")

        self.ont_id_input = QLineEdit(placeholderText="0-127")
        vlan_id = int(self.olt_data.get('vlan_id', 0))
        default_ont_id = vlan_id % 10
        self.ont_id_input.setText(str(default_ont_id))

        # Add labeled inputs using function
        ont_service_layout.addLayout(add_labeled_input("Serial Number:", self.serial_number_input))
        ont_service_layout.addLayout(add_labeled_input("ONT ID:", self.ont_id_input))

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

        # === Control Buttons ===
        control_button_layout = QHBoxLayout()
        self.save_button = QPushButton("Save")
        self.save_button.setFixedSize(100, 30)
        self.save_button.clicked.connect(self.save_configurations)
    
        self.back_button = QPushButton("← Back")
        self.back_button.setFixedSize(100, 30)
        self.back_button.setStyleSheet(
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
        self.back_button.clicked.connect(self.go_to_back)
        control_button_layout.addStretch(2)
        control_button_layout.addWidget(self.save_button, alignment=Qt.AlignCenter)
        control_button_layout.addStretch(1)
        control_button_layout.addWidget(self.back_button, alignment=Qt.AlignRight)
        main_layout.addLayout(control_button_layout)

        self.setLayout(main_layout)

    def go_to_back(self):
        self.stack.setCurrentIndex(0)

    def on_checkbox_toggle(self, state):
        self.debug_enabled = state == 2

    def update_olt_data(self, new_olt_data):
        """Update ONT input fields with latest OLT data if not already set"""
        
        if self.profile_id_input.text().strip() == "":
            self.profile_id_input.setText(new_olt_data.get('vlan_id', ""))
        if self.tcont_id_input.text().strip() == "":
            vlan_id = int(new_olt_data.get('vlan_id', 0))
            default_tcont_id = vlan_id % 10
            self.tcont_id_input.setText(str(default_tcont_id))
        if self.gemport_id_input.text().strip() == "":
            self.gemport_id_input.setText("1")
        if self.serial_number_input.text().strip() == "":
            self.serial_number_input.setText("DPDP-C1000168")
        if self.ont_id_input.text().strip() == "":
            vlan_id = int(new_olt_data.get('vlan_id', 0))
            default_ont_id = vlan_id % 10
            self.ont_id_input.setText(str(default_ont_id))

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
            send_request("ont/create_profile", data, self.ont_profile_output, DebugMode.DEBUG if self.debug_enabled else DebugMode.NO_DEBUG)

    def status_profile(self):
        data = self.validate_and_get_ont_profile_data()
        if data:
            if self.debug_enabled:
                send_request("ont/status_profile_details", data, self.ont_profile_output, DebugMode.DEBUG if self.debug_enabled else DebugMode.NO_DEBUG)
            else:
                send_request("ont/status_profile_summary", data, self.ont_profile_output, DebugMode.SUMMARY)

    def delete_profile(self):
        data = self.validate_and_get_ont_profile_data()
        if data:
            send_request("ont/delete_profile", data, self.ont_profile_output, DebugMode.DEBUG if self.debug_enabled else DebugMode.NO_DEBUG)

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
            send_request("ont/create_service", data, self.ont_service_output, DebugMode.DEBUG if self.debug_enabled else DebugMode.NO_DEBUG)

    def status_service(self):
        data = self.validate_and_get_ont_service_data()
        if data:
            if self.debug_enabled:
                send_request("ont/status_service_details", data, self.ont_service_output, DebugMode.DEBUG if self.debug_enabled else DebugMode.NO_DEBUG)
            else:
                send_request("ont/status_service_summary", data, self.ont_service_output, DebugMode.SUMMARY)

    def delete_service(self):
        data = self.validate_and_get_ont_service_data()
        if data:
            send_request("ont/delete_service", data, self.ont_service_output, DebugMode.DEBUG if self.debug_enabled else DebugMode.NO_DEBUG)

    def save_configurations(self):
        data = {"ip": self.olt_data.get("ip")}
        send_request("ont/save_configurations", data, self.ont_service_output, DebugMode.DEBUG if self.debug_enabled else DebugMode.NO_DEBUG)

