from qtpy.QtWidgets import QApplication
from gui.main_page import MainPage  # Use absolute import

if __name__ == "__main__":
    app = QApplication([])
    window = MainPage()
    window.show()
    app.exec_()
