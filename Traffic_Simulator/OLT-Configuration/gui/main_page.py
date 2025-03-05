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
        self.olt_page = OLTConfiguration(self.stack)
        self.ont_page = ONTConfiguration(self.stack, self.olt_page)

        self.stack.addWidget(self.olt_page)
        self.stack.addWidget(self.ont_page)

        layout = QVBoxLayout()
        layout.addWidget(self.stack)
        self.setLayout(layout)
