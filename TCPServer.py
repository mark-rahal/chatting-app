import json
from socket import *
from threading import Thread

users = {}
userToSocket = {}
numUsers = 0


def send(socket, obj):
    socket.send((json.dumps(obj) + '\n').encode())


def syncUsers():
    global users
    global userToSocket
    global numUsers

    for sock in userToSocket.values():
        send(sock, {'msgType': 1, 'users': users})


def handleConnection(socket):
    global users
    global userToSocket
    global numUsers

    userId = str(numUsers)
    userToSocket[userId] = socket
    while 1:
        msg = socket.recv(1024)
        if (len(msg) == 0):
            break

        msg = json.loads(msg.decode())

        msgType = msg['msgType']
        if (msgType == 0):
            # msg type 0 = register user
            users[userId] = {"username": msg['username'], "chatWith": None}
            numUsers += 1
            print(users)
            send(socket, {'msgType': 0, 'id': userId,
                          'msg': 'Welcome, ' + msg['username']})
            syncUsers()
        elif (msgType == 2):
            # msg type 2 = chat request
            print(msg)
            otherUserId = msg['chatWith']
            users[userId]['chatWith'] = otherUserId
            syncUsers()
            send(userToSocket[otherUserId], {'msgType': 2, 'id': userId})
        elif(msgType == 3):
            # msg type 3 = close connection
            break
        elif(msgType == 4):
            # msg type 4 = receive chat msg
            print(userToSocket)
            text = msg['msg']
            otherUserIds = users[userId]['chatWith']
            for other in otherUserIds:
              send(userToSocket[other], {
                 'msgType': 4, 'username': users[userId]['username'], 'msg': text})
            if (text == 'exit'):
                # set chatwith to None for both users
                print("blah")
        elif(msgType == 6):
            # msg type 6 = push msg to all clients
            print(userToSocket)
            text = msg['msg']
            for socket in userToSocket:
                send(socket[otherUserId], {'msgType': 4, 'username': users[userId]['username'], 'msg': text})
            if (text == 'exit'):
                # set chatwith to None for both users
                print("blah")

    users.pop(userId)
    del userToSocket[userId]
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
