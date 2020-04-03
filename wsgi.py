#!/usr/bin/python3
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/RespiratorControlSystem/WebServer")
sys.path.append("/var/www/RespiratorControlSystem/WebServer/utils")
from WebServer import app as application
application.secret_key = "test"
