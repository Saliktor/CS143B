from Project1.PriorityQueue import *
from Project1.RCB import *
from collections import namedtuple

Request = namedtuple('Request', 'process amount')

process_list = {}
ready_list = PQ()
current_process = None
resources = {"R1": [RCB("R1", 1, 1), []], "R2": [RCB("R2", 2, 2), []], "R3": [RCB("R3", 3, 3), []],
             "R4": [RCB("R4", 4, 4), []]}

class PCB:
    def __init__(self, ID:str, priority:int, creation_tree):
        self.ID = ID
        self.resources = {"R1": 0, "R2": 0, "R3": 0, "R4": 0}
        self.status = "ready"
        self.creation_tree = {"parent": creation_tree, "children": []}
        self.priority = priority

    def __repr__(self):
        return "PCB(ID: " + self.ID + ", status: " + self.status + ")"

    def __str__(self):
        string_list = []
        string_list.append("ID: " + str(self.ID))
        string_list.append("Resources: " + str(self.resources))
        string_list.append("Status: " + str(self.status))
        string_list.append("Creation_Tree: " + str(self.creation_tree))
        string_list.append("Priority: " + str(self.priority))
        return "\n".join(string_list)

    def addResource(self, RID, amount):
        self.resources[RID] += amount

    def releaseResource(self, RID, amount):
        self.resources[RID] -= amount

    def changeStatus(self, newStatus: str):
        self.status = newStatus

    def addChild(self, child):
        self.creation_tree["children"].append(child)

    def destroy(self):
        for child in self.creation_tree["children"]:
            child.destroy()

        current_process = self

        for RID, amount in self.resources.items():
            if amount > 0:
                releaseResource(RID, amount)

        return self.creation_tree["parent"].creation_tree["children"].remove(self)


    #Create destroy method that will destroy all children, itself and remove self from parents creation_tree


#Process ID cannot already be used by currently existing process
def processExist(p_ID: str) -> bool:
    return p_ID in process_list

#Process can only have a priority of 1-2. 0 = Init, 1 = User, 2 = System
def correctProcessPriority(priority:int) -> bool:
    return priority == 1 or priority == 2

def createNewProcess(p_ID: str, priority: int, parent=None ) -> str:
    global current_process
    output_txt = ""

    if processExist(p_ID):
        output_txt =  "Process with ID \"" + p_ID + "\" already exist"
    elif not correctProcessPriority(priority):
        output_txt = "Process cannot have a priority of " + str(priority)
    else:
        process = PCB(p_ID, priority, creation_tree=parent)
        process_list[p_ID] = process
        ready_list.add(process)
        updateCurrentProcess()

    return output_txt


def resourceExist(RID:str) -> bool:
    return RID in resources

#Requested or Release size cannot be more than the max amount of total resource available and less than or equal to 0
def validResourceSize(RID:str, amount:int) -> bool:
    return  amount <= resources[RID][0].max and amount > 0

def requestResource(RID:str, amount:int) -> str:
    global current_process
    output_txt = ""

    if not resourceExist(RID):
        output_txt = "Resource " + RID + " does not exist"
    elif not validResourceSize(RID, amount):
        output_txt = "Request size of " + str(amount) + " for resource " + RID +" not valid"
    elif waitListEmpty(RID) and availableResources(RID, amount):
        current_process.addResource(RID, amount)
    else:
        blockProcess(RID, amount)

    return output_txt

#Wait list is the second element in the list for each resource. Checks to ensure its not empty
def waitListEmpty(RID) -> bool:
    return not resources[RID][1]


#Resource object(RCB) is first element in the list for each resource. Sends request to RCB object to see if it
#   has enough remaining resource for request. Will return false if not enough available or true and properly
#   reduce the available resources from the RCB object
def availableResources(RID: str, amount: int) -> bool:
    return resources[RID][0].request(amount)


def blockProcess(RID: str, amount: int) -> None:
    global current_process

    resources[RID][1].append(Request(process=current_process, amount=amount))
    current_process.changeStatus("blocked")
    ready_list.remove(current_process)
    updateCurrentProcess()

def updateCurrentProcess():
    global current_process

    current_process.changeStatus = "ready"
    current_process = ready_list.front()
    current_process.changeStatus = "running"


def releaseResource(RID:str, amount: int) -> str:
    global current_process
    output_txt = ""

    if not resourceExist(RID):
        output_txt = "Resource " + RID + " does not exist"
    elif not validResourceSize(RID, amount):
        output_txt = "Release size of " + str(amount) + " for resource " + RID +" not valid"
    elif not processReleaseAvailable(RID, amount):
        output_txt = "Process " + current_process.ID + " does not have " + str(amount) + "of resource " + RID \
                     + " to release"
    else:
        current_process.releaseResources(RID, amount)
        resources[RID][0].release(amount)
        checkWaitList(RID)

    return output_txt


def checkWaitList(RID:str):
    waitList = resources[RID][1]
    if not waitList: #if waitlist is empty then just return
        return
    for request in waitList:
        if availableResources(RID, request.amount):
            request.process.addResource(RID, request.amount)
            request.process.changeStatus("ready")
            resources[RID][1].remove(request) #Remove request from waitlist in resources
            ready_list.add(request.process)
            updateCurrentProcess()
        else:
            return


def deleteProcess(PID:str):
    output_txt = ""

    if not processExist(PID):
        output_txt = "Process with ID \"" + PID + "\" does not exist"
    process_list[PID].destroy() #Testing required
    updateCurrentProcess()

    return output_txt

def processTimeOut():
    global current_process

    current_process.changeStatus("ready")
    ready_list.remove(current_process)
    ready_list.add(current_process)
    updateCurrentProcess()

#Returns bool representing if the currently running process actually contains enough of selected resource
#   to release
def processReleaseAvailable(RID: str, amount:int):
    return current_process.resources[RID] >= amount

def test():
    #Need to create Ready List implemented by some sort priority queue
    global current_process

    createNewProcess("Init", 0)
    print(ready_list)
    # print(current_process)
    # print()
    createNewProcess("a", 2, current_process)
    print(ready_list)
    # print(current_process)
    # print()
    createNewProcess("b", 1, current_process)
    print(ready_list)
    # print(current_process)
    # print()
    # createNewProcess("a", 2, current_process)

if __name__ == '__main__':
    test()



