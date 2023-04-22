import socket
import subprocess

def get_my_ip():
    cmd = ['hostname', '-I']
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    o, e = proc.communicate()
    my_ip = o.decode('ascii')
    return my_ip[:-2]

def set_up_irc():
    host = get_my_ip()
    port = 6667
    clients = 1

    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    print(f"irc listening ({host}, {port})")

    server_socket.listen(clients)
    conn, address = server_socket.accept()
    print("Connection from: " + str(address))

    while True:
        data = conn.recv(1024).decode()
        if not data or data == "exit":
            break
        print("from connected user: " + str(data))

    conn.close()  # close the connection