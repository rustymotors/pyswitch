from enum import Enum
from pyswitch.src.utils import bin2hex


class SSLv2State(Enum):
    HANDSHAKE = "handshake"
    DONE = "done"


class SSLv2HandshakeClientHello:
    def __init__(self, data: bytes):
        self.version = SSLProtocolVersion(data[:2])
        self.cipher_specs = data[2:22]
        self.connection_id = data[22:24]
        self.challenge = data[24:32]

    def __str__(self):
        return "Version: {}, Cipher Specs: {}, Connection ID: {}, Challenge: {}".format(
            self.version,
            bin2hex(self.cipher_specs),
            bin2hex(self.connection_id),
            bin2hex(self.challenge),
        )


class SSLv2HandshakeType(Enum):
    CLIENT_HELLO = 1
    CLIENT_MASTER_KEY = 2
    CLIENT_FINISHED = 3
    SERVER_HELLO = 4
    SERVER_VERIFY = 5
    SERVER_FINISHED = 6
    REQUEST_CERTIFICATE = 7
    CLIENT_CERTIFICATE = 8
    CLIENT_KEY_EXCHANGE = 9


class SSLv2Handshake:
    def __init__(self, data: bytes):
        self.handshake_type = SSLv2HandshakeType(data[0])
        self.data = data

    def __str__(self):
        return f"Handshake type: {self.handshake_type.name}, Data: {bin2hex(self.data)}"


class SSLv2StateMachine:
    def __init__(self):
        self.state = SSLv2State.HANDSHAKE
        self.handshake = None

    def process(self, data: bytes):
        if self.state == SSLv2State.HANDSHAKE:
            self.handshake = SSLv2Handshake(data)
            if self.handshake.handshake_type == SSLv2HandshakeType.CLIENT_HELLO:
                client_hello = SSLv2HandshakeClientHello(self.handshake.data[1:])
                print(client_hello)
        else:
            raise ValueError("Invalid state")

    def __str__(self):
        return f"State: {self.state}, Handshake: {self.handshake}"


class SSLProtocolVersion:
    def __init__(self, data: bytes):
        self.major = data[1]
        self.minor = data[0]

    def __str__(self):
        return f"Major: {self.major}, Minor: {self.minor}"


class SSLv2RecordHeader:
    def __init__(self, data: bytes):
        self.length = ((data[0] & 0x7F) << 8) | data[1]
        self.is_escape = data[2] & 0x80
        if self.is_escape:
            raise ValueError("SSLv2 Escape Record, not supported")
        self.record_type = data[2]

    def __str__(self):
        return "Length: {}, Is Escape: {}, Record Type: {}".format(
            self.length, self.is_escape, self.record_type
        )


class SSLv2Record:
    def __init__(self, data: bytes):
        self.header = SSLv2RecordHeader(data[:3])
        self.record_type = data[2]
        self.data = data[3:]

    def __str__(self):
        return "Length: {}, Is Escape: {}, Record Type: {}, Data: {}".format(
            self.header.length,
            self.header.is_escape,
            self.header.record_type,
            bin2hex(self.data),
        )
