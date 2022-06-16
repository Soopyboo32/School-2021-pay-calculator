import json

from settings import Settings

class TranslatorClass:
    def __init__(self):
        self.selectedLanguage = Settings.getLanguage()
        self.defaultLanguage = "english"
        self.translationData = None
        self.loadedTranslations = False
        self.aboutData = None

        self.addToTranslationFileWhenNotFound = False # disable when not in dev or making placeholder translation file
        
        with open("./CODE/translations.json", "r") as file:
            self.allTranslationData = json.load(file)
        
    def reloadLanguage(self):
        try:
            with open("./CODE/translations/" + self.selectedLanguage + ".json", "r") as file:
                self.translationData = json.load(file)
            
            self.aboutData = open("./CODE/about/" + self.selectedLanguage + ".txt", "r").read()
        except:
            #File not found? lmfao editing config moment
            self.setLanguage(self.defaultLanguage)
            self.reloadLanguage()
            return;
        
        self.loadedTranslations = True

    def translateComponent(self, key):
        if (not self.loadedTranslations):
            self.reloadLanguage()

        if(key in self.translationData["translations"]):
            return self.translationData["translations"][key]
        else:
            print("[WARNING] No " + self.selectedLanguage + " translation defined for " + key)

            if (self.addToTranslationFileWhenNotFound):
                self.translationData["translations"][key] = key
                
                with open("./CODE/translations/english.json", "w") as file:
                    json.dump(self.translationData, file, indent=4, sort_keys=True)

            return key
    
    def getAbout(self):
        return self.aboutData

    def setLanguage(self, lang):
        self.selectedLanguage = lang
        self.translationData = None
        self.loadedTranslations = False
        self.aboutData = None
        Settings.setLanguage(lang)
    
    def getLanguages(self):
        return self.allTranslationData

Translator = TranslatorClass()