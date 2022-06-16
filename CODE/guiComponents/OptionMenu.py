import tkinter as tk

class LinkedIntStringVar(tk.StringVar):
    '''Takes a dictionary of int to strings. default 'get' function
        will return strings as normal, but there is also special function for
        returning based on the integer values 'get_int'.
    Setting the variable requires using the integer value set in int_string_dict'''
    def __init__(self, master=None, int_string_dict=None, value=None, name=None):
        tk.StringVar.__init__(self, master, value, name)
        self.__int_string_dict = int_string_dict
        self.__current_int_value = None

    def get_int(self):
        """Return value of variable as integer."""
        return self.__current_int_value

    def set(self, value):
        """Set the variable to VALUE."""
        try:
            string_value = self.__int_string_dict[value]
            self.__current_int_value = value
        except:
            string_value = value

        super().set(string_value)

# No changes from tkinter's implementation here, I just like it to be available.
class _setit:
    """Internal class. It wraps the command in the widget OptionMenu."""
    def __init__(self, var, value, callback=None):
        self.__value = value
        self.__var = var
        self.__callback = callback
    def __call__(self, *args):
        self.__var.set(self.__value)
        if self.__callback:
            self.__callback(self.__value, *args)

# Changes to this class are commented below
class OptionMenu(tk.Menubutton):
    """OptionMenu which allows the user to select a value from a menu."""
    def __init__(self, master, variable, values, **kwargs): # removed 'value' from args
        """Construct an optionmenu widget with the parent MASTER, with
        the resource textvariable set to VARIABLE, the initially selected
        value VALUE, the other menu values VALUES and an additional
        keyword argument command."""
        kw = {"borderwidth": 2, "textvariable": variable,
              "indicatoron": 1, "relief": tk.RAISED, "anchor": "c",
              "highlightthickness": 2}
        tk.Widget.__init__(self, master, "menubutton", kw)
        self.widgetName = 'tk_optionMenu'
        self.theVariable = variable
        menu = self.__menu = tk.Menu(self, name="menu", tearoff=0)
        self.menuname = menu._w
        # 'command' is the only supported keyword
        callback = kwargs.get('command')
        if 'command' in kwargs:
            del kwargs['command']
        if kwargs:
            raise tk.TclError('unknown option -'+kwargs.keys()[0])
        # Issues with the variables clashing, 
        # I personally just depend on the variable's value so it was easiest 
        # just to remove this unneeded portion (for my case)
        #menu.add_command(label=value,
        #         command=_setit(variable, value, callback))
        for v in values.keys(): # Change this line to handle dict instead of list
            # Change this line to set to the String value in the dict
            menu.add_command(label=values[v],
                     command=_setit(variable, v, callback))
        self["menu"] = menu

    def __getitem__(self, name): # No changes
        if name == 'menu':
            return self.__menu
        return tk.Widget.__getitem__(self, name)

    def destroy(self): # No changes
        """Destroy this widget and the associated menu."""
        tk.Menubutton.destroy(self)
        self.__menu = None