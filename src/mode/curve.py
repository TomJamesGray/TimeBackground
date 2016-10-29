from src.mode import default
from src.helpers.helpers import getArgsBy
from src.helpers.getConfig import getConfigPart

class CurveImage(default.DefaultImage):
    def retrieveThemeConfig(self):
        self.colors = getArgsBy(getConfigPart(self.theme,"colours"),",")
    def drawImage(self):
        self.retrieveThemeConfig()


