import os
import numpy as np
import math
from datetime import datetime, timedelta
from typing import List, Tuple

# import from package
from resistics.ioHandlers.ioHandler import IOHandler
from resistics.dataObjects.calibrationData import CalibrationData
from resistics.utilities.utilsIO import checkAndMakeDir
from resistics.utilities.utilsPrint import listToString


class CalibrationIO(IOHandler):
    """Class for reading and writing calibration files

    Calibration files hold impulse response data for instruments and sensors that needs to be removed from time series data.

    Calibration data is stored in:
    project -> calData

    Attributes
    ----------
    datafile : str
        Path to calibration data file
    extend : bool
        Boolean flag for extending (extrapolating) the calibration data

    Methods
    -------
    __init__(datapath, fileformat, chopper, extend)
        Initialise the CalibrationIO object.
    refresh(datapath, fileformat, chopper, extend)
        Refresh the CalibrationIO parameters
    read()
        Read calibration file
    readInductionData()
        Read internal format calibration file for induction coils        
    readMetronixData()
        Read metronix style calibration file for induction coils
    readRSPData()
        Read RSP style calibration file for induction coils
    readRSPXData()
        Read RSPX style calibration file for induction coils
    readInternalFormat()
        Read internal format calibration file
    unitCalibration()
        A unit calibration, used if nothing else is found
    sortCalData(data)
        Sort calibration data into ascending order (lower to higher)
    extendCalData(data)
        Extrapolate the calibration data to higher and lower frequencies
    linesToArray(dataLines)
        Convert a set of data lines in a calibration file into a list    
    writeInternalFormat()
        Write internal format calibration file
    printList()
        Class status returned as list of strings       
	"""

    def __init__(
        self,
        datafile: str = "",
        fileformat: str = "induction",
        chopper: bool = False,
        extend: bool = True,
    ) -> None:
        """Initialise CalibrationIO

        Parameters
        ----------
        datafile : str, optional
            Path to calibration data file
        format : str, optional
            Calibration file format
        chopper : bool
            Boolean flag for reading chopper on or off data, mostly used with metronix data
        extend : bool
            Boolean flag for extrapolating the calibration data
        """

        self.refresh(datafile, fileformat, chopper, extend)

    def refresh(
        self,
        datafile: str = "",
        fileformat: str = "inductiontxt",
        chopper: bool = False,
        extend: bool = True,
    ) -> None:
        """Refresh the CalibrationIO parameters

        Parameters
        ----------
        datafile : str, optional
            Path to calibration data file
        format : str, optional
            Calibration file format
        chopper : bool
            Boolean flag for reading chopper on or off data, mostly used with metronix data
        extend : bool
            Boolean flag for extrapolating the calibration data
        """

        self.datafile: str = datafile
        self.fileformat: str = fileformat
        self.chopper: bool = chopper
        self.extend: bool = extend

    def read(self) -> CalibrationData:
        """Read data from calibration file and return CalibrationData object

        Notes
        -----
        Data for magnetic channel calibration is returned with units: F [Hz], Magnitude [mV/nT], Phase [radians]

        Returns
        -------
        CalibrationData
            A calibration data object
        """

        if self.fileformat == "metronix":
            return self.readMetronixData()
        elif self.fileformat == "rsp":
            return self.readRSPData()
        elif self.fileformat == "rspx":
            return self.readRSPXData()
        elif self.fileformat == "induction":
            return self.readInductionData()
        else:
            return self.unitCalibration()

    def readInductionData(self):
        """Read data from a text based calibration file for induction coils
        
        Text based calibration files should be used when reading of other formats appears to be failing or are not supported. 

        Notes
        -----
        Data in file is assumed to be in units: F [Hz], Magnitude [mv/nT], Phase [degrees or radians]
        Data is returned with units: F [Hz], Magnitude [mV/nT], Phase [radians]

        Returns
        -------
        CalibrationData
            A calibration data object
        """

        calData = self.readInternalFormat()
        return calData

    def readMetronixData(self) -> CalibrationData:
        """Read data from metronix calibration file
        
        Notes
        -----
        Metronix data is in units: F [Hz], Magnitude [V/nT*Hz], Phase [deg] for both chopper on and off.
        Data is returned with units: F [Hz], Magnitude [mV/nT], Phase [radians].  

        Returns
        -------
        CalibrationData
            A calibration data object
        """

        with open(self.datafile, "r") as f:
            lines = f.readlines()
        numLines = len(lines)

        # no static gain - already included
        staticGain: float = 1
        # variables to save line numbers
        chopperOn: int = 0
        chopperOff: int = 0
        # find locations for chopperOn and chopperOff
        for il in range(0, numLines):
            # remove whitespace and new line characters
            lines[il] = lines[il].strip()
            if "Chopper On" in lines[il]:
                chopperOn = il
            if "Chopper Off" in lines[il]:
                chopperOff = il

        # get the part of the file required depending on chopper on or off
        dataLines: List = []
        dataReadFrom: int = chopperOff
        if self.chopper:
            dataReadFrom = chopperOn
        # get the data - starting from the next line
        il = dataReadFrom + 1
        while il < numLines and lines[il] != "":
            # save line then increment
            dataLines.append(lines[il])
            il = il + 1

        # get the data as an array
        data = self.linesToArray(dataLines)
        # sort and extend
        data = self.sortCalData(data)
        if self.extend:
            data = self.extendCalData(data)
        # unit manipulation - change V/(nT*Hz) to mV/nT
        data[:, 1] = data[:, 1] * data[:, 0] * 1000
        # unit manipulation - change phase to radians
        data[:, 2] = data[:, 2] * (math.pi / 180)

        return CalibrationData(
            self.datafile,
            data[:, 0],
            data[:, 1],
            data[:, 2],
            staticGain=staticGain,
            chopper=self.chopper,
        )

    def readRSPData(self) -> CalibrationData:
        """Read data from a RSP calibration file
        
        Notes
        -----        
        RSP data is in units: F [Hz], Magnitude [mv/nT], Phase [deg]
        Data is returned with units: F [Hz], Magnitude [mV/nT], Phase [radians]

        Returns
        -------
        CalibrationData
            A calibration data object
        """

        with open(self.datafile, "r") as f:
            lines = f.readlines()
        numLines = len(lines)

        staticGain = 1
        dataReadFrom = 0
        for il in range(0, numLines):
            # remove whitespace and new line characters
            lines[il] = lines[il].strip()
            # find static gain value
            if "StaticGain" in lines[il]:
                staticGain = float(lines[il].split()[1])
            if "FREQUENCY" in lines[il]:
                dataReadFrom = il
        dataLines = []
        il = dataReadFrom + 2
        # get part of file desired
        while il < numLines and lines[il] != "":
            # save line then increment
            dataLines.append(lines[il])
            il = il + 1

        # get the data as an array
        data = self.linesToArray(dataLines)
        # unit manipulation - change phase to radians and apply static gain
        data[:, 1] = data[:, 1] * staticGain
        data[:, 2] = data[:, 2] * (math.pi / 180)
        # sort and extend
        data = self.sortCalData(data)
        if self.extend:
            data = self.extendCalData(data)

        return CalibrationData(
            self.datafile, data[:, 0], data[:, 1], data[:, 2], staticGain
        )

    def readRSPXData(self) -> CalibrationData:
        """Read data from calibration file
        
        Notes
        -----
        RSPX data is in units: F [Hz], Magnitude [mv/nT], Phase [deg]
        Data is returned with units: F [Hz], Magnitude [mV/nT], Phase [radians]

        Returns
        -------
        CalibrationData
            A calibration data object
        """

        # this is xml format - use EL tree
        import xml.etree.ElementTree as ET

        tree = ET.parse(self.datafile)
        root = tree.getroot()
        # static gain
        staticGain = 1
        if root.find("StaticGain") is not None:
            staticGain = float(root.find("StaticGain").text)
        # get the calibration data
        dataList = []
        for resp in root.findall("ResponseData"):
            dataList.append(
                [
                    float(resp.get("Frequency")),
                    float(resp.get("Magnitude")),
                    float(resp.get("Phase")),
                ]
            )
        # now create array
        data = np.array(dataList)
        # change phase to radians and apply static gain
        data[:, 1] = data[:, 1] * staticGain
        data[:, 2] = data[:, 2] * (math.pi / 180)
        # sort and extend
        data = self.sortCalData(data)
        if self.extend:
            data = self.extendCalData(data)

        return CalibrationData(
            self.datafile, data[:, 0], data[:, 1], data[:, 2], staticGain
        )

    def unitCalibration(self) -> CalibrationData:
        """Return a unit calibration

        Returns
        -------
        CalibrationData
            A calibration data object
        """

        data = np.array([[0.0000001, 1, 0], [100000000, 1, 0]])
        staticGain = 1
        return CalibrationData(
            self.datafile, data[:, 0], data[:, 1], data[:, 2], staticGain
        )

    def readInternalFormat(self):
        """Read data from a text based calibration file for any type of instrument 

        Notes
        -----
        Text based calibration files should be used when reading of other formats appears to be failing or are not supported. Nothing is assumed or promised about the data units.

        Returns
        -------
        CalibrationData
            A calibration data object
        """

        with open(self.datafile, "r") as f:
            lines = f.readlines()

        for il, line in enumerate(lines):
            if "Serial" in line:
                serial = int(line.split("=")[1].strip())
            if "Static gain" in line:
                staticGain = float(line.split("=")[1].strip())
            if "Magnitude unit" in line:
                magnitudeUnit = line.split("=")[1].strip()
            if "Phase unit" in line:
                phaseUnit = line.split("=")[1].strip()
            if "Chopper" in line:
                chopper = bool(line.split("=")[1].strip())
            if "CALIBRATION DATA" in line:
                dataReadFrom = il + 1
                break

        dataLines = lines[dataReadFrom:]
        data = self.linesToArray(dataLines)
        # sort and extend
        data = self.sortCalData(data)
        if self.extend:
            data = self.extendCalData(data)        
        # apply static gain
        data[:, 1] = data[:, 1] * staticGain
        if phaseUnit == "degrees":
            data[:, 2] = data[:, 2] * (math.pi / 180)

        calData = CalibrationData(
            self.datafile, data[:, 0], data[:, 1], data[:, 2], staticGain, chopper
        )
        calData.magnitudeUnit = magnitudeUnit
        calData.phaseUnit = "radians"
        calData.serial = serial
        return calData

    def sortCalData(self, data: np.ndarray) -> np.ndarray:
        """Sort calibration data by frequency ascending (low to high)

        Parameters
        ----------
        data : np.ndarray
            Unsorted calibration data   

        Returns
        -------
        data : np.ndarray
            Sorted calibration data
        """

        return data[data[:, 0].argsort()]

    def extendCalData(self, data: np.ndarray) -> np.ndarray:
        """Extend calibration data by frequency

        Add extra points at the start and end of the calibration data to ensure complete coverage with the time data. 

        Notes
        -----
        It is assumed that the calibration data is already sorted in ascending order (using sortCalData)

        Parameters
        ----------
        data : np.ndarray
            Calibration data   

        Returns
        -------
        data : np.ndarray
            Extended calibration data
        """

        if data[0, 0] > 0.0000001:
            # add a line at the top (low frequency) extending the calibration information
            data = np.vstack((np.array([0.0000001, data[0, 1], data[0, 2]]), data))
        if data[-1, 0] < 100000000:
            # add a line at the top (high frequency) extending the calibration information
            data = np.vstack((data, np.array([100000000, data[-1, 1], data[-1, 2]])))
        return data

    def linesToArray(self, dataLines: List) -> np.ndarray:
        """Convert data lines from a file to an array

        Parameters
        ----------
        dataLines : list
            Data lines read in from a file   

        Returns
        -------
        data : np.ndarray
            Data lines converted to a float array
        """

        # data to columns
        numData = len(dataLines)
        for il in range(0, numData):
            dataLines[il] = dataLines[il].split()
        return np.array(dataLines, dtype=float)

    def writeInternalFormat(self, calData: CalibrationData, filepath: str) -> None:
        """Write out a calibration data file

        Parameters
        ----------
        calibrationData : CalibrationData
            Calibration data to write out
        filepath : str
            The file to write out to
        """

        with open(filepath, "w") as f:
            f.write("Serial = {}\n".format(calData.serial))
            f.write("Static gain = {}\n".format(calData.staticGain))
            f.write("Magnitude unit = {}\n".format(calData.magnitudeUnit))
            f.write("Phase unit = {}\n".format(calData.phaseUnit))
            f.write("Chopper = {}\n".format(calData.chopper))
            f.write("\n")
            f.write("CALIBRATION DATA\n")
            for ii in range(0, calData.numSamples):
                f.write(
                    "{:+.4e}  {:+.4e}  {:+.4e}\n".format(
                        calData.freqs[ii], calData.magnitude[ii], calData.phase[ii]
                    )
                )

    def printList(self) -> List[str]:
        """Class information as a list of strings

        Returns
        -------
        out : List[str]
            List of strings with information
        """

        textLst = []
        if self.datafile == "":
            textLst.append(
                "No datafile given. Please set the datafile attribute of the class"
            )
        else:
            textLst.append("datafile = {}".format(self.datafile))
        textLst.append("Extend = {}".format(self.extend))
        return textLst
