import pytest
from unittest.mock import patch, MagicMock
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
    assert app_instance.history_button is not None

def test_ping_host_valid_input(app_instance, qtbot):
    app_instance.input_box.setText("8.8.8.8")

    mock_response = MagicMock()
    mock_response.json.return_value = {"output": "Reply from 8.8.8.8"}

    with patch("gui.ping_gui.requests.post", return_value=mock_response) as mock_post:
        app_instance.ping_host()
        assert app_instance.output_box.toPlainText() == "Reply from 8.8.8.8"
        mock_post.assert_called_once_with("http://localhost:5000/ping", json={"host": "8.8.8.8"})

def test_ping_host_empty_input(app_instance):
    app_instance.input_box.setText("")
    app_instance.ping_host()
    assert app_instance.output_box.toPlainText() == "Please enter a host."

def test_get_history(app_instance):
    app_instance.input_box.setText("8.8.8.8")

    mock_response = MagicMock()
    mock_response.json.return_value = [
        {"host": "8.8.8.8", "output": "Reply 1"},
        {"host": "8.8.8.8", "output": "Reply 2"}
    ]

    with patch("gui.ping_gui.requests.post", return_value=mock_response) as mock_post:
        app_instance.get_history()
        output = app_instance.output_box.toPlainText()
        assert "Reply 1" in output and "Reply 2" in output
        mock_post.assert_called_once_with("http://localhost:5000/history", json={"host": "8.8.8.8"})

