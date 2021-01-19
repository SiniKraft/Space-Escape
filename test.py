import tkinter
import tkinter.ttk
parent_widget = tkinter.Tk()
control_variable = tkinter.StringVar(parent_widget)
OPTION_TUPLE = ("Option 1", "Option 2", "Option 3") 
optionmenu_widget = tkinter.OptionMenu(parent_widget,
                     control_variable, *OPTION_TUPLE)
optionmenu_widget.pack()
tkinter.mainloop()