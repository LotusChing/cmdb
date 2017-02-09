import os
import sys
from flask import Flask
from flask_cors import CORS, cross_origin
sys.path.append(os.getcwd())
application = Flask(__name__, static_url_path='/static')
CORS(application)
from cmdb import route
