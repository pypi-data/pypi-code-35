# package com.games.thraxis.framework.application;
# 
# /##
#  # Holds constants used to
#  #
#  # Created by Zack on 9/28/2017.
#  #/
# 
# public interface TGApplicationConstants {
# 
# 	String CARD_PAGE_LOADED = "CARD_PAGE_LOADED";
# 	String CARD_DOWNLOAD_COMPLETE = "CARD_DOWNLOAD_COMPLETE";
# 	String CARD_SERVICE_FAILED = "CARD_SERVICE_FAILED";
# 	String FILE_READ_COMPLETE = "FILE_READ_COMPLETE";
# 	String DELIMITER = "@";
# 	String FILE_NAME = "MtgCardLibrary.txt";
# 	String ACTION_START_GAME = "ACTION_START_GAME";
# 	String ACTION_LOGIN = "ACTION_LOGIN";
# }
from abc import ABC


class TGConstantsInterface(ABC):
    def __init__(self):
        self.CARD_PAGE_LOADED = "CARD_PAGE_LOADED"
        self.CARD_DOWNLOAD_COMPLETE = "CARD_DOWNLOAD_COMPLETE"
        self.CARD_SERVICE_FAILED = "CARD_SERVICE_FAILED"
        self.FILE_READ_COMPLETE = "FILE_READ_COMPLETE"
        self.DELIMITER = "@"
        self.ACTION_START_GAME = "ACTION_START_GAME"
        self.ACTION_LOGIN = "ACTION_LOGIN"
