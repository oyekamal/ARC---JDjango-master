#!/bin/bash

# Function to start a service
start_service() {
    local service_name=$1
    echo "Starting ${service_name}..."
    sudo systemctl start "${service_name}.service"
}

# Start Redis
start_service redis

# Start MQTT
start_service mosquitto
