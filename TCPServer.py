import json
from socket import *
from threading import Thread

users = {}
userToSocket = {}
numUsers = 0


def syncUsers():
    global userToSocket

    for sock in userToSocket.values():
        sock.send(json.dumps({'msgType': 1, 'users': users}).encode())


def handleConnection(socket):
    global numUsers
    global users
    global userToSocket

    userId = str(numUsers)
    userToSocket[userId] = socket
    while 1:
        msg = socket.recv(1024)
        msg = json.loads(msg.decode())
        print(msg)

        msgType = msg['msgType']
        if (msgType == 0):
            # msg type 0 = register user
            welcomeMsg = json.dumps(
                {'id': userId, 'msg': 'Welcome, ' + msg['username']})
            users[userId] = {"username": msg['username'],  "chatWith": None}
            numUsers += 1
            print(users)
            socket.send(welcomeMsg.encode())
            syncUsers()
        elif (msgType == 2):
            # msg type 2 = chat request
            print(msg)
            otherUserId = msg['chatWith']
            users[userId]['chatWith'] = otherUserId
            syncUsers()
            userToSocket[otherUserId].send(json.dumps(
                {'msgType': 2, 'id': userId}).encode())
        elif(msgType == 3):
            # msg type 3 = close connection
            break
        elif(msgType == 4):
            # msg type 4 = receive chat msg
            print(userToSocket)
            text = msg['msg']
            otherUserId = users[userId]['chatWith']
            socket.send(
                json.dumps({'msgType': 4, 'username': users[userId]['username'], 'msg': text}).encode())
            userToSocket[otherUserId].send(
                json.dumps({'msgType': 4, 'username': users[userId]['username'], 'msg': text}).encode())
            if (text == 'exit'):
                # set chatwith to None for both users
                print("blah")
    users.pop(userId)
    syncUsers()
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
