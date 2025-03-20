from olt_page import OLTConfiguration
from ont_page import ONTConfiguration
from qtpy.QtWidgets import QWidget, QVBoxLayout, QStackedWidget
from PyQt5.QtGui import QIcon
import os

class MainPage(QWidget):
    """Main Window with Stacked Pages"""

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Huawei OLT Configuration")
        img_path = os.path.join(os.getcwd(), "dixon_img.png")
        img_path = os.path.normpath(img_path)  
        self.setWindowIcon(QIcon(img_path))
        self.resize(500, 300)

        self.stack = QStackedWidget()
        self.olt_page = OLTConfiguration(self.stack)  # Initialize OLT Page

        # Create ONT Page once but don't add to stack initially
        self.ont_page = None 

        self.stack.addWidget(self.olt_page)  # Only add OLT Page initially

        layout = QVBoxLayout()
        layout.addWidget(self.stack)
        self.setLayout(layout)

        # Connect "Next" button to dynamically load ONT Page
        self.olt_page.next_button.clicked.connect(self.load_ont_page)

    def load_ont_page(self):
        """Create ONT Page dynamically with latest OLT data"""
        olt_data = self.olt_page.get_olt_data()  # Fetch fresh OLT data

        if self.ont_page is None:
            self.ont_page = ONTConfiguration(self.stack, olt_data)  # Pass updated data
            self.stack.addWidget(self.ont_page)  # Add ONT Page to stack
        else:
            # Update ONT page inputs with new OLT data (keep existing output data)
            self.ont_page.update_olt_data(olt_data)
        
        self.stack.setCurrentWidget(self.ont_page)  # Switch to ONT Page
