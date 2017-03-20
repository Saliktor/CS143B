from collections import OrderedDict
from Project3.PM import PM

class TLB:
    def __init__(self, memory):
        self.buffer = OrderedDict()
        self.memory = memory

    def update(self, key, pf):
        # print(key, pf)
        newBuffer= OrderedDict()
        newBuffer[key] = pf

        count = 1

        for key, value in self.buffer.items():
            if key in newBuffer:
                continue
            else:
                newBuffer[key] = value
                count += 1
                if count == 4:
                    break

        self.buffer = newBuffer

    def findPageFrameNum(self, ST_Index, PT_Index):
        PT_Frame = self.memory.ST[ST_Index]

        if PT_Index < 512:
            return self.memory.memory[PT_Frame][PT_Index]
        else:
            return self.memory.memory[PT_Frame + 1][PT_Index%512]


    def read(self, VA):
        ST_Index, PT_Index, Page_Offset = self.memory.breakDownVA(VA)
        key = (ST_Index, PT_Index)


        # print(self.buffer)
        # input("Enter")

        if key in self.buffer:
            address = self.buffer[key] * 512 + Page_Offset
            self.update(key, self.buffer[key])
            return ("h", address)

        address = self.memory.readMemory(VA)
        if address > 0: #If no page fault or error, update TLB with new entry
            PageFrame = self.findPageFrameNum(ST_Index, PT_Index)
            self.update(key, PageFrame)

        return ("m", address) #return as miss whether or not it page faulted, error or was succesful

    def write(self, VA):
        ST_Index, PT_Index, Page_Offset = self.memory.breakDownVA(VA)
        key = (ST_Index, PT_Index)

        # print(self.buffer)
        # input("Enter")


        if key in self.buffer:
            address = self.buffer[key] * 512 + Page_Offset
            self.update(key, self.buffer[key])
            #print("Output:", "h", address)
            return ("h", address)

        address = self.memory.writeMemory(VA)
        if address > 0:  # If no page fault or error, update TLB with new entry
            PageFrame = self.findPageFrameNum(ST_Index, PT_Index)
            self.update(key, PageFrame)

        #print("Output:", "m", address)
        return ("m", address)  # return as miss whether or not it page faulted, error or was succesful

