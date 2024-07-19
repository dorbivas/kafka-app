#!/bin/bash

# Define the names of the pods to watch, assuming labels are used to filter
PRODUCER_LABEL=app=api-producer
CONSUMER_LABEL=app=kafka-consumer

# Interval in seconds between checks
INTERVAL=5

# Clear the screen initially
clear

# Function to describe pods
describe_pods() {
    echo "Describing pods with label $1"
    POD_NAME=$(kubectl get pod -l $1 --no-headers -o custom-columns=":metadata.name")
    if [[ ! -z "$POD_NAME" ]]; then
        kubectl describe pod $POD_NAME
    else
        echo "No pods found with label $1"
    fi
    echo "-------------------------------------------------------"
}

# Main loop to keep the script running
while true; do
    # Describe the API Producer Pod
    describe_pods $PRODUCER_LABEL

    # Describe the Kafka Consumer Pod
    describe_pods $CONSUMER_LABEL

    # Wait for the specified interval
    sleep $INTERVAL
done

