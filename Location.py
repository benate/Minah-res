class Location():
    def __init__(self, type):
        self.users = {}
        self.type = type

    def enter(self, user):
        self.users[user.nickname] = user
        user.location = self
        return True

    def leave(self, user):
        if user.nickname not in self.users:
            return False
        del self.users[user.nickname]
        user.location = None
        return True

    def notifyToAllUsers(self, noti):
        self._notifyToUsers(self.users.values(), noti)

    def notifyToOthers(self, notifier,  noti):
        users = [u for u in self.users.values() if u != notifier]
        self._notifyToUsers(users, noti)

    def _notifyToUsers(self, users, noti):
        for user in users:
            user.notify(noti)
