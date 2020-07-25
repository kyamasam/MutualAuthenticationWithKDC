# load additional Python modules
import socket  
import pickle
import time
import secret_key
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
server_address = (ip_address, 23457)
sock.connect(server_address)  
print("connecting to %s (%s) with %s" % (local_hostname, local_fqdn, ip_address))

# make a request to speak to bob
request_msg = []

request_msg.append("I am Alice")
request_msg.append("alice")


sock.send(pickle.dumps(request_msg))

counter = 0
key =0
verifier_msg = "msg"
# keep the connection open
while True:
        data = sock.recv(64)
        # receive data on : second client address and shared key
        if data:
            if counter == 0:
                second_party_data = pickle.loads(data)
                print(second_party_data)
                sock.close()

                time.sleep(1)
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
                print("Starting Auth by sending message to Alice")

                key = second_party_data[0]
                print("key is ", key)
                msg = secret_key.encrypt(verifier_msg, int(key))

                # sending an encrypted message
                counter += 1
                sock.send(pickle.dumps(msg))
            elif counter == 1:
                # receive a new message
                received_msg = pickle.loads(data)
                print("received ", received_msg)
                print("another ", verifier_msg)
                # compare that with the original message
                counter += 1
                if verifier_msg == str(received_msg):
                    print("Identity of Party 1 Verified \n Start Identification of party 2 ")
                    sock.send(pickle.dumps("sth"))
                # break
            elif counter == 2:
                print("Received a message from party 2 ", pickle.loads(data))
                print("Decrypting and Sending message back to party 2")

                sock.close()
                # connect to the other party
                # create TCP/IP socket
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                # retrieve local hostname
                local_hostname = socket.gethostname()

                # get fully qualified hostname
                local_fqdn = socket.getfqdn()

                # get the according IP address
                ip_address = socket.gethostbyname(local_hostname)

                # bind the socket to the port 23456, and connect
                server_address = (ip_address, 23456)
                sock.connect(server_address)
                print("Starting Auth by sending message to Alice")
                # receive the message and decrypt
                sock.send(pickle.dumps(secret_key.decrypt(pickle.loads(data), key)))

            else:
                print("going")






