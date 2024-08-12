from pyswitch.utils import bin2hex


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
