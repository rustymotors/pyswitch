import unittest

from pyswitch.src.ssl.ssl_v2_constants import SSLv2HandshakeType
from pyswitch.src.ssl.ssl_v2_state_machine import (
    is_valid_sslv2_handshake_transition,
)


class SSLv2StateMachineTestCase(unittest.TestCase):
    def test_valid_transition(self):
        # Test a valid transition from SSLvHandshakeType.CLIENT_HELLO to SSLv2HandshakeType.SERVER_HELLO
        from_state = SSLv2HandshakeType.CLIENT_HELLO
        to_state = SSLv2HandshakeType.SERVER_HELLO
        result = is_valid_sslv2_handshake_transition(from_state, to_state)
        self.assertTrue(result)

    def test_invalid_transition(self):
        # Test an invalid transition from SSLv2HandshakeType.CLIENT_HELLO to SSLv2HandshakeType.CLIENT_MASTER_KEY
        from_state = SSLv2HandshakeType.CLIENT_HELLO
        to_state = SSLv2HandshakeType.CLIENT_MASTER_KEY
        result = is_valid_sslv2_handshake_transition(from_state, to_state)
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
