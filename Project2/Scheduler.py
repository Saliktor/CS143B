from Project2 import FIFO, SJF, SRT, MLF
from codecs import open

input_fname = "E:/input.txt"
output_fname = "E:/31646543.txt"

output_string = ""

def readFile():
    processList = []

    f = open(input_fname, encoding='utf8', mode='r')
    line = f.readline().split()
    f.close()

    index = 0

    while(index != len(line)):
        processList.append((int(line[index]), int(line[index+1])))
        index += 2


    getOutput(FIFO.main(processList))
    getOutput(SJF.main(processList))
    getOutput(SRT.main(processList))
    getOutput(MLF.main(processList))

    writeToFile()

def writeToFile():
    global output_string, output_fname

    with open(output_fname, encoding='utf8', mode='w') as f:
        f.write(output_string)


def getOutput(output):
    global output_string

    for index in range(len(output)):
        if index == 0:
            numstring = format(output[index], ".3f")
            output_string += numstring[:numstring.find('.')+3]
        else:
            output_string += " " + str(output[index])

    output_string += "\n"

if __name__ == '__main__':
    readFile()



