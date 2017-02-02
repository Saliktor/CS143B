class RCB:
    def __init__(self, RID, status, max):
        self.RID = RID
        self.status = status
        self.max = max

    def request(self, amount):
        if self.status <= amount:
            self.status -= amount
            return True
        else:
            return False

    def release(self, amount):
        self.status += amount
