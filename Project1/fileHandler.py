from Project1 import PCB

input_fname = "D:/input.txt"
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
        output_string = "error"
    else:
        output_string = PCB.createInitProcess()

def processCreation(command_line: [str]) -> None:
    global output_string

    if len(command_line) != 3:
        output_string = "error"
    else:   #Handle check of inputs to ensure they can be typecasted to proper type
        output_string = PCB.createNewProcess(command_line[1], int(command_line[2]))

def resourceRequest(command_line: [str]) -> None:
    global output_string

    if len(command_line) != 3:
        output_string = "error"
    else:
        output_string = PCB.requestResource(command_line[1], int(command_line[2]))
    #Should request resource on behalf of currently running process. Should call function from PCB

def resourceRelease(command_line: [str]) -> None:
    global output_string

    if len(command_line) != 3:
        output_string = "error"
    else:
        output_string = PCB.releaseResource(command_line[1], int(command_line[2]))
    #Should release resource on behalf of currently running process. Should call function from PCB

def deleteProcess(command_line: [str]) -> None:
    global output_string

    if len(command_line) != 2:
        output_string = "error"
    else:
        output_string = PCB.deleteProcess(command_line[1])
    #Delete process that is passed in and properly delete all children of process and inform parent proces that process
    #   no longer exist

def timeOut(command_line: [str]) -> None:
    global output_string

    if len(command_line) != 1:
        output_string = "error"
    else:
        PCB.processTimeOut()

def cleanSlate() -> None:
    global output_string

    PCB.systemWipe()


if __name__ == '__main__':
    PCB.createInitProcess()
    readFile()