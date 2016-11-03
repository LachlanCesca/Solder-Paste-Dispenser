from ApertureClasses import *

class GerberParser:

    def __init__(self,filePath):
        # Read in gerber file
        self.Gerber = self.readGerber(filePath)

        # Set-up lists for population
        self.d_codes = []
        self.apertureDefinition = []

        # Functions to extract information from Gerber
        self.extractInfo()


    # Simple read file, given filePath
    #TODO: add assertion for GTP filetype?
    def readGerber(self, filePath):
        with open(filePath, 'r') as f:
            lines = f.readlines()
        return lines


    # Some of these require specific order for operation
    # Take care when modifying the order of functions
    def extractInfo(self):
        self.coordinateFormat() #get format for coordinate information
        self.unitInfo() # Whether Gerber is in mm or inch

        # Gets D-codes and aperture definitions for all apertures (Custom & std)
        self.saveCodes()

        self.coords = self.findCoords() # Get list of all coordinates

        # Match up all coordinates with a corresponding aperture
        self.apertureList = self.apertureList()

        # Converts coordinates into mm and applies correct formatting
        self.convertCoords()

        self.findBounds() # Find bounds of PCB (min,max)


    # Get Gerber coordinate format information
    def coordinateFormat(self):
        count = 0
        formatSpec = self.Gerber[count]
        while(formatSpec.find('%FS')==-1):
            count+=1
            formatSpec = self.Gerber[count]

        self.leadingZeros = formatSpec[3] == 'L'
        self.intPlaces = int(formatSpec[formatSpec.find('X')+1])
        self.decPlaces = int(formatSpec[formatSpec.find('X')+2])



    # Get Gerber unit information (mm or inch).
    def unitInfo(self):
        count = 0
        measurement = self.Gerber[count]
        while(measurement.find('%MO')==-1):
            count+=1
            measurement = self.Gerber[count]
        if(measurement.find("MM")==-1): #assumed Inches
           conversionRatio = 25.4
           self.convert = True
        else:
           conversionRatio = 1
           self.convert = False

        self.conversionRatio = conversionRatio



    # Create list of apertures that match up with coordinates
    def apertureList(self):
        apertures = []
        currentAperture = 0
        for line in self.Gerber:
            if(line[0] == 'D'):
                if(line[:-2] != 'D03'):
                    index = self.d_codes.index(line[:-2])
                    currentAperture = self.apertureDefinition[index]
                elif(line[:-2] == 'D03'):
                    apertures.append(currentAperture)
        return apertures


    # Extract all coordinate information
    def findCoords(self):
        coords = []
        for line in self.Gerber:
            f_index = line.find('D02')
            if(f_index!=-1):
                x_index = line.find('X')
                y_index = line.find('Y')

                # If coordinate doesnt have an x or y component, substitute
                # with previous x or y coordinate information.
                if(x_index != -1) and (y_index!=-1):
                    coords.append(((line[x_index+1:y_index]),(line[y_index+1:f_index])))
                elif (y_index != -1):
                    coords.append((coords[-1][0],(line[y_index+1:f_index])))
                else:
                    coords.append(((line[x_index+1:f_index]),coords[-1][1]))

        return coords

    # Applies measurement conversion ratio as well as coordiante formatting to
    # all coordinates
    def convertCoords(self):
        convRatio = self.conversionRatio
        for i in range(len(self.coords)):
            c = self.coords[i] # Get coords in the form they are in

            # Turn string coordinates with leading/trailing zeros to values
            self.coords[i] = (self.convertCoord(c[0])*convRatio
                              ,self.convertCoord(c[1])*convRatio)

    # Formats coordinate based on Gerber formatting information
    def convertCoord(self,strCoord):
        negative = strCoord.startswith('-')
        if(strCoord.startswith('+') or negative):
            strCoord = strCoord[1:]

        while(len(strCoord) < self.intPlaces + self.decPlaces):
            if(self.leadingZeros):
               strCoord = '0'+strCoord
            else:
                strCoord = strCoord+'0'
        strCoord = strCoord[0:self.intPlaces]+'.'+strCoord[self.intPlaces:]
        if(negative):
            strCoord = '-'+strCoord
        return float(strCoord)

    # Find the bounds of the Gerber (min,max)
    def findBounds(self):
        xmin,ymin,xmax,ymax = None,None,None,None

        for coord in self.coords:
            x,y = coord

            if xmin is None:
                xmin, xmax = x, x
                ymin, ymax = y, y
            else:
                if(x > xmax):
                    xmax = x
                if(x < xmin):
                    xmin = x
                if(y> ymax):
                    ymax = y
                if(y<ymin):
                    ymin = y

        self.min = (xmin,ymin)
        self.max = (xmax,ymax)
        self.mid = (((xmin+xmax)/2),((ymin+ymax)/2))
        self.dimensions = ((xmax-xmin),(ymax-ymin))


    # Find and save all aperture definitions and D-codes to respective lists
    # These are only the definitions of the apertures and will need to be
    # matched up with their respective coordinates.
    def saveCodes(self):
        lines = self.Gerber
        for i in range(len(lines)):
            if(isStandardApertureString(lines[i])):
                self.apertureDefinition.append(StandardApertureObject(lines[i],self.convert))
                self.d_codes.append(lines[i][3:(lines[i].find(',')-1)])
            elif(isCustomApertureString(lines[i])):
                apertureString = lines[i]
                j = i+1
                line = lines[j]
                while(line.find('%') == -1):
                    apertureString += line
                    j+=1
                    line = lines[j]
                self.apertureDefinition.append(CustomApertureObject(apertureString,self.convert))
            elif(isCustomDCodeString(lines[i])):
                apertureString = lines[i]
                for j in range(len(apertureString)):
                    if(isNumber(lines[i][4:-j])):
                        d_code = lines[i][3:-j]
                        break
                self.d_codes.append(d_code)






if __name__ == "__main__":
    GP = GerberParser("Solder Paste Files/C2DR-P02-V00R00-CascodeGateDrive.GTP")
    #GP2 = GerberParser("Solder Paste Files/LBCM-P01-V00R00-ControlModule.GTP")
