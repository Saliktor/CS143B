from __future__ import division

#Global variable representing a time stamp of the system
currentTime = 0

def main(processes):
    global currentTime
    waitList = list(processes)
    currentProcess = None
    finishedList = [None]*len(processes)


    while(waitList):
        currentProcess = getNextProcess(waitList)

        #In case a process has run time of 0, we simply wont increment current time and will add it to finishedlist
        if currentProcess[1] != 0:
            #Process will be run until completed thus increment currentTime according to how long process will take
            currentTime += currentProcess[1]

        #Gets the index of the currentProcess according to passed list processes for ordering of finishedList
        index = processes.index(currentProcess)
        finishedList[index] = currentTime - currentProcess[0]
        waitList.remove(currentProcess)

    #Return a list with first element being average turnaround time followed by turnaround time for each process in order they arrived
    return [sum(finishedList)/len(finishedList)] + finishedList


#Will go through all processes that need to be executed, seperate out all processes that are currently available, and then return
#   the process that has the shortest job time
def getNextProcess(processList):
    global currentTime
    availableProcesses= []

    for process in processList:
        #All available processes will have their arrival time less than or equal to current time
        if process[0] <= currentTime:
            availableProcesses.append(process)
        #Processlist is sorted according to arrival time so once a process is hit that is not avaialable, it is safe to exit loop
        else:
            break

    #If no processes are currently available due to currentTime, increment currentTime to next available process in passed list
    #   which has processes ordered by arrival time and recursively call function
    if not availableProcesses:
        currentTime = processList[0][0]
        return getNextProcess(processList)

    #Sort the available processes according to the time it would take to complete process
    availableProcesses.sort(key=lambda x: x[1])
    return availableProcesses[0]



