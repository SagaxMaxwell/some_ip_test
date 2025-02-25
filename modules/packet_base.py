import struct


class PacketBase:
    SERVICE_ID_LENGTH = 2
    METHOD_ID_LENGTH = 2
    LENGTH_LENGTH = 4
    CLIENT_ID_LENGTH = 2
    SESSION_ID_LENGTH = 2
    PROTOCOL_VERSION_LENGTH = 1
    INTERFACE_VERSION_LENGTH = 1
    MESSAGE_TYPE_LENGTH = 1
    RETURN_CODE_LENGTH = 1

    HEADER_LENGTH = (
        SERVICE_ID_LENGTH
        + METHOD_ID_LENGTH
        + LENGTH_LENGTH
        + CLIENT_ID_LENGTH
        + SESSION_ID_LENGTH
        + PROTOCOL_VERSION_LENGTH
        + INTERFACE_VERSION_LENGTH
        + MESSAGE_TYPE_LENGTH
        + RETURN_CODE_LENGTH
    )

    def __init__(
        self,
        service_id: bytes,
        method_id: bytes,
        length: bytes,
        client_id: bytes,
        session_id: bytes,
        protocol_version: bytes,
        interface_version: bytes,
        message_type: bytes,
        return_code: bytes,
        payload: bytes,
    ):
        self.service_id = service_id
        self.method_id = method_id
        self.client_id = client_id
        self.session_id = session_id
        self.protocol_version = protocol_version
        self.interface_version = interface_version
        self.message_type = message_type
        self.return_code = return_code
        self.payload = payload
        self.length = length

    @property
    def length(self) -> bytes:
        return self.__length

    @length.setter
    def length(self, value: bytes):
        expect_length = len(
            self.request_id
            + self.protocol_version
            + self.interface_version
            + self.message_type
            + self.return_code
            + self.payload
        )
        if not all(
            [
                isinstance(value, bytes),
                len(value) == PacketBase.LENGTH_LENGTH,
                int(value, 16) == expect_length,
            ]
        ):
            raise ValueError(f"length must be {PacketBase.LENGTH_LENGTH} bytes")
        self.__length = value

    @property
    def message_id(self) -> bytes:
        return self.service_id + self.method_id

    @property
    def request_id(self) -> bytes:
        return self.client_id + self.session_id

    @property
    def service_id(self) -> bytes:
        return self.__service_id

    @service_id.setter
    def service_id(self, value: bytes):
        if not isinstance(value, bytes) or len(value) != PacketBase.SERVICE_ID_LENGTH:
            raise ValueError(f"service_id must be {PacketBase.SERVICE_ID_LENGTH} bytes")
        self.__service_id = value

    @property
    def method_id(self) -> bytes:
        return self.__method_id

    @method_id.setter
    def method_id(self, value: bytes):
        if not isinstance(value, bytes) or len(value) != PacketBase.METHOD_ID_LENGTH:
            raise ValueError(f"method_id must be {PacketBase.METHOD_ID_LENGTH} bytes")
        self.__method_id = value

    @property
    def client_id(self) -> bytes:
        return self.__client_id

    @client_id.setter
    def client_id(self, value: bytes):
        if not isinstance(value, bytes) or len(value) != PacketBase.CLIENT_ID_LENGTH:
            raise ValueError(f"client_id must be {PacketBase.CLIENT_ID_LENGTH} bytes")
        self.__client_id = value

    @property
    def session_id(self) -> bytes:
        return self.__session_id

    @session_id.setter
    def session_id(self, value: bytes):
        if not isinstance(value, bytes) or len(value) != PacketBase.SESSION_ID_LENGTH:
            raise ValueError(f"session_id must be {PacketBase.SESSION_ID_LENGTH} bytes")
        self.__session_id = value

    @property
    def protocol_version(self) -> bytes:
        return self.__protocol_version

    @protocol_version.setter
    def protocol_version(self, value: bytes):
        if (
            not isinstance(value, bytes)
            or len(value) != PacketBase.PROTOCOL_VERSION_LENGTH
        ):
            raise ValueError(
                f"protocol_version must be {PacketBase.PROTOCOL_VERSION_LENGTH} byte"
            )
        self.__protocol_version = value

    @property
    def interface_version(self) -> bytes:
        return self.__interface_version

    @interface_version.setter
    def interface_version(self, value: bytes):
        if (
            not isinstance(value, bytes)
            or len(value) != PacketBase.INTERFACE_VERSION_LENGTH
        ):
            raise ValueError(
                f"interface_version must be {PacketBase.INTERFACE_VERSION_LENGTH} byte"
            )
        self.__interface_version = value

    @property
    def message_type(self) -> bytes:
        return self.__message_type

    @message_type.setter
    def message_type(self, value: bytes):
        if not isinstance(value, bytes) or len(value) != PacketBase.MESSAGE_TYPE_LENGTH:
            raise ValueError(
                f"message_type must be {PacketBase.MESSAGE_TYPE_LENGTH} byte"
            )
        self.__message_type = value

    @property
    def return_code(self) -> bytes:
        return self.__return_code

    @return_code.setter
    def return_code(self, value: bytes):
        if not isinstance(value, bytes) or len(value) != PacketBase.RETURN_CODE_LENGTH:
            raise ValueError(
                f"return_code must be {PacketBase.RETURN_CODE_LENGTH} byte"
            )
        self.__return_code = value

    @property
    def payload(self) -> bytes:
        return self.__payload

    @payload.setter
    def payload(self, value: bytes):
        if not isinstance(value, bytes):
            raise ValueError("payload must be bytes")
        self.__payload = value

    @property
    def header(self) -> bytes:
        return (
            self.message_id
            + self.length
            + self.request_id
            + self.protocol_version
            + self.interface_version
            + self.message_type
            + self.return_code
        )

    def encode(self) -> bytes:
        return self.header + self.payload

    @classmethod
    def decode(cls, data: bytes) -> "PacketBase":
        if len(data) < PacketBase.HEADER_LENGTH:
            raise ValueError("Invalid data length")
        header = data[:16]
        service_id = header[0:2]
        method_id = header[2:4]
        client_id = header[8:10]
        session_id = header[10:12]
        protocol_version = header[12:13]
        interface_version = header[13:14]
        message_type = header[14:15]
        return_code = header[15:16]
        payload = data[16:]
        return cls(
            service_id=service_id,
            method_id=method_id,
            client_id=client_id,
            session_id=session_id,
            protocol_version=protocol_version,
            interface_version=interface_version,
            message_type=message_type,
            return_code=return_code,
            payload=payload,
        )

    def __repr__(self):
        return "\n".join(
            [
                f"{'Service ID':<20}: {self.service_id}",
                f"{'Method ID':<20}: {self.method_id}",
                f"{'Client ID':<20}: {self.client_id}",
                f"{'Session ID':<20}: {self.session_id}",
                f"{'Length':<20}: {self.length}",
                f"{'Protocol Version':<20}: {self.protocol_version}",
                f"{'Interface Version':<20}: {self.interface_version}",
                f"{'Message Type':<20}: {self.message_type}",
                f"{'Return Code':<20}: {self.return_code}",
                f"{'Payload':<20}: {self.payload}",
            ]
        )
