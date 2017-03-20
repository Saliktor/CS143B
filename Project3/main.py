from codecs import open
from Project3.PM import PM
from Project3.TLB import TLB


init_fname = "E:\input1.txt"
input_fname = "E:\input2.txt"
outputnotlb_fname = "E:\\31646543-notlb.txt"
outputtlb_fname = "E:\\31646543-tlb.txt"

def readInit():
    file = open(init_fname, encoding="utf8", mode='r')
    line = file.readline().split()

    memory = PM()

    i = 0
    while(i < len(line)):
        s = int(line[i])
        f = int(line[i+1])
        i += 2
        memory.initST(s,f)

    line = file.readline().split()
    i = 0
    while(i < len(line)):
        p = int(line[i])
        s = int(line[i+1])
        f = int(line[i+2])
        i += 3

        memory.initPT(s, f, p)

    file.close()
    return memory

def readInput(memory, tlb):
    file = open(input_fname, encoding="utf8", mode='r')
    line = file.readline().split()
    output_notlb = []
    output_tlb = []

    i = 0
    while(i < len(line)):
        operation = int(line[i])
        VA = int(line[i+1])
        # print(i//2, operation, VA)
        i += 2

        if operation == 0:
            output_notlb.append(memory.readMemory(VA))
            output_tlb.append(tlb.read(VA))
        elif operation == 1:
            output_notlb.append(memory.writeMemory(VA))
            output_tlb.append(tlb.write(VA))

    output_notlb = decodeOutputList(output_notlb)
    output_tlb = decodeOutputListTLB(output_tlb)

    writeToFile(output_notlb, output_tlb)

    file.close()

def decodeOutputList(output):
    newOutput = []
    for i in range(len(output)):
        if output[i] == -1:
            newOutput.append("pf")
        elif output[i] == 0:
            newOutput.append("err")
        else:
            newOutput.append(str(output[i]))

    return newOutput


def decodeOutputListTLB(output):
    newOutput = []
    for i in range(len(output)):
        if output[i][1] == -1:
            newOutput.extend((output[i][0], "pf"))
        elif output[i][1] == 0:
            newOutput.extend((output[i][0], "err"))
        else:
            newOutput.extend((output[i][0], str(output[i][1])))

    return newOutput


def writeToFile(output_notlb, output_tlb):
    file1 = open(outputnotlb_fname, encoding="utf8", mode='w')
    output_str = " ".join(output_notlb)
    file1.write(output_str)

    file1.close()

    file2 = open(outputtlb_fname, encoding="utf8", mode='w')
    output_str = " ".join(output_tlb)
    file2.write(output_str)

    file2.close()



if __name__ == "__main__":
    memory = readInit()

    tlb = TLB(memory.copy())

    readInput(memory, tlb)
