class NetworkError(Exception):
    def __init__(self, code, error):
        self.code = code
        self.error = error
        super().__init__(f"{code}: {error}")
