import sys
from gcodeTextWriter import *

class laserTestPatternGenerator:
    

    #Error code definition
    OK                                      = 0
    ERROR_MODE                              = 1
    ERROR_LINE_RESOLUION_CUT_POWER                    = 2
    ERROR_MIN_POWER                         = 3
    ERROR_MAX_POWER                         = 4
    ERROR_STEPS_POWER                       = 5
    ERROR_RANGE_POWER                       = 6
    ERROR_MIN_FEED                          = 7
    ERROR_MAX_FEED                          = 8
    ERROR_RANGE_FEED                        = 9
    ERROR_STEPS_FEED                        = 10
    ERROR_LINE_RESOLUTION                   = 11

    def __init__(self,mode,minPowerPasses, maxPowerPasses, stepsPowerPasses, minFeed, maxFeed, stepsFeed, sampleLineResoultion = 10):
        self.mode = mode.lower()
        self.minPowerPasses = minPowerPasses
        self.maxPowerPasses = maxPowerPasses
        self.stepsPowerPasses = stepsPowerPasses
        self.minFeed = minFeed
        self.maxFeed = maxFeed
        self.stepsFeed = stepsFeed     
        self.LineResolutionCutPower = sampleLineResoultion

        #config default sample size and resolution
        self.cutSampleWidth = 10
        self.cutSampleHeight = 10
        
        self.engraveSampleWidth = 5
        self.engraveSampleHeight = 5
        
        self.sampleHorizontalSpace = 5
        self.sampleVerticalSpace = 5
      
        #config font sizes
        self.topHeaderFontWidth = 3
        self.topHeaderFontHeight = 6
        self.powerFeedHeaderFontWidth = 3
        self.powerFeedHeaderFontHeight = 3
        self.powerFeedValuesFontWidth = 3
        self.powerFeedValuesFontHeight = 3



        #instanciate test writer
        self.gtw = gcodeTextWriter()
        
        return

    def validateParameters(self):
        #Check mode
        if (self.mode).lower() != "cut" and (self.mode).lower() != "engrave":
            return self.ERROR_MODE

        #check lineResolution
        if self.mode == "cut":
            if self.LineResolutionCutPower < 0 or self.LineResolutionCutPower > 255:
                return self.ERROR_LINE_RESOLUION_CUT_POWER
        else:
            if self.LineResolutionCutPower < 0 or self.LineResolutionCutPower > 40:
                return self.ERROR_LINE_RESOLUION_CUT_POWER

        #check power parameters
        if self.minPowerPasses < 0 or self.minPowerPasses > 255:
            return self.ERROR_MIN_POWER
            
        if self.maxPowerPasses < 0 or self.maxPowerPasses > 255:
            return self.ERROR_MAX_POWER
        
        if self.stepsPowerPasses < 0 or self.stepsPowerPasses > 10:
            return self.ERROR_STEPS_POWER
        
        if self.maxPowerPasses < self.minPowerPasses:
            return self.ERROR_RANGE_POWER

        #check feed parameters
        if self.minFeed < 0 or self.minFeed > 30000:
            return self.ERROR_MIN_FEED
            
        if self.maxFeed < 0 or self.maxFeed > 30000:
            return self.ERROR_MAX_FEED
        
        if self.stepsFeed < 0 or self.stepsFeed > 10:
            return self.ERROR_STEPS_FEED
        
        if self.maxFeed < self.minFeed:
            return self.ERROR_RANGE_FEED

        return self.OK

    # def setSampleConfiguration(self,width,horizontalSpace,height,verticalSpace,LineResolutionCutPower):
    #     self.sampleWidth = width
    #     self.sampleHorizontalSpace = horizontalSpace
    #     self.sampleHeight = height
    #     self.sampleVerticalSpace = verticalSpace
    #     self.LineResolutionCutPower = LineResolutionCutPower
    
    def startGcode(self):
        #generate the GCODE file header
        print("; G-Code header")
        print("G21         ; Set units to mm")
        print("G90         ; Absolute positioning")
        print("M3 S0       ; Enable Laser (0 power)")
        print()

    def endGcode(self):
        #generate the GCODE file footer
        print()
        print("; G-Code footer")
        print("M5")

    def createHeaders(self):    
        #calculate test pattern dimentions
        if self.mode == "cut":
            self.tpgWidth = self.stepsFeed*(self.cutSampleWidth + self.sampleHorizontalSpace)
            self.tpgHeight = self.stepsPowerPasses * (self.cutSampleHeight + self.sampleVerticalSpace)
        else:
            self.tpgWidth = self.stepsFeed*(self.engraveSampleWidth + self.sampleHorizontalSpace)
            self.tpgHeight = self.stepsPowerPasses * (self.engraveSampleHeight + self.sampleVerticalSpace)
        
        #write the  top header
        self.gtw.fontConfig(self.topHeaderFontWidth, self.topHeaderFontHeight,space = self.topHeaderFontWidth / 2, feedRate = 1000, power = 150)
        if(self.mode == "cut"):
            self.gtw.printGcode(0,self.tpgHeight + self.powerFeedHeaderFontHeight * 1.5 + self.powerFeedValuesFontWidth * 4 * 1.5, self.gtw.ORIENTATION_HORIZONTAL,"CUTTING TEST")
        else:
            self.gtw.printGcode(0,self.tpgHeight + self.powerFeedHeaderFontHeight * 1.5 + self.powerFeedValuesFontWidth * 4 * 1.5, self.gtw.ORIENTATION_HORIZONTAL,"ENGRAVING TEST")

        
        #config font for power and feed headers
        self.gtw.fontConfig(self.powerFeedHeaderFontWidth, self.powerFeedHeaderFontHeight,self.powerFeedHeaderFontWidth/2,feedRate = 1000,power = 150)
        
        #write the feed speed header
        self.gtw.printGcode(self.powerFeedHeaderFontHeight * 1.5 + self.powerFeedValuesFontWidth * 3 * 1.5,self.tpgHeight + self.powerFeedValuesFontWidth * 4 * 1.5, self.gtw.ORIENTATION_HORIZONTAL,"FEED [MM/MIN]")

        #write the power header
        if(self.mode == "cut"):
            self.gtw.printGcode(self.powerFeedHeaderFontHeight, 0, self.gtw.ORIENTATION_VERTICAL,"PASSES [P=" + str(self.LineResolutionCutPower)+"]")
        else:
            self.gtw.printGcode(self.powerFeedHeaderFontHeight, 0, self.gtw.ORIENTATION_VERTICAL,"POWER")

        #config font for power and feed values
        self.gtw.fontConfig(self.powerFeedValuesFontWidth, self.powerFeedValuesFontHeight,self.powerFeedValuesFontWidth/2, feedRate = 1000, power = 150)
        
        #write the feed values
        if self.mode == "cut":
            x = self.powerFeedHeaderFontHeight * 1.5 + 3 * self.powerFeedValuesFontWidth * 1.5 + self.cutSampleWidth
        else:
            x = self.powerFeedHeaderFontHeight * 1.5 + 3 * self.powerFeedValuesFontWidth * 1.5 + self.engraveSampleWidth
        y = self.tpgHeight
        for feed in self.feedSetpoints:
            self.gtw.printGcode(x, y, self.gtw.ORIENTATION_VERTICAL, str(round(feed,2)))
            if self.mode == "cut":
                x = x + self.cutSampleWidth + self.sampleHorizontalSpace
            else:
                x = x + self.engraveSampleWidth + self.sampleHorizontalSpace

        #write the power values
        x = self.powerFeedHeaderFontHeight * 1.5
        if self.mode == "cut":
            y = self.tpgHeight - self.cutSampleHeight - self.sampleVerticalSpace
        else:
            y = self.tpgHeight - self.engraveSampleHeight - self.sampleVerticalSpace
        for power in self.powerSetpoints:
            self.gtw.printGcode(x, y, self.gtw.ORIENTATION_HORIZONTAL,str(round(power,2)))
            if self.mode == "cut":
                y = y - self.cutSampleHeight - self.sampleVerticalSpace
            else:
                y = y - self.engraveSampleHeight - self.sampleVerticalSpace

    def drawTestBox(self, mode, x, y, feed, powerPasses):
        print("G0 X"+str(x)+" Y"+str(y))
        if self.mode == "cut":
            print(";cut box x=" + str(x) + " y=" + str(y) + " feed="+str(feed) + " power= " + str(LineResolutionCutPower) + "passes= " + str(powerPasses))    
            for i in range(powerPasses):
                print("G1 S" + str(LineResolutionCutPower) + " F" + str(feed) + " X" + str(x)+" Y" + str(y + self.cutSampleHeight))
                print("G1 S" + str(LineResolutionCutPower) + " F" + str(feed) + " X" + str(x + self.cutSampleWidth) + " Y" + str(y + self.cutSampleHeight))
                print("G1 S" + str(LineResolutionCutPower) + " F" + str(feed) + " X" + str(x + self.cutSampleWidth) + " Y" + str(y))
                print("G1 S" + str(LineResolutionCutPower) + " F" + str(feed) + " X" + str(x) + " Y" + str(y))

        else:
            print(";engrave box x=" + str(x) + " y=" + str(y) + " feed="+str(feed) + " power=" + str(powerPasses))
            currentY = y
            for verticalStep in range(self.engraveSampleHeight * self.LineResolutionCutPower):
                print("G1 S" + str(powerPasses) + " F" + str(feed) + " X" + str(x + self.engraveSampleWidth)+" Y" + str(currentY))
                currentY = y + verticalStep / self.LineResolutionCutPower
                print("G0 X" + str(x)+" Y" + str(currentY))

    def fillupTestBoxes(self):
        #fillup the test boxes
        x = self.powerFeedHeaderFontHeight * 1.5 + 3 * self.powerFeedValuesFontWidth * 1.5
        if self.mode == "cut":
            y = self.tpgHeight - self.cutSampleHeight - self.sampleVerticalSpace
        else:
            y = self.tpgHeight - self.engraveSampleHeight - self.sampleVerticalSpace
        for power in self.powerSetpoints:    
            for feed in self.feedSetpoints:
                self.drawTestBox(mode,x,y,feed,power)
                if self.mode == "cut":
                    x = x + self.cutSampleWidth + self.sampleHorizontalSpace
                else:
                    x = x + self.engraveSampleWidth + self.sampleHorizontalSpace
            x = self.powerFeedHeaderFontHeight * 1.5 + 3 * self.powerFeedValuesFontWidth * 1.5
            if self.mode == "cut":
                y = y - self.cutSampleHeight - self.sampleVerticalSpace
            else:
                y = y - self.engraveSampleHeight - self.sampleVerticalSpace

    def buildTestPattern(self):
        error = self.validateParameters()
        if error != self.OK:
            return error

        #prepare the power setpoints list
        self.powerSetpoints = []
        for powerStep in range(self.stepsPowerPasses - 1):
            self.powerSetpoints.append(round(self.minPowerPasses + powerStep * (self.maxPowerPasses - self.minPowerPasses) / (self.stepsPowerPasses - 1)))
        self.powerSetpoints.append(round(self.maxPowerPasses))
        
        #prepare the feed  setpoints list
        self.feedSetpoints = []
        for feedStep in range(self.stepsFeed - 1):
            self.feedSetpoints.append(round(self.minFeed + feedStep * (self.maxFeed - self.minFeed) / (self.stepsFeed - 1)))
        self.feedSetpoints.append(round(self.maxFeed))
        
        #generate the test pattern        
        self.startGcode()
        self.createHeaders()
        self.fillupTestBoxes()
        self.endGcode()

        
