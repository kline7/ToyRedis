import asyncore
import socket


class MainServerSocket(asyncore.dispatcher):
    def __init__(self, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind(('', port))
        self.listen(5)
    def handle_accept(self) -> None:
        newSocket, address = self.accept()
        print("Connected from ", address)
        SecondaryServerSocket(newSocket)



class SecondaryServerSocket(asyncore.dispatcher_with_send):
    def handle_read(self):
        receivedData = self.recv(32)
        response = "+PONG\r\n"
        if receivedData: 
            print('received "{}"'.format(receivedData.decode('utf-8')))
            self.send(response.encode())
        else: self.close()
    def handle_close(self):
        print("Disconnected from ")

MainServerSocket(6379)
asyncore.loop( )
