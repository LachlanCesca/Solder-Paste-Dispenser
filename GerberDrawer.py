import turtle
from math import *
from GerberParsing import *
from ScreenDrawer import *

'''
Subclass of ScreenDrawer, both this class and super class are deprecated.
These classes use turtle graphics library which has since been swapped out for
image maniuplation.

Refer to: ImageDrawer and ImageGerberDrawer
'''
class GerberDrawer(ScreenDrawer):

    def __init__(self,filePath):
        self.GP = GerberParser(filePath)
        self.width = self.GP.max[0]-self.GP.min[0]#self.width = width
        self.height = self.GP.max[1]-self.GP.min[1]#

        #self.dark = 'blue'
        #self.clear = 'white'

        # Classis green and silver PCB colours
        self.dark = '#ded9d6'
        self.clear = '#0b663c'

        self.margin = 10
        self.scalingFactor = 10
        screenEdge = 40

        #Dont know why or how this 30,-30 business works but it does
        width = self.width*self.scalingFactor+screenEdge
        height = self.height*self.scalingFactor+screenEdge
        turtle.setup(width,height,0,0)
        turtle.setworldcoordinates(-screenEdge,-screenEdge,width,height)
        turtle.mode('world')
        turtle.bgcolor(self.clear)

        turtle.title(filePath)

        self.t = turtle.Turtle()
        self.t.hideturtle()
        self.t.tracer(0,0)
        self.t.speed(10)
        #self.drawBounds()
        self.t.pencolor(self.dark)

        #self.drawPadCenters()
        self.drawPads()

        turtle.exitonclick()


    def drawPads(self):
        GP = self.GP
        scaling = self.scalingFactor
        offset = GP.min
        for i in range(len(GP.apertureList)):
            ap = GP.apertureList[i]
            coord = GP.coords[i]
            coord = ((coord[0]-offset[0]),(coord[1]-offset[1]))
            if(isinstance(ap,StandardApertureObject)):
                shape = ap.apertureId
                #ToDo: Add check for hole (None)
                if(shape == 'C'):
                    self.drawCircle(coord,ap.diameter,scaling,None)
                elif(shape == 'R'):
                    self.drawRect(coord,ap.x_size,ap.y_size,scaling,None)
                elif(shape == 'O'):
                    self.drawObround(coord,ap.x_size,ap.y_size,scaling,None)
                elif(shape == 'P'):
                    self.drawPolygon(coord,ap.outer_diameter,ap.num_vertices,scaling,0,None)
            elif(isinstance(ap,CustomApertureObject)):
                #print self.GP.apertureList[i].primitives_list
                self.drawCustomAperture(coord,self.GP.apertureList[i],scaling)


    def drawCustomAperture(self,coord,aperture,scaling):
        num_primitives = aperture.num_primitives
        for i in range(num_primitives):
            current_primitive = aperture.primitives_list[i]
            shape = current_primitive[0]

            exposure = current_primitive[1]
            if(shape == 1):
                diameter = current_primitive[2]
                center = current_primitive[3]
                rotation = current_primitive[4]
                new_pos = (coord[0]+center[0],coord[1]+center[1])
                self.drawCircle(new_pos,diameter,scaling,rotation=rotation,
                anchor=coord)
            elif(shape == 21):
                width = current_primitive[2]
                height = current_primitive[3]
                center = current_primitive[4]
                rotation = current_primitive[5]
                new_pos = (coord[0]+center[0],coord[1]+center[1])
                self.drawRect(new_pos,width,height,scaling,rotation=rotation,
                anchor=coord)
            elif(shape == 4):
                point_coords = current_primitive[3]
                rotation = current_primitive[4]
                self.drawCustomPolygon(coord,point_coords,scaling,rotation,coord)



    def drawPadCenters(self):
        scaling = self.scalingFactor
        offset = self.GP.min
        for coord in self.GP.coords:
            self.drawDot((coord[0]-offset[0])*scaling,(coord[1]-offset[1])*scaling)



    def drawBounds(self):
        margin = self.margin
        scaling = self.scalingFactor
        self.t.pu()
        self.t.setpos(-margin,-margin)
        self.t.pd()
        self.t.setpos(self.width*scaling+margin,-margin)
        self.t.setpos(self.width*scaling+margin,self.height*scaling+margin)
        self.t.setpos(-margin,self.height*scaling+margin)
        self.t.setpos(-margin,-margin)
        self.t.pu()



if __name__ == "__main__":
    GD = GerberDrawer("Solder Paste Files/C2DR-P02-V00R00-CascodeGateDrive.GTP")
    GD = GerberDrawer("Solder Paste Files/QUTid-P01-V00R00-CardHolder.GTP")
    GD = GerberDrawer("Solder Paste Files/LBCM-P01-V00R00-ControlModule.GTP")

    #turtle.update()
    #turtle.exitonclick()
