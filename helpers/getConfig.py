from configparser import SafeConfigParser
import os
def getConfigPart(section,key):
    parser = SafeConfigParser()
    #Get absolute dir for config file
    configLocation = __file__.replace("helpers/getConfig.py","config.ini")
    parser.read(configLocation)
    return parser.get(section,key)
