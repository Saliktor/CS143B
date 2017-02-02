from Project1.PriorityQueue import *
from Project1.RCB import *
from collections import namedtuple

Request = namedtuple('Request', 'process amount')
Resource = namedtuple('Resource', 'resource, waitList')

process_list = []
ready_list = PQ()
current_process = None
resources = {"R1": Resource(RCB("R1", 1, 1), []), "R2": Resource(RCB("R2", 2, 2), []), "R3": Resource(RCB("R3", 3, 3), []),
             "R4": Resource(RCB("R4", 4, 4), [])}

class PCB:
    def __init__(self, ID:str, priority:int, creation_tree):
        self.ID = ID
        self.resources = {"R1": 0, "R2": 0, "R3": 0, "R4": 0}
        self.status = "running"
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
        process_list.append(p_ID)
        ready_list.add(PCB(p_ID, priority, creation_tree = parent))
        current_process = ready_list.front()

    return output_txt


def resourceExist(RID:str) -> bool:
    return RID in resources

#Requested size cannot be more than the max amount of total resource available and more than 0
def validRequestSize(RID:str, amount:int) -> bool:
    return  amount <= resources[RID].resource.max and amount > 0

def requestResource(RID:str, amount:int) -> str:
    output_txt = ""

    if not resourceExist(RID):
        output_txt = "Resource " + RID + " does not exist"
    elif not validRequestSize(RID, amount):
        output_txt = "Request size of " + str(amount) + " for resource " + RID +" not valid"
    elif waitListEmpty(RID) and availableResources(RID, amount):
        current_process.addResource(RID, amount)
    else:
        blockProcess(RID, amount)

    return output_txt

#Access second element of the tuple for each resource to see if its waiting list is empty
def waitListEmpty(RID) -> bool:
    return not resources[RID].waitList

def availableResources(RID, amount) -> bool:
    return resources[RID].resource.request(amount) #Namedtuple might not like this

def blockProcess(RID:str, amount:int) -> None:
    resources[RID].waitList.append(Request(process=current_process, amount = amount)) #Could cause issue if namedtuple doesnt like this
    current_process.changeStatus("blocked")
    ready_list.remove(current_process)
    updateCurrentProcess()

def updateCurrentProcess():
    current_process = ready_list.front()

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



