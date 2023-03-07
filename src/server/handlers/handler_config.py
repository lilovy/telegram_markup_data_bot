class AccessLevel:
    def __init__(self):
        self.handler: list
    
    @property
    def user(self):
        self.handler = [
            '/users',
        ]
        return self.handler
    
    @property
    def guest(self):
        self.user
        self.handler += [
            '/run',
            '/return',
        ]
        return self.handler
