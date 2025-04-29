import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QLineEdit, QLabel

API_BASE = "http://localhost:5000"

class PingApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ping GUI")

        self.layout = QVBoxLayout()
        self.input_box = QLineEdit()
        self.output_box = QTextEdit()
        self.output_box.setReadOnly(True)

        self.layout.addWidget(QLabel("Enter host/IP:"))
        self.layout.addWidget(self.input_box)

        self.ping_button = QPushButton("Ping")
        self.save_button = QPushButton("Fetch History")

        self.layout.addWidget(self.ping_button)
        self.layout.addWidget(self.save_button)
        self.layout.addWidget(self.output_box)

        self.setLayout(self.layout)

        self.ping_button.clicked.connect(self.ping_host)
        self.save_button.clicked.connect(self.get_history)

    def ping_host(self):
        host = self.input_box.text().strip()
        if not host:
            self.output_box.setText("Please enter a host.")
            return
        res = requests.post(f"{API_BASE}/ping", json={"host": host})
        self.output_box.setText(res.json()["output"])

    def get_history(self):
        res = requests.get(f"{API_BASE}/history")
        history = res.json()
        out = "\n---\n".join(f"{h['host']}:\n{h['output']}" for h in history)
        self.output_box.setText(out or "No history available.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PingApp()
    window.show()
    sys.exit(app.exec_())
