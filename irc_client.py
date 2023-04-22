import socket

def irc_client_program():
    # server info
    host = input("Type the ip of the bot you want to connect to: ")
    port = 6667

    # connect to server
    client_socket = socket.socket()
    client_socket.connect((host, port))
    
    message = input("msg to send to bot -> ") 
    while message.lower().strip() != 'exit':
        client_socket.send(message.encode())
        # data = client_socket.recv(1024).decode()

        # print('Received from server: ' + data)

        message = input("msg to send to bot -> ")

    client_socket.close()


if __name__ == '__main__':
    irc_client_program()