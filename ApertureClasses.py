from math import *
class StandardApertureObject:
    # Identifier for the four standard apertures
    stdApId = ['C','R','O','P'] # Circle, Rectangle, Oval, Polygon

    '''
    Parameters:
        string: the line from the Gerber file thats specifically for aperture
        definition (begins with %ADD)

        convert: boolean that tells whether the aperture measurements need to
        be converted to mm (if in inches)
    '''
    def __init__(self,string,convert):
             assert(string.find('%ADD')!=-1) #Make sure it is an aperture def
             self.convert = convert # Whether units needed to be converted

             # Iterate through potential apertures and see which one matches
             for i in range(len(self.stdApId)):
                 # If aperture id is found in string, will return non -1
                 if(string.find(self.stdApId[i])!=-1):
                     self.apertureId = self.stdApId[i]
                     self.numParams = len(string.split('X'))
                     break

            # Handle the corresponding aperture
             if(self.apertureId == 'C'):
                self.case_C(string)
             elif(self.apertureId == 'R' or self.apertureId == 'O'):
                self.case_OR(string)
             elif(self.apertureId == 'P'):
                 self.case_P(string)


    # Case for circle aperture
    def case_C(self,string):
        if(self.numParams>1):
            self.hole = True
            diameter = float(string[string.find(',')+1:string.find('X')])
            self.diameter = self.convertUnit(diameter)
            hole_diameter = float(string[string.find('X')+1:string.find('*')])
            self.hole_diameter = self.convertUnit(hole_diameter)
        else:
            self.hole = False
            diameter = float(string[string.find(',')+1:string.find('*')])
            self.diameter = self.convertUnit(diameter)

        # Calculate Area
        self.area = pi*((self.diameter/2)*(self.diameter/2))


    # Case for orbround or rectangle, as both have the same parameters
    def case_OR(self,string):
        if(self.numParams>2):
            self.hole = True
            x_size = float(string.split('X')[0][string.find(',')+1:])
            y_size = float(string.split('X')[1])
            hole_diameter = float(string.split('X')[2][:string.split('X')[2].find('*')])

            self.x_size = self.convertUnit(x_size)
            self.y_size = self.convertUnit(y_size)
            self.hole_diameter = self.convertUnit(hole_diameter)

        else:
            self.hole = False
            x_size = float(string.split('X')[0][string.find(',')+1:])
            y_size = float(string.split('X')[1][:string.split('X')[1].find('*')])

            self.x_size = self.convertUnit(x_size)
            self.y_size = self.convertUnit(y_size)

        # Calculate Area
        if(self.apertureId == 'R'):
            self.area = self.x_size*self.y_size
        elif(self.apertureId == 'O'):
            self.area = (self.x_size*self.y_size)
            if(x_size>y_size):
                self.area += pi*pow(((self.y_size)/2),2)
            else:
                self.area += pi*pow(((self.x_size)/2),2)


    # Case for polygon aperture
    def case_P(self,string):
        if(self.numParams>3):
            self.hole = True
            outer_diameter = float(string.split('X')[0][string.find(',')+1:])
            num_vertices = int(string.split('X')[1])
            rotation = float(string.split('X')[2])
            hole_diameter = float(string.split('X')[3][:string.split('X')[3].find('*')])

            self.outer_diameter = self.convertUnit(outer_diameter)
            self.num_vertices = num_vertices
            self.rotation = rotation
            self.hole_diameter = self.convertUnit(hole_diameter)


        elif(self.numParams>2):
            self.hole = False
            outer_diameter = float(string.split('X')[0][string.find(',')+1:])
            num_vertices = int(string.split('X')[1])
            rotation = float(string.split('X')[2][:string.split('X')[2].find('*')])

            self.outer_diameter = self.convertUnit(outer_diameter)
            self.num_vertices = num_vertices
            self.rotation = rotation

        else:
            self.hole = False
            outer_diameter = float(string.split('X')[0][string.find(',')+1:])
            num_vertices = int(string.split('X')[1][:string.split('X')[1].find('*')])

            self.outer_diameter = self.convertUnit(outer_diameter)
            self.num_vertices = num_vertices

        # Calculate Area
        n = self.num_vertices
        r = self.outer_diameter/2
        self.area = 0.5*n*pow(r,2)*sin(2*pi/n)

    # Convert from inches to mm if boolean convert is true
    def convertUnit(self,value):
        if(self.convert):
            return value*25.4
        else:
            return value



