import socket
from socket import SocketKind


class Connection:
    def __init__(self, ipv4: str, port: int):
        self.__ipv4 = ipv4
        self.__port = port
        self.__sock = None

    @property
    def ipv4(self) -> str:
        return self.__ipv4

    @property
    def port(self) -> int:
        return self.__port

    def connect(self, net: SocketKind) -> None:
        if not self.__sock:
            self.__sock = socket.socket(socket.AF_INET, net)

    def send(self, packet: bytes, timeout: int = 5) -> bytes:
        if not self.__sock:
            raise ConnectionError()
        self.sock.settimeout(timeout)
        self.__sock.sendto(packet, (self.server_ip, self.server_port))
        try:
            response, server_address = self.sock.recvfrom(1024)
            return response
        except socket.timeout:
            raise TimeoutError()
        except Exception:
            raise Exception()

    def close(self):
        if self.__sock:
            self.__sock.close()
            self.__sock = None


client = Connection("127.0.0.1", 5000)
client.connect(SocketKind.SOCK_DGRAM)
client.send(b"Hello, World!")
client.close()
