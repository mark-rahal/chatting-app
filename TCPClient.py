import json
from socket import *
from threading import Thread

userId = None
users = None
clientSocket = None


def send(obj):
    global userId
    global users
    global clientSocket

    clientSocket.send(json.dumps(obj).encode())


def handleMessage(msg):
    global userId
    global users
    global clientSocket

    msgType = msg['msgType']

    if (msgType == 0):
        userId = msg['id']
        print(msg['msg'])

    elif (msgType == 1):
        # updated users event
        users = msg['users']
        print("users updated")

    elif (msgType == 2):
        otherUserId = msg['id']
        print(users[otherUserId]['username'],
              'wants to chat with you, enter 2')

    elif (msgType == 4):
        # direct message received

        print('\r                                       \r', end='')

        if (msg['msg'] == 'exit'):
            print(msg['username'] + ' left the chat.')
        else:
            print(msg['username'] + ': ' + msg['msg'])


def receiveMessageLoop(socket):
    global userId
    global users
    global clientSocket

    while 1:
        msg = socket.recv(1024).decode()
        lines = msg.split('\n')

        for line in lines:
            if (line == ""):
                continue

            msg = json.loads(line)
            handleMessage(msg)


def run():
    global userId
    global users
    global clientSocket

    serverName = '127.0.0.1'
    serverPort = 12000
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))
    username = input('Enter your username: ')
    send({'msgType': 0, 'username': username})

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
                        send({'msgType': 2, 'chatWith': tempId})
                        break

                while 1:
                    # asdf = True
                    chatMsg = input('chat (type exit to exit): ')
                    if (chatMsg == "exit"):
                        break

                    send({'msgType': 4, 'msg': chatMsg})

        elif (selectedAction == 3):
            print('Goodbye.')
            send({'msgType': 3})
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
