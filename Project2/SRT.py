from __future__ import division
from collections import OrderedDict

currentTime = 0

def main(processes):
    global currentTime
    currentProcess = None
    finishedList = [None]*len(processes)

    waitList = OrderedDict()
    index = 0

    for process in processes:
        waitList[index] = [process[0], process[1]]
        index += 1


    while(waitList):
        #currentProcess = (index, [arrival, remaining time])
        currentProcess = getNextProcess(waitList)

        currentTime += 1

        currentProcess[1][1] -= 1
        if currentProcess[1][1] == 0:
            finishedList[currentProcess[0]] = currentTime - currentProcess[1][0]
            del waitList[currentProcess[0]]
        else:
            waitList[currentProcess[0]] = currentProcess[1]

    #Return a list with first element being average turnaround time followed by turnaround time for each process in order they arrived
    return [sum(finishedList)/len(finishedList)] + finishedList


#Will go through all processes that need to be executed, seperate out all processes that are currently available, and then return
#   the process that has the shortest job time
def getNextProcess(processList):
    global currentTime
    availableProcesses= []

    for process in processList.items():
        #All available processes will have their arrival time less than or equal to current time
        if process[1][0] <= currentTime:
            availableProcesses.append(process)
        #Processlist is sorted according to arrival time so once a process is hit that is not available, it is safe to exit loop
        else:
            break

    #If no processes are currently available due to currentTime, increment currentTime to next available process in passed list
    #   which has processes ordered by arrival time and recursively call function
    if not availableProcesses:
        currentTime = processList.values()[0]
        availableProcesses = getNextProcess(processList)

    #Sort the available processes according to the time it would take to complete process
    availableProcesses.sort(key=lambda x: x[1][1])
    return availableProcesses[0]


if __name__ == '__main__':
    test_list = [(0,4), (0,2), (3,1)]
    print(main(test_list))

