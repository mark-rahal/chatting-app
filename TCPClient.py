import json
from socket import *


def getUserList(socket):
    socket.send(json.dumps({'msgType': 1}).encode())
    return json.loads(socket.recv(1024).decode())['users']


def chatRequest(socket, chatWith):
    socket.send(json.dumps({'msgType': 2, 'chatWith': chatWith}).encode())
    return json.loads(socket.recv(1024).decode())


def run():
    userId = None
    serverName = 'localhost'
    serverPort = 12000
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))
    username = input('Enter your username: ')
    clientSocket.send(json.dumps(
        {'msgType': 0, 'username': username}).encode())
    welcomeObj = json.load(clientSocket.recv(1024).decode())
    print(welcomeObj['msg'])
    userId = welcomeObj['id']
    while 1:
        selectedAction = int(promptAction())
        if (selectedAction == 1):
            users = getUserList(clientSocket)
            for user in users:
                print(user, end=': ')
                if (users[user].get('chattingWith') == None):
                    print('Available')
                else:
                    print('Chatting with ' + user)
        elif (selectedAction == 2):
            users = getUserList(clientSocket)
            for user in users:
                if (users[user].get('chattingWith') == None):
                    print(user, end=': ')
                    print('Available')
            chatWith = input(
                'Enter the username of who you want to chat with: ')
        elif (selectedAction == 3):
            print('bleh')
        else:
            print('Please enter a valid option.')
    clientSocket.close()


def promptAction():
    print('1. List Users')
    print('2. Chat')
    print('3. Exit')
    return input('Enter choice: ')


run()
