class SSLProtocolVersion:
    def __init__(self, data: bytes):
        self.major = data[1]
        self.minor = data[0]

    def __str__(self):
        return f"Major: {self.major}, Minor: {self.minor}"
