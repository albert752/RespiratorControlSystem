#!/bin/bash

# Update on the system
echo "****** PERFORMING SYSTEM UPGRADE STEP 1/7 ******"
sudo apt update -y
sudo apt upgrade -y

echo "****** INSTALLING COMPONENTS STEP 2/7 ******"
# Install the required components
sudo apt install git -y
sudo apt install python -y 
sudo apt install python3-pip -y
sudo apt install apache2 -y
sudo apt install libapache2-mod-wsgi-py3 python-dev python3-dev -y
sudo a2enmod wsgi
sudo apt install rpi.gpio -y

echo "****** CLONING REPO STEP 3/7 ******"
# Clone the repository
git clone https://github.com/albert752/RespiratorControlSystem.git

echo "****** COPY OF THE FILES STEP 4/7 ******"
# Copy the WebServer files to the correct location
sudo cp -r RespiratorControlSystem/WebServer /var/www

echo "****** INSTALLING FLASK STEP 5/7 ******"
# Install flask
pip3 install flask
pip3 install rpi.gpio

echo "****** APACHE2 CONFIGURATION STEP 6/7 ******"
# Copy the apache2 configuration
sudo cp configs/webserver.conf /etc/apache2/sites-available
sudo a2ensite webserver
sudo a2dissite 000-default.conf 

echo "****** START SERVICE STEP 7/7 ******"
# Restart apache2
sudo service apache2 stop
sleep 1
sudo service apache2 start



