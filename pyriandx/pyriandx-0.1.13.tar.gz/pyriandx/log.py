import coloredlogs, logging

coloredlogs.DEFAULT_LOG_FORMAT = '%(message)s'
coloredlogs.DEFAULT_LEVEL_STYLES = 'spam=22;debug=28;verbose=34;notice=220;warning=202;success=118,bold;error=124;critical=196' #color codes https://jonasjacek.github.io/colors/
coloredlogs.install(level='INFO')
log = logging.getLogger()

