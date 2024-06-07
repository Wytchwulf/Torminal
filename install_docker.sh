#!/bin/bash

# Update package information
sudo apt update

# Install necessary packages
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common

# Add Docker's official GPG key
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Add Docker's official repository
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Update package information again with Docker repo included
sudo apt update

# Install Docker
sudo apt install -y docker-ce

# Start and enable Docker service
sudo systemctl start docker
sudo systemctl enable docker

# Add the current user to the Docker group
sudo usermod -aG docker $USER

# Apply the new group membership
newgrp docker

# Print Docker version to verify installation
docker --version

echo "Docker has been installed and started successfully. You have been added to the docker group. Please log out and log back in for the changes to take full effect."
