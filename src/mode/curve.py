import logging
from src.mode import default
from src.helpers.helpers import getArgsBy
from src.helpers.getConfig import getConfigPart

class CurveImage(default.DefaultImage):
    def retrieveThemeConfig(self):
        colorsTemp = getArgsBy(getConfigPart(self.theme,"colours"),",")
        self.colors = []
        for col in colorsTemp:
            tempList = []
            for val in col.split("-"):
                tempList.append(int(val))
            self.colors.append(tuple(tempList))


    def drawImage(self):
        self.retrieveThemeConfig()


