# -*- coding: utf-8 -*-
## Text menu Calibrador loco
#!/usr/bin/env python2.7
#from uart import send_to_uart
import os
import argparse
import textwrap
import serial, time
import sys

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
    print "Data input (Have in mind that you should enter the values in amount of pulses each pulse have a duration of 10nS and for all the values the interb¿val is from 1-64)"

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
######################### read of temporary file ####################
## values must be entered in scientific notation
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
    trigger_value = file.readline().strip()
    laser1 = file.readline().strip()
    laser2 = file.readline().strip()
    laser3 = file.readline().strip()
    laser4 = file.readline().strip()
    ##print "\033[1;34;40m Laser1_power: %s \033[0m" % (laser1)
    file.close()

    ######################## data accomodation  #########################
    ### convert of values to binary
    f_time_on1 = format(int(time_on1),'#010b')[2:]
    ##print "\033[1;34;40m test: %s \033[0m" % (f_time_on1)
    f_time_delay1 = format(int(time_delay1),'#010b')[2:]
    f_time_on2 = format(int(time_on2),'#010b')[2:]
    f_time_delay2 = format(int(time_delay2),'#010b')[2:]
    f_time_on3 = format(int(time_on3),'#010b')[2:]
    f_time_delay3 = format(int(time_delay3),'#010b')[2:]
    f_time_on4 = format(int(time_on4),'#010b')[2:]
    f_time_delay4 = format(int(time_delay4),'#010b')[2:]
    f_trigger_int_ext = format(int(trigger_int_ext),'#010b')[2:]
    f_trigger_value = format(int(trigger_value),'#034b')[2:]
    f_laser1 = format(int(laser1),'#010b')[2:]
    f_laser2 = format(int(laser2),'#010b')[2:]
    f_laser3 = format(int(laser3),'#010b')[2:]
    f_laser4 = format(int(laser4),'#010b')[2:]
    trigger = f_trigger_value
    #trigger = "{:032b}".format(int(f_trigger_value))
    trigger1 = trigger[0:8]
    trigger2 = trigger[8:16]
    trigger3 = trigger[16:24]
    trigger4 = trigger[24:32]
    ##print "\033[1;34;40m trigger: %s \033[0m" % (trigger)
    ######################### send to final file ########################
    saveFile = open('send.txt', 'w')
    saveFile.write("00000000" +"\n")
    saveFile.write(f_time_on1 +"\n")
    saveFile.write("00000001" +"\n")
    saveFile.write(f_time_delay1 +"\n")
    saveFile.write("00000010" +"\n")
    saveFile.write(f_time_on2 +"\n")
    saveFile.write("00000011" +"\n")
    saveFile.write(f_time_delay2 +"\n")
    saveFile.write("00000100" +"\n")
    saveFile.write(f_time_on3 +"\n")
    saveFile.write("00000101" +"\n")
    saveFile.write(f_time_delay3 +"\n")
    saveFile.write("00000110" +"\n")
    saveFile.write(f_time_on4 +"\n")
    saveFile.write("00000111" +"\n")
    saveFile.write(f_time_delay4 +"\n")    
    saveFile.write("00001000" +"\n")
    saveFile.write(f_trigger_int_ext +"\n")
    saveFile.write("00001001" +"\n")
    saveFile.write( f_laser1+"\n")
    saveFile.write("00001010" +"\n")
    saveFile.write(f_laser2 +"\n")
    saveFile.write("00001011" +"\n")
    saveFile.write(f_laser3 +"\n")
    saveFile.write("00001100" +"\n")
    saveFile.write(f_laser4 +"\n")
    saveFile.write("00001101" +"\n")
    saveFile.write(trigger1 +"\n")
    saveFile.write("00001110" +"\n")
    saveFile.write(trigger2 +"\n")
    saveFile.write("00001111" +"\n")
    saveFile.write(trigger3 +"\n")
    saveFile.write("00010000" +"\n")
    saveFile.write(trigger4 +"\n")
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
    ## add crazy function calls here
    #import uart
    print ""
#initialization and open the port

