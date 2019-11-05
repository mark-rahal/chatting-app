import json
from socket import *
from threading import Thread

userId = None
users = None


def receiveMessageLoop(socket):
    global users

    while 1:
        msg = socket.recv(1024)
        msg = json.loads(msg.decode())
        msgType = msg['msgType']

        if (msgType == 1):
            # updated users event
            users = msg['users']
            print("users updated")

        elif (msgType == 2):
            otherUserId = msg['id']
            print(users[otherUserId]['username'],
                  'wants to chat with you, enter 2')

        elif (msgType == 4):
            # direct message received

            print(msg['username'] + ': ' + msg['msg'])
            if (msg['msg'] == 'exit'):
                print(msg['username'] + ' left the chat.')
                # break


def run():
    global userId
    global users

    serverName = '127.0.0.1'
    serverPort = 12000
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))
    username = input('Enter your username: ')
    clientSocket.send(json.dumps(
        {'msgType': 0, 'username': username}).encode())
    welcomeRes = clientSocket.recv(1024).decode()
    welcomeObj = json.loads(welcomeRes)
    print(welcomeObj['msg'])
    userId = welcomeObj['id']

    Thread(target=receiveMessageLoop, args=[clientSocket]).start()

    while 1:
        selectedAction = int(promptAction())
        if (selectedAction == 1):
            if (len(users) == 1):
                print('No other users online.')
            else:
                for user in users:
                    if (user != userId):
                        print(users[user]['username'], end=': ')
                        if (users[user]['chatWith'] == None):
                            print('Available')
                        else:
                            print('Chatting with ' + user)
        elif (selectedAction == 2):
            if (len(users) == 1):
                print('No other users online.')
            else:
                for user in users:
                    if (user != userId):
                        if (users[user]['chatWith'] == None):
                            print(users[user]['username'], end=': ')
                            print('Available')
                chatWith = input(
                    'Enter the username of who you want to chat with: ')
                for tempId, user in users.items():
                    if (user['username'] == chatWith):
                        clientSocket.send(json.dumps(
                            {'msgType': 2, 'chatWith': tempId}).encode())
                        break

                while 1:
                    # asdf = True
                    chatMsg = input('chat (type exit to exit): ')
                    clientSocket.send(json.dumps(
                        {'msgType': 4, 'msg': chatMsg}).encode())

        elif (selectedAction == 3):
            print('Goodbye.')
            clientSocket.send(json.dumps({'msgType': 3}).encode())
            break
        else:
            print('Please enter a valid option.')
    clientSocket.close()


def promptAction():
    print('1. List Users')
    print('2. Chat')
    print('3. Exit')
    return input('Enter choice: ')


run()
