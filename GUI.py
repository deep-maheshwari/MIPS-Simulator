from tkinter import *
from tkinter import filedialog
from functools import partial
import Simulator_interface as Sim

s = Sim.Simulator()

# from Simulator import *
# import Simulator as sim
# data_and_text = {'data':[],'main':[],}
# instructions = []
# data = {'.word':[],'.text':[]}
# reg = {"zero":0, "r0":0, "at":0, "v0":0, "v1":0, "a0":0, "a1":0, "a2":0, "a3":0, "t0":0, "t1":0, "t2":0, "t3":0, "t4":0, "t5":0, "t6":0, "t7":0,"s0":0, "s1":0, "s2":0, "s3":0 ,"s4":0 ,"s5":0, "s6":0, "s7":0, "t8":0, "t9":0, "k0":0, "k1":0, "gp":0, "sp":0, "s8":0, "ra":0}
# PC = 0
# base_address = 0x10010000
# bne_flag = ''
# beq_flag = ''
# j_flag = ''    
# label_address = {}
# main = {}

app = Tk()

app.title('DTSpim')
app.geometry('1400x800')
frame = Frame(app)
frame.grid(sticky = 'nwes')

app.filename = ""

def run_sbs(s):
    print(s.data_and_text['main'])
    print(s.PC)
    if(s.PC == len(s.data_and_text['main'])):
        msg_popup("Program finished!")
        s.PC = 0

    s.Simulate_step()

    if(s.msg==''):

        reg_list2.delete(0, END)
        reg_list2.insert(END, '')
        reg_list2.insert(END, str(s.PC))
        reg_list2.insert(END, '')
        reg_list2.insert(END, '')
        reg_list2.insert(END, '')
        reg_list2.insert(END, '')
        for register in s.reg:
            reg_list2.insert(END, str(s.reg[register]))
        reg_list2.insert(END, '')

        ic_list.delete(0, END)
        ic_list.insert(END, '')
        ic_list.insert(END, 'Data Segment')
        ic_list.insert(END, '')
        for i in range(len(s.data['.word'])):
            ic_list.insert(END, hex((s.base_address+4*i))+": "+str(s.data['.word'][i]))
        ic_list.insert(END, '')
        ic_list.insert(END, '')
        ic_list.insert(END, 'Text Segment')
        ic_list.insert(END, '')
        for i in s.data_and_text['main']:
            ic_list.insert(END, str(i))
            ic_list.insert(END, '')
        ic_list.insert(END, '')

        ic_list.itemconfig(len(s.data['.word']) + 5 + s.PC*2, background = '#00ff01')

    else:
        error_popup(s.msg)
        
def run_file(s):

    s.Simulate_all()
    if(s.msg==""):

    # while(PC!=len(data_and_text['main'])-1):

    #     PC = run_instruction(data_and_text['main'][PC],PC)

        # if(PC>len(data_and_text['main'])):
        #     print("Unexpected error occured.")
        #     break
        reg_list2.delete(0, END)
        reg_list2.insert(END, '')
        reg_list2.insert(END, str(s.PC))
        reg_list2.insert(END, '')
        reg_list2.insert(END, '')
        reg_list2.insert(END, '')
        reg_list2.insert(END, '')
        for register in s.reg:
            reg_list2.insert(END, str(s.reg[register]))
        reg_list2.insert(END, '')

        ic_list.delete(0, END)
        ic_list.insert(END, '')
        ic_list.insert(END, 'Data Segment')
        ic_list.insert(END, '')
        for i in range(len(s.data['.word'])):
            ic_list.insert(END, hex((s.base_address+4*i))+": "+str(s.data['.word'][i]))
        ic_list.insert(END, '')
        ic_list.insert(END, '')
        ic_list.insert(END, 'Text Segment')
        ic_list.insert(END, '')
        for i in s.data_and_text['main']:
            ic_list.insert(END, str(i))
            ic_list.insert(END, '')
        ic_list.insert(END, '')
        scrollbar.config(command = ic_list.yview)

    else:
        error_popup(s.msg)

# def addressfetch(data_and_text,instructions,data,reg,PC,base_address,bne_flag,beq_flag,j_flag,label_address,main):
    
#     loadfile(app.filename,data_and_text,instructions,data,reg,PC,base_address,bne_flag,beq_flag,j_flag,label_address,main)

