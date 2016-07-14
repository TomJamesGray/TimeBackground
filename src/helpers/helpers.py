import re
def getArgsBy(argString,regExp,strip=True):
    if strip:
        argString = argString.strip()
    return re.split(regExp, argString)
