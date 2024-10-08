from enum import Enum


class TLSContentType(Enum):
    INVALID = 0
    CHANGE_CIPHER_SPEC = 20
    ALERT = 21
    HANDSHAKE = 22
    APPLICATION_DATA_1 = 23
    APPLICATION_DATA_2 = 255
    APPLICATION_DATA = APPLICATION_DATA_1 | APPLICATION_DATA_2


class TLSHandshakeType(Enum):
    CLIENT_HELLO = 1
    SERVER_HELLO = 2
    NEW_SESSION_TICKET = 4
    END_OF_EARLY_DATA = 5
    ENCRYPTED_EXTENSIONS = 8
    CERTIFICATE = 11
    CERTIFICATE_REQUEST = 13
    CERTIFICATE_VERIFY = 15
    FINISHED = 20
    KEY_UPDATE = 24
    MESSAGE_HASH_1 = 254
    MESSAGE_HASH_2 = 255
    MESSAGE_HASH = MESSAGE_HASH_1 | MESSAGE_HASH_2


class TLSVersion(Enum):
    SSL_3_0 = 0x0300
    TLS_1_0 = 0x0301
    TLS_1_1 = 0x0302
    TLS_1_2 = 0x0303
    TLS_1_3 = 0x0304
