class UserDoesExistsError(Exception):
    def __init__(self, *args):
        super().__init__(*args)
        self.message = "User already exists"

class UserDoesNotExistsError(Exception):
    def __init__(self, *args):
        super().__init__(*args)
        self.message = "User already exists"