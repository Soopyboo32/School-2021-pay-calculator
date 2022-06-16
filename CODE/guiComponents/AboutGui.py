import tkinter as tk
from language import Translator

class AboutGui(tk.Frame):
    def __init__(self):
        master = tk.Toplevel()
        super().__init__(master)
        self.master = master
        self.master.title(Translator.translateComponent("about.gui.title"))
        self.master.minsize(350, 250)
        master.columnconfigure(0, weight=1)
        master.rowconfigure(0, weight=1)
        self.grid(row=0,column=0,sticky="nsew")
        self.initText()

        self.update()
        self.master.minsize(self.master.winfo_width(), self.master.winfo_height())

        # self.mainloop()
    
    def initText(self):
        text = Translator.getAbout()
        tk.Label(self, text=text).grid(row=1,column=1)
        tk.Button(self, text=Translator.translateComponent("gui.button.ok"), command=self.master.destroy).grid(row=2,column=1)

        self.columnconfigure(0, weight=1, minsize=50)
        self.rowconfigure(0, weight=1, minsize=50)
        self.columnconfigure(2, weight=1, minsize=50)
        self.rowconfigure(3, weight=1, minsize=50)
