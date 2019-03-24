from pkgutil import get_data
from getpass import getuser
import json
import sys
import os
import shutil
import difflib
import subprocess
# import pprint
# from pathlib import Path

name = "qbs"


class qbscolors:
    reset = "\033[0m"
    bold = "\033[1m"
    brightred = "\033[91m"
    brightyellow = "\033[93m"
    green = "\033[32m"
    warn = bold + brightyellow + "Warning:" + reset
    err = bold + brightred + "Error:" + reset
    info = bold + "Info:" + reset


class UnsupportedLanguageError(Exception):
    def __init__(self, lang):
        self.lang = lang

    def __str__(self):
        return "qbs does not know how to build " + self.lang


class UnsupportedCommandError(Exception):
    def __init__(self, command, lang="this language"):
        self.command = command
        self.lang = lang

    def __str__(self):
        return "qbs does not know how to do " + self.command + " for "\
               + self.lang


class AmbiguousCommandError(Exception):
    def __init__(self, command, possibilities, lang="this language"):
        self.command = command
        self.possibilities = possibilities
        self.lang = lang

    def __str__(self):
        return self.command + " could mean " + str(self.possibilities)\
               + " for " + self.lang


class UnsupportedArgumentError(Exception):
    def __init__(self, argument):
        self.argument = argument

    def __str__(self):
        return "argument " + self.argument + " not allowed"


class NoClobberError(Exception):
    def __init__(self, filename):
        self.filename = filename

    def __str__(self):
        return "refusing to clobber " + self.filename


class MissingTestPropertyError(Exception):
    def __init__(self, prop):
        self.prop = prop

    def __str__(self):
        return "tester is missing property " + self.prop


class InvalidTestPropertyError(Exception):
    def __init__(self, prop):
        self.prop = prop

    def __str__(self):
        return "tester property " + self.prop + " is invalid"


class TestFailedError(Exception):
    def __init__(self, num, reason, output=None):
        self.num = num
        self.reason = reason
        self.output = output

    def __str__(self):
        output = ""
        if self.output is not None:
            output = "\n" + qbscolors.info + " output was\n```\n"\
                     + self.output.decode(sys.stdout.encoding) + "```"
        return "test " + str(self.num) + " failed: "\
               + self.reason + output


def parseCommand(command, allowedCommands, lang="no language configured",
                 config={}):
    result = [x for x in allowedCommands if x.startswith(command)]
    if len(result) == 0:
        raise UnsupportedCommandError(command, lang)
    elif len(result) > 1:
        raise AmbiguousCommandError(command, result, lang)
    else:
        result = result[0]
        return result


def getLanguageAlias(lang, config):
    while lang in config and isinstance(config[lang], str):
        lang = config[lang]
    if lang not in config:
        raise UnsupportedLanguageError(lang)
    return lang


