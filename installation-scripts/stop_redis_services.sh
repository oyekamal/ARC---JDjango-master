#!/bin/bash

# Function to stop a service
stop_service() {
    local service_name=$1
    echo "Stopping ${service_name}..."
    sudo systemctl stop "${service_name}.service"
}

# Stop Redis
stop_service redis

# Stop MQTT
# stop_service mosquitto
