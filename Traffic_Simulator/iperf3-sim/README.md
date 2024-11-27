## Iperf3 Simulator

This project simulates traffic using iperf3. Below are the test and code coverage stats:

-   **Tests Status:** [![Tests](https://github.com/prashantpateldixoninfo/MyLearning/actions/workflows/run-tests-iperf3.yml/badge.svg)](https://github.com/prashantpateldixoninfo/MyLearning/actions/workflows/run-tests-iperf3.yml)
-   **Code Coverage:** [![codecov](https://codecov.io/gh/prashantpateldixoninfo/MyLearning/branch/main/graph/badge.svg)](https://codecov.io/gh/prashantpateldixoninfo/MyLearning)

### Prequisites

    python3.10+ &

    Run "python setup_virtual_env_and_libraries.py". It will create virtual environment(venv folder) for python and install all required packages from requirements.txt file.

    Activate the virtual environment by executing ".\venv\Scripts\activate"
    PS C:\Dixon_Project\MyLearning\Traffic_Simulator\iperf3-sim>.\venv\Scripts\activate
    (venv) PS C:\Dixon_Project\MyLearning\Traffic_Simulator\iperf3-sim>

    And Deactivate the virtual environment by executing "deactivate"
    (venv) PS C:\Dixon_Project\MyLearning\Traffic_Simulator\iperf3-sim>deactivate                        PS C:\Dixon_Project\MyLearning\Traffic_Simulator\iperf3-sim>

### Run the dixon_wifi_traffic_automation.py file to collect the traffic losses based on Bitrate, Packet Length and Timing Variation.

    (venv) PS C:\Dixon_Project\MyLearning\Traffic_Simulator\iperf3-sim>python dixon_wifi_traffic_automation.py

### Once log is collected in Logs folder, Run the below command to extract the loss percentage information and generate the graph in excel-sheet

    (venv) PS C:\Dixon_Project\MyLearning\Traffic_Simulator\iperf3-sim>python dixon_log_extracter_graph_generator.py

### Unit Testing, This wiil generate index.html file under htmlcov folder and coverage.xml can be used for CI/CD Automation.

    (venv) PS C:\Dixon_Project\MyLearning\Traffic_Simulator\iperf3-sim>python -m pytest test_setup_venv_and_libraries.py --cov=setup_venv_and_libraries --cov-report=term-missing --cov-report=html --cov-report=xml
