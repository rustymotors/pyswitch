from loguru import logger
from pyswitch.src.ssl.ssl_v2_constants import SSLv2HandshakeType
from pyswitch.src.utils import bin2hex
from pyswitch.src.utils import assert_enough_data


class SSLv2HandshakeClientHello:
    def __init__(self, data: bytes):
        self.client_version = SSLProtocolVersion(data[:2])
        self.cipher_specs = data[2:22]
        self.session_id = data[22:24]
        self.challenge = data[24:32]

    def __str__(self):
        return "Version: {}, Cipher Specs: {}, Connection ID: {}, Challenge: {}".format(
            self.client_version,
            bin2hex(self.cipher_specs),
            bin2hex(self.session_id),
            bin2hex(self.challenge),
        )


class SSLv2Handshake:
    def __init__(self, data: bytes):
        self.handshake_type = SSLv2HandshakeType(data[0])
        self.data = data

    def __str__(self):
        return f"Handshake type: {self.handshake_type.name}, Data: {bin2hex(self.data)}"


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
        try:
            logger.debug("Data length: {}".format(len(data)))
            assert_enough_data(len(data), self.length)
        except ValueError as e:
            logger.error("Error: {}".format(e))
            logger.error("Data: {}".format(bin2hex(data)))
        self.record_type = bin2hex(data[2:3])

    def __str__(self):
        return "Length: {}, Is Escape: {}, Record Type: {}".format(
            self.length, self.is_escape, self.record_type
        )


class SSLv2Record:
    def __init__(self, data: bytes):
        self.header = SSLv2RecordHeader(data)
        self.record_type = self.header.record_type
        self.data = data

    def __str__(self):
        return "Length: {}, Is Escape: {}, Record Type: {}, Data: {}".format(
            self.header.length,
            self.header.is_escape,
            self.header.record_type,
            bin2hex(self.data),
        )
