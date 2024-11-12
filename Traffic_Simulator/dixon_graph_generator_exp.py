import xlwings as xw
import os


# Function to create a blank Excel file and save it in the background
def create_blank_excel(file_path):
    app = xw.App(visible=False)
    try:
        workbook = app.books.add()
        workbook.save(file_path)
        workbook.close()
    finally:
        app.quit()


# Function to populate the Excel file with flexible data inputs from a dictionary
def populate_data(file_path, data_dict):
    app = xw.App(visible=False)
    try:
        workbook = app.books.open(file_path)
        sheet = workbook.sheets[data_dict["sheet_num"]]
        sheet.name = data_dict["sheet_name"]

        # Insert headers and data based on dictionary keys
        headers = [
            data_dict["x_axis"],
            data_dict["first_header"],
            data_dict["sec_header"],
        ]
        data = [
            data_dict["x_axis_value"],
            data_dict["first_header_value"],
            data_dict["sec_header_value"],
        ]

        for col, (header, values) in enumerate(zip(headers, data), start=1):
            header_cell = sheet.range((1, col))
            data_range = sheet.range((2, col), (len(values) + 1, col))

            # Write header and data
            header_cell.value = header
            data_range.value = [[v] for v in values]

            # Format header: blue color text on white background, bold
            header_cell.api.Font.Color = 0xFF0000  # Blue text
            header_cell.api.Font.Bold = True

        # Apply grid lines around the entire data range
        data_range = sheet.range(
            (1, 1), (len(data_dict["x_axis_value"]) + 1, len(headers))
        )
        data_range.api.Borders.LineStyle = 1

        # Auto-fit columns
        sheet.autofit()

        # Save and close the workbook
        workbook.save()
        workbook.close()
    finally:
        app.quit()


# Function to add a chart to the Excel file and display it to the user
def add_chart(file_path, sheet_num, chart_title):
    app = xw.App(visible=False)
    try:
        workbook = app.books.open(file_path)
        sheet = workbook.sheets[sheet_num]  # Assuming we work with the first sheet

        # Add a 2-D Line Chart (Lines with Markers) for the data
        chart = sheet.charts.add()
        chart.chart_type = "line_markers"
        chart.set_source_data(sheet.range("B1:C11"))
        chart.name = chart_title
        chart.api[1].HasTitle = True
        chart.api[1].ChartTitle.Text = chart_title
        chart.api[1].ApplyLayout(2)

        # Set x-axis to use manual labels from column A
        chart.api[1].Axes(1).CategoryNames = sheet.range("A2:A11").value

        # Position chart from E2 to L11
        chart.top = sheet.range("E2").top
        chart.left = sheet.range("E2").left
        chart.width = sheet.range("E2:L2").width
        chart.height = sheet.range("E2:E11").height

        # Save and close the workbook
        workbook.save()
        workbook.close()
    finally:
        app.quit()


def display_chart(file_path):
    app = xw.App(visible=True)
    workbook = app.books.open(file_path)
    sheet = workbook.sheets[0]  # Assuming we work with the first sheet


if __name__ == "__main__":
    # Define file path and data dictionary
    file_path = os.path.join(os.getcwd(), "line_chart_example_final.xlsx")
    data_dict = {
        "sheet_num": 0,  # First sheet in the workbook
        "sheet_name": "Bitrate",
        "x_axis": "Bitrate",
        "first_header": "Zyxel-2.4_Bitrate",
        "sec_header": "DXB-2.4_Bitrate",
        "x_axis_value": [50, 80, 120, 200, 300, 400, 500, 700, 800, 1000],
        "first_header_value": [0, 6.5, 23, 22, 29, 53, 40, 57, 43, 45],
        "sec_header_value": [0, 5.4, 13, 32, 39, 42, 42, 51, 48, 51],
    }
    chart_title = "Bitrate Comparison"

    # Execute each function sequentially
    create_blank_excel(file_path)
    populate_data(file_path, data_dict)
    add_chart(file_path, 0, chart_title)
    display_chart(file_path)
