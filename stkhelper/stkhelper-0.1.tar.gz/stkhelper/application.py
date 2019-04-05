"""

Provides the Application class to create an STK11 object.

The purpose of this code is to add simplicity to STK integration with
the Python programming language.

"""

from win32api import GetSystemMetrics
from comtypes.client import CreateObject
from comtypes.gen import STKObjects

#Inner-package imports
from tle_manager import TLE_Manager
from processing import Processing

__author__ = "W. Conor McFerren"
__version__ = "0.1"
__maintainer__ = "W. Conor McFerren"
__email__ = "cnmcferren@gmail.com"

class Application:
    """
    
    Application object that holds the STK11 application
    
    """

#%% init Function
    
    def __init__(self):
        
        """
        
        Initialization function for the Application class. Creates a new
        application of STK11 and sets visibility and user control to true.
        Also initializes the list of area targets, the list of satellites,
        and the list of cameras.
        
        """
        
        self.uiApplication = CreateObject("STK11.Application")
        self.uiApplication.Visible = True
        self.uiApplication.UserControl = True
        
        self.root = self.uiApplication.Personality2
        
        self.areaTargetList = []
        self.satelliteList = []
        self.cameraList = []

#%% Methods to add objects
        
    def AddScenario(self, name, timePeriod):
        
        """
        
        Adds a scenario to the STK11 application (uiApplication) and
        creates the root.
        
        Parameters:
            name (str): Name of the new scenario
            timePeriod (str): Time period for the scenario to continue
            to. Written in the form "+24hr"
            
        """
        
        self.root.NewScenario(name.replace(' ','_'))
        self.scenario = self.root.CurrentScenario
        self.scenario = self.scenario.QueryInterface(STKObjects.IAgScenario)
        self.scenario.SetTimePeriod('Today',str(timePeriod))

    def AddSatellite(self, name, tleFile):
        
        """
        
        Adds satellite to the current scenario of the application.
        
        Parameters:
            name (str): Name of the satellite to be displayed in program.
            tleFile (str): Name of the TLE file to be used.
            
        """
        
        tle = TLE_Manager.ParseTLE(tleFile)
        self.scenario = self.scenario.QueryInterface(STKObjects.IAgScenario)
        satellite = self.root.CurrentScenario.Children.New(STKObjects.eSatellite, name)
        self.root.ExecuteCommand('SetState */Satellite/' + name + ' TLE "' +
                                 tle[0] + '" "' + tle[1] +
                                 '" TimePeriod "' +
                                 self.scenario.StartTime + '" "' +
                                 self.scenario.StopTime + '"')
        
        self.satelliteList.append([name, satellite])
        
    def AddCamera(self, name, hostSat, fovWidth, fovLength):
        
        """
        
        Adds a camera to a host satellite with a certain rectangular
        field of view.
        
        Parameters:
            name (str): Name of camera to be displayed in program.
            hostSat (STKObjects.eSatellite): Satellite to hold the camera.
            fovWidth (float): Width of field of view (in degrees).
            fovLength (float): Length of field of view (in degrees).
            
        """
        
        self.root.BeginUpdate()
        
        cameraGeneral = hostSat.Children.New(20, name)
        camera = cameraGeneral.QueryInterface(STKObjects.IAgSensor)
        camera.CommonTasks.SetPatternRectangular(fovWidth, fovLength)
        
        self.root.EndUpdate()
        
        self.cameraList.append([camera,cameraGeneral])
        
    def AddAreaTarget(self, name, coordPoints):
        
        """
        
        Adds area target to the scenario of the application
        
        Parameters:
            name (str): Name of area target to be displayed in program.
            coordPoints (list): List of tuples containing coordinate 
            representing coordinate pairs.
            
        """
        
        self.root.BeginUpdate()
        
        self.scenario = self.scenario.QueryInterface(STKObjects.IAgScenario)
        areaTarget = self.root.CurrentScenario.Children.New(STKObjects.eAreaTarget, name)
        areaTarget = areaTarget.QueryInterface(STKObjects.IAgAreaTarget)
        areaTarget.AreaType = STKObjects.ePattern
        patterns = areaTarget.AreaTypeData
        patterns = patterns.QueryInterface(STKObjects.IAgAreaTypePatternCollection)
        
        for i in range(len(coordPoints)):
            patterns.Add(coordPoints[i][0],coordPoints[i][1])
        
        areaTarget.AutoCentroid = True
        
        self.areaTargetList.append([areaTarget, name, patterns])
        
        self.root.EndUpdate()


#%% Access Functions
        
    def ComputeAccess(self, cameraArray, areaTargetArray):
        
        """
        
        Computes access between a camera and an area target and saves access
        to file with area targets name in the local directory.
        
        Parameters:
            cameraArray (list): List of camera and info from cameraList.
            areaTargetArray (list): List of area target and info from 
            areaTargetList.
        
        """
        
        self.root.BeginUpdate()
        
        access = cameraArray[1].GetAccessToObject(areaTargetArray[0])
        access.ComputeAccess()
        intervalCollection = access.ComputedAccessIntervalTimes
        try:
            computedIntervals = intervalCollection.ToArray(0,-1)
            filename = areaTargetArray[1] + '.txt'
            Processing.ArrayToFile(computedIntervals,filename)
        except Exception:
            filename = areaTargetArray[1] + '.txt'
            blankFile = open(filename,'w')
            blankFile.close()
            
        self.root.EndUpdate()
    
    def ComputeAllAccess(self, cameraArray):
        for i in range(len(self.areaTargetList)):
            self.ComputeAccess(cameraArray,self.areaTargetList[i])
            
#%% Setter Functions
        
    def SetTimePeriod(self, elapseTime):
        
        """
        
        Sets the time period of the scenario/
        
        Parameters:
            elapseTime (str): Time for scenario to run in the form "+24hr".
            
        """
        
        self.scenario.SetTimePeriod('Today',str(elapseTime))
        
#%% Getter Functions 
        
    def GetRoot(self):
        
        """
        
        Returns the root of the application.
        
        Returns:
            self.root: Root of the application.
            
        """
        
        return self.root
    
    def GetScenario(self):
        
        """
        
        Returns the scenario of the application.
        
        Returns:
            self.root: The scenario of the application.
            
        """
        
        return self.scenario
    
    def GetAreaTargets(self):
        
        """
        
        Returns the list of all area targets in the scenario.
        
        Returns:
            self.areaTargetList: List of area targets.
            
        """
        
        return self.areaTargetList
    
    def GetSatellites(self):
        
        """
        
        Returns the list of all satellites in the scenario.
        
        Returns:
            self.satelliteList: List of satellites.
            
        """
        
        return self.satelliteList
    
    def GetCameras(self):
        
        """
        
        Returns the list of all cameras in the scenario
        
        Returns:
            self.cameraList: List of all cameras
            
        """
        
        return self.cameraList

#%% STK Functions
        
    def CloseScenario(self):
        
        """
        
        INCOMPLETE
        
        """
        
        ##TODO Add code to close scenario when AGI Interface is back online.
        return 0
    
    def SaveScenario(self):
        
        """
        
        INCOMPLETE
        
        """
        
        ##TODO Add code to save scenario when AGI Interface is back online.
        return 0
    
    def TerminateApplication(self):
        
        """
        
        INCOMPLETE
        
        """
        
        ##TODO Add code to close entire program when AGI Interface is back online
        return 0
    
    