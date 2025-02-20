from qtpy.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QGroupBox,
)
from qtpy.QtCore import Qt
import requests
import re

BACKEND_URL = "http://127.0.0.1:8000"


class OLTConfiguration(QWidget):
    """First Page with Next Button to Navigate to the Second Page"""

    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # === OLT Connection Block ===
        olt_connection_group = QGroupBox("OLT Connection")
        olt_connection_group.setStyleSheet(
            "QGroupBox { font-weight: bold; font-size: 14px; }"
        )
        olt_layout = QVBoxLayout()

        # Input Fields for OLT Connection
        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("IP Address")

        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("User")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)  # Hide password input

        olt_layout.addWidget(self.ip_input)
        olt_layout.addWidget(self.user_input)
        olt_layout.addWidget(self.password_input)

        # Output Field and Submit Button
        self.olt_output = QTextEdit()
        self.olt_output.setPlaceholderText("OLT Connection Output...")
        self.olt_output.setReadOnly(True)

        self.olt_submit_btn = QPushButton("Submit")
        self.olt_submit_btn.clicked.connect(self.submit_credentials)

        olt_button_layout = QHBoxLayout()
        olt_button_layout.addWidget(self.olt_output)
        olt_button_layout.addWidget(self.olt_submit_btn)

        olt_layout.addLayout(olt_button_layout)
        olt_connection_group.setLayout(olt_layout)

        main_layout.addWidget(olt_connection_group)

        # === OLT Port Setting Block ===
        olt_port_group = QGroupBox("OLT Port Setting")
        olt_port_group.setStyleSheet(
            "QGroupBox { font-weight: bold; font-size: 14px; }"
        )
        olt_port_layout = QVBoxLayout()

        # Input Fields for OLT Port Setting
        self.olt_port_input = QLineEdit()
        self.olt_port_input.setPlaceholderText("OLT Port")

        self.vlan_input = QLineEdit()
        self.vlan_input.setPlaceholderText("VLAN")

        self.upstream_input = QLineEdit()
        self.upstream_input.setPlaceholderText("Upstream Port")

        olt_port_layout.addWidget(self.olt_port_input)
        olt_port_layout.addWidget(self.vlan_input)
        olt_port_layout.addWidget(self.upstream_input)

        # Output Field and Submit Button
        self.olt_port_output = QTextEdit()
        self.olt_port_output.setPlaceholderText("OLT Port Setting Output...")
        self.olt_port_output.setReadOnly(True)

        self.olt_port_submit_btn = QPushButton("Submit")

        olt_port_button_layout = QHBoxLayout()
        olt_port_button_layout.addWidget(self.olt_port_output)
        olt_port_button_layout.addWidget(self.olt_port_submit_btn)

        olt_port_layout.addLayout(olt_port_button_layout)
        olt_port_group.setLayout(olt_port_layout)

        main_layout.addWidget(olt_port_group)

        # === Next Button ===
        next_button = QPushButton("Next →")
        next_button.setFixedSize(100, 30)
        next_button.setStyleSheet(
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
        next_button.clicked.connect(self.go_to_next)
        main_layout.addWidget(next_button, alignment=Qt.AlignRight)

        self.setLayout(main_layout)

    def go_to_next(self):
        """Switch to Second Page"""
        self.stack.setCurrentIndex(1)

    def validate_inputs(self, ip, username, password):
        """Validate IP Address, Username, and Password"""
        ip_pattern = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"

        if not ip or not re.match(ip_pattern, ip):
            return "Invalid IP Address format!"
        if not username:
            return "Username cannot be empty!"
        if len(password) < 4:
            return "Password must be at least 4 characters long!"

        return None

    def submit_credentials(self):
        """Collect, validate, and send data to the backend"""
        ip = self.ip_input.text().strip()
        username = self.user_input.text().strip()
        password = self.password_input.text().strip()

        validation_error = self.validate_inputs(ip, username, password)
        if validation_error:
            self.olt_output.setText(validation_error)
            self.olt_output.setStyleSheet("color: red;")
            return

        data = {"ip": ip, "username": username, "password": password}
        try:
            response = requests.post(f"{BACKEND_URL}/connect", json=data)
            if response.status_code == 200:
                self.olt_output.setText(f"Success: {response.json().get('message')}")
                self.olt_output.setStyleSheet("color: green;")
            else:
                self.olt_output.setText(f"Error: {response.json().get('error')}")
                self.olt_output.setStyleSheet("color: red;")
        except requests.exceptions.RequestException as e:
            self.olt_output.setText(f"Connection Error: {e}")
            self.olt_output.setStyleSheet("color: red;")