def reinit(s):
    
    s.reinitialize()

    reg_list2.delete(0, END)
    reg_list2.insert(END, '')
    reg_list2.insert(END, str(s.PC))
    reg_list2.insert(END, '')
    reg_list2.insert(END, '')
    reg_list2.insert(END, '')
    reg_list2.insert(END, '')
    for register in s.reg:
        reg_list2.insert(END, str(s.reg[register]))
    reg_list2.insert(END, '')

    ic_list.delete(0, END)    
    ic_list.insert(END, '')
    ic_list.insert(END, 'Data Segment')
    ic_list.insert(END, '')
    ic_list.insert(END, '')
    ic_list.insert(END, 'Text Segment')
    ic_list.insert(END, '')
    ic_list.insert(END, '')
    print(s.data_and_text)
    print(s.data)

def loadfile(s):
    if(len(s.instructions) != 0):
        msg_popup("WARNING!!! If you do not reinitialize, the data will get appended twice.\nIt is recommended to reintialize before load file.")

    else:
        app.filename = filedialog.askopenfilename(initialdir = '/CO', title = 'Select a File', filetypes = (('asm files', '*.asm'), ('s files', '*.s')))
        filename = app.filename

        s.fetch_and_load_file(filename)
        s.load_data_and_text()
        s.load_data()
        s.load_main()
        s.set_data_and_text()

        # label = Label(app, text = str(data['.word']))
        # label.grid(row = 1, column = 1)
        # ic_list = Listbox(app, height = 100, width = 80)
        # ic_list.grid(row = 1, column = 1, pady = 20, padx = 20, columnspan = 3, rowspan = 6)
        ic_list.delete(0, END)
        ic_list.insert(END, '')
        ic_list.insert(END, 'Data Segment')
        ic_list.insert(END, '')
        for i in range(len(s.data['.word'])):
            ic_list.insert(END, hex((s.base_address+4*i))+": "+str(s.data['.word'][i]))
        ic_list.insert(END, '')
        ic_list.insert(END, '')
        ic_list.insert(END, 'Text Segment')
        ic_list.insert(END, '')
        for i in s.data_and_text['main']:
            ic_list.insert(END, str(i))
            ic_list.insert(END, '')
        ic_list.insert(END, '')
        scrollbar.config(command = ic_list.yview)
    # s.print_all()

def int_console():
    console = Tk()
    console.title('Interactive Console')
    console.geometry('800x600')
    # instructs = StringVar()
    # arrows = Label(console, text = '>>')
    # arrows.grid(row = 0, column = 0, sticky = W)
    # entry = Entry(console, textvariable = instructs)
    # entry.grid(row = 0, column = 1, columnspan = 5)
    # console.bind('<Return>', run)
    # def run():
    #     print(instructs)
    #     s.run_instruction(s, instructs, 0)
    # output = Label(console, text = "")
    progress = Label(console, text = "Interactive Console is on progress, sorry for the inconvenience")
    progress.grid(row = 0, column = 0, pady = 50, padx = 175)

def settings():
    setting = Tk()
    setting.title('Settings')
    setting.geometry('800x600')
    progress = Label(setting, text = "Settings is on progress, sorry for the inconvenience")
    progress.grid(row = 0, column = 0, pady = 50, padx = 175)

def help_win():
    window = Tk()
    window.title('Help')
    window.geometry('800x600')
    progress = Label(window, text = "Help window is on progress, sorry for the inconvenience")
    progress.grid(row = 0, column = 0, pady = 50, padx = 175)

def close_window():
    app.destroy()

def msg_popup(msg):
    popup = Tk()
    popup.title("Program executed successfully")
    popup.geometry('450x110')
    
    def reinit_popup(s):
        reinit(s)
        popup.destroy()

    error = Label(popup, text = msg)
    error.grid(row = 0, column = 0, columnspan = 2, pady = 10)
    ri_btn = Button(popup, text = "Reinitialize", command = partial(reinit_popup, s))
    ri_btn.grid(row = 1, column = 0, pady = 20, sticky = 'we')

def error_popup(msg):
    popup = Tk()
    popup.title("Oops! Error!!!")
    popup.geometry('450x110')
    
    def reinit_popup(s):
        reinit(s)
        popup.destroy()

    error = Label(popup, text = msg)
    error.grid(row = 0, column = 0, columnspan = 2, pady = 10)
    ri_btn = Button(popup, text = "Reinitialize", command = partial(reinit_popup, s))
    ri_btn.grid(row = 1, column = 0, pady = 20, sticky = 'we')
    abort_btn = Button(popup, text = "Abort", command = popup.destroy)
    abort_btn.grid(row = 1, column = 1, pady = 20, sticky = W)


