from Project1 import PCB

input_fname = "D:/input1.txt"
output_fname = "D:/31646543.txt"

output_string = ""

def readFile() -> None:
    global output_string
    output = open(output_fname, encoding='utf8', mode='w')
    writeToFile(output)

    with open(input_fname, encoding='utf8', mode='r') as f:
        for line in f:
            if line == "\n":
                cleanSlate()
                output.write("\n")
                continue

            output_string = ""
            command_line = line.split()
            if command_line[0] == "init":
                handleInit(command_line)
            elif command_line[0] == "cr":
                processCreation(command_line)
            elif command_line[0] == "req":
                resourceRequest(command_line)
            elif command_line[0] == "rel":
                resourceRelease(command_line)
            elif command_line[0] == "de":
                deleteProcess(command_line)
            elif command_line[0] == "to":
                timeOut(command_line)
            elif command_line[0] == "...":
                output.write("...")
                return
            else:
                output_txt = "error"
                #output_string = "Not a known command"

            writeToFile(output)

def writeToFile(output):
    global output_string

    if output_string: #If its not empty then write out the message
        output.write(output_string + " ")
    else: #If empty then output will just be the currently running process
        output.write(PCB.current_process.ID + " ")

def handleInit(command_line: [str]) -> None:
    global output_string

    if len(command_line) > 1:
        output_string = "To many arguments with init command"
    else:
        output_string = PCB.createInitProcess()

def processCreation(command_line: [str]) -> None:
    global output_string

    if len(command_line) != 3:
        output_string = "Incorrect number of arguments with cr command"
    else:   #Handle check of inputs to ensure they can be typecasted to proper type
        output_string = PCB.createNewProcess(command_line[1], int(command_line[2]))

def resourceRequest(command_line: [str]) -> None:
    global output_string

    if len(command_line) != 3:
        output_string = "Incorrect number of arguments with req command"
    else:
        output_string = PCB.requestResource(command_line[1], int(command_line[2]))
    #Should request resource on behalf of currently running process. Should call function from PCB

def resourceRelease(command_line: [str]) -> None:
    global output_string

    if len(command_line) != 3:
        output_string = "Incorrect number of arguments with rel command"
    else:
        output_string = PCB.releaseResource(command_line[1], int(command_line[2]))
    #Should release resource on behalf of currently running process. Should call function from PCB

def deleteProcess(command_line: [str]) -> None:
    global output_string

    if len(command_line) != 2:
        output_string = "Incorrect number of arguments with de command"
    else:
        output_string = PCB.deleteProcess(command_line[1])
    #Delete process that is passed in and properly delete all children of process and inform parent proces that process
    #   no longer exist

def timeOut(command_line: [str]) -> None:
    global output_string

    if len(command_line) != 1:
        output_string = "Incorrect number of arguments with to command"
    else:
        PCB.processTimeOut()

def cleanSlate() -> None:
    global output_string

    PCB.systemWipe()


#on initial startup of the script, need to make init on own

def test():
    PCB.createInitProcess()
    print(PCB.current_process.ID)

    PCB.createNewProcess("x", 2)
    print(PCB.current_process.ID)

    PCB.createNewProcess("y", 1)
    print(PCB.current_process.ID)

    PCB.processTimeOut()
    print(PCB.current_process.ID)

    PCB.createNewProcess("z", 2)
    print(PCB.current_process.ID)

    PCB.processTimeOut()
    print(PCB.current_process.ID)

    PCB.requestResource("R1", 1)
    print(PCB.current_process.ID)

    PCB.processTimeOut()
    print(PCB.current_process.ID)

    PCB.requestResource("R1", 1)
    print(PCB.current_process.ID)

    PCB.deleteProcess("z")
    print(PCB.current_process.ID)

    PCB.releaseResource("R1", 1)

    PCB.deleteProcess("x")
    print(PCB.current_process.ID)

    print()
    PCB.systemWipe()
    print()

    PCB.createInitProcess()
    print(PCB.current_process.ID)

    PCB.createNewProcess("x", 1)
    print(PCB.current_process.ID)

    PCB.createNewProcess("p", 1)
    print(PCB.current_process.ID)

    PCB.createNewProcess("q", 1)
    print(PCB.current_process.ID)

    PCB.createNewProcess("r", 1)
    print(PCB.current_process.ID)

    PCB.processTimeOut()
    print(PCB.current_process.ID)

    PCB.requestResource("R2", 2)
    print(PCB.current_process.ID)

    PCB.processTimeOut()
    print(PCB.current_process.ID)

    PCB.requestResource("R3", 2)
    print(PCB.current_process.ID)

    PCB.processTimeOut()
    print(PCB.current_process.ID)

    PCB.requestResource("R4", 1)
    print(PCB.current_process.ID)

    PCB.processTimeOut()
    print(PCB.current_process.ID)

    PCB.processTimeOut()
    print(PCB.current_process.ID)

    PCB.requestResource("R3", 2)
    print(PCB.current_process.ID)

    PCB.requestResource("R4", 4)
    print(PCB.current_process.ID)

    PCB.requestResource("R2", 1)
    print(PCB.current_process.ID)

    PCB.processTimeOut()
    print(PCB.current_process.ID)

    PCB.deleteProcess("q")
    print(PCB.current_process.ID)

    PCB.processTimeOut()
    print(PCB.current_process.ID)

    PCB.processTimeOut()
    print(PCB.current_process.ID)

    print(PCB.requestResource("R1", 2))

    # print(PCB.current_process)
    # print(PCB.ready_list)
    # print(PCB.resources["R3"])
    # print(PCB.resources["R4"])



if __name__ == '__main__':
    #test()
    PCB.createInitProcess()
    readFile()