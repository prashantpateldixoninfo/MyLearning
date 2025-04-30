#!/bin/bash

set -e
cd "$(dirname "$0")"

CONTAINER_NAME="ping-app-mongo"

echo "Stopping MongoDB container: $CONTAINER_NAME ..."
docker stop "$CONTAINER_NAME" || echo "No running container to stop."

echo "Removing MongoDB container: $CONTAINER_NAME ..."
docker rm "$CONTAINER_NAME" || echo "No container to remove."

echo "Cleanup complete!"
