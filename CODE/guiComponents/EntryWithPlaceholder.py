import tkinter as tk
     
class EntryWithPlaceholder(tk.Entry):
    def __init__(self, master=None, placeholder="PLACEHOLDER", color='grey', vcmd=None, width=None, onChange=None):
        
        super().__init__(master, validate="key", width=width)

        self.vcmd = vcmd

        vcmdself = (self.register(self.vcmdThing),
                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
    
        super().__init__(master, validate="key", vcmd=vcmdself, width=width)

        self.placeholder = placeholder
        self.placeholder_color = color
        self.onChange = onChange
        self.default_fg_color = self['fg']

        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)

        self.put_placeholder()

    def vcmdThing(self, action, index, value_if_allowed,
        prior_value, text, validation_type, trigger_type, widget_name):
        if(text == self.placeholder or not self.vcmd):
            if(self.onChange):
                self.onChange(value_if_allowed)
            return True
        if(self.vcmd(action, index, value_if_allowed, prior_value, text, validation_type, trigger_type, widget_name)):
            if(self.onChange):
                self.onChange(value_if_allowed)
            return True
        return False
    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color

    def foc_in(self, *args):
        if self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color

    def foc_out(self, *args):
        if not self.get():
            self.put_placeholder()

    def setText(self, text):
        self.delete('0', 'end')
        self['fg'] = self.default_fg_color
        self.insert(0, text)
        if not self.get():
            self.put_placeholder()
