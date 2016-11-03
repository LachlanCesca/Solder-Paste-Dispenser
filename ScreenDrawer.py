import turtle
from math import *
from ApertureClasses import *


'''
ScreenDrawer and subclass GerberDrawer are both deprecated.
These classes use turtle graphics library which has since been swapped out for
image maniuplation.

Refer to: ImageDrawer and ImageGerberDrawer
'''
class ScreenDrawer:

    def __init__(self,width,height):
        self.width = width
        self.height = height

        self.dark = 'black'
        self.clear = 'white'

        self.margin = 10
        self.scalingFactor = 10
        screenEdge = 40

        width = self.width*self.scalingFactor+screenEdge
        height = self.height*self.scalingFactor+screenEdge

        turtle.mode('world')
        turtle.bgcolor(self.clear)

        turtle.title("Default Screen")

        self.t = turtle.Turtle()
        self.t.hideturtle()
        self.t.tracer(0,0)
        self.t.speed(10)

        self.t.pencolor(self.dark)



    def exitTurtle(self):
        turtle.exitonclick()


    def drawDot(self,x,y):
        self.t.pu()
        self.t.setpos(x,y)
        self.t.pd()
        self.t.dot()
        self.t.pu()
        turtle.update()



    def drawCircle(self,pos,diameter,scaling,hole_diameter=None,rotation=None,
    anchor=None):
        dark = self.dark
        clear = self.clear

        x,y = pos
        x = x*scaling
        y = y*scaling
        diameter = diameter*scaling

        t = turtle.Turtle()
        t.hideturtle()
        t.tracer(0,0)
        t.speed(10)
        t.pencolor(dark)
        t.fillcolor(dark)


        t.pu()
        circle_center = (x,y-((diameter)/2))

        if(anchor is None):
            anchor = circle_center
        else:
            anchor = (anchor[0]*scaling,anchor[1]*scaling)

        if(rotation is not None):
            circle_center = rotate_point(circle_center,rotation,anchor)

        t.setpos(circle_center)
        t.pd()
        t.begin_fill()
        t.circle((diameter)/2)
        t.end_fill()
        t.pu()

        if(hole_diameter is not None):
            hole_diameter = hole_diameter*scaling
            hole_pos = (x,y-((hole_diameter)/2))
            if(rotation is not None):
                hole_pos = rotate_point(hole_pos,rotation,anchor)
            t.setpos(hole_pos)
            t.fillcolor(clear)
            t.begin_fill()
            t.circle((hole_diameter)/2)
            t.end_fill()



    def drawRect(self,pos,xsize,ysize,scaling,hole_diameter=None,rotation=None,
    anchor=None):
        dark = self.dark
        clear = self.clear

        x,y = pos
        x = x*scaling
        y = y*scaling
        xsize = xsize*scaling
        ysize = ysize*scaling

        t = turtle.Turtle()
        t.hideturtle()
        t.tracer(0,0)
        t.speed(10)
        t.pencolor(dark)
        t.fillcolor(dark)

        #points array
        points = [((x-xsize/2),(y-ysize/2)),
        ((x+xsize/2),(y-ysize/2)),
        ((x+xsize/2),(y+ysize/2)),
        ((x-xsize/2),(y+ysize/2))]

        if(anchor is None):
            anchor = points[0]
        else:
            anchor = (anchor[0]*scaling,anchor[1]*scaling)

        if(rotation is not None):
            for i in range(len(points)):
                points[i] = rotate_point(points[i],rotation,anchor)

        t.pu()
        t.setpos(points[0]) #origin
        t.pd()
        t.begin_fill()
        t.setpos(points[1]) #pt1
        t.setpos(points[2]) #pt2
        t.setpos(points[3]) #pt3
        t.setpos(points[0]) #origin

        t.end_fill()
        t.pu()

        if(hole_diameter is not None):
            hole_diameter = hole_diameter*scaling
            hole_pos = (x,y-((hole_diameter)/2))
            if(rotation is not None):
                hole_pos = rotate_point(hole_pos,rotation,anchor)
            t.setpos(hole_pos)
            t.fillcolor(clear)
            t.begin_fill()
            t.circle((hole_diameter)/2)
            t.end_fill()



    def drawObround(self,pos,xsize,ysize,scaling,hole_diameter=None,rotation=None,
    anchor=None):
        dark = self.dark
        clear = self.clear

        x,y = pos
        x = x*scaling
        y = y*scaling
        xsize = xsize*scaling
        ysize = ysize*scaling

        t = turtle.Turtle()
        t.hideturtle()
        t.tracer(0,0)
        t.speed(10)
        t.pencolor(dark)
        t.fillcolor(dark)

        t.pu()

        if(xsize>ysize):
            #   /--------\
            #  |          |
            #   \--------/
            r = ysize/2

            #points array
            points = [((x-(xsize/2)+r),(y-ysize/2)),
            ((x+(xsize/2)-r),(y-ysize/2)),
            ((x-(xsize/2)+r),(y+ysize/2))]


        else:
            #  /---\
            # |     |
            # |     |
            # |     |
            #  \---/
            r = xsize/2

            #points array
            points = [((x-(xsize/2)),(y+(ysize/2)-r)),
            ((x-(xsize/2)),(y-(ysize/2)+r)),
            ((x+(xsize/2)),(y+(ysize/2)-r))]

        # Rotate points

        if(anchor is None):
            anchor = points[0]
        else:
            anchor = (anchor[0]*scaling,anchor[1]*scaling)

        if(rotation is not None):
            for i in range(len(points)):
                points[i] = rotate_point(points[i],rotation,anchor)

        t.setpos(points[0])
        t.begin_fill()
        t.pd()
        t.setpos(points[1])
        if(not (xsize>ysize)):
            t.setheading(270)
        t.circle(r,180)
        t.setpos(points[2])
        t.circle(r,180)

        t.end_fill()
        t.pu()

        if(hole_diameter is not None):
            hole_diameter = hole_diameter*scaling
            hole_pos = (x,y-((hole_diameter)/2))
            if(rotation is not None):
                hole_pos = rotate_point(hole_pos,rotation,anchor)
            t.setpos(hole_pos)
            t.fillcolor(clear)
            t.begin_fill()
            t.circle((hole_diameter)/2)
            t.end_fill()


    def drawPolygon(self,pos,diameter,vertices,scaling,
    rotation=None,hole_diameter=None,anchor=None):
        # 3 to 12 verticies
        dark = self.dark
        clear = self.clear
        x,y = pos
        x = x*scaling
        y = y*scaling
        diameter = diameter*scaling

        t = turtle.Turtle()
        t.hideturtle()
        t.tracer(0,0)
        t.speed(10)
        t.pencolor(dark)
        t.fillcolor(dark)

        r = diameter/2
        interior_angle = 180*(vertices-2)/vertices
        angle = 180 - interior_angle



        # To minimize number of loops when drawing polygons, the rotation of
        # each point is merged into the creation of the points and therefore
        # the anchor point must be checked/set in in the first iteration of the
        # for loop.

        points = []
        for i in range(vertices+1):
            # Calculate polygon points
            points.append((x+r*cos(radians(i*angle)),y+r*sin(radians(i*angle))))

            # Set Anchor Point
            if(i == 0):
                if(rotation is not None):
                    if(anchor is None):
                        anchor = points[0]
                    else:
                        anchor = (anchor[0]*scaling,anchor[1]*scaling)

            # If a rotation exists, rotate around anchor point
            if(rotation is not None):
                points[i] = rotate_point(points[i],rotation,anchor)


        t.pu()
        t.setpos(points[0])
        t.pd()
        t.begin_fill()

        for i in range(vertices+1):
            t.setpos(points[i])

        t.end_fill()
        t.pu()

        if(hole_diameter is not None):
            hole_diameter = hole_diameter*scaling
            hole_pos = (x,y-((hole_diameter)/2))
            if(rotation is not None):
                hole_pos = rotate_point(hole_pos,rotation,anchor)
            t.setpos(hole_pos)
            t.fillcolor(clear)
            t.begin_fill()
            t.circle((hole_diameter)/2)
            t.end_fill()

    def drawCustomPolygon(self,origin,points,scaling,rotation=None,
    anchor=None):
        # 3 to 12 verticies
        dark = self.dark
        clear = self.clear
        t = turtle.Turtle()
        t.hideturtle()
        t.tracer(0,0)
        t.speed(10)
        t.pencolor(dark)
        t.fillcolor(dark)
        new_points = [0 for num in points] #init list of length
        # Too many for loops #yolo
        for i in range(len(points)):
            x = (origin[0]+points[i][0])*scaling
            y = (origin[1]+points[i][1])*scaling
            new_points[i] = (x,y)

        # Set Anchor Point
        if(rotation is not None and rotation > 0):
            if(anchor is None):
                anchor = new_points[0]
            else:
                anchor = (anchor[0]*scaling,anchor[1]*scaling)


        # To minimize number of loops when drawing polygons, the rotation of
        # each point is merged into the creation of the points and therefore
        # the anchor point must be checked/set in in the first iteration of the
        # for loop.

        # If a rotation exists, rotate around anchor point
        if(rotation is not None and rotation > 0):
            for i in range(len(new_points)):
                new_points[i] = rotate_point(new_points[i],rotation,anchor)


        t.pu()
        t.setpos(new_points[0])
        t.pd()
        t.begin_fill()

        for i in range(len(new_points)):
            t.setpos(new_points[i])

        #t.setpos(new_points[0])
        t.end_fill()
        t.pu()


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
    SD = ScreenDrawer(250,250)
    scaling = 100

    SD.exitTurtle()
