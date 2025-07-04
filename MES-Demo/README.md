▶️ How to Run This Demo on Laptop
# Run the application with docker-compose
## Install WSL(Windows Subsystem Linux) on your PC(One Time Task)
    [Docker Desktop Installer](https://docs.docker.com/desktop/setup/install/windows-install/)

## Run the docker-compose build up 
```bash
docker-compose up --build
```

# Run the each application independently on Host
## Backend
1. Create virtual environment
```bash
cd backend
python -m venv venv
```

2. Activate virtual environment
```bash
venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Run the FastAPI server
```bash
uvicorn main:app --reload
```

## Test Simulator
1. Create virtual environment
```bash
cd test-simulator
python -m venv venv
```

2. Activate virtual environment
```bash
venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Run the simulator
```bash
python send_test.py
``` 

## Frontend
1. Open dashboard from frontend_static folder
    Open [frontend/index.html](file:///D:/Dixon_Projects/Dixon_R&D_Projects/MyLearning/MES-Demo/frontend/index.html) in browser (no server needed if static)

2. Open dashboard from frontend_streamlit folder
    ```
    mes-demo/
        └── frontend_streamlit/
            ├── dashboard_app.py
            └── requirements.txt
    ```

    ### ✅ How to Run the Streamlit Frontend

    1. Open terminal in `mes-demo/frontend_streamlit`

    2. (Optional) Create a virtual environment:

    ```bash
    python -m venv venv
    venv\Scripts\activate  # On Windows
    ```

    3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

    4. Run the dashboard:

    ```bash
    streamlit run dashboard_app.py
    ```

    5. It opens in browser at:

    ```
    http://localhost:8501
    ```