class CustomApertureObject:
##  Example of a custom aperture
##    %AMROTATEDRECTD12*
##    4,1,4,0.03889,-0.00354,0.00354,-0.03889,-0.03889,0.00354,-0.00354,0.03889,0.03889,-0.00354,0.0*
##    %
    def __init__(self,string,convert):

             lines = string.split('\n')
             assert(lines[0].find('%AM')!=-1) #Make sure it is an aperture defintion
             self.convert = convert
             self.lines = lines

             #TODO: Might be out of scope but change to encapsulate D-codes
             # greater than 2 digits (find last D in string?)
             self.name = lines[0][3:-4]

             self.num_primitives = self.primitiveCount(lines)
             self.primitives_list = []
             #4,21,1
             for line in lines[1:-1]:
                 self.primitives_list.append(self.primitiveParameters(line))

    def primitiveCount(self,lines):
        count = 0
        for line in lines:
            firstChar = line.split(',')[0]
            if(isNumber(firstChar)):
                count = count+1
        return count

    def primitiveParameters(self,line):
        line = line.split(',')
        primitive = int(line[0])
        exposure = int(line[1])
        #Get rid of asterix at end of line
        line[-1] = line[-1][0:-1]

        if(primitive == 1): #circle
            diameter = self.convertUnit(float(line[2]))
            X = self.convertUnit(float(line[3]))
            Y = self.convertUnit(float(line[4]))
            point = tuple((X,Y))
            if(len(line)>4):
                rotation = float(line[-1])
            p = [primitive,exposure,diameter,point,rotation]
            return p

        if(primitive == 21): #Rectangle
            width = self.convertUnit(float(line[2]))
            height = self.convertUnit(float(line[3]))
            X = self.convertUnit(float(line[4]))
            Y = self.convertUnit(float(line[5]))
            point = tuple((X,Y))
            if(len(line)>5):
                rotation = float(line[-1]) #ToDo fix because rotation is not always needed/included
            return [primitive,exposure,width,height,point,rotation]

        if(primitive == 4): #Polygon
            num_points = int(line[2])
            coordinates = []
            points = line[3:-1]
            for i in range(len(line[3:-1])):
               if(i%2==0):
                   X = self.convertUnit(float(points[i]))
               else:
                   Y = self.convertUnit(float(points[i]))
                   coordinates.append(tuple((X,Y)))
            if(len(line)>(4+2*num_points)):
                rotation = float(line[-1]) #ToDo fix because rotation is not always needed/included
            return [primitive,exposure,num_points,coordinates,rotation]

    # Convert from inches to mm if boolean convert is true
    def convertUnit(self,value):
        if(self.convert):
            return value*25.4
        else:
            return value


## Some basic functions that are used throughout both aperture classes
## (convertUnit was omitted because it makes it neater to not require convert
## boolean as function parameter, this could be done differently however)

def isStandardApertureString(line):
    if(line[:4] == '%ADD' and line.find(',')!=-1):
        return True
    else:
        return False

def isCustomApertureString(line):
    if(line[:3] == '%AM'):
        return True
    else:
        return False

def isCustomDCodeString(line):
    if(line[:4] == '%ADD' and line.find(',')==-1):
        return True
    else:
        return False

def isNumber(string):
    try:
        float(string)
        return True
    except:
        return False
