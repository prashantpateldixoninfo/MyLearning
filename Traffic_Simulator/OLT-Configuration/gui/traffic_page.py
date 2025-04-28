from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QPushButton, QHBoxLayout, QTextEdit
from PyQt5.QtCore import Qt
from debug_page import DebugModeConfig  # Import Debug Page
from request_handler import send_request, DebugMode

class TrafficStatistics(QWidget):
    def __init__(self, stack, ont_page):
        super().__init__()
        self.stack = stack
        self.ont_page = ont_page  # Reference to ONT Page
        self.debug_enabled = True 
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # === OLT Port Statistics Block ===
        olt_group = QGroupBox("OLT Port Statistics")
        olt_group.setStyleSheet("QGroupBox { font-weight: bold; font-size: 14px; }")
        olt_layout = QVBoxLayout()

        self.olt_stat_output = QTextEdit()
        self.olt_stat_output.setPlaceholderText("OLT Port Traffic Statistics Output...")
        self.olt_stat_output.setReadOnly(True)

        self.olt_refresh_btn = QPushButton("Refresh")
        self.olt_refresh_btn.setFixedSize(100, 25)
        self.olt_refresh_btn.clicked.connect(self.refresh_olt_statistics)

        olt_layout.addWidget(self.olt_stat_output)
        olt_layout.addWidget(self.olt_refresh_btn, alignment=Qt.AlignRight)
        olt_group.setLayout(olt_layout)
        main_layout.addWidget(olt_group)

        # === Upstream Ethernet Port Statistics Block ===
        eth_group = QGroupBox("Upstream Ethernet Port Statistics")
        eth_group.setStyleSheet("QGroupBox { font-weight: bold; font-size: 14px; }")
        eth_layout = QVBoxLayout()

        self.eth_stat_output = QTextEdit()
        self.eth_stat_output.setPlaceholderText("Upstream Ethernet Port Traffic Statistics Output...")
        self.eth_stat_output.setReadOnly(True)

        self.eth_refresh_btn = QPushButton("Refresh")
        self.eth_refresh_btn.setFixedSize(100, 25)
        self.eth_refresh_btn.clicked.connect(self.refresh_eth_port_statistics)

        eth_layout.addWidget(self.eth_stat_output)
        eth_layout.addWidget(self.eth_refresh_btn, alignment=Qt.AlignRight)
        eth_group.setLayout(eth_layout)
        main_layout.addWidget(eth_group)

        # === Bottom Button Layout (Back | Save | Next) ===
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

        self.save_button = QPushButton("Save Configs")
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
        self.next_button.clicked.connect(self.go_to_next_page)

        button_layout.addWidget(self.back_button, alignment=Qt.AlignLeft)
        button_layout.addWidget(self.save_button, alignment=Qt.AlignCenter)
        button_layout.addWidget(self.next_button, alignment=Qt.AlignRight)

        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

    def go_to_back(self):
        """Navigate back to ONT Configuration page"""
        self.stack.setCurrentWidget(self.ont_page)

    def refresh_olt_statistics(self):
        """Placeholder: Refresh OLT Port Statistics"""
        data = {
            "ip": self.ont_page.olt_data.get("ip"),
            "pon_port": self.ont_page.olt_data.get("pon_port"),
            "ont_id": self.ont_page.ont_id_input.text().strip(),
        }
        if data:
            send_request("traffic/olt_port_statistics", data, self.olt_stat_output, DebugMode.DEBUG if self.debug_enabled else DebugMode.NO_DEBUG)


    def refresh_eth_port_statistics(self):
        """Placeholder: Refresh Upstream Ethernet Port Statistics"""
        data = {
            "ip": self.ont_page.olt_data.get("ip"),
            "uplink_port": self.ont_page.olt_data.get("upstream_port")
        }
        if data:
            send_request("traffic/eth_port_statistics", data, self.eth_stat_output, DebugMode.DEBUG if self.debug_enabled else DebugMode.NO_DEBUG)

    def save_statistics(self):
        data = {"ip": self.ont_page.olt_data.get("ip")}
        send_request("traffic/save_configurations", data, self.eth_stat_output, DebugMode.NO_DEBUG)

    def go_to_next_page(self):
        """Create Debug Page dynamically with latest Traffic Data"""
        if not hasattr(self, 'debug_page'):
            self.debug_page = DebugModeConfig(self.stack, self)  # Pass reference of traffic page
            self.stack.addWidget(self.debug_page)

        self.stack.setCurrentWidget(self.debug_page)
