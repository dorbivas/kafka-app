#!/bin/bash

# Configuration
APP_NAME=$1
DOCKER_USERNAME=$2  # Replace with your Docker Hub username
IMAGE_NAME="$DOCKER_USERNAME/$APP_NAME"
TAG="latest"

# Check if the app name was provided
if [[ -z "$APP_NAME" ]]; then
  echo "Usage: ./deploy.sh <app-name> <docker-username>"
  exit 1
fi

# Step 1: Stop and remove any running containers using this image
echo "Stopping running containers..."
docker ps -a | grep $IMAGE_NAME | awk '{print $1}' | xargs -r docker stop
docker ps -a | grep $IMAGE_NAME | awk '{print $1}' | xargs -r docker rm

# Step 2: Remove the existing image
echo "Removing existing image..."
docker rmi -f $IMAGE_NAME:$TAG

# Step 3: Build the new image
echo "Building new image..."
docker build -t $IMAGE_NAME:$TAG .

# Step 4: Push the new image to Docker Hub
echo "Pushing image to Docker Hub..."
docker push $IMAGE_NAME:$TAG

echo "Deployment complete!"
