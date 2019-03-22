import sys
from e_drive.update import *


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


    def request(self, dataType, repeat, interval):

        #drone = Drone(True, True, True, True, True)
        drone = Drone()
        if drone.open() == False:
            print(Fore.RED + "* Error : Unable to open serial port." + Style.RESET_ALL)
            sys.exit(1)
        
        # 이벤트 핸들링 함수 등록
        drone.setEventHandler(DataType.State, self.eventState)
        drone.setEventHandler(DataType.RawCard, self.eventRawCard)

        # 데이터 요청
        for i in range(repeat):
            drone.sendRequest(DeviceType.Drone, dataType)
            sleep(interval)


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
