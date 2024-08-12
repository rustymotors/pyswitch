from enum import Enum


class SSLContentType(Enum):
    HANDSHAKE = "handshake"
    DATA = "data"
