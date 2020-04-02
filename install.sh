apt update
apt upgrade
apt install git -y
apt install python -y 
apt install python3-pip -y

git clone https://github.com/albert752/RespiratorControlSystem.git
cd RespiratorControlSystem/WebServer

pip3 install flask
pip3  install pydub
apt install rpi.gpio

apt install apache2 -y
apt-get install libapache2-mod-wsgi python-dev -y
a2enmod wsgi
