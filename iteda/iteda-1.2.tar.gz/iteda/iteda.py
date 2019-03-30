# -*- coding: utf-8 -*-
## Text menu Calibrador loco
#!/usr/bin/env python2.7
#from uart import send_to_uart
import os
import argparse
import textwrap
import serial, time
import sys
from subprocess import call

parser=argparse.ArgumentParser(
    description='''My Description. And what a lovely description it is. ''',
    epilog="""All's well that ends well.""")
parser.add_argument('--foo', type=int, default=42, help='FOO!')
parser.add_argument('bar', nargs='*', default=[1, 2, 3], help='BAR!')
args=parser.parse_args()

## title in form of ascii art

header = "\
                                                                                        \n\
██╗████████╗███████╗██████╗  █████╗     ███████╗██████╗ ██╗  ██╗███████╗██████╗ ███████╗\n\
██║╚══██╔══╝██╔════╝██╔══██╗██╔══██╗    ██╔════╝██╔══██╗██║  ██║██╔════╝██╔══██╗██╔════╝\n\
██║   ██║   █████╗  ██║  ██║███████║    ███████╗██████╔╝███████║█████╗  ██████╔╝█████╗  \n\
██║   ██║   ██╔══╝  ██║  ██║██╔══██║    ╚════██║██╔═══╝ ██╔══██║██╔══╝  ██╔══██╗██╔══╝  \n\
██║   ██║   ███████╗██████╔╝██║  ██║    ███████║██║     ██║  ██║███████╗██║  ██║███████╗\n\
╚═╝   ╚═╝   ╚══════╝╚═════╝ ╚═╝  ╚═╝    ╚══════╝╚═╝     ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚══════╝\n"

## Colors definition, you can add more if you like it 
colors = {
        'blue': '\033[94m',
        'pink': '\033[95m',
        'green': '\033[92m',
        'red': '\033[91m',
        'blink': '\33[6m',
        'yellow': '\033[93m',
        'purple': '\033[35m',
        'cyan': '\033[36m'
        }
## function definition section

def colorize(string, color):
    if not color in colors: return string
    return colors[color] + string + '\033[0m'

def data():
    print "Data input (Set all the parameters to send to the Fpga)"
    print "Data input (Have in mind that you should enter the values in amount of pulses, each pulse have a duration of 12,5nS and for all the values of the interval are from 0-254)"

    ## add crazy function calls here
    #Getting What To Write To File
    time_on1 = raw_input('\033[1;33;40m Insert time on value1 :  \033[0m')
    time_delay1 = raw_input('\033[1;33;40m Insert time delay value1 :  \033[0m')
    time_on2 = raw_input('\033[1;33;40m Insert time on value2 :  \033[0m')
    time_delay2 = raw_input('\033[1;33;40m Insert time delay value2 :  \033[0m')
    time_on3 = raw_input('\033[1;33;40m Insert time on value3 :  \033[0m')
    time_delay3 = raw_input('\033[1;33;40m Insert time delay value3 :  \033[0m')
    time_on4 = raw_input('\033[1;33;40m Insert time on value4 :  \033[0m')
    time_delay4 = raw_input('\033[1;33;40m Insert time delay value4 :  \033[0m')
    trigger_int_ext = raw_input('\033[1;33;40m Set the option for the Trigger: 0 for internal or 1 for external :  \033[0m')
    trigger = raw_input('\033[1;33;40m Insert your trigger time, if you use an external one, please leave it blanck :  \033[0m')
    power1 = raw_input('\033[1;33;40m Insert the value for intensity on Laser1 :  \033[0m')
    power2 = raw_input('\033[1;33;40m Insert the value for intensity on Laser2 :  \033[0m')
    power3 = raw_input('\033[1;33;40m Insert the value for intensity on Laser3 :  \033[0m')
    power4 = raw_input('\033[1;33;40m Insert the value for intensity on Laser4 :  \033[0m')
    #Actually Writing It
    saveFile = open('datasend.txt', 'w')
    saveFile.write(time_on1 +"\n")
    saveFile.write(time_delay1 +"\n")
    saveFile.write(time_on2 +"\n")
    saveFile.write(time_delay2 +"\n")
    saveFile.write(time_on3 +"\n")
    saveFile.write(time_delay3 +"\n")
    saveFile.write(time_on4 +"\n")
    saveFile.write(time_delay4 +"\n")
    saveFile.write(trigger_int_ext +"\n")
    saveFile.write(trigger +"\n")
    saveFile.write(power1 +"\n")
    saveFile.write(power2 +"\n")
    saveFile.write(power3 +"\n")
    saveFile.write(power4)
    saveFile.close()
   
    raw_input("Press [Enter] to continue...")
 
