from time import sleep
import psutil
import os
import subprocess
import requests
from requests.auth import HTTPBasicAuth
import json
from flask import Flask, render_template, flash, request
from werkzeug.utils import secure_filename

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
#        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    SECRET_KEY='dev'
    headers = {'Content-type': 'application/json'}
    headers['Authorization'] = 'Bearer ' + SECRET_KEY
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/stats')
    def stats():
        used = 0
        avail = 0
        sp1 = psutil.net_io_counters().bytes_recv
        sleep(1)
        sp2 = psutil.net_io_counters().bytes_recv
        speed = (sp2 - sp1) / (1024.0)
        disk = psutil.disk_usage('/').free / 1024.0
        return str(speed) + ' ' + str(disk)
    
    @app.route('/upload', methods=['GET', 'POST'])
    def upload_file():
        if request.method == 'POST':
            f = request.files['the_file']
            f.save( secure_filename(f.filename))
        return 'Successfully Upload. Go back and refresh to check left free space.'
    return app

