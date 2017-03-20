#Physical Memory
#1024 Frames each of size 512 words(int)
class PM:
    def __init__(self):
        frame = [0]*512
        self.memory = [x[:] for x in [frame]*1024] #Memory is composed of a 2D list with each element being a list of 512 elements representing a frame
        self.ST = self.memory[0] #ST is always takes up very first frame in memory
        self.usedFrames = [0]

    def getNextAvailableFrame(self):
        for i in range(1024):
            if i not in self.usedFrames:

                return i

        return -1 #No frames available

    def getNextAvailablePT(self):
        for i in range(1024):
            if i not in self.usedFrames and i+1 not in self.usedFrames:
                return i

        return -1  # No frames available


    def initST(self, ST_Index, PT_Address):
        if PT_Address == -1:
            self.ST[ST_Index] = -1
        else:
            PT_Frame = PT_Address//512 #Each frame is 512 and address will be multiple of it

            if PT_Frame not in self.usedFrames and PT_Frame+1 not in self.usedFrames:
                self.ST[ST_Index] = PT_Frame
                self.usedFrames.extend((PT_Frame, PT_Frame+1))
            else:
                return -1 #Place where intializing is already used by another PT or Page

        return 1 #This will represent that no problems occured

    def initPT(self, ST_index, Page_Address, PT_index):
        PT_Frame = self.ST[ST_index]

        if PT_index > 511: #PT takes up two frames so if index is larger than first frame it needs to be properly handeled
            PT_Frame = PT_Frame + 1
            PT_index = PT_index%512

        if Page_Address == -1:
            self.memory[PT_Frame][PT_index] = -1
        else:
            Page_Frame = Page_Address//512
            if Page_Frame not in self.usedFrames:
                self.memory[PT_Frame][PT_index] = Page_Frame
                self.usedFrames.append(Page_Frame)
            else:
                return -1 #Place where intializing is already used by another PT or Page

        return 1 #This will represent that no problems occured


    def breakDownVA(self, VA):
        bin_str = "{0:{fill}32b}".format(VA, fill='0')
        st_index = int(bin_str[4:13], 2)
        pt_index = int(bin_str[13:23], 2)
        page_offset = int(bin_str[23:], 2)
        return (st_index, pt_index, page_offset)


    def readMemory(self, VA):
        ST_Index, PT_Index, Page_Offset = self.breakDownVA(VA)

        #Get PT_Frame value, if -1 or 0 then just return
        PT_Frame = self.ST[ST_Index]
        if PT_Frame <= 0:
            return PT_Frame

        #Get the frame location of page from page table. If value returned is 0 or -1 return, else continue
        if PT_Index < 512: #PT takes up two frames so if index is larger than first frame it needs to be properly handeled
            PageFrame = self.memory[PT_Frame][PT_Index]
        else:
            PageFrame = self.memory[PT_Frame + 1][PT_Index%512]
        if PageFrame <= 0:
            return PageFrame

        #Return address of offset into page which will be the current frame time 512 plus the offset into page
        value = PageFrame*512 + Page_Offset
        return value


    def writeMemory(self, VA):
        ST_Index, PT_Index, Page_Offset = self.breakDownVA(VA)

        #Get PT_Frame, if -1 then out of memory and return, if 0 then PT has not been created thus appropriately make and continue
        PT_Frame = self.ST[ST_Index]
        if PT_Frame == -1:
            return -1
        elif PT_Frame == 0:
            frame = self.getNextAvailablePT()
            if frame == -1:
                return 0 #If this is returned then no available frames available to make new PT
            self.ST[ST_Index] = frame
            PT_Frame = frame
            self.usedFrames.extend((frame, frame+1))


        #Get the frame location of page from page table. If value returned is 0 or -1 return, else continue
        if PT_Index > 511: #PT takes up two frames so if index is larger than first frame it needs to be properly handeled
            PT_Frame = PT_Frame + 1
            PT_Index = PT_Index%512

        PageFrame = self.memory[PT_Frame][PT_Index]
        if PageFrame == -1:
            return -1
        elif PageFrame == 0:
            frame = self.getNextAvailableFrame();
            if frame == -1:
                return 0 #If this is returned then no avaialable frames exist
            self.memory[PT_Frame][PT_Index] = frame
            PageFrame = frame
            self.usedFrames.append(frame)

        # Return address of offset into page which will be the current frame time 512 plus the offset into page
        value = PageFrame*512 + Page_Offset
        return value

    def copy(self):
        newPM = PM()
        newPM.memory = self.memory[:]
        newPM.ST = self.ST
        newPM.usedFrames = self.usedFrames
        return newPM


    def __str__(self):
        return_string = ""

        ST_List = []
        for i in range(512):
            if self.ST[i] != 0:
                ST_List.append((i, self.ST[i]))

        return ST_List.__str__()








