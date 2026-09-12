import unittest

from pyswitch.ConnectionHandler import ConnectionHandler


class ClassifyConnectionTestCase(unittest.TestCase):
    def test_real_tls_handshake_is_not_legacy(self):
        # ContentType=0x16 (Handshake), version 0x0301 (TLS 1.0), length 0x0001
        data = bytes([0x16, 0x03, 0x01, 0x00, 0x01])
        self.assertFalse(ConnectionHandler._is_legacy_ssl(data))

    def test_real_tls_alert_is_not_legacy(self):
        # ContentType=0x15 (Alert)
        data = bytes([0x15, 0x03, 0x03, 0x00, 0x02])
        self.assertFalse(ConnectionHandler._is_legacy_ssl(data))

    def test_sslv2_short_header_is_legacy(self):
        # MSB set -> 2-byte header, record length in low 15 bits
        data = bytes([0x80, 0x2E, 0x01, 0x00, 0x02])
        self.assertTrue(ConnectionHandler._is_legacy_ssl(data))

    def test_sslv2_long_header_is_legacy(self):
        # MSB clear -> 3-byte header, record length in low 14 bits
        data = bytes([0x2E, 0x01, 0x00, 0x00, 0x02])
        self.assertTrue(ConnectionHandler._is_legacy_ssl(data))

    def test_content_type_0xff_is_not_misclassified_as_modern(self):
        # Regression: TLSContentType(255) aliases APPLICATION_DATA due to a
        # bitwise-OR bug in tls_constants.py, which would have misrouted a
        # legacy record with this first byte to the modern backend.
        data = bytes([0xFF, 0x00, 0x02])
        self.assertTrue(ConnectionHandler._is_legacy_ssl(data))

    def test_unrecognizable_data_raises(self):
        data = bytes([0x00, 0x00])
        with self.assertRaises(ValueError):
            ConnectionHandler._is_legacy_ssl(data)

    def test_too_short_raises(self):
        with self.assertRaises(ValueError):
            ConnectionHandler._is_legacy_ssl(bytes([0x16]))


if __name__ == "__main__":
    unittest.main()
