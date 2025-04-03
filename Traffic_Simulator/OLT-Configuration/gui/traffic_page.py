from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QPushButton, QHBoxLayout, QTextEdit
from PyQt5.QtCore import Qt
from debug_page import DebugModeConfig  # Import Debug Page

class TrafficStatistics(QWidget):
    def __init__(self, stack, ont_page):
        super().__init__()
        self.stack = stack
        self.ont_page = ont_page  # Reference to ONT Page
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # === OLT Statistics Block ===
        olt_group = QGroupBox("OLT Statistics")
        olt_group.setStyleSheet("QGroupBox { font-weight: bold; font-size: 14px; }")
        olt_layout = QVBoxLayout()

        self.olt_stat_output = QTextEdit()
        self.olt_stat_output.setPlaceholderText("OLT Traffic Statistics Output...")
        self.olt_stat_output.setReadOnly(True)

        olt_layout.addWidget(self.olt_stat_output)
        olt_group.setLayout(olt_layout)
        main_layout.addWidget(olt_group)

        # === ONT Statistics Block ===
        ont_group = QGroupBox("ONT Statistics")
        ont_group.setStyleSheet("QGroupBox { font-weight: bold; font-size: 14px; }")
        ont_layout = QVBoxLayout()

        self.ont_stat_output = QTextEdit()
        self.ont_stat_output.setPlaceholderText("ONT Traffic Statistics Output...")
        self.ont_stat_output.setReadOnly(True)

        ont_layout.addWidget(self.ont_stat_output)
        ont_group.setLayout(ont_layout)
        main_layout.addWidget(ont_group)

        # === Button Layout ===
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
        self.back_button.clicked.connect(self.go_to_back)
        
        self.save_button = QPushButton("Save")
        self.save_button.setFixedSize(100, 30)
        self.save_button.clicked.connect(self.save_statistics)

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
        self.next_button.clicked.connect(self.go_to_next_page)  # Placeholder for the next page

        button_layout.addWidget(self.back_button, alignment=Qt.AlignLeft)
        button_layout.addWidget(self.save_button, alignment=Qt.AlignCenter)
        button_layout.addWidget(self.next_button, alignment=Qt.AlignRight)

        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

    def go_to_back(self):
        """Navigate back to ONT Configuration page"""
        self.stack.setCurrentWidget(self.ont_page)

    def save_statistics(self):
        """Placeholder for saving statistics"""
        print("Saving traffic statistics...")

    def get_statistics_data(self):
        """Fetch and return OLT and ONT statistics data"""
        pass

    def go_to_next_page(self):
        """Create Debug Page dynamically with latest Traffic Data"""

        if not hasattr(self, 'debug_page'):
            self.debug_page = DebugModeConfig(self.stack, self)  # Pass reference of traffic page
            self.stack.addWidget(self.debug_page)  # Add Debug Page to stack
        else:
            # Keep existing data, only update if necessary
            self.debug_page.update_data(self.get_statistics_data())

        self.stack.setCurrentWidget(self.debug_page)  # Switch to Debug Page
