"""
Script used for jenkins pipeline for clean up the environment at the end of pipeline
Stops rest_api and web_api servers
"""
import requests

try:
    requests.get('http://127.0.0.1:5000/stop_server')
except:
    print("rest_api server is not responding...")

try:
    requests.get('http://127.0.0.1:5001/stop_server')
except:
    print("web_api server is not responding...")