def main():
    config = json.loads(get_data("qbs", "conf/default_config.json"))
    config_prefix = []

    if sys.platform.startswith("linux") or \
       sys.platform.startswith("cygwin") or \
       sys.platform.startswith("darwin"):
        config_prefix = ["/etc/",
                         "/home/{user}/.".format(user=getuser()),
                         "/home/{user}/.config/".format(user=getuser()),
                         "./.",
                         "./"]
    elif sys.platform.startswith("win"):
        config_prefix = ["C:\\ProgramData\\qbs\\",
                         "C:\\Users\\{user}\\AppData\\Roaming\\qbs\\"
                         .format(user=getuser()),
                         ".\\"]
    updated = False
    for pref in config_prefix:
        try:
            with open(pref + "qbs.json", "r") as conffile:
                config.update(json.load(conffile))
                updated = True
        except OSError:
            pass  # it's fine if the file doesn't exist
        except json.JSONDecodeError as e:
            print(qbscolors.warn + " parsing of " + conffile.name
                  + " failed:\n" + str(e), file=sys.stderr)
    if not updated:
        print(qbscolors.warn + " could not load any external configuration"
              " files. Using qbs defaults.", file=sys.stderr)
    cache = None
    try:
        with open("./.qbs.cache", "r") as cachefile:
            loadedcache = json.load(cachefile)
            cache = dict()
            cache["lang"] = getLanguageAlias(loadedcache["lang"], config)
            # that shouldn't be necessary but it can't hurt to be safe
            cache["filename"] = loadedcache["filename"]
        if cache["lang"] not in config:
            raise UnsupportedLanguageError(cache["lang"])
    except OSError:
        pass  # this is fine
    except (json.JSONDecodeError, KeyError):
        print(qbscolors.err + " .qbs.cache has been tampered with. Please fix "
              "it or delete it and re-initialize qbs.", file=sys.stderr)
        sys.exit(1)
    except UnsupportedLanguageError as e:
        print(qbscolors.err + " " + str(e) + " (from cache)", file=sys.stderr)
        sys.exit(2)

    arglist = sys.argv[1:]

    allowedCommands = []
    if cache is None:
        allowedCommands = ["init"]
        cache = {"lang": "no language configured"}
    else:
        allowedCommands = list(config[cache["lang"]].keys())
        allowedCommands.append("init")
        # allowedCommands.append("test")

    try:
        i = 0
        while i < len(arglist):
            command = parseCommand(arglist[i], allowedCommands,
                                   cache["lang"], config)
            if command == "init":
                # special case: init supports options
                i += 1
                template = None
                language = None
                while arglist[i].startswith("-"):
                    if arglist[i] == "-t":
                        i += 1
                        template = arglist[i]
                    elif arglist[i] == "-l":
                        i += 1
                        language = arglist[i]
                    else:
                        raise UnsupportedArgumentError(arglist[i])
                    i += 1
                filename = arglist[i]
                filepath, fileext = os.path.splitext(filename)

                if language is None:
                    language = fileext[1:]  # remove the dot
                if template is not None:
                    if os.path.exists(filename):
                        raise NoClobberError(filename)
                    with open(template, "r") as infile,\
                            open(filename, "w") as outfile:
                        for line in infile:
                            outfile.write(
                             line.format(progname=os.path.basename(filepath),
                                         progext=fileext))
                if language not in config:
                    raise UnsupportedLanguageError(language)
                cache["lang"] = getLanguageAlias(language, config)
                cache["filename"] = filename
                # write out cache
                with open("./.qbs.cache", "w") as cachefile:
                    json.dump(cache, cachefile)
                # regenerate allowed commands
                allowedCommands = list(config[cache["lang"]].keys())
                allowedCommands.append("init")
                # allowedCommands.append("test")
            elif command == "t_auto":
                filepath, fileext = os.path.splitext(cache["filename"])
                if "run" not in config[cache["lang"]]:
                    raise UnsupportedCommandError("run", config[cache["lang"]])
                for prop in ["input", "infiles", "output", "outfiles"]:
                    if prop not in config[cache["lang"]]["t_auto"]:
                        raise MissingTestPropertyError(prop)
                input = config[cache["lang"]]["t_auto"]["input"].format(
                    progname=os.path.basename(filepath),
                    progext=fileext
                )
                infiles = config[cache["lang"]]["t_auto"]["infiles"]
                output = config[cache["lang"]]["t_auto"]["output"].format(
                    progname=os.path.basename(filepath),
                    progext=fileext
                )
                outfiles = config[cache["lang"]]["t_auto"]["outfiles"]
                infilenum = 0
                try:
                    if "begin" in config[cache["lang"]]["t_auto"]:
                        infilenum = config[cache["lang"]]["t_auto"]["begin"]
                    while True:
                        run_args = {}
                        thisinfile = infiles.format(
                         num=infilenum,
                         progname=os.path.basename(filepath),
                         progext=fileext)
                        thisoutfile = outfiles.format(
                         num=infilenum,
                         progname=os.path.basename(filepath),
                         progext=fileext)
                        if output != "-" and os.path.exists(output):
                            print(qbscolors.warn + " output file " + output
                                  + " exists before starting test "
                                  + str(infilenum), file=sys.stderr)
                        with open(thisinfile, "r") as thisinobj,\
                                open(thisoutfile, "r") as thisoutobj:
                            if input == "-":
                                run_args["stdin"] = thisinobj
                            else:
                                if os.path.exists(input):
                                    raise NoClobberError(input)
                                try:
                                    os.symlink(thisinfile, input)
                                except (OSError,
                                        NotImplementedError,
                                        PermissionError):
                                    shutil.copyfile(thisinfile, input)
                                    # symlink could be drastically more
                                    # efficient but copy if we must
                            if output == "-":
                                run_args["stdout"] = subprocess.PIPE
                            cmdline = [x.format(progname=filepath,
                                                progext=fileext)
                                       for x in config[cache["lang"]]["run"]]
                            if len(cmdline) > 0:
                                print(qbscolors.bold + "Test " + str(infilenum)
                                      + ":" + qbscolors.reset, file=sys.stderr)
                                print(qbscolors.green + "+ "
                                      + " ".join(cmdline)
                                      + qbscolors.reset, file=sys.stderr)
                                cproc = subprocess.run(cmdline, **run_args)
                                if cproc.returncode != 0:
                                    raise TestFailedError(
                                           infilenum, "nonzero return code "
                                           + str(cproc.returncode),
                                           cproc.stdout)
                                diffresult = []
                                if output == "-":
                                    diffresult = list(difflib.unified_diff(
                                     thisoutobj.readlines(),
                                     cproc.stdout.decode(sys.stdout.encoding)
                                     .splitlines(keepends=True),
                                     fromfile=thisoutfile,
                                     tofile="stdout"
                                    ))
                                else:
                                    try:
                                        with open(output, "r") as actualout:
                                            diffresult = list(
                                             difflib.unified_diff(
                                              thisoutobj.readlines(),
                                              actualout.readlines(),
                                              fromfile=thisoutfile,
                                              tofile=output
                                             ))
                                    except OSError:
                                        raise TestFailedError(
                                         infilenum,
                                         "did not create output file "
                                         + output)
                                # pprint.pprint(diffresult)
                                if len(diffresult) > 0:
                                    raise TestFailedError(
                                     infilenum,
                                     "output ""differs from testcase:\n"
                                     + "".join(diffresult),
                                     cproc.stdout)
                            else:
                                print(qbscolors.warn + " doing nothing for "
                                      "run in test " + str(infilenum),
                                      file=sys.stderr)
                            if input != "-":
                                try:
                                    os.remove(input)
                                except OSError:
                                    pass  # no one cares
                            if output != "-":
                                try:
                                    os.remove(output)
                                except OSError:
                                    pass  # no one cares
                            infilenum = infilenum + 1

                except OSError:  # couldn't find last file means we're finished
                    pass
                except TestFailedError as e:
                    if input != "-":
                        try:
                            os.remove(input)
                        except OSError:
                            pass  # no one cares
                    print(qbscolors.err + " " + str(e), file=sys.stderr)
                    sys.exit(6)
                if infilenum == 0:
                    print(
                     qbscolors.warn + " no tests were found!",
                     file=sys.stderr)

                print(qbscolors.bold + qbscolors.green + "All tests passed!"
                      + qbscolors.reset, file=sys.stderr)
            else:
                if command.endswith("_auto"):
                    print(
                     qbscolors.warn + " commands ending with _auto may "
                     "be reserved in the future", file=sys.stderr)
                filepath, fileext = os.path.splitext(cache["filename"])
                cmdline = [x.format(progname=filepath, progext=fileext)
                           for x in config[cache["lang"]][command]]
                if len(cmdline) > 0:
                    print(qbscolors.green + "+ " + " ".join(cmdline)
                          + qbscolors.reset, file=sys.stderr)
                    cproc = subprocess.run(cmdline)
                    if cproc.returncode != 0:
                        print(qbscolors.err + " nonzero return code "
                              + str(cproc.returncode), file=sys.stderr)
                        sys.exit(cproc.returncode)
                else:
                    print(qbscolors.warn + " doing nothing for " + command,
                          file=sys.stderr)
            i += 1
    except UnsupportedLanguageError as e:
        print(qbscolors.err + " " + str(e), file=sys.stderr)
        sys.exit(2)
    except (AmbiguousCommandError,
            UnsupportedCommandError,
            UnsupportedArgumentError) as e:
        print(qbscolors.err + " " + str(e), file=sys.stderr)
        sys.exit(3)
    except (MissingTestPropertyError, InvalidTestPropertyError) as e:
        print(qbscolors.err + " " + str(e), file=sys.stderr)
        sys.exit(4)
    except NoClobberError as e:
        print(qbscolors.err + " " + str(e), file=sys.stderr)
        sys.exit(5)
    except OSError as e:
        print(qbscolors.err + " " + str(e), file=sys.stderr)
        sys.exit(1)
