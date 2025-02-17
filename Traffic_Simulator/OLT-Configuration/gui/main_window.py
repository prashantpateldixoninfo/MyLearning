from qtpy.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QTextEdit,
    QMessageBox,
)
import requests
from shared.config import BACKEND_URL
from qtpy.QtCore import Qt


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Create input and output text areas
        self.input_text = QTextEdit(self)
        self.input_text.setFixedSize(100, 25)
        self.input_text.setStyleSheet(
            """
            background-color: #e6f3ff;
            border: 2px solid #1e90ff;
        """
        )
        self.input_text.setPlaceholderText("Serial-Number")
        self.input_text.textChanged.connect(
            self.update_button_style
        )  # Enable hover effect dynamically

        self.output_text = QTextEdit(self)
        self.output_text.setFixedSize(200, 25)
        self.output_text.setStyleSheet(
            """
            background-color: #ffffe0;
            border: 2px solid #1e90ff;
        """
        )
        self.output_text.setReadOnly(True)
        self.output_text.setPlaceholderText("Processing...")

        # Submit button
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

        self.submit_button.setStyleSheet(self.default_button_style)  # Set initial style
        self.submit_button.clicked.connect(self.send_data)
        self.submit_button.clicked.connect(self.fetch_data)

        # Layouts
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.input_text)
        h_layout.addWidget(self.output_text)

        v_layout = QVBoxLayout()
        v_layout.addLayout(h_layout)
        v_layout.addWidget(self.submit_button, alignment=Qt.AlignCenter)

        self.setLayout(v_layout)

        # Window settings
        self.setWindowTitle("Huawei OLT Configuration")
        self.resize(500, 300)

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
                self.output_text.setPlainText(data)
                self.output_text.setStyleSheet(
                    """
                    background-color: #4CAF50;
                    border: 2px solid #1e90ff;
                """
                )
            else:
                QMessageBox.critical(self, "Error", "No data available on backend.")
                self.output_text.setPlainText("No data available on backend.")
                self.output_text.setStyleSheet(
                    """
                    background-color: #FF7F7F;
                    border: 2px solid #1e90ff;
                """
                )
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")
            self.output_text.setPlainText(f"An error occurred: {e}")
            self.output_text.setStyleSheet(
                """
                background-color: #FF0000;
                border: 2px solid #1e90ff;
            """
            )


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
