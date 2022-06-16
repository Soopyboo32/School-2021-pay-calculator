import json
import traceback
import tkinter as tk
from tkinter import filedialog
from language import Translator
from data import InteractData
from tkinter import messagebox
from guiComponents.AboutGui import AboutGui
from guiComponents.SettingsGui import SettingsGui
from guiComponents.CustomNotebook import CustomNotebook
from guiComponents.EmployeeTab import EmployeeTab
from guiComponents.ManageJobPositionsGui import ManageJobPositionsGui
from guiComponents.AddEmployeeGui import AddEmployeeGui
from guiComponents.CreateJobPosition import CreateJobPosition
from settings import Settings


class PayGui(tk.Frame):
    def __init__(self):
        master = tk.Tk()
        super().__init__(master)
        self.master = master
        self.employeeTabs = []
        self.master.title(Translator.translateComponent("window.gui.title"))
        self.master.minsize(350, 250)
        self.master.resizable(False, False)
        self.needsReload = False
        self.employeePanel = None
        self.noteBook = CustomNotebook(self.master)
        self.noteBook.bind('<<NotebookTabChanged>>', self.noteBookTabChanged)
        self.noteBook.setCloseHandler(self.tabClosed)
        self.noteBook.pack(expand = 1, fill ="both")
        self.menuBar = self.initMenuBar()

        for employeedata in InteractData.dataStorages.values():      
            tab = EmployeeTab(self.noteBook, employeedata)
            self.noteBook.add(tab, text=tab.getTitle())
            self.employeeTabs.append(tab)
        
        if(len(self.employeeTabs)>0):
            self.initMenuBar()

        self.mainloop()
    
    def tabClosed(self, tab):
        shouldClose = True

        if(shouldClose):
            del InteractData.dataStorages[self.employeeTabs[tab].data.thisId]
            self.employeeTabs[tab].destroy()
            del self.employeeTabs[tab]
        
        self.initMenuBar()

        return shouldClose
    
    def shouldRespawn(self):
        return self.needsReload
    
    def initMenuBar(self):
        #Command bar is the bar at the top with like file, help ect
        menuBar = tk.Menu(self.master)

        self.master.option_add('*tearOff', False)
        
        #----------------  FILE CASCADE MENU ----------------------
        fileMenu = tk.Menu(menuBar)

        newWhat = tk.Menu(fileMenu)
        newWhat.add_command(label=Translator.translateComponent("filemenu.new.employeeFile"), command=self.menuCommandNewEmployeeFile)
        newWhat.add_separator()
        newWhat.add_command(label=Translator.translateComponent("filemenu.new.employee"), command=self.menuCommandNewEmployee, state=(tk.ACTIVE if len(self.employeeTabs)>0 else tk.DISABLED))
        newWhat.add_command(label=Translator.translateComponent("filemenu.new.jobPosition"), command=self.menuCommandNewJobPosition, state=(tk.ACTIVE if len(self.employeeTabs)>0 else tk.DISABLED))

        fileMenu.add_cascade(label=Translator.translateComponent("filemenu.new"), menu=newWhat)
        fileMenu.add_command(label=Translator.translateComponent("filemenu.open"), command=self.menuCommandOpen)

        #open recent intermission
        openRecent = tk.Menu(fileMenu)
        
        for recent in Settings.getRecent():
            def _():#scoping
                fileloc, filename = recent
                openRecent.add_command(label=filename, command=lambda:self.menuCommandOpenSpecific(fileloc))
            _()

        fileMenu.add_cascade(label=Translator.translateComponent("filemenu.openrecent"), menu=openRecent)

        fileMenu.add_command(label=Translator.translateComponent("filemenu.save.employeeData"), command=self.menuCommandSaveEmployee, state=((tk.ACTIVE if self.getSelectedTab().isSaved() else tk.DISABLED) if self.getSelectedTab() else tk.DISABLED))
        fileMenu.add_command(label=Translator.translateComponent("filemenu.save.employeeDataAs"), command=self.menuCommandSaveAsEmployee, state=(tk.ACTIVE if len(self.employeeTabs)>0 else tk.DISABLED))
        fileMenu.add_separator()
        fileMenu.add_command(label=Translator.translateComponent("filemenu.clear.hours"), command=self.menuCommandClearHours, state=(tk.ACTIVE if len(self.employeeTabs)>0 else tk.DISABLED))
        fileMenu.add_separator()
        fileMenu.add_command(label=Translator.translateComponent("filemenu.exit"), command=self.menuCommandClose)


        menuBar.add_cascade(label=Translator.translateComponent("filemenu.name"), menu=fileMenu)

    
        #----------------  MANAGE CASCADE MENU ----------------------
        manageMenu = tk.Menu(menuBar)
        manageMenu.add_command(label=Translator.translateComponent("managemenu.manageJobPositions"), command=self.menuCommandManageJobs, state=(tk.ACTIVE if len(self.employeeTabs)>0 else tk.DISABLED))
        manageMenu.add_command(label=Translator.translateComponent("managemenu.manageSettings"), command=self.menuCommandSettings)
    
        #----------------  HELP CASCADE MENU ----------------------
        helpMenu = tk.Menu(menuBar)
        helpMenu.add_command(label=Translator.translateComponent("helpmenu.about"), command=self.menuCommandAbout)

        #language selection
        languageMenu = tk.Menu(helpMenu)

        for language in Translator.getLanguages().items():
            languageMenu.add_command(label=language[1]["name"], command=self.loadLanguage(language[0]))

        helpMenu.add_cascade(label=Translator.translateComponent("helpmenu.translate"), menu=languageMenu)

        menuBar.add_cascade(label=Translator.translateComponent("managemenu.name"), menu=manageMenu)
        menuBar.add_cascade(label=Translator.translateComponent("helpmenu.name"), menu=helpMenu)

        self.master.config(menu=menuBar)

        return menuBar
    
    def loadLanguage(self, lang):
        def loadLanguage2():
            Translator.setLanguage(lang)
            self.reloadWindow()

        return loadLanguage2

    def reloadWindow(self):
        self.needsReload = True
        self.master.destroy()

    def menuCommandNewJobPosition(self):
        CreateJobPosition(self.getSelectedTab(), None, False)
        
    def menuCommandNewEmployee(self):
        AddEmployeeGui(self.getSelectedTab())
        
    def menuCommandManageJobs(self):
        ManageJobPositionsGui(self.getSelectedTab(), self.getSelectedTab().data)
    
    def getSelectedTab(self):
        if self.noteBook.select():
            return self.employeeTabs[self.noteBook.index('current')]
        return None

    def menuCommandNewEmployeeFile(self, data=None):
        tab = None
        if(data==None):
            tab = EmployeeTab(self.noteBook, InteractData.newEmployeeFile())
        else:
            tab = EmployeeTab(self.noteBook, data)
        self.noteBook.add(tab, text=tab.getTitle())
        self.employeeTabs.append(tab)
        self.noteBook.select(tab)
        self.initMenuBar()
     
    def noteBookTabChanged(self, _event):
        self.initMenuBar()

    def menuCommandOpen(self):
        possTypes = [(Translator.translateComponent("file.filetype.employee"), ".apaycalc")]
        file = filedialog.askopenfile(filetypes=possTypes)
        if(file == None):
            return #happens if the user clicks cancel
        
        try:
            newData = json.load(file)
            NewIData = InteractData.loadFromJSON(newData)
            NewIData.fileLocationFull = file.name
            partsArr = file.name.split("/")
            NewIData.filename = partsArr[len(partsArr)-1].split(".")[0]
            self.menuCommandNewEmployeeFile(NewIData)
        except Exception as e:
            #TODO: make into a dialog box maby
            print("[ERROR] Error during file loading")
            print(e)
            traceback.print_tb(e.__traceback__)
        file.close()
        
        Settings.setRecent(self.getSelectedTab().data.fileLocationFull, self.getSelectedTab().data.filename)
    def menuCommandOpenSpecific(self, file1):
        file = open(file1, "r")
        try:
            newData = json.load(file)
            NewIData = InteractData.loadFromJSON(newData)
            NewIData.fileLocationFull = file.name
            partsArr = file.name.split("/")
            NewIData.filename = partsArr[len(partsArr)-1].split(".")[0]
            self.menuCommandNewEmployeeFile(NewIData)
        except Exception as e:
            #TODO: make into a dialog box maby
            print("[ERROR] Error during file loading")
            print(e)
            traceback.print_tb(e.__traceback__)
        file.close()
        
        Settings.setRecent(self.getSelectedTab().data.fileLocationFull, self.getSelectedTab().data.filename)

    def menuCommandSaveEmployee(self):
        with open(self.getSelectedTab().data.fileLocationFull, "w") as file:
            json.dump(self.getSelectedTab().data.toJSON(), file)
        
        Settings.setRecent(self.getSelectedTab().data.fileLocationFull, self.getSelectedTab().data.filename)

    def menuCommandSaveAsEmployee(self):
        file = filedialog.asksaveasfile(defaultextension=".apaycalc",filetypes=[(Translator.translateComponent("file.filetype.employee"), ".apaycalc")])
        #file is a TextIOWrapper and so can have .write directly used on it
        if(file == None):
            return #happens if the user clicks cancel
        try:
            json.dump(self.getSelectedTab().data.toJSON(), file)
            self.getSelectedTab().data.fileLocationFull = file.name
            partsArr = file.name.split("/")
            self.getSelectedTab().data.filename = partsArr[len(partsArr)-1].split(".")[0]
            self.getSelectedTab().data.isEmployeeFileSaved = True
        except Exception as e:
            #TODO: make into a dialog box maby
            print("[ERROR] Error during file saving")
            print(e)
        file.close()

        Settings.setRecent(self.getSelectedTab().data.fileLocationFull, self.getSelectedTab().data.filename)
    
    def menuCommandSettings(self):
        SettingsGui(self)

    def menuCommandClose(self):
        self.master.destroy()
    def menuCommandClearHours(self):
        if(messagebox.askyesno(Translator.translateComponent("warning.clearhours.title"), Translator.translateComponent("warning.clearhours.message"), parent=self)):
            for id in self.getSelectedTab().data.getEmployeeIds():
                self.getSelectedTab().data.getEmployeeFromId(id).hoursWorked = {"0":0,"1":0,"2":0,"3":0,"4":0,"5":0,"6":0}
            self.getSelectedTab().updateEmployeePanel()
    def menuCommandAbout(self):
        AboutGui()