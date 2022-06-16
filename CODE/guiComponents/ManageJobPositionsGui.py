import tkinter as tk
from tkinter import messagebox
from language import Translator
from guiComponents.EntryWithPlaceholder import EntryWithPlaceholder
from guiComponents.CreateJobPosition import CreateJobPosition

class ManageJobPositionsGui(tk.Frame):
    def __init__(self, parent, data):
        master = tk.Toplevel()
        super().__init__(master)
        self.master = master
        self.parentGui = parent
        self.data = data
        self.window = None
        self.master.title(Translator.translateComponent("manageJobPositions.gui.title"))
        master.columnconfigure(0, weight=1)
        master.rowconfigure(0, weight=1)
        self.grid(row=0,column=0,sticky="nsew")
        self.initText()

        self.master.minsize(350, 250)

        self.update()
        self.master.resizable(False, False)

        # self.mainloop()
    
    def initText(self):

        if(self.window):
            self.window.destroy()

        self.window = tk.Frame(self)
        self.window.grid(row=0, column=0, sticky="nesw")

        rowCount = 0
        colCount = 0

        for posId in self.data.getJobPositionIds():
            position = self.data.getJobFromId(posId)

            button = tk.Button(self.window, text=Translator.translateComponent("manageJobPositions.button.edit"), command=self.editPosition(posId)).grid(row=rowCount, column=colCount)
            colCount+= 1

            label1 = tk.Label(self.window, text=position.getName()).grid(row=rowCount, column=colCount)
            colCount+= 1

            label2 = tk.Label(self.window, text=str(position.getPay()) + "$/h").grid(row=rowCount, column=colCount)
            colCount+= 1

            rowCount += 1
            colCount = 0
        
        button = tk.Button(self.window, text=Translator.translateComponent("manageJobPositions.button.add"), command=self.addNew).grid(row=rowCount, column=1)

        rowCount+= 1
        
    def addNew(self):
        CreateJobPosition(self)
    
    def editPosition(self, posId):
        def editPositionTemp():
            position = self.data.getJobFromId(posId)
            CreateJobPosition(self, position)
        
        return editPositionTemp
    
    def addJobPosition(self, jobPos):
        self.data.addJobPosition(jobPos)
        self.initText()
        self.parentGui.updateEmployeePanel()
    
    def editedJobPosition(self):
        self.initText()
        self.parentGui.updateEmployeePanel()