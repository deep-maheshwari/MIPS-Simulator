from tkinter import *

def time_pass():
    print('It works for now!!!')

app = Tk()

app.title('DTSpim')
app.geometry('1000x800')

#Buttons
load_btn = Button(app, text = 'Load File', width = 18, command = time_pass)
load_btn.grid(row = 0, column = 0, pady = 20)
#Buttons
run_btn = Button(app, text = 'Run File', width = 18, command = time_pass)
run_btn.grid(row = 0, column = 1, pady = 20)
#Buttons
sbs_btn = Button(app, text = 'Run File Step-by-Step', width = 18, command = time_pass)
sbs_btn.grid(row = 0, column = 2, pady = 20)
#Buttons
ic_btn = Button(app, text = 'Open Interactive Console', width = 18, command = time_pass)
ic_btn.grid(row = 0, column = 3, pady = 20)

#ListBox
reg_list = Listbox(app, height = 100, width = 20)
reg_list.grid(row = 1, column = 0, pady = 20, padx = 20)
#ListBox
ic_list = Listbox(app, height = 100, width = 80)
ic_list.grid(row = 1, column = 1, pady = 20, padx = 20, columnspan = 3, rowspan = 6)


app.mainloop()