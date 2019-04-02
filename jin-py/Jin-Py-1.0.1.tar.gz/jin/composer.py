import os
import sys

pushCommandTemplate = ["rsync", "-vzaPr"]
clearCommandTemplate = ["rsync", "-vPr", "--delete", "--existing", "--ignore-existing"]

class Composer():
    """Composes an rsync command from system arguements and jinconfig file"""

    def __init__(self, args, config):
        self.args        = args
        self.config      = config
        self.isDryRun    = False
        self.isHot       = False
        self.minToWatch  = 1
        self.command     = self.dispatchCommandFromType(self.args[0])

    def checkConfigForRequired(self, command, config):
        if command == "push":
            if self.config.get("sloc") == None and self.config.get("sdir") == None:
                print(".jinconfig doesn't contain source information!")
                sys.exit(1)
            if self.config.get("dloc") == None and self.config.get("ddir") == None:
                print(".jinconfig doesn't contain destination information!")
                sys.exit(1)
            if self.config.get("wmin") != None:
                self.minToWatch = int(self.config.get("wmin")[0])

        if command == "empty":
            if self.config.get("dloc") == None and self.config.get("ddir") == None:
                print(".jinconfig doesn't contain destination information!")
                sys.exit(1)

    def dispatchCommandFromType(self, command):
        if command == "push":
            self.checkConfigForRequired(command, self.config)

            if len(self.args) > 1:
                for arg in self.args[1:]:
                    if arg == "dry":
                        pushCommandTemplate.append("--dry-run")
                        self.isDryRun = True
                    elif arg == "watch":
                        self.isHot = True
                    elif arg == "match-host":
                        pushCommandTemplate.append("--delete")
                    else:
                        print(f"Invalid command '{arg}'!")
                        sys.exit(1)

            return self.generatePushCommand()
        elif command == "empty":
            self.checkConfigForRequired(command, self.config)

            if len(self.args) > 1:
                for arg in self.args:
                     if arg == "dry":
                         clearCommandTemplate.append("--dry-run")
                         self.isDryRun = True

            return self.generateClearCommand()
        else:
            print(f"Invalid command '{command}'! Exiting...")
            sys.exit(1)

    def generateClearCommand(self):
        command = clearCommandTemplate
        destination = ""

        if not os.path.exists("./.jin/_blank/"):
            print(".jin/_blank directory doesn't exist! Run 'jin make' to fix this.")
            sys.exit(1)

        if self.config.get("dloc") == None:
            destination = self.config.get("ddir")[0]
        else:
            destination = f"{self.config.get('dloc')[0]}:{self.config.get('ddir')[0]}"

        # command = rsync -r --delete --existing --ignore-existing ./jin/_blank/ [destination]
        command.extend((".jin/_blank/", destination))
        return command

    def generatePushCommand(self):
        command = pushCommandTemplate

        source = ""
        destination = ""
        ignoreSpecific = []
        ignoreType = []

        if self.config.get("sloc") == None:
            source = self.config.get("sdir")[0]
        else:
            source = f"{self.config.get('sloc')[0]}:{self.config.get('sdir')[0]}"

        if self.config.get("dloc") == None:
            destination = self.config.get("ddir")[0]
        else:
            destination = f"{self.config.get('dloc')[0]}:{self.config.get('ddir')[0]}"

        if self.config.get("igspec") != None:
            for excludedSpecific in self.config.get("igspec"):
                ignoreSpecific.append("--exclude")
                ignoreSpecific.append(f"\'{excludedSpecific}\'")

        if self.config.get("igtype") != None:
            for excludedType in self.config.get("igtype"):
                ignoreType.append("--exclude")
                ignoreType.append(f"\'{excludedType}\'")

        for spec in ignoreSpecific: command.append(spec)
        for spec in ignoreType:     command.append(spec)

        # command = rsync -vzaPr --exclude [ignoreSpecific] --exclude [ignoreType] [source] [destination]
        command.extend((source, destination))
        print(" ".join(command), "\n")
        return command
