from qtpy.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QTextEdit,
    QMessageBox,
)
import requests
from qtpy.QtCore import Qt
from shared.config import BACKEND_URL


class SecondPage(QWidget):
    """Second Page with Huawei OLT Configuration"""

    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        self.init_ui()

    def init_ui(self):
        self.input_text = QTextEdit(self)
        self.input_text.setFixedSize(100, 25)
        self.input_text.setStyleSheet(
            "background-color: #e6f3ff; border: 2px solid #1e90ff;"
        )
        self.input_text.setPlaceholderText("Enter Serial Number")
        self.input_text.textChanged.connect(self.update_button_style)

        self.output_text = QTextEdit(self)
        self.output_text.setFixedSize(200, 25)
        self.output_text.setStyleSheet(
            "background-color: #ffffe0; border: 2px solid #1e90ff;"
        )
        self.output_text.setReadOnly(True)
        self.output_text.setPlaceholderText("Result...")

        self.submit_button = QPushButton("Submit")
        self.submit_button.setFixedSize(100, 30)
        self.default_button_style = """
            QPushButton {
                background-color: #A5D6A7;
                border: 1px solid #1e90ff;
                border-radius: 5px;
                color: white;
                font-weight: bold;
                padding: 5px;
            }
        """
        self.hover_enabled_style = (
            self.default_button_style
            + """
            QPushButton:hover {
                background-color: #45a049;
            }
        """
        )

        self.submit_button.setStyleSheet(self.default_button_style)
        self.submit_button.clicked.connect(self.send_data)
        self.submit_button.clicked.connect(self.fetch_data)

        back_button = QPushButton("Back")
        back_button.setFixedSize(100, 30)
        back_button.setStyleSheet(
            """
            QPushButton {
                background-color: #FFA07A;
                border: 2px solid #1e90ff;
                border-radius: 5px;
                color: white;
                font-weight: bold;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #FF6347;
            }
        """
        )
        back_button.clicked.connect(self.go_back)

        # Layouts
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.input_text)
        h_layout.addWidget(self.output_text)

        v_layout = QVBoxLayout()
        v_layout.addLayout(h_layout)
        v_layout.addWidget(self.submit_button, alignment=Qt.AlignCenter)
        v_layout.addWidget(back_button, alignment=Qt.AlignCenter)

        self.setLayout(v_layout)

    def update_button_style(self):
        """Enable hover effect only when input field is not empty."""
        if self.input_text.toPlainText().strip():
            self.submit_button.setStyleSheet(self.hover_enabled_style)
        else:
            self.submit_button.setStyleSheet(self.default_button_style)

    def send_data(self):
        user_input = self.input_text.toPlainText().strip()
        if not user_input:
            QMessageBox.critical(self, "Error", "Input cannot be empty!")
            return

        try:
            response = requests.post(
                f"{BACKEND_URL}/submit", json={"input": user_input}
            )
            if response.status_code == 200:
                QMessageBox.information(
                    self, "Success", f"Data sent successfully!\n{response.json()}"
                )
            else:
                QMessageBox.critical(
                    self, "Error", f"Failed to send data: {response.status_code}"
                )
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")

    def fetch_data(self):
        try:
            response = requests.get(f"{BACKEND_URL}/get_data")
            if response.status_code == 200:
                data = response.json().get("data", "No data found")
                self.output_text.setPlainText(f"Passed: {data}")
                self.output_text.setStyleSheet(
                    "background-color: #4CAF50; border: 2px solid #1e90ff;"
                )
            else:
                QMessageBox.critical(
                    self, "Error", "Failed: Your Data is not processed"
                )
                self.output_text.setPlainText("Failed: Your Data is not processed")
                self.output_text.setStyleSheet(
                    "background-color: #FF7F7F; border: 2px solid #1e90ff;"
                )
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")
            self.output_text.setPlainText(f"An error occurred: {e}")
            self.output_text.setStyleSheet(
                "background-color: #FF0000; border: 2px solid #1e90ff;"
            )

    def go_back(self):
        """Go back to First Page"""
        self.stack.setCurrentIndex(0)
