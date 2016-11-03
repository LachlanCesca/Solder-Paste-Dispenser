from ScreenDrawer import *

def standardApertureVarietyTest():
    SD = ScreenDrawer(250,250)
    scaling = 100

    ap = StandardApertureObject('%ADD22R,0.75X0.5*%',False)
    SD.drawRect((-2,2),ap.x_size,ap.y_size,scaling,None)
    ap = StandardApertureObject('%ADD22R,0.75X0.5X0.4*%',False)
    SD.drawRect((-2,1),ap.x_size,ap.y_size,scaling,ap.hole_diameter)


    ap = StandardApertureObject('%ADD10C,0.5*%',False)
    SD.drawCircle((0,2),ap.diameter,scaling,None)
    ap = StandardApertureObject('%ADD10C,0.5X0.25*%',False)
    SD.drawCircle((0,1),ap.diameter,scaling,ap.hole_diameter)

    ap = StandardApertureObject('%ADD22O,0.75X0.5*%',False)
    SD.drawObround((2,2),ap.x_size,ap.y_size,scaling,None)
    ap = StandardApertureObject('%ADD22O,0.75X0.5X0.3*%',False)
    SD.drawObround((2,1),ap.x_size,ap.y_size,scaling,ap.hole_diameter)

    for i in range(3,8):
        ap = StandardApertureObject('%ADD17P,.5X8*%',False)
        SD.drawPolygon((-5+i,-0.5),ap.outer_diameter,i,scaling,0,None)
        ap = StandardApertureObject('%ADD17P,.5X8X0.0X0.2*%',False)
        SD.drawPolygon((-5+i,-1.5),ap.outer_diameter,i,scaling,0,ap.hole_diameter)

    SD.exitTurtle()

def drawCustomAperture(self,coord,ap,scaling):
        num_primitives = ap.num_primitives
        #print num_primitives
        for i in range(num_primitives):
            current_primitive = ap.primitives_list[i]
            shape = current_primitive[0]
            print shape
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
                points = current_primitive[3]
                rotation = current_primitive[4]
                self.drawCustomPolygon(coord,points,scaling,rotation,coord)

def customApertureTesting():
    SD = ScreenDrawer(250,250)
    scaling = 100


    string1 = '''%AMROTATEDRECTD24*
4,1,4,-0.00070,-0.02018,-0.02018,-0.00070,0.00070,0.02018,0.02018,0.00070,-0.00070,-0.02018,0.0*
%'''
    string2 = '''%AMOVALD25*
21,1,0.04528,0.01181,0.00000,0.00000,315.0*
1,1,0.01181,-0.01601,0.01601*
1,1,0.01181,0.01601,-0.01601*
%'''

    string3 = '''%AMOVALD26*
21,1,0.04528,0.01181,0.00000,0.00000,45.0*
1,1,0.01181,-0.01601,-0.01601*
1,1,0.01181,0.01601,0.01601*
%'''
    CAP = CustomApertureObject(string3,True)
    drawCustomAperture(SD,(0,0),CAP,scaling)
    #drawCustomAperture(SD,(0,1),CAP,scaling)

    SD.exitTurtle()





if __name__ == "__main__":
    customApertureTesting()
