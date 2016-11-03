from PIL import Image, ImageDraw
from math import *
from ApertureClasses import *

class ImageDrawer:

    def __init__(self,width,height,scaling=None):
        self.width = width
        self.height = height

        self.dark = 'black'
        self.clear = 'white'


        if(scaling is None):
            self.scaling = 10
        else:
            self.scaling = scaling

        self.margin = 10
        screenEdge = 40

        width = self.width*self.scaling+screenEdge
        height = self.height*self.scaling+screenEdge

        self.img = Image.new('RGB',(width,height),self.clear)

        self.draw = ImageDraw.Draw(self.img)



    def saveImage(self,name):
        self.img.save(name+'.png')

    def openImage(self):
        self.img.show()

    def drawDot(self,pos):
        scaling = self.scaling

        x,y = pos
        x = x*scaling
        y = y*scaling

        self.draw.point((x,y),fill=self.dark)


    def drawCircle(self,pos,diameter,rotation=None,anchor=None):
        scaling = self.scaling

        x,y = pos
        x = x*scaling
        y = y*scaling
        r = diameter*scaling/2

        if(anchor is None):
            _anchor = (x,y)
        else:
            _anchor = (anchor[0]*scaling,anchor[1]*scaling)

        if(rotation is not None):
            x,y = rotate_point((x,y),rotation,_anchor)

        self.draw.ellipse((x-r, y-r, x+r, y+r),fill=self.dark)

    def drawRect(self,pos,xsize,ysize,rotation=None,anchor=None):
        scaling = self.scaling
        x,y = pos
        x = x*scaling
        y = y*scaling
        xsize = xsize*scaling
        ysize = ysize*scaling

        #points array
        points = [((x-xsize/2),(y-ysize/2)),
        ((x+xsize/2),(y-ysize/2)),
        ((x+xsize/2),(y+ysize/2)),
        ((x-xsize/2),(y+ysize/2))]

        if(anchor is None):
            _anchor = points[0]
        else:
            _anchor = (anchor[0]*scaling,anchor[1]*scaling)

        if(rotation is not None):
            for i in range(len(points)):
                points[i] = rotate_point(points[i],rotation,_anchor)

        self.draw.polygon(points,fill=self.dark)


    def drawObround(self,pos,xsize,ysize,rotation=None,anchor=None):
        x,y = pos
        if(xsize>ysize):
            #   /--------\
            #  |          |
            #   \--------/
            r = ysize/2

            #points array
            self.drawRect(pos,xsize-r*2,ysize,rotation,anchor)

            circ = [((x-(xsize/2)),y),((x+(xsize/2)),y)]

        else:
            #  /---\
            # |     |
            # |     |
            # |     |
            #  \---/
            r = xsize/2

            #points array
            self.drawRect(pos,xsize,ysize-r*2,rotation,anchor)

            circ= [(x,(y-(ysize/2)+r)),(x,(y+(ysize/2)-r))]


        self.drawCircle(circ[0],r*2,rotation,anchor)
        self.drawCircle(circ[1],r*2,rotation,anchor)

    def drawPolygon(self,pos,diameter,vertices,rotation=None,anchor=None):
        scaling = self.scaling
        # 3 to 12 verticies
        dark = self.dark
        clear = self.clear
        x,y = pos
        x = x*scaling
        y = y*scaling
        diameter = diameter*scaling

        r = diameter/2
        interior_angle = 180*(vertices-2)/vertices
        angle = 180 - interior_angle

        # To minimize number of loops when drawing polygons, the rotation of
        # each point is merged into the creation of the points and therefore
        # the anchor point must be checked/set in in the first iteration of the
        # for loop.

        points = []
        for i in range(vertices):
            # Calculate polygon points
            points.append((x+r*cos(radians(i*angle)),y+r*sin(radians(i*angle))))

            # Set Anchor Point
            if(i == 0):
                if(rotation is not None):
                    if(anchor is None):
                        _anchor = points[0]
                    else:
                        _anchor = (anchor[0]*scaling,anchor[1]*scaling)

            # If a rotation exists, rotate around anchor point
            if(rotation is not None):
                points[i] = rotate_point(points[i],rotation,_anchor)


        self.draw.polygon(points,fill=self.dark)

    def drawCustomPolygon(self,origin,points,rotation=None,anchor=None):
        scaling = self.scaling
        # 3 to 12 verticies
        new_points = [0 for num in points] #init list of length
        # Too many for loops #yolo
        for i in range(len(points)):
            x = (origin[0]+points[i][0])*scaling
            y = (origin[1]+points[i][1])*scaling
            new_points[i] = (x,y)

        # Set Anchor Point
        if(rotation is not None and rotation > 0):
            if(anchor is None):
                _anchor = new_points[0]
            else:
                _anchor = (anchor[0]*scaling,anchor[1]*scaling)


        # To minimize number of loops when drawing polygons, the rotation of
        # each point is merged into the creation of the points and therefore
        # the anchor point must be checked/set in in the first iteration of the
        # for loop.

        # If a rotation exists, rotate around anchor point
        if(rotation is not None and rotation > 0):
            for i in range(len(new_points)):
                new_points[i] = rotate_point(new_points[i],rotation,_anchor)

        self.draw.polygon(new_points,fill=self.dark)




# Used to rotate the points that represent a shape in order to rotate the shape
def rotate_point(point, angle, anchor):
    angle = radians(angle)
    p_x = point[0]
    p_y = point[1]

    # translate point back to origin:
    p_x -= anchor[0];
    p_y -= anchor[1];

    # rotate point
    xnew = p_x * cos(angle) - p_y * sin(angle);
    ynew = p_x * sin(angle) + p_y * cos(angle);

    # translate point back:
    p_x = xnew + anchor[0];
    p_y = ynew + anchor[1];
    return (p_x,p_y);


if __name__ == "__main__":
    ID = ImageDrawer(250,250)
    ID.drawDot((5,5))
    ID.drawCircle((100,100),50)
    ID.saveImage()
