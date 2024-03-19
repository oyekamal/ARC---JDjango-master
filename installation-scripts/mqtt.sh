#!/bin/bash


# chmod +x install_redis.sh install_mqtt.sh

# Update package lists
sudo apt-get update


# Install MQTT
sudo apt-get install mosquitto mosquitto-clients -y

# Check MQTT service status
if systemctl is-active --quiet mosquitto; then
    echo "MQTT is installed and running."
else
    echo "MQTT is installed but not running."
fi
