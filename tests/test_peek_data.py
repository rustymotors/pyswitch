import socket
import unittest
from unittest.mock import MagicMock

from pyswitch.ConnectionHandler import peek_data


class PeekDataTestCase(unittest.TestCase):
    def test_peek_data_returns_bytes(self):
        # Create a mock socket object
        sock = MagicMock(spec=socket.socket)

        # Set the return value of the recv method to a byte string
        sock.recv.return_value = b"Hello, World!"

        # Call the peek_data function
        result = peek_data(sock, 10)

        # Assert that the result is a byte string
        self.assertIsInstance(result, bytes)

    def test_peek_data_calls_recv_with_correct_arguments(self):
        # Create a mock socket object
        sock = MagicMock(spec=socket.socket)

        # Call the peek_data function
        peek_data(sock, 10)

        # Assert that the recv method was called with the correct arguments
        sock.recv.assert_called_once_with(10, socket.MSG_PEEK)


if __name__ == "__main__":
    unittest.main()
