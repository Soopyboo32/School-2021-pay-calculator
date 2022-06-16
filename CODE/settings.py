import json

class SettingsClass:
    def __init__(self):
        with open("./CODE/settings.json", "r") as f:
            self.settingsData = json.load(f)
        
        self.needsUpdate = False
        self.interactData=None
    
    def getLanguage(self):
        return self.settingsData["localisation"]

    def setLanguage(self, language):
        self.settingsData["localisation"] = language
        self.needsUpdate = True
    
    def getDayOverTimePercentageUnder3(self, dayId):
        return self.settingsData["overTimePercentUnder3"][dayId]
    
    def setOverTimePercentageUnder3(self, dayId, val):
        self.settingsData["overTimePercentUnder3"][dayId] = val
        self.needsUpdate = True

        if(self.interactData):
            for key in self.interactData.dataStorages:
                self.interactData.dataStorages[key].updateCalculations()

    def getDayBaseRate(self, dayId):
        return self.settingsData["baseRate"][dayId]
    
    def setDayBaseRate(self, dayId, val):
        self.settingsData["baseRate"][dayId] = val
        self.needsUpdate = True

        if(self.interactData):
            for key in self.interactData.dataStorages:
                self.interactData.dataStorages[key].updateCalculations()

    def getDayOverTimePercentageOver3(self, dayId):
        return self.settingsData["overTimePercentOver3"][dayId]
    
    def setOverTimePercentageOver3(self, dayId, val):
        self.settingsData["overTimePercentOver3"][dayId] = val
        self.needsUpdate = True

        if(self.interactData):
            for key in self.interactData.dataStorages:
                self.interactData.dataStorages[key].updateCalculations()

    def getDayRegularHours(self, dayId):
        return self.settingsData["dayRegularHours"][dayId]
    
    def setDayRegularHours(self, dayId, val):
        self.settingsData["dayRegularHours"][dayId] = val
        self.needsUpdate = True

        if(self.interactData):
            for key in self.interactData.dataStorages:
                self.interactData.dataStorages[key].updateCalculations()

    def getDayBonusPay(self, dayId):
        return self.settingsData["bonusPay"][dayId]
    
    def setDayBonusPay(self, dayId, val):
        self.settingsData["bonusPay"][dayId] = val
        self.needsUpdate = True

        if(self.interactData):
            for key in self.interactData.dataStorages:
                self.interactData.dataStorages[key].updateCalculations()

    def saveToFile(self):
        if(self.needsUpdate):
            with open("./CODE/settings.json", "w") as f:
                json.dump(self.settingsData, f, indent=4)
            
            self.needsUpdate = False

    def setRecent(self, file, filename):
        newFiles = [(file, filename)]
        index = 0
        for tfile in self.settingsData["recentFiles"]:
            if(index >= 10):
                break;
            if(tfile[0] == file):
                continue
            
            newFiles.append((tfile[0], tfile[1]))
            index+= 1
        
        self.settingsData["recentFiles"] = newFiles
        self.needsUpdate = True

    def getRecent(self):
        resU = []
        for file in self.settingsData["recentFiles"]:
            resU.append((file[0], file[1]))
        
        return resU

Settings = SettingsClass()