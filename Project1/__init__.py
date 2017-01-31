class PCB:
    def __init__(self):
        self.ID = None
        self.resources = None
        self.status = None
        self.creation_tree = {"parent": None, "children": []}
        self.priority = None

    def __init__(self, ID:str, priority:int, resources=0, creation_tree=None, status = "running"):
        self.ID = ID
        self.resources = resources
        self.status = status
        self.creation_tree = {"parent": creation_tree, "children": []}
        self.priority = priority

    def __repr__(self):
        return "PCB( " + self.ID + ")"

    def __str__(self):
        string_list = []
        string_list.append("ID: " + str(self.ID))
        string_list.append("Resources: " + str(self.resources))
        string_list.append("Status: " + str(self.status))
        string_list.append("Creation_Tree: " + str(self.creation_tree))
        string_list.append("Priority: " + str(self.priority))
        return "\n".join(string_list)

    def addResource(self, amount:int):
        self.resources += amount

    def changeStatus(self, newStatus: str):
        self.status = newStatus


#Init process will be only process without a parent
def createInitProcess() -> PCB:
    return PCB("Init", 0)

def createNewProcess(p_name: str, priority: int, parent: PCB ) -> PCB:
    return PCB(p_name, priority, parent)


if __name__ == '__main__':
    initPCB = createInitProcess()
    myPCB = createNewProcess("a", 2, initPCB)
