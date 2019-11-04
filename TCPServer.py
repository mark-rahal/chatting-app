import json
from socket import *
from threading import Thread

users = {}
numUsers = 0


def handleConnection(socket):
    global numUsers
    while 1:
        msg = json.loads(socket.recv(1024).decode())
        if (msg['msgType'] == 0):
            welcomeMsg = json.dumps(
                {'id': numUsers, 'msg': 'Welcome, ' + msg['username']})
            users[msg['username']] = {"id": numUsers, "chatWith": None}
            numUsers += 1
            print(users)
            socket.send(welcomeMsg.encode())
        elif (msg['msgType'] == 1):
            socket.send(json.dumps({'users': users}).encode())
        elif (msg['msgType'] == 2):
            print(msg['chatWith'])
            socket.send(json.dumps({'status': 'connected'}).encode())
    socket.close()


def run():
    serverPort = 12000
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('', serverPort))
    serverSocket.listen(1)
    print('Listening on port ' + str(serverPort))
    while 1:
        connectionSocket, addr = serverSocket.accept()
        Thread(target=handleConnection, args=[connectionSocket]).start()


run()
