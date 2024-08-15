from enum import Enum


class SSLContentType(Enum):
    HANDSHAKE = "handshake"
    DATA = "data"


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


# SSLv2 Handshake Valid State Transition Map (from_state -> to_state)
SSLv2HandshakeTransitionMap = {
    SSLv2HandshakeType.CLIENT_HELLO: [SSLv2HandshakeType.SERVER_HELLO],
    SSLv2HandshakeType.SERVER_HELLO: [
        SSLv2HandshakeType.CLIENT_MASTER_KEY,
        SSLv2HandshakeType.CLIENT_FINISHED,
    ],
    SSLv2HandshakeType.CLIENT_MASTER_KEY: [SSLv2HandshakeType.CLIENT_FINISHED],
    SSLv2HandshakeType.CLIENT_FINISHED: [SSLv2HandshakeType.SERVER_VERIFY],
    SSLv2HandshakeType.SERVER_VERIFY: [
        SSLv2HandshakeType.SERVER_FINISHED,
        SSLv2HandshakeType.REQUEST_CERTIFICATE,
    ],
    SSLv2HandshakeType.SERVER_FINISHED: [],
    SSLv2HandshakeType.REQUEST_CERTIFICATE: [SSLv2HandshakeType.CLIENT_CERTIFICATE],
    SSLv2HandshakeType.CLIENT_CERTIFICATE: [SSLv2HandshakeType.SERVER_FINISHED],
}


class SLv2HandshakeState(Enum):
    CLIENT_HELLO = "client_hello"
    SERVER_HELLO = "server_hello"
    CLIENT_MASTER_KEY = "client_master_key"
    CLIENT_FINISHED = "client_finished"
    SERVER_VERIFY = "server_verify"
    REQUEST_CERTIFICATE = "request_certificate"
    CLIENT_CERTIFICATE = "client_certificate"
    SERVER_FINISHED = "server_finished"


class SSLv2State(Enum):
    """
    Represents the state of the SSLv2 protocol.

    Attributes:
        HANDSHAKE (str): Represents the state during the handshake phase.
        DONE (str): Represents the state when the handshake is completed.
    """

    HANDSHAKE = "handshake"
    DONE = "done"
