from PriorityQueue import PQ

process_list = []
ready_list = PQ()
current_process = None

class PCB:
    def __init__(self, ID:str, priority:int, creation_tree, resources=0, status = "running"):
        self.ID = ID
        self.resources = resources
        self.status = status
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

    def addResource(self, amount:int):
        self.resources += amount

    def changeStatus(self, newStatus: str):
        self.status = newStatus

    def addChild(self, child):
        self.creation_tree["children"].append(child)


def checkIfProcessExist(p_ID: str) -> bool:
    return p_ID in process_list

def createNewProcess(p_ID: str, priority: int, parent=None ) -> None:
    global current_process
    if not checkIfProcessExist(p_ID):
        process_list.append(p_ID)
        current_process = PCB(p_ID, priority, creation_tree = parent)
        ready_list.add(current_process)
    else:
        print("Process with ID \"" + p_ID + "\" already exist");

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



