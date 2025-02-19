from qtpy.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from qtpy.QtCore import Qt


class FirstPage(QWidget):
    """First Page with Next Button to Navigate to the Second Page"""

    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        label = QLabel("Welcome to Page 1")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        next_button = QPushButton("Next")
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
        layout.addWidget(next_button, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def go_to_next(self):
        """Switch to Second Page"""
        self.stack.setCurrentIndex(1)
