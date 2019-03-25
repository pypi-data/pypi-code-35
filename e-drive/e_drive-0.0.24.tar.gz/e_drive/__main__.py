import sys
from e_drive.update import *
from e_drive.cards import CardsReaderGUI


# CommandParser Start


class CommandParser():

    def __init__(self):

        self.program_name   = None
        self.arguments      = None
        self.count          = 0

        self.flagRawCardShowRange   = False


    def run(self):
        
        self.program_name   = sys.argv[0]
        self.arguments      = sys.argv[1:]
        self.count          = len(self.arguments)

        colorama.init()

        if (self.count > 0) and (self.arguments != None):

            print("Count:{0} ".format(self.count) , end='')

            for arg in self.arguments:
                print("/ {0} ".format(arg), end='')

            print("")

            # >python -m e_drive upgrade
            # >python -m e_drive update
            if      (self.arguments[0] == "upgrade") or (self.arguments[0] == "update"):
                updater = Updater()
                updater.update()
                return

            # >python -m e_drive request State 10 0.2
            elif    ((self.count == 4) and 
                    (self.arguments[0] == "request") and
                    (self.arguments[1] == "State")):         # time interval
                #print("* State - Ready     Blue    Red     Black   Black   None_             1830   1631   2230     76")    
                print ("         |Mode     |Color                          |Card           |IR           |Bright|Battery|")
                print ("         |Drive    |Front  |Rear   |Left   |Right  |               | Front|  Rear|ness  |       |")
                self.request(DataType.State, int(self.arguments[2]), float(self.arguments[3]))
                return

            # >python -m e_drive request Motion 10 0.2
            elif    ((self.count == 4) and 
                    (self.arguments[0] == "request") and
                    (self.arguments[1] == "Motion")):         # time interval
                #print("* Motion      -38      64     -32     457     -40    -400      16       0   20500")    
                print ("         |Accel                  |Gyro                   |Angle                  |")
                print ("         |      X|      Y|      Z|   Roll|  Pitch|    Yaw|   Roll|  Pitch|    Yaw|")
                self.request(DataType.Motion, int(self.arguments[2]), float(self.arguments[3]))
                return

            # >python -m e_drive request RawLineTracer 10 0.2
            elif    ((self.count == 4) and 
                    (self.arguments[0] == "request") and
                    (self.arguments[1] == "RawLineTracer")):         # time interval
                #print("* RawLineTracer     36   140   219    36    30   340    33    45 Black       Black       Blue        Red")
                print ("               |Raw         |Front            |Rear             |Color                                           |")
                print ("               |  Left|Right|    H|    S|    V|    H|    S|    V|Left       |Right      |Front      |Rear        |")
                self.request(DataType.RawLineTracer, int(self.arguments[2]), float(self.arguments[3]))
                return

            # >python -m e_drive request RawCard 10 0.2
            elif    ((self.count == 4) and 
                    (self.arguments[0] == "request") and
                    (self.arguments[1] == "RawCard")):         # time interval
                #print("* RawCard   335  503  766  692  309  395 100  39  96  40   9  17 303  61  39 344  77  15   Magenta         Red")
                print ("          |Front Raw     |Rear Raw      |Front RGB  |Rear RGB   |Front HSV  |Rear HSV   |Front Color  |Rear Color   |")
                print ("          |   R    G    B|   R    G    B|  R   G   B|  R   G   B|  H   S   V|  H   S   V|             |             |")
                self.flagRawCardShowRange = False
                self.request(DataType.RawCard, int(self.arguments[2]), float(self.arguments[3]))
                return

            # >python -m e_drive request RawCardRange 10 0.2
            elif    ((self.count == 4) and 
                    (self.arguments[0] == "request") and
                    (self.arguments[1] == "RawCardRange")):         # time interval
                #print("* RawCardRange    200  2000   200  2000   200  2000   200     0   200     0   200     0")
                print ("               |Front                              |Rear                               |")
                print ("               |Red        |Green      |Blue       |Red        |Green      |Blue       |")
                print ("               |  Min|  Max|  Min|  Max|  Min|  Max|  Min|  Max|  Min|  Max|  Min|  Max|")
                self.flagRawCardShowRange = True
                self.request(DataType.RawCard, int(self.arguments[2]), float(self.arguments[3]))
                return

            # >python -m e_drive buzzer 2000 2
            elif    ((self.count == 3) and 
                    (self.arguments[0] == "buzzer")):
                print (Fore.WHITE + "Buzz Sound: " + Fore.YELLOW + "{0}".format(int(self.arguments[1])) + Fore.WHITE + "Hz, " + Fore.CYAN + "{0}".format(int(self.arguments[2])) + Fore.WHITE + "ms" + Style.RESET_ALL)
                self.buzzer(int(self.arguments[1]), int(self.arguments[2]))
                return

            # >python -m e_drive cards
            elif    ((self.count == 1) and 
                    (self.arguments[0] == "cards")):
                print (Fore.YELLOW + "cards" + Style.RESET_ALL)
                self.cardReaderGUI()
                return


    def request(self, dataType, repeat, interval):

        #drone = Drone(True, True, True, True, True)
        drone = Drone()
        if drone.open() == False:
            print(Fore.RED + "* Error : Unable to open serial port." + Style.RESET_ALL)
            sys.exit(1)
        
        # 이벤트 핸들링 함수 등록
        drone.setEventHandler(DataType.State, self.eventState)
        drone.setEventHandler(DataType.Motion, self.eventMotion)
        drone.setEventHandler(DataType.RawLineTracer, self.eventRawLineTracer)
        drone.setEventHandler(DataType.RawCard, self.eventRawCard)

        # 데이터 요청
        for i in range(repeat):
            drone.sendRequest(DeviceType.Drone, dataType)
            sleep(interval)


    def buzzer(self, hz, time):

        #drone = Drone(True, True, True, True, True)
        drone = Drone()
        if drone.open() == False:
            print(Fore.RED + "* Error : Unable to open serial port." + Style.RESET_ALL)
            sys.exit(1)
        
        if ( (not isinstance(hz, int)) or (not isinstance(time, int)) ):
            return None

        header = Header()
        
        header.dataType = DataType.Buzzer
        header.length   = Buzzer.getSize()
        header.from_    = DeviceType.Base
        header.to_      = DeviceType.Drone
        
        data = Buzzer()

        data.mode       = BuzzerMode.Hz
        data.value      = hz
        data.time       = time

        drone.transfer(header, data)
        sleep(time / 1000)


    def cardReaderGUI(self):

        colorama.init()
        cr = CardsReaderGUI()
        cr.run()


    def eventState(self, state):

        print("* State   " +
                Fore.YELLOW + "{0:10}".format(state.modeDrive.name) +
                Fore.WHITE + "{0:8}".format(state.colorFront.name) +
                Fore.WHITE + "{0:8}".format(state.colorRear.name) +
                Fore.WHITE + "{0:8}".format(state.colorLeft.name) +
                Fore.WHITE + "{0:8}".format(state.colorRight.name) +
                Fore.CYAN + "{0:15}".format(state.card.name) +
                Fore.CYAN + "{0:7}".format(state.irFrontLeft) +
                Fore.CYAN + "{0:7}".format(state.irFrontRight) +
                Fore.GREEN + "{0:7}".format(state.brightness) +
                Fore.GREEN + "{0:7}".format(state.battery) + Style.RESET_ALL)


    def eventMotion(self, motion):

        print("* Motion " +
                Fore.YELLOW + "{0:8}".format(motion.accelX) +
                Fore.YELLOW + "{0:8}".format(motion.accelY) +
                Fore.YELLOW + "{0:8}".format(motion.accelZ) +
                Fore.WHITE + "{0:8}".format(motion.gyroRoll) +
                Fore.WHITE + "{0:8}".format(motion.gyroPitch) +
                Fore.WHITE + "{0:8}".format(motion.gyroYaw) +
                Fore.CYAN + "{0:8}".format(motion.angleRoll) +
                Fore.CYAN + "{0:8}".format(motion.anglePitch) +
                Fore.CYAN + "{0:8}".format(motion.angleYaw) + Style.RESET_ALL)


    def eventRawLineTracer(self, rawLineTracer):

        print("* RawLineTracer " +
                Fore.RED        + "{0:6}".format(rawLineTracer.left) +
                Fore.RED        + "{0:6}".format(rawLineTracer.right) +
                Fore.YELLOW     + "{0:6}".format(rawLineTracer.frontH) +
                Fore.YELLOW     + "{0:6}".format(rawLineTracer.frontS) +
                Fore.YELLOW     + "{0:6}".format(rawLineTracer.frontV) +
                Fore.CYAN       + "{0:6}".format(rawLineTracer.rearH) +
                Fore.CYAN       + "{0:6}".format(rawLineTracer.rearS) +
                Fore.CYAN       + "{0:6} ".format(rawLineTracer.rearV) +
                Fore.MAGENTA    + "{0:12}".format(rawLineTracer.leftColor.name) +
                Fore.MAGENTA    + "{0:12}".format(rawLineTracer.rightColor.name) +
                Fore.GREEN      + "{0:12}".format(rawLineTracer.frontColor.name) +
                Fore.GREEN      + "{0:12}".format(rawLineTracer.rearColor.name) + Style.RESET_ALL)


    def eventRawCard(self, rawCard):

        if self.flagRawCardShowRange:
    
            print("* RawCardRange " +
                    Fore.RED    + "{0:6}".format(rawCard.range[0][0][0]) +
                    Fore.RED    + "{0:6}".format(rawCard.range[0][0][1]) +
                    Fore.GREEN  + "{0:6}".format(rawCard.range[0][1][0]) +
                    Fore.GREEN  + "{0:6}".format(rawCard.range[0][1][1]) +
                    Fore.BLUE   + "{0:6}".format(rawCard.range[0][2][0]) +
                    Fore.BLUE   + "{0:6}".format(rawCard.range[0][2][1]) +
                    Fore.RED    + "{0:6}".format(rawCard.range[1][0][0]) +
                    Fore.RED    + "{0:6}".format(rawCard.range[1][0][1]) +
                    Fore.GREEN  + "{0:6}".format(rawCard.range[1][1][0]) +
                    Fore.GREEN  + "{0:6}".format(rawCard.range[1][1][1]) +
                    Fore.BLUE   + "{0:6}".format(rawCard.range[1][2][0]) +
                    Fore.BLUE   + "{0:6}".format(rawCard.range[1][2][1]) + Style.RESET_ALL)

        else:
    
            print("* RawCard " +
                    Fore.RED    + "{0:5}".format(rawCard.rgbRaw[0][0]) +
                    Fore.GREEN  + "{0:5}".format(rawCard.rgbRaw[0][1]) +
                    Fore.BLUE   + "{0:5}".format(rawCard.rgbRaw[0][2]) +
                    Fore.RED    + "{0:5}".format(rawCard.rgbRaw[1][0]) +
                    Fore.GREEN  + "{0:5}".format(rawCard.rgbRaw[1][1]) +
                    Fore.BLUE   + "{0:5}".format(rawCard.rgbRaw[1][2]) +
                    Fore.RED    + "{0:4}".format(rawCard.rgb[0][0]) +
                    Fore.GREEN  + "{0:4}".format(rawCard.rgb[0][1]) +
                    Fore.BLUE   + "{0:4}".format(rawCard.rgb[0][2]) +
                    Fore.RED    + "{0:4}".format(rawCard.rgb[1][0]) +
                    Fore.GREEN  + "{0:4}".format(rawCard.rgb[1][1]) +
                    Fore.BLUE   + "{0:4}".format(rawCard.rgb[1][2]) +
                    Fore.RED    + "{0:4}".format(rawCard.hsv[0][0]) +
                    Fore.GREEN  + "{0:4}".format(rawCard.hsv[0][1]) +
                    Fore.BLUE   + "{0:4}".format(rawCard.hsv[0][2]) +
                    Fore.RED    + "{0:4}".format(rawCard.hsv[1][0]) +
                    Fore.GREEN  + "{0:4}".format(rawCard.hsv[1][1]) +
                    Fore.BLUE   + "{0:4} ".format(rawCard.hsv[1][2]) +
                    Fore.CYAN   + "{0:14}".format(rawCard.color[0].name) +
                    Fore.CYAN   + "{0:14}".format(rawCard.color[1].name) + Style.RESET_ALL)


# CommandParser End



if __name__ == '__main__':

    parser = CommandParser()

    parser.run()
