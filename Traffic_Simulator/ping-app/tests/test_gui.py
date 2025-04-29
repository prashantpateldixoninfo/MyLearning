import pytest
from gui.ping_gui import PingApp
from PyQt5.QtWidgets import QApplication

@pytest.fixture
def app_instance(qtbot):
    test_app = PingApp()
    qtbot.addWidget(test_app)
    return test_app

def test_gui_input_box(app_instance, qtbot):
    app_instance.input_box.setText("8.8.8.8")
    assert app_instance.input_box.text() == "8.8.8.8"

def test_gui_buttons_exist(app_instance):
    assert app_instance.ping_button is not None
    assert app_instance.save_button is not None
