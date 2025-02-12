import struct


class SomeIP:
    def __init__(
        self,
        service_id: int,
        method_id: int,
        client_id: int,
        session_id: int,
        length: int,
        protocol_version: int,
        interface_version: int,
        message_type: int,
        return_code: int,
        payload: bytes,
    ):
        self.service_id: int = service_id
        self.method_id: int = method_id
        self.client_id: int = client_id
        self.session_id: int = session_id
        self.length: int = length
        self.protocol_version: int = protocol_version
        self.interface_version: int = interface_version
        self.message_type: int = message_type
        self.return_code: int = return_code
        self.payload: bytes = payload

    def get_message_id(self) -> int:
        return (self.service_id << 16) | self.method_id

    def get_request_id(self) -> int:
        return (self.client_id << 16) | self.session_id

    def set_message_id(self, message_id: int):
        self.service_id = (message_id >> 16) & 0xFFFF
        self.method_id = message_id & 0xFFFF

    def set_request_id(self, request_id: int):
        self.client_id = (request_id >> 16) & 0xFFFF
        self.session_id = request_id & 0xFFFF

    def encode(self) -> bytes:
        header = struct.pack(
            ">HHIHHBBBB",
            self.service_id,
            self.method_id,
            self.length,
            self.client_id,
            self.session_id,
            self.protocol_version,
            self.interface_version,
            self.message_type,
            self.return_code,
        )
        return header + self.payload

    @classmethod
    def decode(cls, data: bytes) -> "SomeIP":
        header = data[:16]
        payload = data[16:]
        (
            service_id,
            method_id,
            length,
            client_id,
            session_id,
            protocol_version,
            interface_version,
            message_type,
            return_code,
        ) = struct.unpack(">HHIHHBBBB", header)
        return SomeIP(
            service_id=service_id,
            method_id=method_id,
            client_id=client_id,
            session_id=session_id,
            length=length,
            protocol_version=protocol_version,
            interface_version=interface_version,
            message_type=message_type,
            return_code=return_code,
            payload=payload,
        )
