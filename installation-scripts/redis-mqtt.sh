#!/bin/bash


# chmod +x install_redis.sh install_mqtt.sh

# Update package lists
sudo apt-get update

# Install Redis
sudo apt-get install redis-server -y

# Enable systemd supervision for Redis
sudo sed -i 's/^supervised .*/supervised systemd/' /etc/redis/redis.conf

# Restart Redis service
sudo systemctl restart redis.service

# Test Redis connection
if redis-cli ping | grep -q 'PONG'; then
    echo "Redis is installed and running."
else
    echo "Failed to connect to Redis."
fi

# Install MQTT
sudo apt-get install mosquitto mosquitto-clients -y

# Check MQTT service status
if systemctl is-active --quiet mosquitto; then
    echo "MQTT is installed and running."
else
    echo "MQTT is installed but not running."
fi
