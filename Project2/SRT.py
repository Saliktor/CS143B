from __future__ import division

class SRTProcess:
    # This is a 2D list representing each level of the MLF.

    def __init__(self, index, arrival, exe_time):
        self.index = index #Index will mark the order in which processes arrived from file
        self.arrival = arrival  #Arrival time of process
        self.exe_time = exe_time    #Remaining execution time for process

    def __repr__(self):
        return "MLFProcess(" + str(self.index) + ", " + str(self.arrival) + ", " + str(self.exe_time) + ", " +  \
               str(self.queue_level) + ", " + str(self.queue_time) + ")"


currentTime = 0

def main(processes):
    global currentTime
    currentProcess = None
    finishedList = [None]*len(processes)

    waitList = []
    index = 0

    #Create a list of SRTProcess objects from passed list of tuple objects
    for process in processes:
        waitList.append(SRTProcess(index, process[0], process[1]))
        index += 1


    while(waitList):
        currentProcess = getNextProcess(waitList)

        currentTime += 1
        currentProcess.exe_time -= 1

        if currentProcess.exe_time == 0:
            finishedList[currentProcess.index] = currentTime - currentProcess.arrival
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
        if process.arrival <= currentTime:
            availableProcesses.append(process)
        #Processlist is sorted according to arrival time so once a process is hit that is not available, it is safe to exit loop
        else:
            break

    #If no processes are currently available due to currentTime, increment currentTime to next available process in passed list
    #   which has processes ordered by arrival time and recursively call function
    if not availableProcesses:
        currentTime = processList[0].arrival
        return getNextProcess(processList)

    #Sort the available processes according to the time it would take to complete process
    availableProcesses.sort(key=lambda x: x.exe_time)
    return availableProcesses[0]


if __name__ == '__main__':
    test_list = [(0,4), (0,2), (3,1)]
    print(main(test_list))

