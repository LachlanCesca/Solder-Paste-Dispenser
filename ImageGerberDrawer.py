from PIL import Image, ImageDraw
from math import *
from GerberParsing import *
from ImageDrawer import *
from PastePlacer import *


class GerberDrawer(ImageDrawer):

    def __init__(self,filePath):
        self.GP = GerberParser(filePath)
        self.width = self.GP.max[0]-self.GP.min[0]#self.width = width
        self.height = self.GP.max[1]-self.GP.min[1]#

        #self.dark = 'blue'
        #self.clear = 'white'

        # Use of class green and silver PCB colours
        self.dark = '#ded9d6'
        self.clear = '#0b663c'

        # 1 px = 1/scaling mm
        self.scaling = 100

        # Arbitrary margins for drawing, makes it look cleaner when drawn
        self.margin = (3,3)

        #Account for pad size, as max is measured by centre of last shape
        self.screenEdge = 4

        #Dont know why or how this 30,-30 business works but it does
        self.w = int((self.width+self.screenEdge+self.margin[0])*self.scaling)
        self.h = int((self.height+self.screenEdge+self.margin[1])*self.scaling)


        self.img = Image.new('RGB',(self.w,self.h),self.clear)

        self.draw = ImageDraw.Draw(self.img)


        self.drawPads()

        pitch = 0.01

        self.PP = PastePlacer(pitch,self.GP,self.img,self.draw,
        self.scaling,self.margin)

        #self.placeDots(self.scaling/1,10)
        #self.drawBounding()

        # Image requires transposing to display correctly
        self.img = self.img.transpose(Image.FLIP_TOP_BOTTOM)

        #self.saveImage()




    def markFirstPad(self):
        self.img = self.img.transpose(Image.FLIP_TOP_BOTTOM)
        GP = self.GP
        first_coords = GP.coords[0]
        offset = ((self.margin[0]-GP.min[0]),(self.margin[1]-GP.min[1]))
        first_coords = ((first_coords[0]+offset[0]),(first_coords[1]+offset[1]))
        x = first_coords[0]*self.scaling
        y = first_coords[1]*self.scaling
        r = 50
        draw = ImageDraw.Draw(self.img)
        draw.ellipse((x-r, y-r,x+r, y+r),fill='red')
        self.img = self.img.transpose(Image.FLIP_TOP_BOTTOM)

    # Draw bounding box around each pad
    def drawBounding(self):
        scaling = self.scaling
        GP = self.GP

        offset = ((self.margin[0]-GP.min[0]),(self.margin[1]-GP.min[1]))

        #ToDo: paramter not
        PP = self.PP

        boundingBoxes = PP.boundingBoxes
        for box in boundingBoxes:
            min = box[0]
            min = ((min[0]+offset[0])*scaling,(min[1]+offset[1])*scaling)

            max = box[1]
            max = ((max[0]+offset[0])*scaling,(max[1]+offset[1])*scaling)

            points = [(min[0],min[1]),(max[0],min[1]),
            (max[0],max[1]),(min[0],max[1])]
            self.draw.polygon(points,outline='red')


    # Has since been replaced with PastePlacer class
    def placeDots(self,pitch,r):
        scaling = self.scaling
        pix = self.img.load()


        for i in range(0,int(self.w)):
            for j in range(0,int(self.h)):
                if(i%int(pitch)==0 and j%int(pitch)==0):
                    if(pix[i,j] == (222,217,214)):
                        #print pix[i,j]
                        self.draw.ellipse((i-r, j-r,i+r, j+r),fill='red')
                    else:
                        #self.draw.ellipse((i-r, j-r,i+r, j+r),fill='blue')
                        pass


    def drawPads(self):
        GP = self.GP
        offset = ((self.margin[0]-GP.min[0]),(self.margin[1]-GP.min[1]))
        for i in range(len(GP.apertureList)):
            ap = GP.apertureList[i]
            coord = GP.coords[i]
            coord = ((coord[0]+offset[0]),(coord[1]+offset[1]))
            if(isinstance(ap,StandardApertureObject)):
                shape = ap.apertureId
                #ToDo: Add check for hole (None)
                if(shape == 'C'):
                    self.drawCircle(coord,ap.diameter,None)
                elif(shape == 'R'):
                    self.drawRect(coord,ap.x_size,ap.y_size,None)
                elif(shape == 'O'):
                    self.drawObround(coord,ap.x_size,ap.y_size,None)
                elif(shape == 'P'):
                    self.drawPolygon(coord,ap.outer_diameter,ap.num_vertices,0,None)
            elif(isinstance(ap,CustomApertureObject)):
                #print self.GP.apertureList[i].primitives_list
                self.drawCustomAperture(coord,self.GP.apertureList[i])


    def drawCustomAperture(self,coord,aperture):
        scaling = self.scaling
        num_primitives = aperture.num_primitives
        for i in range(num_primitives):
            current_primitive = aperture.primitives_list[i]
            shape = current_primitive[0]

            exposure = current_primitive[1]
            if(shape == 1): #circle
                diameter = current_primitive[2]
                center = current_primitive[3]
                rotation = current_primitive[4]
                new_pos = (coord[0]+center[0],coord[1]+center[1])
                self.drawCircle(new_pos,diameter,rotation=rotation,
                anchor=coord)
            elif(shape == 21): #rect
                width = current_primitive[2]
                height = current_primitive[3]
                center = current_primitive[4]
                rotation = current_primitive[5]
                new_pos = (coord[0]+center[0],coord[1]+center[1])
                self.drawRect(new_pos,width,height,rotation=rotation,
                anchor=coord)
            elif(shape == 4): #polygon
                point_coords = current_primitive[3]
                rotation = current_primitive[4]
                self.drawCustomPolygon(coord,point_coords,rotation,coord)



if __name__ == "__main__":
    #GD = GerberDrawer("Solder Paste Files/C2DR-P02-V00R00-CascodeGateDrive.GTP")
    #GD = GerberDrawer("Solder Paste Files/QUTid-P01-V00R00-CardHolder.GTP")
    #GD = GerberDrawer("Solder Paste Files/LBCM-P01-V00R00-ControlModule.GTP")

    fileName = "Solder Paste Files/QUTid-P01-V00R00-CardHolder.GTP"
    GD = GerberDrawer(fileName)
    GD.markFirstPad()
    GD.openImage()
