from qtpy.QtWidgets import QApplication
from main_page import MainPage

if __name__ == "__main__":
    app = QApplication([])
    window = MainPage()
    window.show()
    app.exec_()