def reset():
    ## add crazy function calls here
    if os.path.exists("datasend.txt"):
        os.remove("datasend.txt")
        print "(All the data previously entered was removed)"
    else:
        print("The file does not exist")
    raw_input("Press [Enter] to continue...")

def check():
    print "Check the values of the data entered \n"
    ## add crazy function calls here
    file = open("datasend.txt","r")
    print "\033[1;35;40m Name of the file: %s \n \033[0m" % file.name
    line = file.readline().strip()
    print "\033[1;35;40m Time_on1: %s \033[0m" % (line)
    line = file.readline().strip()
    print "\033[1;35;40m Time_delay1: %s \033[0m" % (line)
    line = file.readline().strip()
    print "\033[1;35;40m Time_on2: %s \033[0m" % (line)
    line = file.readline().strip()
    print "\033[1;35;40m Time_delay2: %s \033[0m" % (line)
    line = file.readline().strip()
    print "\033[1;35;40m Time_on3: %s \033[0m" % (line)
    line = file.readline().strip()
    print "\033[1;35;40m Time_delay3: %s \033[0m" % (line)
    line = file.readline().strip()
    print "\033[1;35;40m Time_on4: %s \033[0m" % (line)
    line = file.readline().strip()
    print "\033[1;35;40m Time_delay4: %s \033[0m" % (line)
    line = file.readline().strip()
    print "\033[1;35;40m Trigger_int_ext: %s \033[0m" % (line)
    line = file.readline().strip()
    print "\033[1;35;40m Trigger_value: %s \033[0m" % (line)
    line = file.readline().strip()
    print "\033[1;35;40m Laser1_power: %s \033[0m" % (line)
    line = file.readline().strip()
    print "\033[1;35;40m Laser2_power: %s \033[0m" % (line)
    line = file.readline().strip()
    print "\033[1;35;40m Laser3_power: %s \033[0m" % (line)
    line = file.readline().strip()
    print "\033[1;35;40m Laser4_power: %s \033[0m" % (line)
    file.close()
    raw_input("Press [Enter] to continue...")

def start():	
    file = open("datasend.txt","r")
    time_on1 = file.readline().strip()
    time_delay1 = file.readline().strip()
    time_on2 = file.readline().strip()
    time_delay2 = file.readline().strip()
    time_on3 = file.readline().strip()
    time_delay3 = file.readline().strip()
    time_on4 = file.readline().strip()
    time_delay4 = file.readline().strip()
    trigger_int_ext = file.readline().strip()
    trigger = file.readline().strip()
    power1 = file.readline().strip()
    power2 = file.readline().strip()
    power3 = file.readline().strip()
    power4 = file.readline().strip()
    call(["./menu", time_on1, time_delay1, power1, time_on2, time_delay2, power2, time_on3, time_delay3, power3, time_on4, time_delay4, power4, trigger_int_ext, trigger])
    raw_input("Press [Enter] to continue...")


def help():
    print "Help (User manual)"
    ## add crazy function calls here, in this case, only a text with information about how to not screw up things
    raw_input("Press [Enter] to continue...")

## items to put in the menu
menuItems = [
    { "Call Data input": data },
    { "Call Reset_info": reset },
    { "Call Data send": start },
    { "Call Check_information": check },
    { "Exit": exit },
]
## main menu function operation
def main():
    while True:
        os.system('clear')
        # Print some badass ascii art header here !
        print colorize(header, 'red')
        print colorize('Authors : Victor Esparza -- Fabrizio Di Francesco                               Version 1.1\n', 'green')
        for item in menuItems:
            print colorize("[" + str(menuItems.index(item)) + "] ", 'blue') + item.keys()[0]
        choice = raw_input(">> ")
        try:
            if int(choice) < 0 : raise ValueError
            # Call the matching function
            menuItems[int(choice)].values()[0]()
        except (ValueError, IndexError):
            pass
 
if __name__ == "__main__":
    main()