#Buttons
load_btn = Button(app, text = 'Load File', width = 18, command = partial(loadfile,s))
load_btn.grid(row = 1, column = 0, pady = 0, padx = 0, columnspan = 2)
#Buttons
ri_btn = Button(app, text = 'Reinitialize', width = 18, command = partial(reinit,s))
ri_btn.grid(row = 1, column = 2, pady = 5, padx = 0, sticky = E)
#Buttons
run_btn = Button(app, text = 'Run File', width = 18, command = partial(run_file,s))
run_btn.grid(row = 1, column = 3, pady = 0, padx = 0, sticky = E)
#Buttons
sbs_btn = Button(app, text = 'Run File Step-by-Step', width = 18, command = partial(run_sbs,s))
sbs_btn.grid(row = 1, column = 4, pady = 0, padx = 0, sticky = E)
#Buttons
ic_btn = Button(app, text = 'Open Interactive Console', width = 18, command = int_console)
ic_btn.grid(row = 1, column = 5, pady = 0, padx = 0, sticky = E)


#ListBox
reg_list = Listbox(app, height = 40, width = 10, borderwidth = 0, font = ('Times', 12, 'bold'), bg = '#a4cac2')
reg_list.grid(row = 2, column = 0, pady = 20, sticky = 'ns')
reg_list.insert(END, '')
reg_list.insert(END, 'PC')
reg_list.insert(END, '')
reg_list.insert(END, '')
reg_list.insert(END, '')
reg_list.insert(END, '')
i = 0
for register in s.reg:
    if(i < 10):
        reg_list.insert(END, "R" + str(i) + "    " + "[" + str(register) + "]")
    else:
        reg_list.insert(END, "R" + str(i) + "  " + "[" + str(register) + "]")
    i+=1

reg_list.insert(END, '')

#listBox
reg_list2 = Listbox(app, height = 40, width = 10, borderwidth = 0, font = ('Times', 12), bg = '#a4cac2')
reg_list2.grid(row = 2, column = 1, pady = 20, sticky = 'ns')
reg_list2.insert(END, '')
reg_list2.insert(END, str(s.PC))
reg_list2.insert(END, '')
reg_list2.insert(END, '')
reg_list2.insert(END, '')
reg_list2.insert(END, '')
for register in s.reg:
    reg_list2.insert(END, str(s.reg[register]))
reg_list2.insert(END, '')

# height = len(reg)
# for i in range(height):
#     reg_lis

# ListBox
ic_list = Listbox(app, height = 40, width = 120, font = ('Times', 13, 'bold'), bg = 'LightBlue')
ic_list.grid(row = 2, column = 2, pady = 20, padx = 10, columnspan = 4, rowspan = 6, sticky = 'ns')
ic_list.insert(END, '')
ic_list.insert(END, 'Data Segment')
ic_list.insert(END, '')
ic_list.insert(END, '')
ic_list.insert(END, 'Text Segment')
ic_list.insert(END, '')
ic_list.insert(END, '')

#ScrollBar
scrollbar = Scrollbar(app, command = ic_list.yview, orient = VERTICAL)
scrollbar.grid(row = 2, column = 6, sticky = 'ns')

#Set Scrollbar to listbox
# scrollbar.config(command = ic_list.yview)
ic_list.configure(yscrollcommand = scrollbar.set)

#Menu
menu = Menu(app)
app.config(menu = menu)

submenu = Menu(menu)
menu.add_cascade(label = "File", menu = submenu)
submenu.add_command(label = "Load File", command = partial(loadfile,s))
submenu.add_command(label = "Reinitialize", command = partial(reinit,s))
submenu.add_separator()
submenu.add_command(label = "Exit", command = close_window)

simmenu = Menu(menu)
menu.add_cascade(label = "Simulator", menu = simmenu)
simmenu.add_command(label = "Run program", command = partial(run_file,s))
simmenu.add_command(label = "Step-by-Step", command = partial(run_sbs,s))
simmenu.add_separator()
simmenu.add_command(label = "Settings", command = settings)

openmenu = Menu(menu)
menu.add_cascade(label = "Open", menu = openmenu)
openmenu.add_command(label = "Interactive Console", command = int_console)
openmenu.add_separator()
openmenu.add_command(label = "Help", command = help_win)

app.mainloop()