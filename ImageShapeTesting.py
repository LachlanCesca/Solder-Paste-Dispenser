from ImageDrawer import *

def standardApertureVarietyTest():   
    scaling = 100
    SD = ImageDrawer(25,25,scaling)
    
    ap = StandardApertureObject('%ADD22R,0.75X0.5*%',False)
    SD.drawRect((5,5),ap.x_size,ap.y_size,None)
    ap = StandardApertureObject('%ADD22R,0.75X0.5X0.4*%',False)
    SD.drawRect((10,5),ap.x_size,ap.y_size,ap.hole_diameter)


    ap = StandardApertureObject('%ADD10C,0.5*%',False)
    SD.drawCircle((5,10),ap.diameter,None)
    ap = StandardApertureObject('%ADD10C,0.5X0.25*%',False)
    SD.drawCircle((10,10),ap.diameter,None)

    ap = StandardApertureObject('%ADD22O,0.75X0.5*%',False)
    SD.drawObround((5,15),ap.x_size,ap.y_size,None)
    ap = StandardApertureObject('%ADD22O,0.75X0.5X0.3*%',False)
    SD.drawObround((10,15),ap.y_size,ap.x_size,None)

    for i in range(3,8):
        ap = StandardApertureObject('%ADD17P,.5X8*%',False)
        SD.drawPolygon((i*3,20),ap.outer_diameter,i,0,None)

    SD.saveImage()
 

if __name__ == "__main__":
    standardApertureVarietyTest()
