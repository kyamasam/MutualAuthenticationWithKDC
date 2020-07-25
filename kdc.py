# load additional Python module
import socket
import pickle
import time
import random
# create TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# retrieve local hostname
local_hostname = socket.gethostname()

# get fully qualified hostname
local_fqdn = socket.getfqdn()

# get the according IP address
ip_address = socket.gethostbyname(local_hostname)

# output hostname, domain name and IP address
print("working on %s (%s) with %s" % (local_hostname, local_fqdn, ip_address))

# bind the socket to the port 23456
server_address = (ip_address, 23457)
print('starting up KDC on %s port %s' % server_address)
sock.bind(server_address)

# listen for incoming connections (server mode)
sock.listen(2)

registered_clients = {"alice": 23456}

while True:  
    # wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()

    # show who connected to us
    print('connection from', client_address)
    data = connection.recv(64)

    request_message = pickle.loads(data)

    print(request_message[0])
    print(request_message[1])
    second_party_address = 0
    for k in registered_clients:
        if k == request_message[1]:
            print("we have found ", request_message[1])
            second_party_address = registered_clients[k]

    # generate shared key
    shared_key = random.randrange(2, 10)

    message_to_party = list()

    message_to_party.append(shared_key)
    message_to_party.append(second_party_address)

    # send a message to the initiating party containing shared key and the address of the other party
    connection.send(pickle.dumps(message_to_party))

    # send a message to the other party.
    # connect to the other party
    # create TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # retrieve local hostname
    local_hostname = socket.gethostname()

    # get fully qualified hostname
    local_fqdn = socket.getfqdn()

    # get the according IP address
    ip_address = socket.gethostbyname(local_hostname)

    # connect with the KDC
    # bind the socket to the port 23456, and connect
    server_address = (ip_address, 23456)
    sock.connect(server_address)
    sock.send(pickle.dumps(shared_key))

    print("finished sharing keys. Closing connection...")
    break




