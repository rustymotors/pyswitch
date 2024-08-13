from pyswitch.src.tls_constants import TLSHandshakeType
from pyswitch.src.utils import bin2hex


class TLSProtocolVersion:
    def __init__(self, data: bytes):
        self.major = data[0]
        self.minor = data[1]

    def __str__(self):
        return f"Major: {self.major}, Minor: {self.minor}"


class TLSHandshake:
    def __init__(self, data: bytes):

        handshake_type = TLSHandshakeType(data[0])

        print("Handshake type: ", handshake_type.name)

        self.handshake_type = handshake_type
        self.data = data

    def __str__(self):
        return f"Handshake type: {self.handshake_type.name}, Data: {bin2hex(self.data)}"
