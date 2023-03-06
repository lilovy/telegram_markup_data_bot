

class AdminAccess:
    permission = 'admin'
    def __init__(self):
        # super().__init__()
        self.handlers = [
            '/users'
        ]


class UserAccess(AdminAccess):
    permission = 'user'
    def __init__(self):
        super().__init__()
        self.handlers += [
            '/run',
        ]

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
        ]
        return self.handler


# class GuestAccess:
#     permission = 'guest'
#     def __init__(self):
#         self.handlers = [
#             '/start',
#             '/help',
#             ]


