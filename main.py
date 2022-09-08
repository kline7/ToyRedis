import asyncore
import socket

from .resp_decoder import RESPDecoder
from .store import Store


store = Store()

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
            elif command == b"set":
                status = store.set(args)
                if status:
                    self.send(b"+OK\r\n")
                else:
                    self.send(b"-ERR unknown option for set: px\r\n")
            elif command == b"get":
                value = store.get(args)
                if value:
                    self.send(b"$%d\r\n%b\r\n" % (len(value), value))
                else:
                    self.send(b"$-1\r\n")
            else:
                print("Error unkown command")
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