#!/usr/bin/env bash

echo "Check if user exists"
if grep -Fxq "matilda" /etc/sudoers
then
    echo "Matilda User already exists. Skipping..."
else
    echo "Creating user..."
    sudo useradd -r matilda -s /bin/bash
    sudo usermod -aG sudo matilda
    sudo sed -i '/#includedir/i matilda ALL=(ALL) NOPASSWD: ALL' /etc/sudoers
    echo "Matilda User created successfully"
fi

echo "Setting up matilda directory structure"
sudo mkdir -p /opt/matilda
sudo cp -R /tmp/matilda* /opt/matilda/
sudo mkdir -p /var/log/matilda

echo "Changing permissions"
sudo chown -R matilda:matilda /opt/matilda
sudo chown -R matilda:matilda /var/log/matilda

echo "Installing dependencies"
platform=`awk -F= '/^NAME/{print $2}' /etc/os-release`
if [[ $platform = *"Ubuntu"* ]]; then
  sudo apt-get update
  sudo apt-get install python-pip python-dev build-essential -y
  sudo apt-get install libmysqlclient-dev uwsgi -y
else
  sudo yum update
  sudo yum install python python-pip python-setuptools -y
  sudo yum install libmysqlclient-dev uwsgi -y
fi

SLUGIFY_USES_TEXT_UNIDECODE=yes pip install apache-airflow
sudo pip install -r /opt/matilda/matilda-release/requirements.txt

echo "Setting up Matilda plugin API service"
sudo cp /opt/matilda/matilda-release/etc/matilda-release-api.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable matilda-release-api
sudo systemctl start matilda-release-api
echo "Setup Complete"

