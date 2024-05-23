import errno
from select import poll, POLLIN
from socket import socket
from socketserver import BaseRequestHandler, TCPServer


class tcpRequestHandler(BaseRequestHandler):
    def handle(self):
        print("Connection from: ", self.client_address)
        self.request.sendall(b"Hello, World!\n")


def main():
    print("Hello, World!")

    loginSocket = socket()
    loginSocket.setblocking(False)
    personaSocket = socket()
    personaSocket.setblocking(False)

    try:
        loginSocket.bind(("0.0.0.0", 8226))
        print("Bound to port 8226")
    except OSError as e:
        print("Error binding to port 8226: ", e)
        
    try:
        personaSocket.bind(("0.0.0.0", 8228))
        print("Bound to port 8228")
    except OSError as e:
        print("Error binding to port 8228: ", e)
        
    try:
        loginSocket.listen(5)
        print("Listening on port 8226")
    except OSError as e:
        print("Error listening on port 8226: ", e)
        
    try:
        personaSocket.listen(5)
        print("Listening on port 8228")
    except OSError as e:
        print("Error listening on port 8228: ", e)
        
    
    fdMapper = {loginSocket.fileno(): loginSocket, personaSocket.fileno(): personaSocket}
        
        
    try:
        poller = poll()
        poller.register(loginSocket, POLLIN)
        poller.register(personaSocket, POLLIN)
        print("Registered login and persona sockets")
        
        
        while True:
            incoming = poller.poll()
            
            for fd, event in incoming:
                if fd == loginSocket.fileno():
                    print("Login socket ready")
                elif fd == personaSocket.fileno():
                    print("Persona socket ready")
                else:
                    print("Unknown socket ready")
                    
            try:
                incomingSocket = fdMapper[fd]
                
                newSocket, addr = incomingSocket.accept()            
                
                print("Accepted connection on port", incomingSocket.getsockname()[1])
            except OSError as e:
                print("Error accepting connection on port ", fd, ": ", e)
            
        
    except OSError as e:
        print("Error registering login and persona sockets: ", e)

    except KeyboardInterrupt:
        print("Caught KeyboardInterrupt")
        loginSocket.close()
        personaSocket.close()
        print("Closed login and persona sockets")
        print("Exiting")
        exit(0)        


if __name__ == "__main__":
    main()
