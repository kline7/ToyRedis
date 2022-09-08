import socket
import sys
import time


def get_constants(prefix):
    """Create a dictionary mapping socket module constants to their names."""
    return dict( (getattr(socket, n), n)
                 for n in dir(socket)
                 if n.startswith(prefix)
                 )

families = get_constants('AF_')
types = get_constants('SOCK_')
protocols = get_constants('IPPROTO')

t0 = time.perf_counter()
sock = socket.create_connection(('localhost', 6379))

print('Family   :', families[sock.family])
print('Type     :', types[sock.type])
print('Protocols:', protocols[sock.proto])

try:
    while True:
        payload = "*1\r\n$4\r\nPING"
        other_payload = "*2\r\n$4\r\necho\r\n$7\r\noranges\r\n"
        message = '{}'.format(other_payload)
        print('sending {}'.format(message))
        sock.sendall(message.encode())
        print('sent')

        amount_received = 0
        amount_expected = len(message)

        while amount_received < amount_expected:
            data = sock.recv(16)
            amount_expected += len(data)
            print('received "{}"'.format(data.decode('utf-8')))
except KeyboardInterrupt:
    print('Interrupted')

finally:
    print('closing socket')
    sock.close()
    print("Time elapsed: ", time.perf_counter() - t0) # CPU seconds elapsed (floating point)