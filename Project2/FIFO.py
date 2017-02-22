from __future__ import division

def main(processes):
    currentTime = 0
    finishedList = []

    for process in processes:
        #If currentTime is not yet at the point in which the next available process has become available, change currentTime
        #   to be equal to the start time of that process
        if currentTime < process[0]:
            currentTime = process[0]

        #Process will be run until completed thus increment currentTime according to how long process will take
        currentTime += process[1]

        #The run time of the process is the currentTime minus the arrival time of the process
        finishedList.append(currentTime - process[0])

    #Return a list with first element being average turnaround time followed by turnaround time for each process in order they arrived
    return [sum(finishedList)/len(finishedList)] + finishedList
