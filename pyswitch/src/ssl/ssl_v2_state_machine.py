from pyswitch.src.ssl.ssl_v2 import (
    SSLv2Handshake,
    SSLv2HandshakeClientHello,
)
from pyswitch.src.ssl.ssl_v2_constants import (
    SSLv2HandshakeTransitionMap,
    SSLv2HandshakeType,
    SSLv2State,
)


def is_valid_sslv2_handshake_transition(
    from_state: SSLv2HandshakeType,
    to_state: SSLv2HandshakeType,
) -> bool:
    """
    Checks if a transition from the current state to the given state is valid.

    Args:
        from_state (SSLv2HandshakeType): The state from which the transition is made.
        to_state (SSLv2HandshakeType): The state to which the transition is made.

    Returns:
        bool: True if the transition is valid, False otherwise.
    """
    return to_state in SSLv2HandshakeTransitionMap[from_state]


class SSLv2StateMachine:
    """
    Represents the SSLv2 state machine.

    Attributes:
        state (SSLv2State): The current state of the state machine.
        handshake (SSLv2Handshake): The current handshake being processed.

    Methods:
        process(data: bytes): Processes the given data based on the current state.
    """

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
