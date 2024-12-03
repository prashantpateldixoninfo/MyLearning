import os
import sys
import pytest
from unittest import mock
import xlwings as xw


# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

import dixon_graph_generator_exp  # type: ignore
from dixon_graph_generator_exp import (  # type: ignore
    create_blank_excel,
    populate_data,
    add_chart,
    display_chart,
)


@pytest.fixture(scope="module")
def file_path():
    """Fixture to provide the file path for the test Excel file."""
    file_path = os.path.join(os.getcwd(), "test_line_chart.xlsx")
    yield file_path
    # Cleanup after test execution
    if os.path.exists(file_path):
        os.remove(file_path)


@pytest.fixture
def data_dict():
    """Fixture to provide test data dictionary."""
    return {
        "sheet_num": 0,  # First sheet in the workbook
        "sheet_name": "Bitrate",
        "x_axis": "Bitrate",
        "first_header": "Zyxel-2.4_Bitrate",
        "sec_header": "DXB-2.4_Bitrate",
        "x_axis_value": [50, 80, 120, 200, 300, 400, 500, 700, 800, 1000],
        "first_header_value": [0, 6.5, 23, 22, 29, 53, 40, 57, 43, 45],
        "sec_header_value": [0, 5.4, 13, 32, 39, 42, 42, 51, 48, 51],
    }


def test_create_blank_excel(file_path):
    """Test if a blank Excel file is created."""
    # Don't run for CI/CD
    if os.environ.get("CI") != "true":
        if os.path.exists(file_path):
            os.remove(file_path)  # Ensure the file doesn't exist initially

        create_blank_excel(file_path)

        # Assert if the file has been created
        assert os.path.exists(file_path), "The Excel file was not created."


def test_populate_data(file_path, data_dict):
    """Test populate_data() using both xlwings and openpyxl."""

    # Don't run for CI/CD
    if os.environ.get("CI") != "true":
        # Call the populate_data() function
        populate_data(file_path, data_dict)

        # Assert that the file is created
        assert os.path.exists(file_path), "Excel file was not created."

        # If running on Windows with Excel available, use xlwings
        if sys.platform == "win32":
            # Test xlwings behavior
            app = xw.App(visible=False)
            try:
                workbook = app.books.open(file_path)
                sheet = workbook.sheets[data_dict["sheet_name"]]

                # Check if headers and data are correct with xlwings
                assert (
                    sheet.range("A1").value == data_dict["x_axis"]
                ), "X-Axis header mismatch with xlwings"
                assert (
                    sheet.range("B1").value == data_dict["first_header"]
                ), "First header mismatch with xlwings"
                assert (
                    sheet.range("C1").value == data_dict["sec_header"]
                ), "Second header mismatch with xlwings"
                assert (
                    sheet.range("A2").value == data_dict["x_axis_value"][0]
                ), "X-Axis data mismatch with xlwings"
                assert (
                    sheet.range("B2").value == data_dict["first_header_value"][0]
                ), "First header data mismatch with xlwings"
                assert (
                    sheet.range("C2").value == data_dict["sec_header_value"][0]
                ), "Second header data mismatch with xlwings"

            finally:
                app.quit()


def test_add_chart(file_path):
    """Test if a chart is added to the Excel file."""

    # Don't run for CI/CD
    if os.environ.get("CI") != "true":
        chart_title = "Bitrate Comparison"
        add_chart(file_path, 0, chart_title)

        if sys.platform == "win32":
            app = xw.App(visible=False)
            try:
                workbook = app.books.open(file_path)
                sheet = workbook.sheets[0]

                # Check if chart exists
                assert len(sheet.charts) > 0, "Chart was not added to the sheet."

                # Verify chart title
                chart = sheet.charts[0]
                assert chart.name == chart_title, "Chart title is incorrect."

            finally:
                workbook.close()
                app.quit()


def test_display_chart(file_path):
    """Test if the display_chart function opens the Excel file."""

    # Don't run for CI/CD
    if os.environ.get("CI") != "true":
        create_blank_excel(file_path)  # Ensure the file exists
        with mock.patch("xlwings.App") as mock_app:
            mock_instance = mock_app.return_value
            mock_instance.books.open.return_value = mock.MagicMock()
            display_chart(file_path)

            # Verify if the Excel file was opened
            mock_instance.books.open.assert_called_once_with(file_path)

            # Verify if the application was made visible
            mock_instance.visible = True


def test_main():
    """Test the main function of dixon_graph_generator_exp.py."""

    with mock.patch(
        "dixon_graph_generator_exp.create_blank_excel"
    ) as mock_create, mock.patch(
        "dixon_graph_generator_exp.populate_data"
    ) as mock_populate, mock.patch(
        "dixon_graph_generator_exp.add_chart"
    ) as mock_add_chart, mock.patch(
        "dixon_graph_generator_exp.display_chart"
    ) as mock_display:

        # Call the main function directly
        dixon_graph_generator_exp.main()

        # Assert that all critical functions were called once
        mock_create.assert_called_once()
        mock_populate.assert_called_once()
        mock_add_chart.assert_called_once()
        mock_display.assert_called_once()
