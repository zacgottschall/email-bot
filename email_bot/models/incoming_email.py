class IncomingEmail:
    def __init__(self, frm: str, subject: str, timestamp: float):
        self.frm: str = frm
        self.subject: str = subject
        self.timestamp: float = timestamp
