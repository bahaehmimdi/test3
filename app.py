from flask import Flask
import pandas as pd
import requests
import wget
import os
import subprocess 

app = Flask(__name__)
os.chdir("static")
@app.route('/')
def hello_world():
    return "hello in bahae api"
def get_html_text(url):
    prefixes = ['http://', 'https://', 'http://www.', 'https://www.']
    
    for prefix in prefixes:
        try:
            response = requests.get(prefix + url)
            if response.status_code == 200:
                return response.text
        except requests.RequestException as e:
            print(f"Error occurred while trying {prefix + url}: {e}")
    
    return "nothing worked"

@app.route('/task/<string:name>')
def task(name):
 return get_html_text(name)
