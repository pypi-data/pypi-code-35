from variablesGlobales    import FILE_LANGUAGE,FILE_LANGUAGE_DEFAULT,CONFIG_PATH
from configparser         import ConfigParser
class Language:

    instance=None
    def __init__(self,language=None):
        config                     = ConfigParser()
        if language is None:
            config_file = open(FILE_LANGUAGE_DEFAULT, encoding="utf-8")
            config.readfp(config_file)
        else:
            config_file = open(FILE_LANGUAGE+language+".lng", encoding="utf-8")
            config.readfp(config_file)
        
        #error
        self.ERROR_FIELD_EMPTY_FIRSTNAME       = config.get("error", "ERROR_FIELD_EMPTY_FIRSTNAME")
        self.ERROR_FIELD_INVALID_FIRSTNAME     = config.get("error", "ERROR_FIELD_INVALID_FIRSTNAME")
        self.ERROR_FIELD_EMPTY_FIRSTNAME       = config.get("error", "ERROR_FIELD_EMPTY_FIRSTNAME")
        self.ERROR_FIELD_INVALID_LASTNAME      = config.get("error", "ERROR_FIELD_INVALID_LASTNAME")
        self.ERROR_FIELD_EMPTY_PHONE           = config.get("error", "ERROR_FIELD_EMPTY_PHONE")
        self.ERROR_FIELD_EMPTY_FIRSTNAME       = config.get("error", "ERROR_FIELD_EMPTY_FIRSTNAME")
        self.ERROR_FIELD_EMPTY_LASTNAME        = config.get("error", "ERROR_FIELD_EMPTY_LASTNAME")
        self.ERROR_FIELD_INVALID_MAIL_FATHER   = config.get("error", "ERROR_FIELD_INVALID_MAIL_FATHER")
        self.ERROR_FIELD_INVALID_MAIL_MOTHER   = config.get("error", "ERROR_FIELD_INVALID_MAIL_MOTHER")
        self.ERROR_FIELD_INVALID_PHONE         = config.get("error", "ERROR_FIELD_INVALID_PHONE") 
        self.ERROR_FIND_IDENTIFICATION         = config.get("error", "ERROR_FIND_IDENTIFICATION")
        self.ERROR_NOT_FIND                    = config.get("error", "ERROR_NOT_FIND")                                                                                                                                   
        self.ERROR_FIELD_MAIL_IDENTICAL        = config.get("error", "ERROR_FIELD_MAIL_IDENTICAL")
        self.ERROR_FIELD_EMPTY_IDENTIFICATION  = config.get("error", "ERROR_FIELD_EMPTY_IDENTIFICATION")
        self.ERROR_SELECTION_ROW               = config.get("error", "ERROR_SELECTION_ROW")
        self.ERROR_FIELD_IDENTIFICATION        = config.get("error", "ERROR_FIELD_IDENTIFICATION")
        self.ERROR_THERE_IS_REGISTERED         = config.get("error", "ERROR_THERE_IS_REGISTERED")
        
        #label
        self.MESSAGE_OK_SAVE_STUDENT    = config.get("message", "MESSAGE_OK_SAVE_STUDENT")
        self.MESSAGE_FIRSTNAME          = config.get("message", "MESSAGE_FIRSTNAME")
        self.MESSAGE_PHONE              = config.get("message", "MESSAGE_PHONE")
        self.MESSAGE_LASTNAME           = config.get("message", "MESSAGE_LASTNAME")
        self.MESSAGE_IDENTICATION       = config.get("message", "MESSAGE_IDENTICATION")
        self.MESSAGE_FATHER_MAIL        = config.get("message", "MESSAGE_FATHER_MAIL")
        self.MESSAGE_MOTHER_MAIL        = config.get("message", "MESSAGE_MOTHER_MAIL")
        self.MESSAGE_STUDENT            = config.get("message", "MESSAGE_STUDENT")
        self.MESSAGE_HELP               = config.get("message", "MESSAGE_HELP")
        self.MESSAGE_FREQUENTLY_ASKED   = config.get("message", "MESSAGE_FREQUENTLY_ASKED")
        self.MESSAGE_PASS_LIST          = config.get("message", "MESSAGE_PASS_LIST")
        self.MESSAGE_MENU               = config.get("message", "MESSAGE_MENU")
        self.MESSAGE_PROCESS            = config.get("message", "MESSAGE_PROCESS")
        self.MESSAGE_DELETE_STUDENT     = config.get("message", "MESSAGE_DELETE_STUDENT")
        self.MESSAGE_SEND_ALL           = config.get("message", "MESSAGE_SEND_ALL")
        self.MESSAGE_SYSTEM             = config.get("message", "MESSAGE_SYSTEM")
        self.MESSAGE_PRESENT_ALL        = config.get("message", "MESSAGE_PRESENT_ALL")
        self.MESSAGE_NO_ATTENDANCE      = config.get("message", "MESSAGE_NO_ATTENDANCE")
        self.MESSAGE_SINCE              = config.get("message", "MESSAGE_SINCE")
        self.MESSAGE_UNTIL              = config.get("message", "MESSAGE_UNTIL")
        self.MESSAGE_ALL_KINDS          = config.get("message", "MESSAGE_ALL_KINDS")
        self.MESSAGE_NOT_REGISTERED     = config.get("message", "MESSAGE_NOT_REGISTERED")
        self.MESSAGE_ABSENCE            = config.get("message", "MESSAGE_ABSENCE")
        self.MESSAGE_STUDENT_TAB        = config.get("message", "MESSAGE_STUDENT_TAB")
        self.MESSAGE_CLASS_ALL          = config.get("message", "MESSAGE_CLASS_ALL")
        self.MESSAGE_MODIFY             = config.get("message", "MESSAGE_MODIFY")
        self.MESSAGE_QUERY              = config.get("message", "MESSAGE_QUERY")
        self.MESSAGE_LIST_STUDENT       = config.get("message", "MESSAGE_LIST_STUDENT")
        self.MESSAGE_EXIT               = config.get("message", "MESSAGE_EXIT")
        self.MESSAGE_SEND_MAIL          = config.get("message", "MESSAGE_SEND_MAIL")
        self.MESSAGE_CAME_ALL           = config.get("message", "MESSAGE_CAME_ALL")
        self.MESSAGE_EXIT               = config.get("message", "MESSAGE_EXIT")
        
        #button
        self.BUTTON_NEW                 = config.get("button", "BUTTON_NEW")
        self.BUTTON_SAVE                = config.get("button", "BUTTON_SAVE")
        self.BUTTON_DELETE              = config.get("button", "BUTTON_DELETE")
        self.BUTTON_QR_PRINT            = config.get("button", "BUTTON_QR_PRINT")
        self.BUTTON_MENU                = config.get("button", "BUTTON_MENU")
        self.BUTTON_HELP                = config.get("button", "BUTTON_HELP")
        self.BUTTON_STUDENTS            = config.get("button", "BUTTON_STUDENTS")
        self.BUTTON_QUERY               = config.get("button", "BUTTON_QUERY")
        self.BUTTON_EXIT                = config.get("button", "BUTTON_EXIT")
        self.BUTTON_PASS_LIST           = config.get("button", "BUTTON_PASS_LIST")
        self.BUTTON_ADD_MANUAL          = config.get("button", "BUTTON_ADD_MANUAL")
        self.BUTTON_FIND                = config.get("button", "BUTTON_FIND")
        self.BUTTON_LIST_STUDENTS       = config.get("button", "BUTTON_LIST_STUDENTS")
        self.BUTTON_STUDENT_SEE         = config.get("button", "BUTTON_STUDENT_SEE")
        self.BUTTON_STUDENT_LIST        = config.get("button", "BUTTON_STUDENT_LIST")
        self.BUTTON_BACK                = config.get("button", "BUTTON_BACK")
        self.BUTTON_LIST_PRINT          = config.get("button", "BUTTON_LIST_PRINT")
        self.BUTTON_STUDENT_PRINT       = config.get("button", "BUTTON_STUDENT_PRINT")
        
        #Tabla
        self.COLUMN_FIRSTNAME           = config.get("table", "COLUMN_FIRSTNAME")
        self.COLUMN_LASTNAME            = config.get("table", "COLUMN_LASTNAME")
        self.COLUMN_IDENTIFICATION      = config.get("table", "COLUMN_IDENTIFACTION")
        self.COLUMN_PRESENT             = config.get("table", "COLUMN_PRESENT")
        self.COLUMN_SKIPPED             = config.get("table", "COLUMN_SKIPPED")
        self.COLUMN_PORCENTAGE          = config.get("table", "COLUMN_PORCENTAGE")
        
        #Splash
        self.SPLASH_WELCOME             = config.get("splash", "SPLASH_WELCOME")
        self.SPLASH_NOTEBOOK            = config.get("splash", "SPLASH_NOTEBOOK")
        self.SPLASH_GREETING            = config.get("splash", "SPLASH_GREETING")
        
        #valid
        self.EXPRESSION_PHONE           = config.get("expression", "EXPRESSION_PHONE")
        self.EXPRESSION_NAME            = config.get("expression", "EXPRESSION_NAME")
        
        #Title
        self.TITLE_MAIN                 = config.get("title", "TITLE_MAIN")
        self.TITLE_CARD_STUDENT         = config.get("title", "TITLE_CARD_STUDENT")
        self.TITLE_HELP                 = config.get("title", "TITLE_HELP")
        self.TITLE_MODIFY               = config.get("title", "TITLE_MODIFY")
        self.TITLE_PASS_LIST            = config.get("title", "TITLE_PASS_LIST")
        self.TITLE_QUERY_STUDENT        = config.get("title", "TITLE_QUERY_STUDENT")
        self.TITLE_STUDENT_TAB          = config.get("title", "TITLE_STUDENT_TAB")
        self.TITLE_STUDENT_LIST         = config.get("title", "TITLE_STUDENT_LIST")
        
        #email
        self.TEMPLATE_MAIL             = config.get("email", "TEMPLATE_MAIL")
        
    @classmethod
    def getInstance(cls):
        if cls.instance is None:
            cls.instance=Language()
        return cls.instance