def printHelp():
    print()
    print()
    print("laserTestPatternGenerator Cut/Engrave minPasses/minPower maxPasses/maxPower stepsPasses/stepsPower minFeed maxFeed stepsFeed [LineResolutionCutPower=10 / cutPower = 100]")
    print("CUT syntax: laserTestPatternGenerator Cut minPasses maxPasses stepsPasses minFeed maxFeed stepsFeed [cutPower = 100]")
    print("Engrave syntax: laserTestPatternGenerator Engrave minPower maxPower stepsPower minFeed maxFeed stepsFeed [LineResolutionCutPower = 10]")
    print()
    
if __name__ == "__main__":
    #check command line variables
    if len(sys.argv) < 8:
        print("Error in command line parameter!")
        printHelp()
        sys.exit()

    if ((sys.argv[1]).lower() != "cut") and ((sys.argv[1]).lower() != "engrave"):
        print("Error in command line parameter!")
        printHelp()
        sys.exit()

    try:
        mode = sys.argv[1]
        minPowerPasses = int(sys.argv[2])
        maxPowerPasses = int(sys.argv[3])
        stepsPowerPasses = int(sys.argv[4])
        minFeed = int(sys.argv[5])
        maxFeed = int(sys.argv[6])
        stepsFeed = int(sys.argv[7])
        if len(sys.argv) == 9:
            LineResolutionCutPower = int(sys.argv[8])
    except:
        print("Error in command line parameter!")
        printHelp()
        sys.exit()
        
    #instantiate laserTestPatternGenerator class
    if len(sys.argv) == 9:
        gtpg = laserTestPatternGenerator(mode,minPowerPasses, maxPowerPasses, stepsPowerPasses, minFeed, maxFeed, stepsFeed, LineResolutionCutPower)
    else:
        gtpg = laserTestPatternGenerator(mode,minPowerPasses, maxPowerPasses, stepsPowerPasses, minFeed, maxFeed, stepsFeed)
    #gtpg.setSampleConfiguration(5,5,5,5,10) #optional command to change the default configuration of the sample
    error = gtpg.buildTestPattern()
    if error != gtpg.OK:
        printHelp()


