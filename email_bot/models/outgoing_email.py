class OutgoingEmail:
    def __init__(self, subject: str, body: str, filename: str = None):
        self.subject: str = subject
        self.body: str = body
        self.filename: str = filename
