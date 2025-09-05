FROM python:3.10-slim

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# Wait for backend to be up, then run the script
CMD ["sh", "-c", "sleep 5 && python send_test.py"]
