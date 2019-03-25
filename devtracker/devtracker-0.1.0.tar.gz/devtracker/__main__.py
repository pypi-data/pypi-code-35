import sys
import os

from pathlib import Path
from .dir_and_path_helpers import get_working_dir
from .report import report,today_report, weekly_report, full_report
from .time import current_status, end_time, make_project_csv

def main():
    working_dir = get_working_dir()

    home = str(Path.home())
    path = home + "/devtrack_projects"
    if os.path.exists(path):
        pass
    else:
        os.mkdir(path)

    args = sys.argv[1:]
    if len(args) > 1:
        if args[0] == "report" or args[0] == "r":
            if args[1] == "--today" or args[1] == "--t":
                today_report(working_dir)
            elif args[1] == "--full" or args[1] == "--f":
                full_report(working_dir)
            elif args[1] == "--weekly" or args[1] == "--w":
                if len(args) == 3:
                    try:
                        int(args[2])
                    except ValueError:
                        print("[-] third arg must be of type integer.")
                    else:
                        weekly_report(working_dir, int(args[2]))
                else:
                    weekly_report(working_dir, 1)
            else:
                print("[-] {} is not a valid argument for 'devTracker report'".format(args[1]))
        else:
            print("[-] {} is not a valid argument for 'devTracker report'".format(args[1]))
    elif len(args) == 1:
        arg = args[0].lower()
        if arg == "start" or arg == "s":
            make_project_csv(working_dir)
        elif arg == "stop" or arg == "sto":
            end_time(working_dir)
        elif arg == "report" or arg == "r":
            report(working_dir)
        elif arg == "status" or arg == "sta":
            current_status(working_dir)
        elif arg == "--help" or arg == "h":
            print("Welcome to devTracker, track your time spent working based on the directory you are working in!\n"
                    "-------------------------------------------------------------------------------------------- \n"
                    "| STARTING AND STOPING |\n"
                    "'devtracker start': Will start tracking time in your current working directory.(shortcut 'dt s') \n"
                    "'devtracker stop': Will stop tracking time in your current working directory.(shortcut 'dt sto') \n\n\n"
                  
                    "| STATUS |\n"
                    "'devtracker status':  Will tell you if you have or haven't started tracking.(shortcut 'dt sta') \n\n\n"

                    "| REPORTING |\n"
                    "'devtracker report': Will give you the total time worked in your working directory.(shortcut 'dt r') \n"
                    "'devtracker report --today': Will report time worked today only.(shortcut 'dt r --t') \n"
                    "'devtracker report --weekly': Will report time for week (7 days).(shortcut 'dt r --w') \n"
                    "'devtracker report --weekly x':  Add an integer value for number of weeks to report ie. '--weekly 2'(shortcut 'dt r --w 2')\n"
                    "'devtracker report --full':  makes .csv file viewable in terminal(shortcut 'dt r --f')\n"
                    "-------------------------------------------------------------------------------------------- \n"
                    )
        else:
            print("[-] Argument: '{0}' not available use --help for more info about arguments".format(arg))
    else:
        print("[-] You must add an argument, use --help or h for more info about arguments")


if __name__ == '__main__':
    sys.exit(main(sys.argv))