#possible timeout values:
#    1. None: wait forever, block call
#    2. 0: non-blocking mode, return immediately
#    3. x, x is bigger than 0, float allowed, timeout block call

    ser = serial.Serial()
    #ser.port = "/dev/ttyUSB0"
    #ser.port = "/dev/ttyUSB7"
    #ser.port = "/dev/tty2"
    ser.port = "/dev/ttyS2"
    ser.baudrate = 38400
    ser.bytesize = serial.EIGHTBITS #number of bits per bytes
    ser.parity = serial.PARITY_EVEN #set parity check: no parity
    ser.stopbits = serial.STOPBITS_ONE #number of stop bits
    #ser.timeout = None          #block read
    ser.timeout = 1            #non-block read
    #ser.timeout = 2              #timeout block read
    ser.xonxoff = False     #disable software flow control
    ser.rtscts = False     #disable hardware (RTS/CTS) flow control
    ser.dsrdtr = False       #disable hardware (DSR/DTR) flow control
    ser.writeTimeout = 0     #timeout for write

    try: 
        ser.open()
    except Exception, e:
        print "error open serial port: " + str(e)
        exit()

    if ser.isOpen():

        try:
            ser.flushInput() #flush input buffer, discarding all its contents
            ser.flushOutput()#flush output buffer, aborting current output 
                    #and discard all that is in buffer

            #write data
            print "\033[1;34;40m Sending this whole data via serial port \033[0m"
            file = open("send.txt","r")
            line = file.readline().strip()
            ser.write(line)
            #time.sleep(0.8)
            line = file.readline().strip()
            print "\033[1;34;40m Time_on1: %s \033[0m" % (line)
            ser.write(line)
            #time.sleep(0.8)
            line = file.readline().strip()
            ser.write(line)
            #time.sleep(0.8)
            line = file.readline().strip()
            print "\033[1;34;40m Time_delay1: %s \033[0m" % (line)
            ser.write(line)
            #time.sleep(0.8)
            line = file.readline().strip()
            ser.write(line)
            #time.sleep(0.8)
            line = file.readline().strip()
            print "\033[1;34;40m Time_on2: %s \033[0m" % (line)
            ser.write(line)
            #time.sleep(0.8)
            line = file.readline().strip()
            ser.write(line)
            #time.sleep(0.8)
            line = file.readline().strip()
            print "\033[1;34;40m Time_delay2: %s \033[0m" % (line)
            ser.write(line)
            #time.sleep(0.8)
            line = file.readline().strip()
            ser.write(line)
            #time.sleep(0.8)
            line = file.readline().strip()
            print "\033[1;34;40m Time_on3: %s \033[0m" % (line)
            ser.write(line)
            #time.sleep(0.8)
            line = file.readline().strip()
            ser.write(line)
            #time.sleep(0.8)
            line = file.readline().strip()
            print "\033[1;34;40m Time_delay3: %s \033[0m" % (line)
            ser.write(line)
            #time.sleep(0.8)
            line = file.readline().strip()
            ser.write(line)
            #time.sleep(0.8)
            line = file.readline().strip()
            print "\033[1;34;40m Time_on4: %s \033[0m" % (line)
            ser.write(line)
            #time.sleep(0.8)
            line = file.readline().strip()
            ser.write(line)
            #time.sleep(0.8)
            line = file.readline().strip()
            print "\033[1;34;40m Time_delay4: %s \033[0m" % (line)
            ser.write(line)
            #time.sleep(0.8)
            line = file.readline().strip()
            ser.write(line)
            #time.sleep(0.8)
            line = file.readline().strip()
            print "\033[1;34;40m Trigger_int_ext: %s \033[0m" % (line)
            ser.write(line)
            #time.sleep(0.8)
            line = file.readline().strip()
            ser.write(line)
            #time.sleep(0.8)
            line = file.readline().strip()
            print "\033[1;34;40m Laser1: %s \033[0m" % (line)
            ser.write(line)
            #time.sleep(0.8)
            line = file.readline().strip()
            ser.write(line)
            #time.sleep(0.8)
            line = file.readline().strip()
            print "\033[1;34;40m Laser2: %s \033[0m" % (line)
            ser.write(line)
            #time.sleep(0.8)
            line = file.readline().strip()
            ser.write(line)
            #time.sleep(0.8)
            line = file.readline().strip()
            print "\033[1;34;40m Laser3: %s \033[0m" % (line)
            ser.write(line)
            #time.sleep(0.8)
            line = file.readline().strip()
            ser.write(line)
            #time.sleep(0.8)
            line = file.readline().strip()
            print "\033[1;34;40m Laser4: %s \033[0m" % (line)
            ser.write(line)
            #time.sleep(0.8)
            line = file.readline().strip()
            ser.write(line)
            #time.sleep(0.8)
            line = file.readline().strip()
            print "\033[1;34;40m Trigger_part1: %s \033[0m" % (line)
            ser.write(line)
            #time.sleep(0.8)
            line = file.readline().strip()
            ser.write(line)
            #time.sleep(0.8)
            line = file.readline().strip()
            print "\033[1;34;40m Trigger_part2: %s \033[0m" % (line)
            ser.write(line)
            #time.sleep(0.8)
            line = file.readline().strip()
            ser.write(line)
            #time.sleep(0.8)
            line = file.readline().strip()
            print "\033[1;34;40m Trigger_part3: %s \033[0m" % (line)
            ser.write(line)
            #time.sleep(0.8)
            line = file.readline().strip()
            ser.write(line)
            #time.sleep(0.8)
            line = file.readline().strip()
            print "\033[1;34;40m Trigger_part4: %s \033[0m" % (line)
            ser.write(line)
            #time.sleep(0.8) #give the serial port sometime to receive the data
            file.close()
            ser.close()
        except Exception, e1:
            print "error communicating...: " + str(e1)

    else:
        print "cannot open serial port "

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
