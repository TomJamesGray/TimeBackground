import configparser
import os
def getConfigPart(section,key,optional=False):
    parser = configparser.SafeConfigParser()
    #Get absolute dir for config file
    configLocation = __file__.replace("helpers/getConfig.py","config.ini")
    parser.read(configLocation)
    try:
        value = parser.get(section,key)
    except configparser.NoOptionError as e:
        if not optional:
            raise e
            return None
        else:
            return None
    return value
