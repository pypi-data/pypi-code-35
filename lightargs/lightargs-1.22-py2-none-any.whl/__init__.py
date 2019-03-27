# PYTHON_ARGCOMPLETE_OK

from .argument import _Argument
from .coloring import *

_COLORING = { "green":b_green,
              "dim":dim,
              "bright":bright }

import os
import traceback
import argcomplete, argparse

from .unknown_argument import UnknownArgument
from .wrong_parameters import WrongParameters


def _print(prefix,what,suffix,modes):

    global _COLORING
    
    if _COLORING is None:
        print (prefix+what+suffix)
        return

    def _get_colored_string(what,modes):
        for mode in modes:
            fn = _COLORING[mode]
            what = fn(what)
        return what

    what = _get_colored_string(what,modes)
    
    print (prefix+what+suffix)
    


_ARGUMENTS = {}
_USAGE = ""
_HIDDEN = "hidden"

# for autocompletion
_PARSER = None


def enable_autocompletion():
    global _PARSER
    _PARSER = argparse.ArgumentParser() 

    
def autocomplete():
    global _PARSER
    if _PARSER is None:
        raise Exception("lightargs: attempting to call autocomplete without previous call to enable_autocompletion")
    argcomplete.autocomplete(_PARSER)


def set_usage(usage):
    global _USAGE
    _USAGE= str(usage)

    
def print_help():

    global _USAGE
    global _HIDDEN
    global _ARGUMENTS
    
    if _USAGE:

        print ("\n" + _USAGE + "\n")

    categories = set( [argument.category for argument in _ARGUMENTS.values()] )
    categories = sorted(categories)

    for category in categories:

        if category != _HIDDEN:

            _print( "\t",
                    str(category) + "\n\t" + "".join(["-" * len(str(category))]),
                    "",
                    ["green"] )

            arguments = [ argument for argument in _ARGUMENTS.values()
                          if argument.category == category ]

            arguments = sorted( arguments, key=lambda argument: argument.command )

            arguments_list = ""
            for argument in arguments:
                if argument.args_labels:
                    arguments_list = " " + " ".join(argument.args_labels)
                else:
                    arguments_list = ""

                _print( "\t\t",
                        str(argument.command),
                        arguments_list,
                        ["bright"] )

                _print ( "\t\t\t",
                         str(argument.man),
                         "\n",
                         ["dim","green"] )
                             

def add( command,
         function,
         nb_args=0,
         args_labels=None,
         defaults=None,
         man="",
         category=None,
         autocompletion=None ):

    global _ARGUMENTS
    global _PARSER
    
    if command in _ARGUMENTS:
        raise Exception(command + " added more than once")

    _ARGUMENTS[command] = _Argument( command,
                                     function,
                                     nb_args=nb_args,
                                     args_labels=args_labels,
                                     defaults=defaults,
                                     man=man,
                                     category=category )
    
    if autocompletion is not None and _PARSER is not None :

        def get_autocompletion(prefix,parsed_args,**kwargs):
            return autocompletion

        _PARSER.add_argument(command).completer = get_autocompletion

    elif _PARSER is not None:

        # allows the command to be autocompleted (even if command
        # does not take any follow up arguments
        
        def no_autocompletion(prefix,parsed_args,**kwargs):
            return []

        _PARSER.add_argument(command).completer = no_autocompletion
        

def execute(args):

    global _ARGUMENTS
    global _HIDDEN
    
    if not args:
        print_help()
        return

    command = args[0]

    if command not in _ARGUMENTS.keys():

        known_args = [
            k for k,
            v in _ARGUMENTS.iteritems() if v.category != _HIDDEN]

        raise UnknownArgument(
            "unknown command: " +
            command +
            "\nknown command: " +
            ",".join(known_args))

    argument_instance = _ARGUMENTS[command]
    args = args[1:]

    return argument_instance.execute(args)
