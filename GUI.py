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
app.geometry('1400x1000')
frame = Frame(app)
frame.grid(sticky = 'nwes')

app.filename = ""

def run_sbs(s):
    print(s.data_and_text['main'])
    print(s.PC)
    s.Simulate_step()
    # highlight = ic_list.get(data_and_text['main'][PC])
    # highlight = Text(app, highlightcolor = 'Red')
    reg_list.delete(0, END)
    reg_list.insert(END, '%-10s %s'%('PC:', str(s.PC)))
    reg_list.insert(END, '')
    reg_list.insert(END, '')
    reg_list.insert(END, '')
    reg_list.insert(END, '')
    for register in s.reg:
        if(register != 'zero'):
            reg_list.insert(END, '%-10s %s'%(str(register) + ":", str(s.reg[register])))
        else:
            reg_list.insert(END, '%-10s %s'%(str(register) + ":", str(s.reg[register])))
        
    reg_list.insert(END, '')

    ic_list.delete(0, END)
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

def run_file(s):
    s.Simulate_all()

    # while(PC!=len(data_and_text['main'])-1):

    #     PC = run_instruction(data_and_text['main'][PC],PC)

        # if(PC>len(data_and_text['main'])):
        #     print("Unexpected error occured.")
        #     break
    reg_list.delete(0, END)
    reg_list.insert(END, '%-10s %s'%('PC:', str(s.PC)))
    reg_list.insert(END, '')
    reg_list.insert(END, '')
    reg_list.insert(END, '')
    reg_list.insert(END, '')
    for register in s.reg:
        if(register != 'zero'):
            reg_list.insert(END, '%-10s %s'%(str(register) + ":", str(s.reg[register])))
        else:
            reg_list.insert(END, '%-10s %s'%(str(register) + ":", str(s.reg[register])))
        
    reg_list.insert(END, '')

    ic_list.delete(0, END)
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

def time_pass():
    print('Ohh! you want to open settings...')

# def addressfetch(data_and_text,instructions,data,reg,PC,base_address,bne_flag,beq_flag,j_flag,label_address,main):
    
#     loadfile(app.filename,data_and_text,instructions,data,reg,PC,base_address,bne_flag,beq_flag,j_flag,label_address,main)

def reinit(s):
    
    s.reinitialize()

    reg_list.delete(0, END)
    reg_list.insert(END, '%-10s %s'%('PC:', str(s.PC)))
    reg_list.insert(END, '')
    reg_list.insert(END, '')
    reg_list.insert(END, '')
    reg_list.insert(END, '')
    for register in s.reg:
        if(register != 'zero'):
            reg_list.insert(END, '%-10s %s'%(str(register) + ":", str(s.reg[register])))
        else:
            reg_list.insert(END, '%-10s %s'%(str(register) + ":", str(s.reg[register])))
        
    reg_list.insert(END, '')

    ic_list.delete(0, END)
    ic_list.insert(END, 'Data Segment')
    ic_list.insert(END, '')
    ic_list.insert(END, '')
    ic_list.insert(END, 'Text Segment')
    ic_list.insert(END, '')
    ic_list.insert(END, '')
    print(s.data_and_text)
    print(s.data)

def loadfile(s):
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
    s.print_all()

def int_console():
    console = Tk()
    console.title('Interactive Console')
    console.geometry('800x600')
    instructs = StringVar()
    arrows = Label(console, text = '>>')
    arrows.grid(row = 0, column = 0, sticky = W)
    entry = Entry(console, textvariable = instructs)
    entry.grid(row = 0, column = 1, columnspan = 5)
    print(instructs)

def close_window():
    app.destroy()




#Buttons
# load_btn = Button(app, text = 'Load File', width = 18, command = addressfetch)
# load_btn.grid(row = 0, column = 0, pady = 20, padx = 5)
#Buttons
# ri_btn = Button(app, text = 'Reinitialize', width = 18, command = reinit)
# ri_btn.grid(row = 0, column = 1, pady = 20, padx = 5)
#Buttons
# run_btn = Button(app, text = 'Run File', width = 18, command = run_file)
# run_btn.grid(row = 0, column = 2, pady = 20, padx = 5)
#Buttons
# sbs_btn = Button(app, text = 'Run File Step-by-Step', width = 18, command = run_sbs)
# sbs_btn.grid(row = 0, column = 3, pady = 20, padx = 5)
#Buttons
# ic_btn = Button(app, text = 'Open Interactive Console', width = 18, command = int_console)
# ic_btn.grid(row = 0, column = 4, pady = 20, padx = 5)


#ListBox
reg_list = Listbox(app, height = 100, width = 20)
reg_list.grid(row = 1, column = 0, pady = 20, padx = 20)
reg_list.insert(END, '%-10s %s'%('PC:', str(s.PC)))
reg_list.insert(END, '')
reg_list.insert(END, '')
reg_list.insert(END, '')
reg_list.insert(END, '')
for register in s.reg:
    if(register != 'zero'):
        reg_list.insert(END, '%-10s %s'%(str(register) + ":", str(s.reg[register])))
    else:
        reg_list.insert(END, '%-10s %s'%(str(register) + ":", str(s.reg[register])))
    
reg_list.insert(END, '')
# ListBox
ic_list = Listbox(app, height = 100, width = 120)
ic_list.grid(row = 1, column = 1, pady = 20, padx = 20, columnspan = 4, rowspan = 6)
ic_list.insert(END, 'Data Segment')
ic_list.insert(END, '')
ic_list.insert(END, '')
ic_list.insert(END, 'Text Segment')
ic_list.insert(END, '')
ic_list.insert(END, '')

#ScrollBar
scrollbar = Scrollbar(app)
scrollbar.grid(row = 1, column = 6)

#Set Scrollbar to listbox
ic_list.config(yscrollcommand = scrollbar.set)
scrollbar.config(command = ic_list.yview)

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
simmenu.add_command(label = "Settings", command = time_pass)

openmenu = Menu(menu)
menu.add_cascade(label = "Open", menu = openmenu)
openmenu.add_command(label = "Interactive Console", command = int_console)
openmenu.add_separator()
openmenu.add_command(label = "Help", command = time_pass)

app.mainloop()