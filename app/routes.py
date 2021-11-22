from app import app
from flask import request, Response, render_template, redirect, url_for, flash, session
import urllib.request
import json
import paramiko
import iptools



@app.route('/')
@app.route('/index', methods=['GET'])
def index():
    external_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')
    title = 'Looking-Glass'
    return render_template('index.html', title = 'Home', ip=external_ip)

@app.route('/lg', methods=['POST'])


    
def ip():
    ip=request.form['ipprefix']
    cmd=request.form['command']
    router_ip = "112.140.164.1"
    source_ip = "112.140.167.69"
    router_username = "rifza"
    router_password = "4AJk1nfo-LK"
    port = "9122"
    title = 'Result | Looking-Glass'
    

    
    if cmd == "bgp":
        command = "sh ip bgp "+ip
    elif cmd == "ping" :
        command = "ping "+ip+" source 112.140.167.69"
    elif cmd == "traceroute":
        command = "traceroute "+ip+" source 112.140.167.69"
        
    ssh = paramiko.SSHClient()

    # Load SSH host keys.
    ssh.load_system_host_keys()
    # Add SSH host key automatically if needed.
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # Connect to router using username/password authentication.
    ssh.connect(router_ip, port=port, username=router_username, password=router_password,look_for_keys=False )

    validate_ip = iptools.ipv4.validate_ip(ip)
    if validate_ip is True and cmd in ['bgp', 'ping', 'traceroute']:
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command)        
    else :
        flash('Input Data Invalid','error')
        return redirect(url_for('index'))
    # Run command.

    output = ssh_stdout.readlines()
    line = ''.join(output)
    # Close connection.
    ssh.close()
    
    return render_template('result.html', line=line, title=title)
    # return command