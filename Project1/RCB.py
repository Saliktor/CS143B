class RCB:
    def __init__(self, RID, status, max):
        self.RID = RID
        self.status = status
        self.max = max

    def __repr__(self):
        return "RCB(ID: " + self.RID + ", Available: " + str(self.status) + ")"


    def request(self, amount):
        if amount <= self.status:
            self.status -= amount
            return True
        else:
            return False

    def release(self, amount):
        self.status += amount


