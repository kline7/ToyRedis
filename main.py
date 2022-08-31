import asyncore
import socket

from .resp_decoder import RESPDecoder



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
        try:
            command, *args = RESPDecoder(self).decode()
            if command == b"ping":
                self.send(b"+PONG\r\n")
            elif command == b"echo":
                self.send(b"$%d\r\n%b\r\n" % (len(args[0]), args[0]))
            else:
                self.send(b"-ERR unkown command\r\n")
        except Exception as e:
            print(f'Err: {str(e)}')
    def handle_close(self):
        print("Disconnected from ")
        self.close()

try:
    MainServerSocket(6379)
    asyncore.loop( )
except KeyboardInterrupt:
    print('ctrl+c')
finally:
    print('closing')
