import tkinter as tk
from tkinter import messagebox
from language import Translator
from guiComponents.EntryWithPlaceholder import EntryWithPlaceholder
from data import JobPosition

class CreateJobPosition(tk.Frame):
    def __init__(self, parent, editPosition=None, parentIsManage=True): #When editPosition is a job position, it will allow editing that position instead of creating a new one
        master = tk.Toplevel()
        super().__init__(master)
        self.master = master
        self.parentGui = parent
        self.parentIsManageJobPositions = parentIsManage
        self.data = parent.data
        self.editPosition = editPosition
        if(self.editPosition):
            self.master.title(Translator.translateComponent("editJobPos.gui.title"))
        else:
            self.master.title(Translator.translateComponent("addJobPos.gui.title"))
        master.columnconfigure(0, weight=1)
        master.rowconfigure(0, weight=1)
        self.grid(row=0,column=0,sticky="nsew")
        self.initText()

        self.update()
        self.master.resizable(False, False)

        # self.mainloop()
    
    def initText(self):
        rowcount = 1
        if(self.editPosition):
            title = tk.Label(self, text=Translator.translateComponent("editJobPos.title"))
        else:
            title = tk.Label(self, text=Translator.translateComponent("addJobPos.title"))

        title.config(font=('helvetica', 14))
        title.grid(row=rowcount,column=1)
        rowcount += 1

        
        self.entry = EntryWithPlaceholder(self, Translator.translateComponent("addJobPos.posName.placeholder"), vcmd=self.validateLength)
        self.entry.grid(row=rowcount,column=1)


        rowcount += 1
        self.entry2 = EntryWithPlaceholder(self, Translator.translateComponent("addJobPos.payrate.placeholder"), vcmd=self.validate_float)
        self.entry2.grid(row=rowcount,column=1)
        # self.entry.focus()

        if(self.editPosition):
            self.entry.setText(self.editPosition.getName())
            self.entry2.setText(str(self.editPosition.getPay()))

        rowcount += 1
        
        if(self.editPosition):
            tk.Button(self, text=Translator.translateComponent("gui.button.edit"), command=self.add).grid(row=rowcount,column=1) 
            rowcount += 1 
            tk.Button(self, text=Translator.translateComponent("gui.button.delete"), command=self.deletePos).grid(row=rowcount,column=1)   
        else:
            tk.Button(self, text=Translator.translateComponent("gui.button.add"), command=self.add).grid(row=rowcount,column=1)

        rowcount += 1
        self.columnconfigure(0, weight=1, minsize=50)
        self.rowconfigure(0, weight=1, minsize=50)
        self.columnconfigure(2, weight=1, minsize=50)
        self.rowconfigure(rowcount, weight=1, minsize=50)
        
    def validateLength(self, action, index, value_if_allowed,
        prior_value, text, validation_type, trigger_type, widget_name):
        # action=1 -> insert
        if (len(value_if_allowed) > 50):
            messagebox.showerror(Translator.translateComponent("warning.jobposition.name.over50.title"), Translator.translateComponent("warning.jobposition.name.over50.message"), parent=self)
            return False
        return True

    def validateName(self):
        if (len(self.entry.get()) > 50):
            messagebox.showerror(Translator.translateComponent("warning.jobposition.name.over50.title"), Translator.translateComponent("warning.jobposition.name.over50.message"), parent=self)
            return False
        if (len(self.entry.get()) < 2):
            messagebox.showerror(Translator.translateComponent("warning.jobposition.name.under2.title"), Translator.translateComponent("warning.jobposition.name.under2.message"), parent=self)
            return False
        if(self.entry.get() == self.entry.placeholder):
            messagebox.showerror(Translator.translateComponent("warning.jobposition.name.mustenter.title"), Translator.translateComponent("warning.jobposition.name.mustenter.message"), parent=self)
            return False
        if(self.entry2.get() == self.entry2.placeholder):
            messagebox.showerror(Translator.translateComponent("warning.jobposition.payrate.mustenter.title"), Translator.translateComponent("warning.jobposition.payrate.mustenter.message"), parent=self)
            return False

        if(not self.editPosition):
            for ID in self.data.getJobPositionIds():
                jobPosition = self.data.getJobFromId(ID)
                if(self.entry.get() == jobPosition.getName()):
                    return messagebox.askyesno(Translator.translateComponent("warning.jobposition.name.duplicate.title"), Translator.translateComponent("warning.jobposition.name.duplicate.message"), parent=self)

        return True
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
    def add(self):
        
        if(not self.validateName()):
            return

        if(self.editPosition):
            newpos = self.editPosition
        else:
            newpos = JobPosition()

        newpos.setName(self.entry.get()).setPay(float(self.entry2.get()))

        if(not self.editPosition):
            if(self.parentIsManageJobPositions):
                self.parentGui.addJobPosition(newpos)
            else:
                self.data.addJobPosition(newpos)
                self.parentGui.updateEmployeePanel()
        else:
            if(self.parentIsManageJobPositions):
                self.parentGui.editedJobPosition()
            else:
                self.parentGui.updateEmployeePanel()
        self.master.destroy()

    def deletePos(self):
        for key in self.data.employees:
            if(self.data.employees[key].jobPosition.getId()==self.editPosition.getId()):
                messagebox.showerror(Translator.translateComponent("warning.jobposition.cantdelete.employeeusing.title"), Translator.translateComponent("warning.jobposition.cantdelete.employeeusing.message"), parent=self)
                return;

        self.data.deletePosition(self.editPosition)
        if(self.parentIsManageJobPositions):
            self.parentGui.editedJobPosition()
        else:
            self.parentGui.updateEmployeePanel()
        self.master.destroy()