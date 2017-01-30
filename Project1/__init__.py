class CreationTree:
    def __init__(self):
        self.parent = None
        self.children = []

    def __init__(self, parent: PCB):
        self.parent = parent
        self.children = []

    def addChild(self, child: PCB):
        self.children.append(child)

    def removeChild(self, child: PCB):
        self.children.remove(PCB)

    def __repr__(self):
        repr_string =  "CreationTree(Parent: " + repr(self.parent)
        repr_string += ", Children: "

        child_repr_list = []
        for child in self.children:
            child_repr_list.append(repr(child))

        if child_repr_list:
            repr_string += ", ".join(child_repr_list)
        else:
            repr_string += "None"

        repr_string += ")"

        return repr_string

    def __str__(self):
        str_string = "Parent: " + str(self.parent)
        str_string += ", Children: "

        child_str_list = []
        for child in self.children:
            child_str_list.append(str(child))

        if child_str_list:
            str_string += ", ".join(child_str_list)
        else:
            str_string += "None"

        return str_string

class PCB:
    def __init__(self):
        self.ID = None
        self.resources = None
        self.status = None
        self.creation_tree = CreationTree()
        self.priority = None

    def __init__(self, ID:str, priority:int, resources=0, creation_tree=CreationTree(), status = "running"):
        self.ID = ID
        self.resources = resources
        self.status = status
        self.creation_tree = creation_tree
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


def createInitProcess() -> PCB:
    return PCB("Init", 0)

def createNewProcess(p_name: str, priority: int, parent: PCB ) -> PCB:
    return PCB(p_name, priority, creation_tree = CreationTree(parent))


if __name__ == '__main__':
    initPCB = createInitProcess()
    myPCB = createNewProcess("a", 2, initPCB)
