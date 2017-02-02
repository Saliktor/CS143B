from Project1.PCB import *

input_fname = "D:/input.txt"
output_fname = "D:/31646543.txt"
output_string = ""

def readFile() -> None:
    output = open(output_fname, encoding='utf8', mode='w')

    with open(input_fname, encoding='utf8', mode='r') as f:
        for line in f:
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
            elif command_line[0] == "\n":
                pass
                #Need to wipe out all process and start clean
            else:
                output_string = "Not a known command"

            writeToFile(output)

def writeToFile(output):
    if not output_string:
        output.write("Process ", current_process.PID, " is running")
    else:
        output.write(output_string)

def handleInit(command_line: [str]) -> None:
    if len(command_line) > 1:
        output_string = "To many arguments with init command"
    else:
        output_string = createNewProcess("Init", 0)

def processCreation(command_line: [str]) -> None:
    if len(command_line) != 3:
        output_string = "Incorrect number of arguments with cr command"
    else:
        output_string = createNewProcess(command_line[1], command_line[2], current_process)

def resourceRequest(command_line: [str]) -> None:
    if len(command_line) != 3:
        output_string = "Incorrect number of arguments with req command"
    else:
        output_string = requestResource(command_line[1], command_line[2])
    #Should request resource on behalf of currently running process. Should call function from PCB

def resourceRelease(command_line: [str]) -> None:
    if len(command_line) != 3:
        output_string = "Incorrect number of arguments with rel command"
    else:
        output_string = releaseResource(command_line[1], command_line[2])
    #Should release resource on behalf of currently running process. Should call function from PCB

def deleteProcess(command_line: [str]) -> None:
    if len(command_line) != 2:
       output_string = "Incorrect number of arguments with de command"
    #Delete currently running process and properly delete all children of process and inform parent proces that process
    #   no longer exist

def timeOut(command_line: [str]) -> None:
    if len(command_line) != 1:
        output_string = "Incorrect number of arguments with to command"
    #Unsure of functionality of this


#on initial startup of the script, need to make init on own