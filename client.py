import socket
import msvcrt
import select

#vars
#client_name = ''
menu = '''1.log in
2.send a message to all the users
3.send a private message to a user
4.get the managers list
5.leave the chat
managers only:
6.manager appointing
7.kick off a user
8.silent a user
9.unsilent a user'''
print(menu)
info = ''
pack = ''
#vars

#gets the info from the user
def get_info():
    x = msvcrt.getch()
    info = ''
    while (x != b'\r'):
        info += x.decode()
        print(x.decode(), end='', flush=True)
        x = msvcrt.getch()
    print('')
    return info
#gets the info from the user

#connecting
client_socket = socket.socket()
client_socket.connect(('127.0.0.1', 23))
#connecting

#the user chooses the order that he wants to commit
def send_pack(num):
    pack =''

#log in
    if num == '1':
        print('please enter your name: ')
        client_name = get_info()
        client_name = client_name.lstrip('@')
        pack = num+'*'+client_name
#log in

#send a message
    elif num == '2':
        print('enter your message: ')
        message = get_info()
        pack = num+'*'+message
#send a message

#send a private message
    elif num == '3':
        print('who would you like to send your message to? ')
        name = get_info()
        print('enter your message: ')
        message = get_info()
        pack = num+'*'+name+'*'+message
#send a private message

#get the managers list
    elif num == '4':
        pack = num
#get the managers list

#log out
    elif num == '5':
        pack = num+'*bye'
#log out

#appoint a user to a manager
    elif num == '6':
        print('who would you like to appoint? ')
        name = get_info()
        pack = num + '*' + name
#appoint a user to a manager

#kick off a user
    elif num == '7':
        print('who would you like to kick off? ')
        name = get_info()
        pack = num+'*'+name
#kick off a user

#mute a user
    elif num == '8':
        print('who would you like to mute? ')
        name = get_info()
        pack = num+'*'+name
#mute a user

#unmute a user
    elif num == '9':
        print('who would you like to unmute? ')
        name = get_info()
        pack = num+'*'+name
#unmute a user
    return pack
#the user chooses the order that he wants to commit

#eternal loop for the chat
while True:
    data = ''
    rlist, wlist, xlist = select.select([client_socket],[client_socket],[] )
    if client_socket in rlist:#if the user is in the chat then send him the chat's messages
        data = (client_socket.recv(1024)).decode()
        print(data)
        if(data=='bye'):#if the data is the key word of logging out then log out
            break
    if msvcrt.kbhit():#if the user is writing something to be sent
        num = get_info()#gets the user's request order number
        num = str(num)
        client_socket.send((send_pack(num)).encode())#activates the method of building the data
client_socket.close()
#eternal loop for the chat
