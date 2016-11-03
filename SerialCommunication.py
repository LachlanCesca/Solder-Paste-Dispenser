import serial, time, re
from GerberParsing import *
from ImageGerberDrawer import *

class SerialCommunication:
    def __init__(self,comPort):
        self.ser = serial.Serial()
        self.ser.port = comPort
        self.ser.baudrate = 9600
        self.ser.timeout=0
        self.ser.parity = serial.PARITY_NONE
        self.ser.stopbits = serial.STOPBITS_ONE
        self.ser.bytesize = serial.EIGHTBITS
        self.ser.rtscts = True

        self.scaling = 192

        self.offset = None

        self.openCommunications()
        self.echo()
        self.setSpeed()
        #85,768 and 77,264
        xMax = 85000
        yMax = 77000
        self.sendCommand("IW0,0,"+str(xMax)+","+str(yMax))



    def openCommunications(self):
        try:
            self.ser.open()
        except Exception, e:
            print "Error open serial port " + str(e)
            exit()

        if self.ser.isOpen():
            print "Communications Opened!"
            try:
                self.ser.flushInput()
                self.ser.flushOutput()
                time.sleep(1)
            except Exception, e1:
                print "Error Communicating...: " + str(e1)

        #self.sendCommand("IN")

    def closeConnection(self):
        self.sendCommand("!CB")
        self.ser.close()

    def sendCommand(self,command):
        #print command
        #time.sleep(0.5)
        self.ser.write(command+";")
        #print self.readSerial()

    def readSerial(self):
        time.sleep(1)
        response = self.ser.readline()
        return response

    def echo(self):
        self.sendCommand("!CT1")


    def setSpeed(self,speed=None):
        max = 80000
        if speed is None:
            self.sendCommand("!VU"+str(max))
        elif(speed < max and speed > 0):
            self.sendCommand("!VU"+str(speed))

    def gotoCoordinate(self,x,y,x_flip=None):
        if(self.offset is None):
            self.sendCommand("PA"+str(x)+","+str(y))
        else:
            new_x = int(x_flip - int(x))*self.scaling + self.offset[0]
            new_y = (int(y))*self.scaling + self.offset[1]

            # Swap X and Y due to machines reference points
            self.sendCommand("PA"+str(new_y)+","+str(new_x))



if __name__ == '__main__':
    ser = SerialCommunication("COM3")
    ser.sendCommand("PU")

    
    fileName = "Solder Paste Files/QUTid-P01-V00R00-CardHolder.GTP"
    #GD = GerberDrawer(fileName)
    GP = GerberParser(fileName)

    exit_flag = False

    while(exit_flag is False):
        _response = raw_input("Offset: ")
        if(_response == 'exit'):
            exit_flag = True
            break
        m = re.search('([\d]*),([\d]*)',_response)
        x_offset = int(m.group(1))
        y_offset = int(m.group(2))
        ser.offset = (x_offset,y_offset)
        ser.gotoCoordinate(GP.coords[0][0],GP.coords[0][1],GP.max[0])
        


    for coord in GP.coords:
        x = coord[0]
        y = coord[1]
        
        ser.gotoCoordinate(x,y,GP.max[0])
        #ser.sendCommand("PD")
        #ser.sendCommand("PU")

    ser.closeConnection()
