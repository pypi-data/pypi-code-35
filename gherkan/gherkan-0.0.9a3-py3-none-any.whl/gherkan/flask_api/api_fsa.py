import datetime
import importlib
import os
import re

import yaml

import gherkan.utils.constants as c
from .raw_text_to_signal import process as nlToSignal
from .signal_to_nl import process as signalToNL
from .speech_to_text import process as speechToText

from flask import send_file


class API_FSA():
    """
    FSA class for tracking state from REST API. State is written into a file
    so it should be persistent even over long time periods.
    """

    # =====>>> PATH variables <<<===== #
    stateFilePath = 'state.fsa'
    logFilePath = 'log.txt'
    configFilePath = 'fsa_config.yaml'

    # This path does not need to be set to the package's root, probably
    rootFolder = c.PROJECT_ROOT_DIR

    dataFolder = os.path.join(rootFolder, 'data')
    audioFolder = os.path.join(dataFolder, 'audio')
    # nlTextFolder = os.path.join(dataFolder, 'nl_text')
    # signalsFolder = os.path.join(dataFolder, 'signals')

    robotProgramsPath = os.path.join(rootFolder, 'utils', 'RobotPrograms_{}.json')

    language = 'en'

    # =====>>> STATE constants <<<===== #
    S_OFF = 0
    S_IDLE = 1
    S_RECEIVED_NL_TEXT = 2
    S_CORRECTING_NL_TEXT = 4
    S_FINISHED_PROCESSING_NL_TEXT = 8
    S_RECEIVED_SIGNAL = 16
    S_FINISHED_PROCESSING_SIGNAL = 32
    S_RECEIVED_AUDIO = 64
    S_CORRECTING_AUDIO = 128
    S_FINISHED_PROCESSING_AUDIO = 256
    S_ERROR = 1024

    # =====>>> PARAMETER name constants <<<===== #
    P_LAST_SIGNAL_FILE = "lastSignalFile"
    P_LAST_NL_TEXT_FILE = "lastNLTextFile"
    P_LAST_AUDIO_FILE = "lastAudioFile"
    P_RESPONSE_MODE = "responseMode"

    # =====>>> parameter VALUES <<<===== #
    PV_RESPONSE_FILE = "responseModeFile"
    PV_RESPONSE_JSON = "responseModeJSON"

    # =====>>> OTHER <<<===== #
    basenameExtractorRegex = re.compile(r"(?P<basename>.+?)(?P<rest>(_signals|\.)+.+)")

    # =====>>> Helper STATIC methods <<<===== #
    @staticmethod
    def toBytes(integer):
        # Maybe extend this with a loop but so far 1024 as the limit is ok
        return bytes([(0b11100000000 & integer) >> 8, 0b11111111 & integer])

    @staticmethod
    def fromBytes(byte):
        # Maybe extend this with a loop but so far 1024 as the limit is ok
        return (byte[0] << 8) | byte[1]

    @staticmethod
    def generateDatestring():
        return datetime.datetime.now().strftime('%Y_%b_%d-%H_%M_%S')

    # =====>>> Helper CLASS methods <<<===== #
    @classmethod
    def getState(cls):
        with open(cls.stateFilePath, 'rb') as statefile:
            state = cls.fromBytes(statefile.read())
        return state

    @classmethod
    def setState(cls, state):
        if isinstance(state, int):
            state = cls.toBytes(state)
        with open(cls.stateFilePath, 'wb') as statefile:
            state = statefile.write(state)

    @classmethod
    def writeLog(cls, message):
        with open(cls.logFilePath, 'a') as logFile:
            logFile.writeline(message)

    @classmethod
    def readLog(cls):
        with open(cls.logFilePath, 'rb') as logFile:
            logFile.seek(-2, os.SEEK_END)
            while logFile.read(1) != b'\n':
                logFile.seek(-2, os.SEEK_CUR)
            line = logFile.readline().decode()
        return line

    @classmethod
    def getConfig(cls, param=None):
        with open(cls.configFilePath, 'r') as cfg:
            config = yaml.load(cfg)
            if param is not None:
                try:
                    config = config[param]
                except:
                    config = None
        return config

    @classmethod
    def setConfig(cls, param, value):
        with open(cls.configFilePath, 'r') as cfg:
            config = yaml.load(cfg)
        config[param] = value
        with open(cls.configFilePath, 'w') as cfg:
            yaml.dump(config, cfg)

    @classmethod
    def regenerateConfig(cls):
        with open(cls.configFilePath, 'w') as cfg:
            # TODO: add more defaults to config
            yaml.dump({"flush": False, "responseMode": "responseModeFile"}, cfg)

    # =====>>> API initialization <<<===== #
    @classmethod
    def init_fsa(cls, address, port):
        print("The RESTful API to the Gherkan NL Instruction Processing system is starting...")

        # Check if the root folder is set correctly
        if not os.path.isdir(cls.rootFolder):
            raise Exception("The root folder is set to a non-existent path!\nRoot folder: {}".format(cls.rootFolder))
        if not os.access(cls.rootFolder, os.W_OK):
            raise Exception("Cannot write to the root folder!\nRoot folder: {}".format(cls.rootFolder))
        if not os.access(cls.rootFolder, os.R_OK):
            raise Exception("Cannot read from the root folder!\nRoot folder: {}".format(cls.rootFolder))


        # Check the existence of data folders
        if not os.path.isdir(cls.audioFolder):
            os.makedirs(cls.audioFolder)
        # if not os.path.isdir(cls.nlTextFolder):
        #     os.makedirs(cls.nlTextFolder)
        # if not os.path.isdir(cls.signalsFolder):
        #     os.makedirs(cls.signalsFolder)

        if not os.path.isfile(cls.configFilePath):
            cls.regenerateConfig()

        print("Host address: {}\nPort number: {}".format(address, port))
        cls.setConfig("host", address)
        cls.setConfig("port", port)

        print("Variable checking done, checking state from previous run...")
        # Check for previous sessions
        if os.path.exists(cls.stateFilePath):
            previousState = cls.getState()
            # Check and handle error
            if previousState == cls.S_ERROR:
                if cls.getConfig('flush'):
                    print("Found error state from a previous run.\nError flushing is set to True - flushing the error and reseting the system.")
                    previousState = cls.S_OFF
                    cls.regenerateConfig()
                else:
                    message = cls.readLog()
                    raise Exception("Previous run of the system resulted in an error! Resolve the error and set the fsa_config\nLast log message: {}".format(message))
            if previousState != cls.S_OFF:
                print("Found non-OFF state from previous run, restoring the system with state {}".format(previousState))
                cls.setState(previousState)
            else:
                # Set state to ready/idle
                print("System ready, state set to IDLE.")
                cls.setState(cls.S_IDLE)
        else:
            print("System ready, state set to IDLE.")
            cls.setState(cls.S_IDLE)

    # =====>>> RESTful API Call handling functions <<<===== #
    @classmethod
    def receiveSignal(cls, text):
        """This function handles the receiving of signal text.
        """

        state = cls.getState()
        if state & (cls.S_RECEIVED_AUDIO | cls.S_RECEIVED_NL_TEXT):
            raise Exception("Different data type already received!")

        if state & cls.S_RECEIVED_SIGNAL:
            signalFileMode = 'a'
            fileName = cls.getConfig(cls.P_LAST_SIGNAL_FILE)
        else:
            cls.setState(state | cls.S_RECEIVED_SIGNAL)
            signalFileMode = 'w'
            fileName = '_'.join([cls.generateDatestring(), 'signals.feature'])
            cls.setConfig(cls.P_LAST_SIGNAL_FILE, fileName)

        with open(fileName, signalFileMode) as sigFile:
            sigFile.writelines(text)

        # Signal text can be iteratively written into the file
        # When all signals were written, the user can request NL file

    @classmethod
    def requestSignal(cls):
        """This function return a composed signal file derived from NL text, if it was provided
        """
        state = cls.getState()
        if state & cls.S_RECEIVED_SIGNAL:  # Signals were sent and requested back (e.g. to check the state of the file)
            return send_file(cls.getConfig(cls.P_LAST_SIGNAL_FILE))
        elif not (state & cls.S_FINISHED_PROCESSING_NL_TEXT):  # Check if NL text was sent and processed
            raise Exception("NL text was not provided, cannot return signal file!")

        signalFilePath = cls.getConfig(cls.P_LAST_SIGNAL_FILE)

        responseMode = cls.getConfig(cls.P_RESPONSE_MODE)
        if responseMode == cls.PV_RESPONSE_FILE:
            response = send_file(signalFilePath)
        elif responseMode == cls.PV_RESPONSE_JSON:
            with open(signalFilePath, "r") as signalFile:
                signalText = signalFile.read()

            # TODO: Split file into response

            response = {
                    "language": "en<OR>cs",
                    "background": "background text",
                    "description": "optional description",
                    "scenarios": [
                        "scenario1 signal text",
                        "scenario2 signal text"
                    ]
            }

        cls.setState(state & ~cls.S_FINISHED_PROCESSING_NL_TEXT)
        return response

    @classmethod
    def requestNLText(cls):
        state = cls.getState()
        if not (state & cls.S_RECEIVED_SIGNAL):
            raise Exception("Signal file was not provided, cannot return NL text!")

        signalFilePath = cls.getConfig(cls.P_LAST_SIGNAL_FILE)

        path, filename = os.path.split(signalFilePath)
        outputFile = os.path.join(path, cls.basenameExtractorRegex.sub("\g<basename>"))

        signalToNL(signalFilePath)

        cls.setState(state & ~cls.S_RECEIVED_SIGNAL)

        responseMode = cls.getConfig(cls.P_RESPONSE_MODE)
        if responseMode == cls.PV_RESPONSE_FILE:
            response = send_file(outputFile)
        elif responseMode == cls.PV_RESPONSE_JSON:
            with open(outputFile, "r") as nlTextFile:
                nlText = nlTextFile.read()

            # TODO: parse text into response

            response = {
                "language":"en<OR>cz",
                "description": "optional description",
                "background": "background/context text",
                "scenarios": "scenarios text"
            }
        else:
            response = {"Message": "Request mode is set to an incorrect value!"}
        return response

    @classmethod
    def receiveNLText(cls, data):
        state = cls.getState()
        if state & (cls.S_RECEIVED_SIGNAL | cls.S_RECEIVED_AUDIO):
            raise Exception("Different data type already received!")

        cls.setState(state | cls.S_RECEIVED_NL_TEXT)

        basepath = os.path.join(cls.dataFolder, cls.generateDatestring())
        nlFilePath = f"{basepath}.feature"
        signalFilePath = f"{basepath}_signals.feature"

        nlToSignal(basepath, data)

        cls.setState((state & ~cls.S_RECEIVED_NL_TEXT) | cls.S_FINISHED_PROCESSING_NL_TEXT)
        cls.setConfig(cls.P_LAST_NL_TEXT_FILE, nlFilePath)
        cls.setConfig(cls.P_LAST_SIGNAL_FILE, signalFilePath)

        # TODO: return possible errors
        return {
            "info": "Processing done",
            "lines": [],
            "error_lines": [],
            "error_hints": [],
            "errors": False
        }

    @classmethod
    def receiveAudio(cls, audioPath):
        state = cls.getState()
        if state & (cls.S_RECEIVED_SIGNAL | cls.S_RECEIVED_NL_TEXT):
            raise Exception("Different data type already received!")

        transcriptPath = '.'.join(audioPath[:audioPath.find(".")], ".txt")
        speechToText(audioPath)

        return send_file(transcriptPath)

    @classmethod
    def requestRobotPrograms(cls, language):
        if not language:
            language = cls.language

        with open(cls.robotProgramsPath.format(language), 'r') as robotProgramFile:
            robotPrograms = robotProgramFile.read()

        return robotPrograms

    @classmethod
    def receiveRobotPrograms(cls, programs, language):
        if not language:
            language = cls.language

        with open(cls.robotProgramsPath.format(language), 'w') as robotProgramFile:
            robotProgramFile.writelines(programs)

    # =====>>> RESTful API Helper functions <<<===== #
    @classmethod
    def canRequestSignal(cls):
        """Checks whether it is possible to request a signal file.
        """
        state = cls.getState()
        return state & cls.S_FINISHED_PROCESSING_NL_TEXT

    @classmethod
    def canRequestNLText(cls):
        """Checks whether it is possible to request a NL text file.
        """
        state = cls.getState()
        return state & cls.S_RECEIVED_SIGNAL
