from Project1.PriorityQueue import *
from Project1 import Resource


class PCB:
    def __init__(self, ID="None", priority=0, parent=None, status="ready"):
        self.ID = ID
        self.resources = {"R1": 0, "R2": 0, "R3": 0, "R4": 0}
        self.status = "ready"
        self.creation_tree = {"parent": parent, "children": []}
        self.priority = priority

    def __repr__(self):
        return "PCB(ID: " + self.ID + ", status: " + self.status + ")"

    def __str__(self):
        string_list = []
        string_list.append("ID: " + str(self.ID))
        string_list.append("Resource.: " + str(self.resources))
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
        global current_process

        for child in self.creation_tree["children"]:
            child.destroy()

        current_process.changeStatus("ready") #Change actual current_process to ready
        current_process = self

        for RID, amount in self.resources.items():
            if amount > 0:
                releaseResource(RID, amount)

        if self.status == "ready" or self.status =="running":
            ready_list.remove(process=self)
        elif self.status == "blocked":
            removeProcessFromWaitList(self)

        del process_list[self.ID]
        return self.creation_tree["parent"].creation_tree["children"].remove(self)


# -----------------------------------------------------------------------------------------------------------------------
# Global Variables


current_process = PCB()
process_list = {}
ready_list = PQ()

#-----------------------------------------------------------------------------------------------------------------------
# Functions


# Process ID cannot already be used by currently existing process
def processExist(p_ID: str) -> bool:
    return p_ID in process_list


# Process can only have a priority of 1-2. 0 = Init, 1 = User, 2 = System
def correctProcessPriority(priority:int) -> bool:
    return priority == 1 or priority == 2


# Creates new process with pass parameters
def createNewProcess(p_ID: str, priority: int ) -> str:
    global current_process
    output_txt = ""

    if processExist(p_ID):
        output_txt =  "error"
    elif not correctProcessPriority(priority):
        output_txt = "error"
    else:

        process = PCB(p_ID, priority, parent=current_process) #create process with pass arguments and cur_proc as parent
        process_list[p_ID] = process #Add PID:process pair to process list
        ready_list.add(process) #Add process to ready_list
        current_process.addChild(process) #Update current process child element in creation tree
        updateCurrentProcess() #Update current Process

    return output_txt


# Create init process
def createInitProcess():
    global current_process

    if processExist("init"):
        return "error"

    process = PCB("init", priority=0, parent=None, status="running")
    process_list["init"] = process
    ready_list.add(process)
    current_process = process


# Request resource on behalf of the currently running process
def requestResource(RID:str, amount:int) -> str:
    global current_process
    output_txt = ""

    #Init process cannot request resource
    if current_process.ID == "init":
        output_txt = "error"
    elif not Resource.resourceExist(RID):
        output_txt = "error"
    elif not Resource.validResourceRequest(RID, amount):
        output_txt = "error"
    elif Resource.waitListEmpty(RID) and Resource.availableResource(RID, amount):
        current_process.addResource(RID, amount)
    else:
        blockProcess(RID, amount)

    return output_txt


# Changes process status to blocked, removes from ready_list, adds to Request(process, amount) to resource waitingList
#   and ensures current_process is properly updated to choose new process to run
def blockProcess(RID: str, amount: int) -> None:
    global current_process

    current_process.changeStatus("blocked")
    Resource.resourceDict[RID][1].append(Resource.Request(process=current_process, amount=amount))
    ready_list.remove(current_process)
    updateCurrentProcess()

# Selects process that is in front of ready_list as new currently running process. Changes old process's status
#   to "ready" in case it is not still in front of ready_list
def updateCurrentProcess():
    global current_process

    # Occurance can be where process is being deleted and end up in this function with status as blocked. Dont want
    #   to change the status from blocked to running so we check to ensure status is running before changing
    if(current_process.status == "running"):
        current_process.changeStatus("ready")

    current_process = ready_list.front()
    current_process.changeStatus("running")


# Releases resource of behalf of currently running process
def releaseResource(RID:str, amount: int) -> str:
    global current_process
    output_txt = ""

    #init cannot release resource
    if current_process.ID == "init":
        output_txt = "error"
    elif not Resource.resourceExist(RID):
        output_txt = "error"
    elif not Resource.validResourceRequest(RID, amount):
        output_txt = "error"
    elif not processReleaseAvailable(RID, amount):
        output_txt = "error"
    else:
        current_process.releaseResource(RID, amount)
        Resource.resourceDict[RID][0].release(amount)
        checkWaitList(RID)

    return output_txt


# After release of resource, checks to any process sitting on that resources waiting list to see if its Request
#   can be satisfied. If so resources are allocated as need be, Request removed and process added to ready_list
def checkWaitList(RID:str):
    waitList = Resource.resourceDict[RID][1]
    if not waitList: #if waitlist is empty then just return
        return
    for request in waitList:
        if Resource.availableResource(RID, request.amount):
            request.process.addResource(RID, request.amount)
            request.process.changeStatus("ready")
            Resource.resourceDict[RID][1].remove(request) #Remove request from waitlist in Resource.resourceDict
            ready_list.add(request.process)
            updateCurrentProcess()
        else:
            return


# Deletes process that matches passed process ID
def deleteProcess(PID:str):
    output_txt = ""

    #cannot delete init process
    if PID == "init":
        output_txt = "error"
    elif not processExist(PID):
        output_txt = "error"
    else:
        process_list[PID].destroy()
        updateCurrentProcess()

    return output_txt


# Will stop currently running function, remove and add back to ready list then sets current process
def processTimeOut():
    global current_process

    current_process.changeStatus("ready")
    ready_list.remove(current_process)
    ready_list.add(current_process)
    updateCurrentProcess()


# Returns bool representing if the currently running process actually contains enough of selected resource to release
def processReleaseAvailable(RID: str, amount:int):
    return current_process.resources[RID] >= amount


# Reinitializes current_process, process_list, ready_list and all resources
def systemWipe():
    global current_process

    Resource.initializeResources()
    ready_list.clear()
    process_list.clear()
    current_process = None


# Searches through all resources waitList and removes any Request that contain passed process
def removeProcessFromWaitList(process: PCB) -> None:
    for key in Resource.resourceDict:
        for request in Resource.resourceDict[key][1]:
            if request.process.ID == process.ID:
                Resource.resourceDict[key][1].remove(request)
                return

