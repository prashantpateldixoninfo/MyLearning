from gui.first_page import FirstPage
from gui.second_page import SecondPage
from qtpy.QtWidgets import QWidget, QVBoxLayout, QStackedWidget


class MainPage(QWidget):
    """Main Window with Stacked Pages"""

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Huawei OLT Configuration")
        self.resize(500, 300)

        self.stack = QStackedWidget()
        self.page1 = FirstPage(self.stack)
        self.page2 = SecondPage(self.stack)

        self.stack.addWidget(self.page1)
        self.stack.addWidget(self.page2)

        layout = QVBoxLayout()
        layout.addWidget(self.stack)
        self.setLayout(layout)
