import sys

class gcodeTextWriter:
    #Error code definition
    OK                      = 0
    CHARACTER_NOT_SUPPORTED = 1

    #orientation definition
    ORIENTATION_VERTICAL = 0
    ORIENTATION_HORIZONTAL = 1


    FONT = { \
        'A':[[0,0,1/2,1],[1/2,1,1,0],[1/3,1/2,2/3,1/2]], \
        'B':[[0,0,0,1],[0,1,1/2,1],[1/2,1,1/2,1/2],[0,1/2,1,1/2],[1,1/2,1,0],[1,0,0,0]], \
        'C':[[1,1,0,1],[0,1,0,0],[0,0,1,0]], \
        'D':[[1/3,0,1/3,1],[0,0,1,0],[1,0,1,1,],[1,1,0,1]], \
        'E':[[1,1,0,1],[0,1,0,0],[0,0,1,0], [0,1/2,1,1/2]], \
        'F':[[1,1,0,1],[0,1,0,0],[0,1/2,1,1/2]], \
        'G':[[1,1,0,1],[0,1,0,0],[0,0,1,0],[1,0,1,1/2],[1,1/2,2/3,1/2]], \
        'H':[[0,0,0,1],[1,1,1,0],[0,1/2,1,1/2]], \
        'I':[[0,0,1,0],[1/2,0,1/2,1],[0,1,1,1]], \
        'J':[[0,0,1/2,0],[1/2,0,1/2,1],[0,1,1,1]], \
        'K':[[0,0,0,1],[0,1/2,1,1],[1,0,0,1/2]], \
        'L':[[0,1,0,0],[0,0,1,0]], \
        'M':[[0,0,0,1],[0,1,1/2,1/2],[1/2,1/2,1,1],[1,1,1,0]], \
        'N':[[0,0,0,1],[0,1,1,0],[1,0,1,1]], \
        'O':[[0,0,0,1],[0,1,1,1],[1,1,1,0],[1,0,0,0]], \
        'P':[[0,0,0,1],[0,1,1,1],[1,1,1,1/2],[1,1/2,0,1/2]], \
        'Q':[[0,0,0,1],[0,1,1,1],[1,1,1,0],[1,0,0,0],[2/3,1/2,1,0]], \
        'R':[[0,0,0,1],[0,1,1/2,1],[1/2,1,1/2,1/2],[0,1/2,1,1/2],[1,1/2,1,0]], \
        'S':[[1,1,0,1],[0,1,0,1/2],[0,1/2,1,1/2],[1,1/2,1,0],[1,0,0,0]], \
        'T':[[0,1,1,1],[1/2,1,1/2,0]], \
        'U':[[0,1,0,0],[0,0,1,0],[1,0,1,1]], \
        'V':[[0,1,1/2,0],[1/2,0,1,1]], \
        'W':[[0,1,0,0],[0,0,1/2,1/2],[1/2,1/2,1,0],[1,0,1,1,1]], \
        'X':[[0,1,1,0],[1,1,0,0]], \
        'Y':[[0,1,1/2,1/2],[1/2,1/2,1,1],[1/2,1/2,1/2,0]], \
        'Z':[[0,1,1,1],[1,1,0,0],[0,0,1,0]], \

        '0':[[0,0,0,1],[0,1,1,1],[1,1,1,0],[1,0,0,0],[0,0,1,1]], \
        '1':[[0,1/2,1/2,1],[1/2,1,1/2,0],[0,0,1,0]], \
        '2':[[0,1,1,1],[1,1,1,1/2],[1,1/2,0,1/2],[0,1/2,0,0],[0,0,1,0]], \
        '3':[[0,1,1,1],[1,1,1,0],[1,0,0,0],[0,1/2,1,1/2]], \
        '4':[[0,1,0,1/2],[0,1/2,1,1/2],[1,1,1,0]], \
        '5':[[2/3,1,0,1],[0,1,0,1/2],[0,1/2,1,1/2],[1,1/2,1,0],[1,0,0,0]], \
        '6':[[2/3,1,0,1],[0,1,0,0],[0,0,1,0],[1,0,1,1/2],[1,1/2,0,1/2]], \
        '7':[[0,1,1,1,],[1,1,1,0]], \
        '8':[[0,0,0,1],[0,1,1,1],[1,1,1,0],[1,0,0,0],[0,1/2,1,1/2]], \
        '9':[[1,1/2,0,1/2],[0,1/2,0,1],[0,1,1,1],[1,1,1,0]], \

        ' ':[], \
        '/':[[0,0,1,1]], \
        '[':[[2/3,1,1/3,1],[1/3,1,1/3,0],[1/3,0,2/3,0]], \
        ']':[[1/3,1,2/3,1],[2/3,1,2/3,0],[2/3,0,1/3,0]], \
        '.':[[7/16,0,7/16,1/8],[7/16,1/8,9/16,1/8],[9/16,1/8,9/16,0],[9/16,0,7/16,0]]}   
        

    def __init__(self):
        return

    def fontConfig(self,width = 2, height = 2,space = 0.5,feedRate = 1000,power = 127):
        self.width = width
        self.height = height
        self.space = space
        self.feedRate = feedRate
        self.power = power
        
        return self.OK

    def printGcode(self,x,y,orientation,text):
        #check the validity of the string
        for char in text:
            error = self.checkChar(char)
            if error != self.OK:
                return error
        
        print(";text ",text)
        print(";-------------------------------------------------------")
        for char in text:
            self.printGcodeChar(x,y,orientation,char)
            if orientation == self.ORIENTATION_HORIZONTAL:
                x += self.width + self.space
            else:
                y += self.width + self.space
        
        return error

    def checkChar(self,char):
        try:
            sequence = self.FONT[char]
        except:
            return(self.CHARACTER_NOT_SUPPORTED)
        
        return self.OK

    def printGcodeChar(self,x,y,orientation,char):
        print(";char " + char)
        try:
            sequence = self.FONT[char]
        except:
            return(self.CHARACTER_NOT_SUPPORTED)

        #print(sequence)
        for line in sequence:
            print("; from (" + str(line[0]) + "," + str(line[1]) +") to (" + str(line[2]) + "," + str(line[3])+")")
            if orientation == self.ORIENTATION_HORIZONTAL:
                x1 = round(x + line[0] * self.width,4)
                y1 = round(y + line[1] * self.height,4)
                x2 = round(x + line[2] * self.width,4)
                y2 = round(y + line[3] * self.height,4)
            else:
                x1 = round(x - line[1] * self.height,4)
                y1 = round(y + line[0] * self.width,4)
                x2 = round(x - line[3] * self.height,4)
                y2 = round(y + line[2] * self.width,4)
            
            print("G0 X"+str(x1)+" Y"+str(y1))
            print("G1 X"+str(x2)+" Y"+str(y2)+" S"+str(self.power)+" F"+str(self.feedRate))
            print()
            

        return self.OK
        
if __name__ == "__main__":
    #instantiate gcodeTextWriter class
    gtw = gcodeTextWriter()
    gtw.fontConfig()
    error = gtw.printGcode(10,10,gtw.ORIENTATION_HORIZONTAL,"ABCDEFGHIJKLMNOPQRSTUVWXYZ.0123456789")
    if error != gtw.OK:
        print("Error writing string")
    # error = gtw.printGcode(10,20,gtw.ORIENTATION_HORIZONTAL,"0123.456789")
    # if error != gtw.OK:
    #     print("Error writing string")
    error = gtw.printGcode(10,15,gtw.ORIENTATION_VERTICAL,"ABCDEFGHIJKLMNOPQRSTUVWXYZ.0123456789")
    if error != gtw.OK:
        print("Error writing string")

    # error = gtw.printGcode(10,30,gtw.ORIENTATION_HORIZONTAL,"abc")
    # if error != gtw.OK:
    #     print("Error writing string")