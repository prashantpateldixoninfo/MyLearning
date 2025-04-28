from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QGroupBox,
    QTextEdit, QLabel
)
from PyQt5.QtCore import Qt
from request_handler import send_request, DebugMode

class DebugModeConfig(QWidget):
    def __init__(self, stack, traffic_page):
        super().__init__()
        self.stack = stack
        self.traffic_page = traffic_page
        self.debug_enabled = True
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # === Command Execution Block ===
        command_group = QGroupBox("Command Execution")
        command_group.setStyleSheet("QGroupBox { font-weight: bold; font-size: 14px; }")
        command_layout = QVBoxLayout()

        self.cmd_input = QTextEdit()
        self.cmd_input.setPlaceholderText("Enter commands...\nUse Shift+Enter for a new line, Enter to submit")
        self.cmd_input.setAcceptRichText(False)  # Plain text only
        self.cmd_input.keyPressEvent = self.handle_keypress  # Override key event

        btn_layout = QHBoxLayout()
        self.clear_btn = QPushButton("Clear")
        self.submit_btn = QPushButton("Submit")
        self.clear_btn.clicked.connect(self.clear_commands)
        self.submit_btn.clicked.connect(self.execute_commands)

        btn_layout.addWidget(self.clear_btn)
        btn_layout.addWidget(self.submit_btn)

        command_layout.addWidget(self.cmd_input)
        command_layout.addLayout(btn_layout)
        command_group.setLayout(command_layout)

        # === Command Output Block ===
        output_group = QGroupBox("Command Output")
        output_group.setStyleSheet("QGroupBox { font-weight: bold; font-size: 14px; }")
        output_layout = QVBoxLayout()

        self.cmd_output = QTextEdit()
        self.cmd_output.setReadOnly(True)

        output_layout.addWidget(self.cmd_output)
        output_group.setLayout(output_layout)

        # === Bottom Button Layout (Back, Save) ===
        button_layout = QHBoxLayout()
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
        self.save_button = QPushButton("Save")
        self.save_button.setFixedSize(100, 30)
        
        self.back_button.clicked.connect(self.go_to_back)
        self.save_button.clicked.connect(self.save_config)

        button_layout.addWidget(self.back_button)
        button_layout.addStretch()  # Center align Save button
        button_layout.addWidget(self.save_button)
        button_layout.addStretch()  # Right align if Next is added later

        # Add widgets to main layout
        main_layout.addWidget(command_group)
        main_layout.addWidget(output_group)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

    def handle_keypress(self, event):
        """Handle Enter and Shift+Enter behavior"""
        if event.key() == Qt.Key_Return:
            if event.modifiers() == Qt.ShiftModifier:
                self.cmd_input.insertPlainText("\n")  # Add a new line
            else:
                self.execute_commands()  # Submit on Enter
                return  # Prevent default new line
        else:
            QTextEdit.keyPressEvent(self.cmd_input, event)  # Normal behavior

    def execute_commands(self):
        """Execute commands"""
        command_text = self.cmd_input.toPlainText().strip()
        data = {
            "ip": "10.11.104.2", 
            "cmd": command_text
        }
        send_request("debug/execute_commands", data, self.cmd_output, DebugMode.DEBUG if self.debug_enabled else DebugMode.NO_DEBUG)
        

    def clear_commands(self):
        """Clear command input and output"""
        self.cmd_input.clear()
        self.cmd_output.clear()

    def go_to_back(self):
        """Navigate back to TrafficStatistics page"""
        self.stack.setCurrentWidget(self.traffic_page)

    def save_config(self):
        """Simulate saving configuration"""
        self.cmd_output.append("Configuration saved successfully! 💾")

    def update_data(self, traffic_data):
        """Update Debug Page with new Traffic Data if needed"""
        # You can use traffic_data to update UI elements if required
        pass