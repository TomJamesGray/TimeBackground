import time
from src.helpers.helpers import getArgsBy
from src.helpers.getConfig import getConfigPart
from src.mode.default import DefaultImage
import src.main
#This class in itself isn't a theme however implements the same basic
#functions such as drawImage, which will in this case draw the 
#image on the parameters provided on the theme for the specified time
class TimeMode(DefaultImage):
    def __init__(self,width,height,theme,superSampling,fileName):
        self.localTime = time.strftime("%H%M")
        self.width = width
        self.height = height
        self.fileName = fileName
        self.theme = theme
        self.superSampling = superSampling

    def retrieveThemeConfig(self):
        self.timeSections = getArgsBy(getConfigPart(self.theme,"timeSections"),",")
        self.themes = getArgsBy(getConfigPart(self.theme,"modes"),",")

    def drawImage(self):
        self.retrieveThemeConfig()
        for i in range(0,len(self.timeSections)):
            if self.timeSections[i] < self.localTime and self.localTime < self.timeSections[i+1]:
                #The current time falls between this part of the time sections
                #in the config file, so use the corresponding theme
                self.currentTheme = self.themes[i]
                #Call main function with all args as string, as if calling
                #from command line, possibly improve with use of 
                #**kwargs?
                if not self.superSampling:
                    main.main(['Something',self.width,self.height,self.fileName,
                        "--theme=" + self.currentTheme])
                elif self.superSampling:
                    main.main(['Something',self.width,self.height,self.fileName,
                        '-s','--theme=' + self.currentTheme])
                else:
                    raise ValueError("Somehow there's no value for superSampling \
                            this error should never really be raised but just in case")
