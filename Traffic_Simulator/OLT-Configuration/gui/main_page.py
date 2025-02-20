from olt_page import OLTConfiguration
from ont_page import ONTConfiguration
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
        self.page1 = OLTConfiguration(self.stack)
        self.page2 = ONTConfiguration(self.stack)

        self.stack.addWidget(self.page1)
        self.stack.addWidget(self.page2)

        layout = QVBoxLayout()
        layout.addWidget(self.stack)
        self.setLayout(layout)
