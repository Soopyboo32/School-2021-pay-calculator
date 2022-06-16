import tkinter as tk
from tkinter import messagebox
from tkinter.constants import S
from language import Translator
from data import Employee
from guiComponents.EntryWithPlaceholder import EntryWithPlaceholder
from guiComponents.OptionMenu import LinkedIntStringVar, OptionMenu
from guiComponents.CreateJobPosition import CreateJobPosition

class AddEmployeeGui(tk.Frame):
    def __init__(self, parent, editEmployee=None): #When editEmployee is a job position, it will allow editing that position instead of creating a new one
        master = tk.Toplevel()
        super().__init__(master)
        self.master = master
        self.data = parent.data
        self.parentGui = parent
        self.editEmployee = editEmployee
        if(self.editEmployee):
            self.master.title(Translator.translateComponent("editEmployee.gui.title"))
        else:
            self.master.title(Translator.translateComponent("addEmployee.gui.title"))
        master.columnconfigure(0, weight=1)
        master.rowconfigure(0, weight=1)
        self.grid(row=0,column=0,sticky="nsew")
        self.window = None
        self.initText()

        self.update()
        self.master.resizable(False, False)

        # self.mainloop()
    
    def initText(self):

        if(self.window):
            self.window.destroy()
        
        self.window = tk.Frame(self)
        self.window.grid(row=0,column=0,sticky="nsew")

        rowcount = 1
        
        if(self.editEmployee):
            title = tk.Label(self.window, text=Translator.translateComponent("editEmployee.title"))
        else:
            title = tk.Label(self.window, text=Translator.translateComponent("addEmployee.title"))
        
        title.config(font=('helvetica', 14))
        title.grid(row=rowcount,column=1)
        rowcount += 1

        
        self.entry = EntryWithPlaceholder(self.window, Translator.translateComponent("addEmployee.employeeName.placeholder"), vcmd=self.validateLength)
        self.entry.grid(row=rowcount,column=1)

        rowcount += 1

        OPTIONS = {
            -2: Translator.translateComponent("addEmployee.createNewJobPosition"),
            -1: Translator.translateComponent("addEmployee.noJobPosition")
        }
        for position in self.data.getJobPositionIds():
            OPTIONS[position] = self.data.getJobFromId(position).getName()
        
        variable = LinkedIntStringVar(self, int_string_dict=OPTIONS)
        variable.set(Translator.translateComponent("addEmployee.selectJobPosition")) # default value
        
        if(self.editEmployee):
            if(self.editEmployee.jobPosition):
                variable.set(self.editEmployee.jobPosition.getId())
            else:
                variable.set(-1)

        self.jobposenter = OptionMenu(self.window, variable, OPTIONS, command=self.onjobChange)
        self.jobposenter.grid(row=rowcount,column=1)
        # self.entry.focus()

        rowcount += 1

        customPayFrame = tk.Frame(self.window)
        tk.Label(customPayFrame, text=Translator.translateComponent("addEmployee.customPayInfo")).grid(row=0,column=0)
        self.customPay = EntryWithPlaceholder(customPayFrame, Translator.translateComponent("addEmployee.customPayRate.placeholder"), vcmd=self.validate_float)
        self.customPay.grid(row=0,column=1)
        customPayFrame.grid(row=rowcount,column=1)

        if(self.editEmployee):
            self.entry.setText(self.editEmployee.getName())

            if(self.editEmployee.customPay):
                self.customPay.setText(self.editEmployee.customPay)

        rowcount += 1

        if(self.editEmployee):
            tk.Button(self.window, text=Translator.translateComponent("gui.button.edit"), command=self.add).grid(row=rowcount,column=1) 
            rowcount += 1 
            tk.Button(self.window, text=Translator.translateComponent("gui.button.delete"), command=self.deleteEmployee).grid(row=rowcount,column=1)  
        else:
            tk.Button(self.window, text=Translator.translateComponent("gui.button.add"), command=self.add).grid(row=rowcount,column=1)

        rowcount += 1
        self.window.columnconfigure(0, weight=1, minsize=50)
        self.window.rowconfigure(0, weight=1, minsize=50)
        self.window.columnconfigure(2, weight=1, minsize=50)
        self.window.rowconfigure(rowcount, weight=1, minsize=50)
    
    def validate_float(self, action, index, value_if_allowed,
        prior_value, text, validation_type, trigger_type, widget_name):
        # action=1 -> insert
        # return True
        if(action=='1'):
            try:
                val = float(value_if_allowed)
                if(val <0):
                    messagebox.showerror(Translator.translateComponent("warning.jobposition.pay.under0.title"), Translator.translateComponent("warning.jobposition.pay.under0.message"), parent=self)
                    return False

                return True
            except ValueError:
                return False
        else:
            return True

    def onjobChange(self, value, *args):
        if(value == -2):
            self.jobposenter.theVariable.set(Translator.translateComponent("addEmployee.selectJobPosition"))
            CreateJobPosition(self)
        
    def validateLength(self, action, index, value_if_allowed,
        prior_value, text, validation_type, trigger_type, widget_name):
        # action=1 -> insert
        if (len(value_if_allowed) > 50):
            messagebox.showerror(Translator.translateComponent("warning.employee.name.over50.title"), Translator.translateComponent("warning.employee.name.over50.message"), parent=self)
            return False
        return True
    def validateName(self):
        if (len(self.entry.get()) > 50):
            messagebox.showerror(Translator.translateComponent("warning.employee.name.over50.title"), Translator.translateComponent("warning.employee.name.over50.message"), parent=self)
            return False
        if (len(self.entry.get()) < 2):
            messagebox.showerror(Translator.translateComponent("warning.employee.name.under2.title"), Translator.translateComponent("warning.employee.name.under2.message"), parent=self)
            return False
        if(self.entry.get() == self.entry.placeholder):
            messagebox.showerror(Translator.translateComponent("warning.employee.name.mustenter.title"), Translator.translateComponent("warning.employee.name.mustenter.message"), parent=self)
            return False

        if(not self.editEmployee):
            for ID in self.data.getEmployeeIds():
                employee = self.data.getEmployeeFromId(ID)
                if(self.entry.get() == employee.getName()):
                    return messagebox.askyesno(Translator.translateComponent("warning.employee.name.duplicate.title"), Translator.translateComponent("warning.employee.name.duplicate.message"), parent=self)

        return True

    def add(self):
        
        if(not self.validateName()):
            return
        
        jobPos = None
        selected = self.jobposenter.theVariable.get_int()
        if(selected is None):
            messagebox.showerror(Translator.translateComponent("warning.employee.job.mustenter.title"), Translator.translateComponent("warning.employee.job.mustenter.message"), parent=self)
            return;
        if(selected != -1):
            jobPos = self.data.getJobFromId(selected)
        
        employeeNew = Employee()

        if(self.editEmployee):
            employeeNew = self.editEmployee
        
        employeeNew.setName(self.entry.get()).setJobPosition(jobPos)

        if(self.customPay.get() != self.customPay.placeholder and self.customPay.get()):
            employeeNew.customPay = float(self.customPay.get())

        if(not self.editEmployee):
            self.data.addEmployee(employeeNew)

        self.parentGui.updateEmployeePanel()
        self.master.destroy()
    
    def deleteEmployee(self):
        self.data.deleteEmployee(self.editEmployee)
        self.parentGui.updateEmployeePanel()
        self.master.destroy()
    
    def addJobPosition(self, jobPos):
        self.data.addJobPosition(jobPos)
        name = self.entry.get()
        self.initText()

        if(name != self.entry.get()):
            self.entry.setText(name)
        self.jobposenter.theVariable.set(jobPos.getId())
