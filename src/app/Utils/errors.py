class UserDoesExistsError(Exception):
    def __init__(self, *args):
        super().__init__(*args)
        self.message = "User already exists"

class UserDoesNotExistsError(Exception):
    def __init__(self, *args):
        super().__init__(*args)
        self.message = "User already exists"

class RoleDoesExistsError(Exception):
    def __init__(self, *args):
        super().__init__(*args)
        self.message = "User already exists"

class RoleDoesNotExistsError(Exception):
    def __init__(self, *args):
        super().__init__(*args)
        self.message = "User already exists"

class FoodDoesExistsError(Exception):
    def __init__(self, *args):
        super().__init__(*args)
        self.message = "User already exists"

class FoodDoesNotExistsError(Exception):
    def __init__(self, *args):
        super().__init__(*args)
        self.message = "User already exists"

class ConfigDoesExistsError(Exception):
    def __init__(self, *args):
        super().__init__(*args)
        self.message = "User already exists"

class ConfigDoesNotExistsError(Exception):
    def __init__(self, *args):
        super().__init__(*args)
        self.message = "User already exists"