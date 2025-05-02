import os
import pytest
from gui.ping_gui import PingApp
from PyQt5.QtWidgets import QApplication

# Detect CI environment
is_ci = os.getenv('CI', 'false').lower() == 'true'

@pytest.mark.skipif(is_ci, reason="Skipping GUI tests in CI environment")
@pytest.fixture
def app_instance(qtbot):
    test_app = PingApp()
    qtbot.addWidget(test_app)
    return test_app

@pytest.mark.skipif(is_ci, reason="Skipping GUI tests in CI environment")
def test_gui_input_box(app_instance, qtbot):
    app_instance.input_box.setText("8.8.8.8")
    assert app_instance.input_box.text() == "8.8.8.8"

@pytest.mark.skipif(is_ci, reason="Skipping GUI tests in CI environment")
def test_gui_buttons_exist(app_instance):
    assert app_instance.ping_button is not None
    assert app_instance.history_button is not None
