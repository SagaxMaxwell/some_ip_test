from modules import Connection


class Producer:
    def __init__(self, connection: Connection):
        self.__connection = connection

    @property
    def connection(self) -> Connection:
        return self.__connection
