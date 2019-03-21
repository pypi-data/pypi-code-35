import sys
from e_drive.update import *


# CommandParser Start


class CommandParser():

    def __init__(self):

        self.program_name   = None
        self.arguments      = None
        self.count          = 0


    def run(self):
        
        self.program_name   = sys.argv[0]
        self.arguments      = sys.argv[1:]
        self.count          = len(self.arguments)

        if (self.count > 0) and (self.arguments != None):

            print("Count:{0} ".format(self.count) , end='')

            for arg in self.arguments:
                print("/ {0} ".format(arg), end='')

            print("")

            if      (self.arguments[0] == "upgrade") or (self.arguments[0] == "update"):
                updater = Updater()
                updater.update()
                return

            elif    ((self.count == 4) and 
                    (self.arguments[0] == "request") and
                    (self.arguments[1] == "State") and
                    isinstance(self.arguments[2], int) and      # repeat
                    isinstance(self.arguments[3], int)):         # time interval
                self.request(DataType.State, self.arguments[2], self.arguments[3])
                return


    def request(self, dataType, repeat, interval):

        drone = Drone()
        if drone.open() == False:
            print(Fore.RED + "* Error : Unable to open serial port." + Style.RESET_ALL)
            sys.exit(1)
        
        # 이벤트 핸들링 함수 등록
        drone.setEventHandler(DataType.State, self.eventState)

        # 데이터 요청
        for i in range(repeat):
            drone.sendRequest(DeviceType.Drone, dataType)
            sleep(interval)


    def eventState(self, state):

        print("* State: " + Fore.YELLOW + "{0:10}".format(state.modeSystem) +
                            Fore.YELLOW + "{0:10}".format(state.modeDrive) +
                            Fore.CYAN + "{0:6}".format(state.irFrontLeft) +
                            Fore.CYAN + "{0:6}".format(state.irFrontRight) +
                            Fore.WHITE + "{0:8}".format(state.colorFront) +
                            Fore.WHITE + "{0:8}".format(state.colorRear) +
                            Fore.WHITE + "{0:8}".format(state.colorLeft) +
                            Fore.WHITE + "{0:8}".format(state.colorRight) +
                            Fore.GREEN + "{0:8}".format(state.card) +
                            Fore.RED + "{0:5}".format(state.brightness) +
                            Fore.BLUE + "{0:5}".format(state.battery) + Style.RESET_ALL)


# CommandParser End



if __name__ == '__main__':

    parser = CommandParser()

    parser.run()
