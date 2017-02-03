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



resourceDict = {"R1": [RCB("R1", 1, 1), []], "R2": [RCB("R2", 2, 2), []],
             "R3": [RCB("R3", 3, 3), []], "R4": [RCB("R4", 4, 4), []]}

def resourceExist(RID:str) -> bool:
    return RID in resourceDict


# Requested or Release size cannot be more than the max amount of total resource available and less than or equal to 0
def validResourceRequest(RID:str, amount:int) -> bool:
    return 0 <= amount <= resourceDict[RID][0].max