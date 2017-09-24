

# -*-coding:Utf-8 -*
"""C'est la partie server de notra application """
import socket
import sys
import select


_PORT = 12800
_HOST = socket.gethostbyname('localhost')
_RECV_BUFFER = 1024
_RUNNING = True
_USERS = []
 
class Server():
    def __init__(self):
        self.port = _PORT
        self.host = _HOST
        self.running = _RUNNING
        self.buffer = _RECV_BUFFER
        self.users = _USERS
        #self.socket = socket()
 
    def send(self, server, sender, data):
        """ auie"""
        data = data.encode('utf-8')
        #data = data.encode()
        for send in self.users:
            if send != sender and send != server:
                self.socket.send(data)
    def welcome_message(self, newclient, message):
        data = message.encode('utf-8')
        #data = message.encode()
        try:
            self.socket.send(data)
        except socket.error:
            print("Sorry there was an error during the data sending...")

    def bind(self):
        """bind"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.bind((self.host, self.port))
            self.socket.listen(5)
            self.users.append(self.socket)

            print("*" * 60)
            print("CHAT SERVER")
            print("*" * 60)
            print("listenning on port: {0}, host: {1}".format(self.port, self.host))
        except socket.error as error:
            print("Couldn't connect to the remote host: {0}" + "\n" + error).format(self.host)
            sys.exit(1)

    def run(self):
        """"auie """
        self.bind()
        while self.running:
            try:
                ready_to_read, ready_to_write, in_error = select.select(self.users, [], [], 0.05)
            except select.error:
                continue
            for sock in ready_to_read:
                # new connection request received
                if sock == self.socket:
                    sockfd, addr = self.socket.accept()
                    self.users.append(sockfd)
                    self.welcome_message(sockfd, "Welcome on H@X0r Chat server")
                    print("New connected client (%s, %s)" % addr)

                    self.send(self.socket, sockfd, "[%s:%s] entered our chatting room" % addr)

                # a message from a client ont a new connection
                else:
                    # process data receiving from client,
                    try:
                        data = self.socket.recv(self.buffer)
                        if data:
                            self.send(self.socket, sock, '\r' + '=>['+str(sock.getpeername())+']' + data)
                        else:
                            if sock in self.users:
                                self.users.remove(sock)

                                # at this stage no data means probably the connection has been broken
                                self.send(self.socket, sock, "Client (%s, %s) is offline\n" % addr)
 
 
                    except:
                        self.send(self.socket, sock, "Client(%s, %s) is offline\n" % addr)
                        continue
        self.socket.close()


if __name__ == '__main__':
    server = Server()
    server.run()  