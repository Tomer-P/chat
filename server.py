import socket
import select
import datetime

# connecting
server_socket = socket.socket()

server_socket.bind(('127.0.0.1', 23))

server_socket.listen(5)
# connecting

# vars
open_client_sockets = []  # sockets array
messages_to_send = []  # messages to send array
clients_list = ['']  # clients array
socket_list = []
managers_list = []  # managers array
muted_users = []  # muted users array


# vars

# sends the messages to the needed client
def send_waiting_messages(wlist):
    '''sends waiting messages that need to be sent, only if the client's socket is writable.'''
    for message in messages_to_send:
        (client_socket, data) = message
        if client_socket in wlist:
            client_socket.send(data.encode())
            messages_to_send.remove(message)


# sends the messages to the needed client

# eternal chat loop that handles the clients and their requests
while True:
    rlist, wlist, xlist = select.select([server_socket] + open_client_sockets, open_client_sockets, [])
    for current_socket in rlist:
        if current_socket is server_socket:
            (new_socket, address) = server_socket.accept()
            open_client_sockets.append(new_socket)
        else:
            if (current_socket not in muted_users):  # activates the loop as long as the user is not muted
                data = current_socket.recv(1024)
                data = data.decode()
                data = str(data)
                data = data.split('*')  # splits the data and handles it
                if data[0] == '1':  # log in
                    name = data[1]
                    messages_to_send.append((current_socket,
                                             'hello: ' + name))  # builts a packet that contains the users_socket, and hello message to him
                    if (clients_list[0] == ''):
                        clients_list[0] = '@' + name
                        managers_list.append(name)
                    else:
                        clients_list.append(name)

                elif data[0] == '2':  # sends a message
                    x = 0
                    current_name = ''
                    for socket1 in open_client_sockets:  # gets the name of the sender by comparing the recieved socket to the other sockets in the array and gets the index of the user in the arrays
                        if (current_socket == socket1):
                            current_name = clients_list[x]
                        else:
                            x += 1
                    time_now = datetime.datetime.now()  # gets the time
                    time = time_now.strftime("%H:%M")
                    for socket1 in open_client_sockets:  # sends everybody the message besides the sender
                        if (socket1 != current_socket):
                            stuff = str(time) + ' ' + str(current_name) + ': ' + str(data[1])
                            messages_to_send.append((socket1,
                                                     stuff))  # builts a packet that contains the users_socket, and the message that needs to be sent

                elif data[0] == '3':  # sends a private message
                    x = 0
                    current_name = ''
                    for socket1 in open_client_sockets:  # gets the name of the sender by comparing the recieved socket to the other sockets in the array and gets the index of the user in the array
                        if (current_socket == socket1):
                            current_name = clients_list[x]
                        else:
                            x += 1
                    time_now = datetime.datetime.now()  # gets the time
                    time = time_now.strftime("%H:%M")
                    i = 0
                    for name in clients_list:  # finds the person who needs to get the message by comparing the data to the array's names
                        name = name.lstrip('@')
                        if name == data[1]:
                            messages_to_send.append((open_client_sockets[i], time + ' ' + current_name + ': ' + data[
                                2]))  # builts a packet that contains the users_socket, and the message that needs to be sent
                        else:
                            i += 1

                elif data[0] == '4':  # sends the managers list
                    messages_to_send.append((current_socket, 'here is the managers list: ' + ' '.join(
                        managers_list)))  # builts a packet that contains the users_socket, and the managers list

                elif data[0] == '5':  # logs out
                    messages_to_send.append((current_socket, 'bye'))  # sends the key word of logging out
                    i = 0
                    for socket1 in open_client_sockets:  # removes this user's socket
                        if socket1 == current_socket:
                            open_client_sockets.remove(socket1)
                            clients_list.remove(clients_list[i])
                        else:
                            i += 1

                elif data[0] == '6':  # appoints a user
                    x = 0
                    current_name = ''
                    for socket1 in open_client_sockets:  # gets the name of the sender by comparing the recieved socket to the other sockets in the array and gets the index of the user in the array
                        if (current_socket == socket1):
                            current_name = clients_list[x]
                        else:
                            x += 1
                    if current_name[:1] == '@':  # checks if this user is a manager and is allowes to this action
                        i = 0
                        for name in clients_list:
                            if name == data[1]:
                                managers_list.append(clients_list[i])  # adds this user's name to the managers list
                                messages_to_send.append((open_client_sockets[i],
                                                         'you have been appointed to a manager'))  # builts a packet that contains the users_socket, and a message that he had been appointed to a manager
                                clients_list[i] = '@' + name  # adds @ to the user's name
                            else:
                                i += 1
                    else:
                        messages_to_send.append((current_socket,
                                                 "I'm sorry you are not a manager"))  # if the user is not a manager it doesn't allow him to do this action

                elif data[0] == '7':  # kicks off a user
                    x = 0
                    current_name = ''
                    for socket1 in open_client_sockets:  # gets the name of the sender by comparing the recieved socket to the other sockets in the array and gets the index of the user in the array
                        if (current_socket == socket1):
                            current_name = clients_list[x]
                        else:
                            x += 1
                    if current_name[:1] == '@':  # checks if this user is a manager and is allowes to this action
                        i = 0
                        for name in clients_list:
                            if name == data[1]:
                                messages_to_send.append(
                                    (open_client_sockets[i], 'bye'))  # sends the key word of logging out
                                open_client_sockets.remove(
                                    open_client_sockets[i])  # removes this user's socket and name from the lists
                                clients_list.remove(data[1])
                            else:
                                i += 1
                    else:
                        messages_to_send.append((current_socket,
                                                 "I'm sorry you are not a manager"))  # if the user is not a manager it doesn't allow him to do this action

                elif data[0] == '8':  # mutes a user
                    x = 0
                    current_name = ''
                    for socket1 in open_client_sockets:  # gets the name of the sender by comparing the recieved socket to the other sockets in the array and gets the index of the user in the array
                        if (current_socket == socket1):
                            current_name = clients_list[x]
                        else:
                            x += 1
                    if current_name[:1] == '@':  # checks if this user is a manager and is allowes to this action
                        i = 0
                        for name in clients_list:
                            if name == data[1]:
                                muted_users.append(open_client_sockets[i])  # adds this user to the muted users list
                                messages_to_send.append((open_client_sockets[i],
                                                         'sorry, you are muted '))  # builts a packet that contains the users_socket, and a message that he had been muted
                            else:
                                i += 1
                    else:
                        messages_to_send.append((current_socket,
                                                 "I'm sorry you are not a manager"))  # if the user is not a manager it doesn't allow him to do this action

                elif data[0] == '9':  # unmutes a user
                    x = 0
                    current_name = ''
                    for socket1 in open_client_sockets:  # gets the name of the sender by comparing the recieved socket to the other sockets in the array and gets the index of the user in the array
                        if (current_socket == socket1):
                            current_name = clients_list[x]
                        else:
                            x += 1
                    if current_name[:1] == '@':  # checks if this user is a manager and is allowes to this action
                        i = 0
                        for name in clients_list:
                            if name == data[1]:
                                muted_users.remove(
                                    open_client_sockets[i])  # removes this user from the muted users list
                                messages_to_send.append((open_client_sockets[i],
                                                         'you are no longer muted '))  # builts a packet that contains the users_socket, and a message that he had been unmuted
                            else:
                                i += 1
                    else:
                        messages_to_send.append((current_socket,
                                                 "I'm sorry you are not a manager"))  # if the user is not a manager it doesn't allow him to do this action

    send_waiting_messages(wlist)
# eternal chat loop that handles the clients and their requests

