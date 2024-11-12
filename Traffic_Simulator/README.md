## Prequisites

    python3.10+
    pip install colorama
    pip install pathlib
    pip install pyfiglet
    pip install xlwings

## Run the dixon_wifi_traffic_automation.py file to collect the traffic losses based on Bitrate, Packet Length and Timing Variation.

    python dixon_wifi_traffic_automation.py

## Once log is collected in Logs folder, Run the below command to extract the loss percentage information and generate the graph in excel-sheet

    python dixon_log_extracter_graph_generator.py
