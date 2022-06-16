
from tkinter import messagebox
from settings import Settings
from data import InteractData
import tkinter as tk
from language import Translator
from guiComponents.EntryWithPlaceholder import EntryWithPlaceholder

class SettingsGui(tk.Frame):
    def __init__(self, parent):
        master = tk.Toplevel()
        super().__init__(master)
        self.master = master
        self.parentGui = parent
        self.window = None
        self.weekendRow = {}
        self.master.title(Translator.translateComponent("settings.gui.title"))
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
        colCount = 1

        for day in InteractData.getWeekDayIds():
            tk.Label(self.window, text=InteractData.getDayNameFromId(day)).grid(row=rowCount, column=colCount)
            colCount += 1
        rowCount+= 1
        colCount=0
        tk.Label(self.window, text=Translator.translateComponent("settings.gui.basePercent.label")).grid(row=rowCount, column=colCount)
        tk.Label(self.window, text=Translator.translateComponent("settings.gui.overtimePercentUnder3.label")).grid(row=rowCount+1, column=colCount)
        tk.Label(self.window, text=Translator.translateComponent("settings.gui.overtimePercentOver3.label")).grid(row=rowCount+2, column=colCount)
        tk.Label(self.window, text=Translator.translateComponent("settings.gui.extraMoneyPerHour.label")).grid(row=rowCount+3, column=colCount)
        tk.Label(self.window, text=Translator.translateComponent("settings.gui.regularhours.label")).grid(row=rowCount+4, column=colCount)
        colCount += 1
        for day in InteractData.getWeekDayIds():
            def _():#Scoping
                dayId = day

                percentRegPay = Settings.getDayBaseRate(dayId)
                baseRate = EntryWithPlaceholder(self.window, placeholder="1.0", width=5, vcmd=self.validate_float, onChange=lambda x: self.regTimePercentChanged(dayId, x))
                baseRate.setText(percentRegPay)

                baseRate.grid(row=rowCount, column=colCount)
                
                percentAgeU3 = Settings.getDayOverTimePercentageUnder3(dayId)
                overTimePercentU3 = EntryWithPlaceholder(self.window, placeholder="1.25", width=5, vcmd=self.validate_float, onChange=lambda x: self.overTimePercentChangedUnder3(dayId, x))
                overTimePercentU3.setText(percentAgeU3)

                overTimePercentU3.grid(row=rowCount+1, column=colCount)

                percentAgeO3 = Settings.getDayOverTimePercentageOver3(dayId)
                overTimePercentO3 = EntryWithPlaceholder(self.window, placeholder="1.5", width=5, vcmd=self.validate_float, onChange=lambda x: self.overTimePercentChangedOver3(dayId, x))
                overTimePercentO3.setText(percentAgeO3)

                overTimePercentO3.grid(row=rowCount+2, column=colCount)

                bonusPay = Settings.getDayBonusPay(dayId)
                bonusPayEntry = EntryWithPlaceholder(self.window, placeholder="0", width=5, vcmd=self.validate_float, onChange=lambda x: self.overTimeBonusPay(dayId, x))
                bonusPayEntry.setText(self.numToString(bonusPay))

                bonusPayEntry.grid(row=rowCount+3, column=colCount)

                dayRegHours = Settings.getDayRegularHours(dayId)
                dayRegHoursPlaceholder = EntryWithPlaceholder(self.window, placeholder="8", width=5, vcmd=self.validate_hours, onChange=lambda x: self.dayRegHoursSet(dayId, x))
                dayRegHoursPlaceholder.setText(self.numToString(dayRegHours))

                dayRegHoursPlaceholder.grid(row=rowCount+4, column=colCount)
            _()
            colCount += 1

        rowCount += 5
    
    def numToString(self, num):
        if(num%1==0):
            return str(int(num))
        else:
            return str(num)

    def regTimePercentChanged(self, dayId, newVal):
        if(newVal):
            Settings.setDayBaseRate(dayId, float(newVal))

    def overTimePercentChangedUnder3(self, dayId, newVal):
        if(newVal):
            Settings.setOverTimePercentageUnder3(dayId, float(newVal))

    def overTimePercentChangedOver3(self, dayId, newVal):
        if(newVal):
            Settings.setOverTimePercentageOver3(dayId, float(newVal))

    def overTimeBonusPay(self, dayId, newVal):
        if(newVal):
            Settings.setDayBonusPay(dayId, float(newVal))

    def dayRegHoursSet(self, dayId, newVal):
        if(newVal):
            Settings.setDayRegularHours(dayId, float(newVal))

    def validate_float(self, action, index, value_if_allowed,
        prior_value, text, validation_type, trigger_type, widget_name):
        # action=1 -> insert
        if(action=='1'):
            try:
                float(value_if_allowed)
                return True
            except ValueError:
                return False
        else:
            return True
    
    def validate_hours(self, action, index, value_if_allowed,
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
