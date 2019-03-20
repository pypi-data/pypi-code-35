#!/usr/bin/env python

import os
import httplib
import base64
from selenium import webdriver
from robot.libraries.BuiltIn import BuiltIn
from applitools import logger
from applitools.logger import StdoutLogger
from applitools.logger import FileLogger
from applitools.geometry import Region
from applitools.eyes import Eyes, BatchInfo
from applitools.selenium.webelement import EyesWebElement
from robot.api import logger as loggerRobot

from EyesLibrary.resources import utils, variables


class SessionKeywords(object):

    library_arguments = {}

    def open_eyes_session(
        self,
        apikey=None,
        appname=None,
        testname=None,
        library=None,
        width=None,
        height=None,
        osname=None,
        browsername=None,
        matchlevel=None,
        enable_eyes_log=None,
        enable_http_debug_log=None,
        baselinename=None,
        batchname=None,
        branchname=None,
        parentbranch=None,
    ):
        """
        Starts a session with the Applitools Eyes Website. See https://eyes.applitools.com/app/sessions/
        Some of the following arguments may also be defined on library import.~
        See `Before running tests` or `Importing`

                | *Arguments*                           | *Description*                                                                                               |
                |  API Key (string)                     | User's Applitools Eyes key.                                                                                 |
                |  Application Name (string)            | The name of the application under test.                                                                     |
                |  Test Name (string)                   | The test name.                                                                                              |  
                |  Library (default=SeleniumLibrary)    | Library to test (Either SeleniumLibrary or AppiumLibrary)                                                   |
                |  (Optional) Width (int)               | The width of the browser window e.g. 1280                                                                   |
                |  (Optional) Height (int)              | The height of the browser window e.g. 1000                                                                  |
                |  (Optional) Operating System (string) | The operating system of the test, can be used to override the OS name to allow cross OS verfication         |
                |  (Optional) Browser Name (string)     | The browser name for the test, can be used to override the browser name to allow cross browser verification  |
                |  (Optional) Match Level (string)      | The match level for the comparison - can be STRICT, LAYOUT, CONTENT or EXACT                                    |
                |  Enable Eyes Log (default=False)     | The Eyes logs will not be included by default. To activate, pass 'True' in the variable.                    |
                |  Enable HTTP Debug Log (default=False)       | The HTTP Debug logs will not be included by default. To activate, pass 'True' in the variable.              |
                |  Baseline Name (default=None)  | Name of the branch where the baseline reference will be taken from and where new and accepted steps will be saved to.                                                  |
                |  Batch Name (default=None)        | The name of the batch                      |
                |  Branch Name (default=None)  | The branch to use to check test                                                                             |
                |  Parent Branch (default=None)        | Parent Branch to base the new Branch on                                                                     |
        Creates an instance of the AppiumLibrary or SeleniumLibrary webdriver, given the library argument.

        Defines a global driver and sets the webdriver to the global driver.

        Checks if there has been a width or height value passed in.
        If there no are values passed in, eyes calls the method open without the width and height values.
        Otherwise, Eyes calls open with the width and height values defined.

        It is mandatory to define at least the Application Name, Test Name and API Key, either through this keyword or when importing the library. 

        *Note:* When opening the session on a mobile browser or hybrid app, the context must be set to WEBVIEW in order to retrieve the correct viewport size. Geolocation of the device may have to be set after switching context.

        *Example:*                                                                                                                                                                                                                               
                | Open Eyes Session  |   YourApplitoolsKey  | Eyes_AppName |  Eyes_TestName | SeleniumLibrary |  1024  |  768  |  OSOverrideName  |  BrowserOverrideName  |  LAYOUT   |  True  |  True  |  BranchName   |  ParentBranch   |
        """

        if appname is None:
            appname = self.library_arguments["appname"]
        if testname is None:
            testname = self.library_arguments["testname"]
        if apikey is None:
            apikey = self.library_arguments["apikey"]
        if library is None:
            library = self.library_arguments["library"]
        if osname is None:
            osname = self.library_arguments["osname"]
        if browsername is None:
            browsername = self.library_arguments["browsername"]
        if matchlevel is None:
            matchlevel = self.library_arguments["matchlevel"]
        if enable_eyes_log is None:
            enable_eyes_log = self.library_arguments["enable_eyes_log"]

        variables.eyes = Eyes()
        variables.eyes.api_key = apikey

        try:
            libraryInstance = BuiltIn().get_library_instance(library)

            if library == "AppiumLibrary":
                driver = libraryInstance._current_application()
            else:
                driver = libraryInstance._current_browser()
        except RuntimeError:
            raise Exception("%s instance not found" % library)

        utils.manage_logging(enable_eyes_log, enable_http_debug_log)

        if osname is not None:
            variables.eyes.host_os = osname  # (str)
        if browsername is not None:
            variables.eyes.host_app = browsername  # (str)
        if baselinename is not None:
            variables.eyes.baseline_branch_name = baselinename  # (str)
        if batchname is not None:
            batch = BatchInfo(batchname)
            variables.eyes.batch = batch
        if matchlevel is not None:
            variables.eyes.match_level = utils.get_match_level(matchlevel)
        if parentbranch is not None:
            variables.eyes.parent_branch_name = parentbranch  # (str)
        if branchname is not None:
            variables.eyes.branch_name = branchname  # (str)

        if width is None and height is None:
            variables.driver = variables.eyes.open(driver, appname, testname)
        else:
            intwidth = int(width)
            intheight = int(height)

            variables.driver = variables.eyes.open(
                driver, appname, testname, {"width": intwidth, "height": intheight}
            )

    def close_eyes_session(self, enable_eyes_log=False, enable_http_debug_log=False):
        """
        Closes a session and returns the results of the session.
        If a test is running, aborts it. Otherwise, does nothing.

                |  *Arguments*                      | *Description*                                                                                   |
                |  Enable Eyes Log (default=False) | The Eyes logs will not be included by default. To activate, pass 'True' in the variable.        |
                |  Enable HTTP Debug Log (default=False)   | The HTTP Debug logs will not be included by default. To activate, pass 'True' in the variable.  |

        *Example:*
            | Close Eyes Session    |    True   |   True    |                                 
        """
        utils.manage_logging(enable_eyes_log, enable_http_debug_log)

        variables.eyes.close()
        variables.eyes.abort_if_not_closed()

    def eyes_session_is_open(self):
        """
        Returns True if an Applitools Eyes session is currently running, otherwise it will return False.

        *Example:*
            | ${isOpen}=        |  Eyes Session Is Open     |                    
        """
        return variables.eyes.is_open
