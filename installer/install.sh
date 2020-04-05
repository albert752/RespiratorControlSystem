#!/bin/bash

# Update on the system
echo "****** PERFORMING SYSTEM UPGRADE STEP 1/7 ******"
apt update
apt upgrade

echo "****** INSTALLING COMPONENTS STEP 2/7 ******"
# Install the required components
apt install git -y
apt install python -y 
apt install python3-pip -y
apt install python3-venv -y
apt install apache2 -y
apt install libapache2-mod-wsgi-py3 python-dev python3-dev -y
a2enmod wsgi
apt install rpi.gpio -y

echo "****** CLONING REPO STEP 3/7 ******"
# Clone the repository
git clone https://github.com/albert752/RespiratorControlSystem.git

echo "****** COPY OF THE FILES STEP 4/7 ******"
# Copy the WebServer files to the correct location
cp -r RespiratorControlSystem/WebServer /var/www
python3 -m venv /var/www/WebServer/venv
cp configs/activate_this.py /var/www/WebServer/venv/bin 
sudo chown -R pi:pi /var/www/WebServer/venv

echo "****** INSTALLING FLASK STEP 5/7 ******"
# Activate the virtual enviroment and install flask
. /var/www/WebServer/venv/bin/activate
pip install flask
deactivate

echo "****** APACHE2 CONFIGURATION STEP 6/7 ******"
# Copy the apache2 configuration
cp configs/webserver.conf /etc/apache2/sites-available
a2ensite webserver
a2dissite 000-default.conf 

echo "****** START SERVICE STEP 7/7 ******"
# Restart apache2
service apache2 stop
sleep(1)
service apache2 start



