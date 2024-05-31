import re
import os
import sys
import datetime
import yaml
import logging
from logging.handlers import RotatingFileHandler


CONFIGFILE = os.environ['CONFIGPATH']
# CONFIGPATH = CONFIGFILE.replace('config.yml', '')


def upperescape(string, title_format):
    """Uppercase and Escape string. Used to help with YT-DL regex match.
    - ``string``: string to manipulate
    - ``title_format``: dict with format options
    - ``title_format.apply_default_format``: bool to use default format or not
    - ``title_format.make_ponctuation_optional``: bool to make ponctuations optional or not
    - ``title_format.prepend``: string to prepend to string
    - ``title_format.append``: string to append to string
    - ``title_format.remove_quotes``: bool to remove quotes
    - ``title_format.replace``: dict with string replacements
    - ``title_format.replace.key``: string to replace
    - ``title_format.replace.value``: string to replace with


    returns:
        ``string``: str new string
    """

    def remove_quotes(string):
        """ Replaces Punctuation Apostrophes by Typewriter Apostrophes
        See https://en.wikipedia.org/wiki/Apostrophe
        """
        string = string.replace('’',"'") 
        string = string.replace('“','"')
        string = string.replace('”','"')

        return string

    def make_ponctuation_optional(string):
        string = string.replace("'","([']?)") # optional apostrophe
        string = string.replace(",","([,]?)") # optional comma
        string = string.replace("!","([!]?)") # optional question mark
        string = string.replace("\\.","([\\.]?)") # optional period
        string = string.replace("\\?","([\\?]?)") # optional question mark
        string = string.replace(":","([:]?)") # optional colon

        return string

    def use_default_format(string):
        # UPPERCASE as YTDL is case insensitive for ease.
        string = string.upper()

        # Remove quote characters as YTDL converts these.
        string = remove_quotes(string)

        # Escape the characters
        string = re.escape(string)

        # Make it look for and as whole or ampersands
        string = string.replace('\\ AND\\ ','\\ (AND|&)\\ ')

        # Make punctuation optional for human error
        string = make_ponctuation_optional(string)
    
        string = re.sub("S\\\\", "([']?)"+"S\\\\", string) # optional belonging apostrophe (has to be last due to question mark)

        return string

    def apply_custom_formats(string, title_format):
        for key, value in title_format.items():
            if key == 'apply_default_format' and value == True:
                string = use_default_format(string)
            if key == 'make_ponctuation_optional' and value == True:
                string = make_ponctuation_optional(string)
            if key == 'prepend':
                string = value + string
            if key == 'append':
                string = string + value
            if key == 'remove_quotes' and value == True:
                string = remove_quotes(string)
            if key == 'replace' and value is not None:
                for key, value in value.items():
                    string = string.replace(key, value)
        
        return string


    try:
        string = apply_custom_formats(string, title_format)
    except Exception as e:
        # Handle the exception here
        print(f"An error occurred: {str(e)}")

    return string


def checkconfig():
    """Checks if config files exist in config path
    If no config available, will copy template to config folder and exit script

    returns:

        `cfg`: dict containing configuration values
    """
    logger = logging.getLogger('sonarr_youtubedl')
    config_template = os.path.abspath(CONFIGFILE + '.template')
    config_template_exists = os.path.exists(os.path.abspath(config_template))
    config_file = os.path.abspath(CONFIGFILE)
    config_file_exists = os.path.exists(os.path.abspath(config_file))
    if not config_file_exists:
        logger.critical('Configuration file not found.')  # print('Configuration file not found.')
        if not config_template_exists:
            os.system('cp /app/config.yml.template ' + config_template)
        logger.critical("Create a config.yml using config.yml.template as an example.")  # sys.exit("Create a config.yml using config.yml.template as an example.")
        sys.exit()
    else:
        logger.info('Configuration Found. Loading file.')  # print('Configuration Found. Loading file.')
        with open(
            config_file,
            "r"
        ) as ymlfile:
            cfg = yaml.load(
                ymlfile,
                Loader=yaml.BaseLoader
            )
        return cfg


def offsethandler(airdate, offset):
    """Adjusts an episodes airdate
    - ``airdate``: Airdate from sonarr # (datetime)
    - ``offset``: Offset from series config.yml # (dict)

    returns:
        ``airdate``: datetime updated original airdate
    """
    weeks = 0
    days = 0
    hours = 0
    minutes = 0
    if 'weeks' in offset:
        weeks = int(offset['weeks'])
    if 'days' in offset:
        days = int(offset['days'])
    if 'hours' in offset:
        hours = int(offset['hours'])
    if 'minutes' in offset:
        minutes = int(offset['minutes'])
    airdate = airdate + datetime.timedelta(weeks=weeks, days=days, hours=hours, minutes=minutes)
    return airdate


class YoutubeDLLogger(object):

    def __init__(self):
        self.logger = logging.getLogger('sonarr_youtubedl')

    def info(self, msg: str) -> None:
        self.logger.info(msg)

    def debug(self, msg: str) -> None:
        self.logger.debug(msg)

    def warning(self, msg: str) -> None:
        self.logger.info(msg)

    def error(self, msg: str) -> None:
        self.logger.error(msg)


def ytdl_hooks_debug(d):
    logger = logging.getLogger('sonarr_youtubedl')
    if d['status'] == 'finished':
        file_tuple = os.path.split(os.path.abspath(d['filename']))
        logger.info("      Done downloading {}".format(file_tuple[1]))  # print("Done downloading {}".format(file_tuple[1]))
    if d['status'] == 'downloading':
        progress = "      {} - {} - {}".format(d['filename'], d['_percent_str'], d['_eta_str'])
        logger.debug(progress)


def ytdl_hooks(d):
    logger = logging.getLogger('sonarr_youtubedl')
    if d['status'] == 'finished':
        file_tuple = os.path.split(os.path.abspath(d['filename']))
        logger.info("      Downloaded - {}".format(file_tuple[1]))

def setup_logging(lf_enabled=True, lc_enabled=True, debugging=False):
    log_level = logging.INFO
    log_level = logging.DEBUG if debugging == True else log_level
    logger = logging.getLogger('sonarr_youtubedl')
    logger.setLevel(log_level)
    log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    if lf_enabled:
        # setup logfile
        log_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'logs'))
        log_file = os.path.abspath(log_file + '/sonarr_youtubedl.log')
        loggerfile = RotatingFileHandler(
            log_file,
            maxBytes=5000000,
            backupCount=5
        )
        loggerfile.setLevel(log_level)
        loggerfile.set_name('FileHandler')
        loggerfile.setFormatter(log_format)
        logger.addHandler(loggerfile)

    if lc_enabled:
        # setup console log
        loggerconsole = logging.StreamHandler()
        loggerconsole.setLevel(log_level)
        loggerconsole.set_name('StreamHandler')
        loggerconsole.setFormatter(log_format)
        logger.addHandler(loggerconsole)

    return logger
