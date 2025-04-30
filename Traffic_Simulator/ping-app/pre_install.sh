#!/bin/bash

set -e
cd "$(dirname "$0")"

CONTAINER_NAME="ping-app-mongo"

echo "Creating virtual environment (if not exists)..."
python3 -m venv venv

echo "Activating virtual environment..."
source venv/bin/activate

echo "Upgrading pip..."
pip install --upgrade pip

echo "Installing backend dependencies..."
pip install -r backend/requirements.txt

echo "Installing GUI dependencies..."
pip install -r gui/requirements.txt

echo "Installing test dependencies..."
pip install pytest pytest-qt

echo "Setting default Mongo URI..."
export MONGO_URI="mongodb://localhost:27017"

echo "Stopping any running MongoDB container..."
docker stop "$CONTAINER_NAME" || echo "No running container to stop."

echo "Removing existing MongoDB container..."
docker rm "$CONTAINER_NAME" || echo "No container to remove."

echo "Starting MongoDB container with fixed name: $CONTAINER_NAME ..."
docker run -d --name "$CONTAINER_NAME" -p 27017:27017 mongo

echo "Checking running containers..."
docker ps

echo "Pre-installation complete!"
