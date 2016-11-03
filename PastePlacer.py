from ApertureClasses import *
from GerberParsing import *
from math import *

class PastePlacer:

    def __init__(self,pitch,GP,img,draw,scaling,margin):

        self.img = img
        self.draw = draw
        self.pix = self.img.load()
        self.scaling = scaling

        self.pitch = pitch
        self.GP = GP
        self.margin = margin
        self.coords = self.GP.coords
        self.apertureList = self.GP.apertureList
        self.boundingBoxes = []

        for i in range(len(self.apertureList)):
            coord = self.coords[i]
            ap = self.apertureList[i]
            self.boundingBoxes.append(self.getBoundingBox(ap,coord))

        #self.dotPlacementMethod1(self.scaling/1,8)
        #self.dotPlacementMethod2(self.scaling/2,8)

    def dotPlacementMethod2(self, pitch, r):
        scaling = self.scaling
        GP = self.GP
        offset = ((self.margin[0]-GP.min[0]),(self.margin[1]-GP.min[1]))

        for box in self.boundingBoxes:
            min, max = box

            min_x = int((min[0]+offset[0])*scaling)
            min_y = int((min[1]+offset[1])*scaling)

            max_x = int((max[0]+offset[0])*scaling)
            max_y = int((max[1]+offset[1])*scaling)


            x_range = [i for i in range(min_x, max_x, pitch)]
            y_range = [j for j in range(min_y, max_y, pitch)]

            for i in x_range:
                for j in y_range:
                    if(self.pix[i,j] == (222,217,214)):
                        self.draw.ellipse((i-r, j-r,i+r, j+r),fill='red')

    def dotPlacementMethod1(self,pitch,r):
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


    def getBoundingBox(self,ap,coord):
        if(isinstance(ap,StandardApertureObject)):
            shape = ap.apertureId
            if(shape == 'R' or shape == 'O'):
                return self.rectangleBoundingBox(coord,ap.x_size,ap.y_size)
            elif(shape == 'C' or shape == 'P'):
                if(shape == 'P'):
                    diameter = ap.outer_diameter
                else:
                    diameter = ap.diameter

                return self.circleBoundingBox(coord,diameter)

        elif(isinstance(ap,CustomApertureObject)):
            return self.customBoundingBox(ap,coord)


    def customBoundingBox(self,ap,coord):

        min_x = float('Inf')
        min_y = float('Inf')

        max_x = -float('Inf')
        max_y = -float('Inf')


        num_primitives = ap.num_primitives
        for i in range(num_primitives):
            current_primitive = ap.primitives_list[i]
            shape = current_primitive[0]
            if(shape == 1): #circle
                diameter = current_primitive[2]
                center = current_primitive[3]
                rotation = current_primitive[4]
                new_pos = (coord[0]+center[0],coord[1]+center[1])

                min,max = self.circleBoundingBox(new_pos,diameter)

            elif(shape == 21): #rect
                width = current_primitive[2]
                height = current_primitive[3]
                center = current_primitive[4]
                rotation = current_primitive[5]
                new_pos = (coord[0]+center[0],coord[1]+center[1])

                min,max = self.rectangleBoundingBox(new_pos,width,height)

            elif(shape == 4): #polygon
                point_coords = current_primitive[3]
                rotation = current_primitive[4]

                new_points = [0 for num in point_coords] #init list of length
                for i in range(len(point_coords)):
                    x = (coord[0]+point_coords[i][0])
                    y = (coord[1]+point_coords[i][1])
                    new_points[i] = (x,y)

                min,max = self.polygonBoundingBox(new_points)

            x1,y1 = min
            x2,y2 = max

            if(x1<min_x):
                min_x = x1
            if(x2>max_x):
                max_x = x2
            if(y1<min_y):
                min_y = y1
            if(y2>max_y):
                max_y = y2

        return ((min_x,min_y),(max_x,max_y))


    def polygonBoundingBox(self,points):
        min_x, min_y  = points[0]
        max_x, max_y = points[0]

        for point in points:
            x,y = point
            if(x<min_x):
                min_x = x
            if(x>max_x):
                max_x = x
            if(y<min_y):
                min_y = y
            if(y>max_y):
                max_y = y
        return ((min_x,min_y),(max_x,max_y))


    def rectangleBoundingBox(self,centre_pos,xsize,ysize):
        x,y = centre_pos

        min_x = x-xsize/2
        min_y = y-ysize/2

        max_x = x+xsize/2
        max_y = y+ysize/2

        return ((min_x,min_y),(max_x,max_y))

    def circleBoundingBox(self,centre_pos,diameter):
        x,y = centre_pos
        r = diameter/2

        min_x = x-r
        min_y = y-r

        max_x = x+r
        max_y = y+r

        return ((min_x,min_y),(max_x,max_y))

if __name__ == "__main__":
    #GD = GerberDrawer("Solder Paste Files/C2DR-P02-V00R00-CascodeGateDrive.GTP")
    #GD = GerberDrawer("Solder Paste Files/QUTid-P01-V00R00-CardHolder.GTP")
    GP = GerberParser("Solder Paste Files/LBCM-P01-V00R00-ControlModule.GTP")

    PP = PastePlacer(1,GP)
