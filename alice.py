# load additional Python module
import socket
import pickle
import _thread
import secret_key
import time
# create TCP/IP socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# retrieve local hostname
local_hostname = socket.gethostname()

# get fully qualified hostname
local_fqdn = socket.getfqdn()

# get the according IP address
ip_address = socket.gethostbyname(local_hostname)

# output hostname, domain name and IP address
print ("working on %s (%s) with %s" % (local_hostname, local_fqdn, ip_address))

# bind the socket to the port 23456
server_address = (ip_address, 23456)  
print('starting up on %s port %s' % server_address)
sock.bind(server_address)

# listen for incoming connections (server mode) with one connection at a time
sock.listen(2)

shared_key = 0
verifier_message = "our"

counter = 0
while True:
    # wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()

    # show who connected to us
    print('connection from', client_address)

    # receive the data i n small chunks and print it
    print("counter value ", counter)
    while True:
        data = connection.recv(64)
        if data:
            if counter == 0:
                shared_key = pickle.loads(data)
                # output received data
                print("Shared key: %s" % shared_key)
                counter += 1
            elif counter == 1:
                message = pickle.loads(data)
                print("Message ,", message)
                print("sending message back")
                counter = 2
                connection.send(pickle.dumps(secret_key.decrypt(message, shared_key)))
                print("Sending verifier message")
                connection.send(pickle.dumps(secret_key.encrypt(verifier_message, shared_key)))
            elif counter == 2:
                print("Receiving the message")
                received_msg = pickle.loads(data)
                print(received_msg)
                if received_msg == verifier_message:
                    print("Identity of Party 2 verified")


        break




