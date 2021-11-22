from app import app
from flask import request

def get_vars(command):
    ip=request.form['ipprefix']
    cmd=request.form['command']
    
    if cmd==0:
        command="show ip bgp "+ip
        
    return command