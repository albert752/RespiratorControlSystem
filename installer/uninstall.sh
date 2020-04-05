rm -r /var/www/WebServer

a2dissite webserver.conf
rm /etc/apache2/sites-available/webserver.conf

service apache2 restart
