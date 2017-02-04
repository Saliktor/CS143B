from collections import namedtuple

Request = namedtuple('Request', 'process amount')

class RCB:
    def __init__(self, RID, status, res_max):
        self.RID = RID
        self.status = status
        self.max = res_max

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


# -----------------------------------------------------------------------------------------------------------------------
#Global Variables

#Dictionary with key being resource id and value being a 2 element list
#First element is the RCB object.
#Second element is a list of Request(see namedtuple) acting as waitingList
resourceDict = {"R1": [RCB("R1", 1, 1), []], "R2": [RCB("R2", 2, 2), []],
             "R3": [RCB("R3", 3, 3), []], "R4": [RCB("R4", 4, 4), []]}


#-----------------------------------------------------------------------------------------------------------------------
#Functions

#Will check to if process exist with passed resource identifier
def resourceExist(RID:str) -> bool:
    return RID in resourceDict


# Requested or Release size cannot be more than the max amount of total resource available and less than or equal to 0
def validResourceRequest(RID:str, amount:int) -> bool:
    return 0 < amount <= resourceDict[RID][0].max


#Resource object(RCB) is first element in the list for each resource. Sends request to RCB object to see if it
#   has enough remaining resource for request. Will return false if not enough available or true and properly
#   reduce the available Resource.resourceDict from the RCB object
def availableResource(RID: str, amount: int) -> bool:
    return resourceDict[RID][0].request(amount)


#Goes thorugh resourceDict and resets RCB's amount back to their max and clears their waiting list
def initializeResources():
    global resourceDict
    for key in resourceDict:
        resourceDict[key][0].status = resourceDict[key][0].max
        resourceDict[key][1].clear()


#Wait list is the second element in the list for each resource. Checks to ensure its not empty
def waitListEmpty(RID) -> bool:
    return not resourceDict[RID][1]

