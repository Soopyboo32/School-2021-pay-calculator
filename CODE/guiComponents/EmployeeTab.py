import tkinter as tk
from tkinter import messagebox
from language import Translator
from data import InteractData
from guiComponents.EntryWithPlaceholder import EntryWithPlaceholder
from guiComponents.AddEmployeeGui import AddEmployeeGui

class EmployeeTab(tk.Frame):
    def __init__(self, master, data):
        super().__init__(master)
        self.master = master
        self.data = data

        self.payElements = {}

        self.employeePanel = None
        # master.columnconfigure(0, weight=1)
        # master.rowconfigure(0, weight=1)
        self.grid(row=0,column=0,sticky="nsew")
        self.updateEmployeePanel()

        self.update()

        data.setParentTab(self)

        # self.mainloop()
    
    def getTitle(self):
        return self.getEmployeeTitle() if self.isSaved() else Translator.translateComponent("tab.title.unsaved")
    
    def getEmployeeTitle(self):
        return self.data.filename

    def isSaved(self):
        return self.data.isEmployeeFileSaved

    def addEmployee(self):
        AddEmployeeGui(self)
        
    def updateEmployeePanel(self):

        self.payElements = {}

        file = tk.Frame(self)

        currRow = 0
        
        currColl = 1

        tk.Label(file, text=Translator.translateComponent("main.title.employees")).grid(row=currRow, column=currColl)

        currColl += 1

        for day in InteractData.getWeekDayIds():
            tk.Label(file, text=InteractData.getDayNameFromId(day)).grid(row=currRow, column=currColl)
            currColl += 1

        tk.Label(file, text=Translator.translateComponent("main.bonus")).grid(row=currRow, column=currColl)
        currColl += 1
        tk.Label(file, text=Translator.translateComponent("main.weeklypay")).grid(row=currRow, column=currColl)
        currColl += 1
        
        currRow+= 1
        for ID in self.data.getEmployeeIds():
            employee = self.data.getEmployeeFromId(ID)
            currColl= 0
            
            tk.Button(file,text=Translator.translateComponent("gui.button.editEmployee"), command=self.editEmployee(ID)).grid(row=currRow, column=currColl)

            currColl+= 1
            tk.Label(file, text=employee.getName() + " (" + (employee.jobPosition.getName() if employee.jobPosition else "None") + ")").grid(row=currRow, column=currColl)

            currColl+= 1

            for day in InteractData.getWeekDayIds():
                def _(): # scoping
                    dayId = day
                    employeeId = ID
                    startVal = employee.getHoursWorked(dayId)

                    entry = EntryWithPlaceholder(file, "0", 'grey', vcmd=self.validate_float, width=4, onChange=lambda value: self.onChange(employeeId, dayId, value))
                    
                    if(startVal > 0):
                        if(startVal%1==0):
                            entry.setText(int(startVal))
                        else:
                            entry.setText(startVal)
                    entry.grid(row=currRow, column=currColl)
                _()
                currColl += 1
                
            def _(): # scoping
                employeeId = ID
                startVal = employee.getBonus()
                bonus = EntryWithPlaceholder(file, "0", 'grey', vcmd=self.validate_float_no_max, width=4, onChange=lambda value: self.onChange(employeeId, -1, value))
                bonus.grid(row=currRow, column=currColl)
                
                if(startVal > 0):
                    if(startVal%1==0):
                        bonus.setText(int(startVal))
                    else:
                        bonus.setText(startVal)
            _()
            currColl += 1
            
            self.payElements[employee.getId()] = tk.StringVar()
            payLabel = tk.Label(file, textvariable=self.payElements[employee.getId()])
            payLabel.grid(row=currRow, column=currColl)
            currColl += 1 

            currRow+= 1


        tk.Button(file,text=Translator.translateComponent("gui.button.newEmployee"), command=self.addEmployee).grid(row=currRow, column=1)
        
        file.grid(row=0, column=0)

        if(self.employeePanel):
            self.employeePanel.destroy()

        self.employeePanel = file

        self.updatePay()
    
    def onChange(self, employeeId, dayId, newValue):
        employee = self.data.getEmployeeFromId(employeeId)
        if(newValue == ""):
            newValue = "0"
        try:
            if(dayId == -1):
                employee.setBonus(float(newValue))
            else:
                employee.setHoursWorked(dayId, float(newValue))
        except:
            return
    
    def updatePay(self):
        for id in self.payElements:
            employee = self.data.getEmployeeFromId(id)
            self.payElements[id].set(Translator.translateComponent("pay.currencySymbol") + str(employee.getTotalPay()["pay"]))

    def validate_float(self, action, index, value_if_allowed,
        prior_value, text, validation_type, trigger_type, widget_name):
        # action=1 -> insert
        if(action=='1'):
            try:
                val = float(value_if_allowed)
                if(val <0):
                    messagebox.showerror(Translator.translateComponent("warning.employee.hours.under0.title"), Translator.translateComponent("warning.employee.hours.under0.message"), parent=self)
                    return False
                if(val > 24):
                    messagebox.showerror(Translator.translateComponent("warning.employee.hours.over24.title"), Translator.translateComponent("warning.employee.hours.over24.message"), parent=self)
                    return False

                return True
            except ValueError:
                return False
        else:
            return True

    def validate_float_no_max(self, action, index, value_if_allowed,
        prior_value, text, validation_type, trigger_type, widget_name):
        # action=1 -> insert
        if(action=='1'):
            try:
                val = float(value_if_allowed)
                if(val <0):
                    messagebox.showerror(Translator.translateComponent("warning.employee.bonus.under0.title"), Translator.translateComponent("warning.employee.bonus.under0.message"), parent=self)
                    return False

                return True
            except ValueError:
                return False
        else:
            return True

    def editEmployee(self, eID):
        def editEmployeeTemp():
            employee = self.data.getEmployeeFromId(eID)
            AddEmployeeGui(self, employee)
        
        return editEmployeeTemp

    def editedEmployee(self):
        self.initText()