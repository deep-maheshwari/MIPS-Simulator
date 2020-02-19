from tkinter import *
from tkinter import filedialog
# from Simulator import *
# import Simulator as sim
data_and_text = {'data':[],'main':[],}
instructions = []
data = {'.word':[],'.text':[]}
reg = {"zero":0, "r0":0, "at":0, "v0":0, "v1":0, "a0":0, "a1":0, "a2":0, "a3":0, "t0":0, "t1":0, "t2":0, "t3":0, "t4":0, "t5":0, "t6":0, "t7":0,"s0":0, "s1":0, "s2":0, "s3":0 ,"s4":0 ,"s5":0, "s6":0, "s7":0, "t8":0, "t9":0, "k0":0, "k1":0, "gp":0, "sp":0, "s8":0, "ra":0}
PC = 0
base_address = 0x10010000
bne_flag = ''
beq_flag = ''
j_flag = ''    
label_address = {}
main = {}

app = Tk()

app.title('DTSpim')
app.geometry('1000x800')

app.filename = ""

def run_instruction(instruction,PC):

    if(instruction[0]=='add'):
        if(len(instruction)!=4):
            print("Error in the given instruction. Missing or extra operand given")

        else:
            reg1 = instruction[1].replace('$','')
            reg2 = instruction[2].replace('$','')
            reg3 = instruction[3].replace('$','')
            reg[reg1] = reg[reg2]+reg[reg3]
            PC+=1

    elif(instruction[0]=='sub'):
        if(len(instruction)!=4):
            print("Error in the given instruction. Missing or extra operand given")

        else:
            reg1 = instruction[1].replace('$','')
            reg2 = instruction[2].replace('$','')
            reg3 = instruction[3].replace('$','')
            reg[reg1] = reg[reg2]-reg[reg3]
            PC+=1

    elif(instruction[0]=='lw'):
        if(len(instruction)!=3):
            print("Error in the given instruction. Missing or extra operand given")

        else:
            reg_pattern = re.search(r"\$[a-z0-9]*",instruction[2],re.MULTILINE)
            offset_pattern = re.search(r"\w+",instruction[2],re.MULTILINE)
            reg1 = instruction[1].replace('$','')
            reg2 = reg_pattern.group(0)
            reg2 = reg2.replace('$','')
            offset = int(offset_pattern.group(0))
            #print(int(reg[reg2],16)-base_address)
            if(int(reg[reg2],16)-base_address>=0 and (int(reg[reg2],16)-base_address)%4==0 and offset%4==0):
                index = int((int(reg[reg2],16)-base_address)/4 + offset/4)
                reg[reg1] = data['.word'][index]
            PC+=1

    elif(instruction[0]=='sw'):
        if(len(instruction)!=3):
            print("Error in the given instruction. Missing or extra operand given")

        else:
            reg_pattern = re.search(r"\$[a-z0-9]*",instruction[2],re.MULTILINE)
            offset_pattern = re.search(r"\w+",instruction[2],re.MULTILINE)
            reg1 = instruction[1].replace('$','')
            reg2 = reg_pattern.group(0)
            reg2 = reg2.replace('$','')
            offset = int(offset_pattern.group(0))

            if(int(reg[reg2],16)>=base_address and (int(reg[reg2],16)-base_address)%4==0 and offset%4==0):
                index = int((int(reg[reg2],16)-base_address)/4 + offset/4)
                if(index>=len(data['.word'])):
                    count = index-len(data['.word'])
                    for i in range(count):
                        data['.word'].append(0)
                    data['.word'].append(reg[reg1])
                else:
                    data['.word'][index] = reg[reg1]
            PC+=1

    elif(instruction[0]=='bne'):

        if(len(instruction)!=4):
            print("Error in the given instruction. Missing or extra operand given")
        
        else:
            reg1 = instruction[1].replace('$','')
            reg2 = instruction[2].replace('$','')
            
        if(reg[reg1]!=reg[reg2]):
            bne_flag = instruction[3]   
            PC = main[bne_flag] 

        else:
            bne_flag = ''
            PC+=1

    elif(instruction[0]=='lui'):

        if(len(instruction)!=3):
            print("Error in the given instruction. Missing or extra operand given")

        else:
            reg1 = instruction[1].replace('$','')
            reg[reg1] = hex(int(instruction[2]+'0000',16))
            PC+=1

    elif(instruction[0]=='slt'):

        if(len(instruction)!=4):
            print("Error in the given instruction. Missing or extra operand given")

        else:
            reg1 = instruction[1].replace('$','')
            reg[reg1] = 0
            reg2 = instruction[2].replace('$','')
            reg3 = instruction[3].replace('$','')
            if(reg[reg2]<reg[reg3]):
                reg[reg1] = 1
            PC+=1

    elif(instruction[0]=='beq'):

        if(len(instruction)!=4):
            print("Error in the given instruction. Missing or extra operand given")

        else:
            reg1 = instruction[1].replace('$','')
            if(instruction[2][0]=='$'):
                reg2 = instruction[2].replace('$','')
                if(reg[reg1]==reg[reg2]):
                    beq_flag = instruction[3]
                    PC = main[beq_flag]

                else:
                    beq_flag = ''
                    PC+=1
            
            else:
                reg2 = int(instruction[2])
                if(reg[reg1]==reg2):
                    beq_flag = instruction[3]
                    PC = main[beq_flag]

                else:
                    beq_flag = ''
                    PC+=1

    elif(instruction[0]=='j'):

        if(len(instruction)!=2):
            print("Error in the given instruction. Missing or extra operand given")

        else:
            j_flag = instruction[1]
            PC = main[j_flag]

    elif(instruction[0]=='addi'):

        if(len(instruction)!=4):
            print("Error in the given instruction. Missing or extra operand given")

        else:
            reg1 = instruction[1].replace('$','')
            reg2 = instruction[2].replace('$','')
            addend = int(instruction[3])
            if(type(reg[reg2])==str and reg[reg2][0:2]=='0x'):
                reg[reg1] = hex(int(reg[reg2],16)+addend)
            else:
                reg[reg1] = reg[reg2] + addend
            PC+=1
    elif(instruction[0]=='andi'):

        if(len(instruction)!=4):
            print("Error in the given instruction. Missing or extra operand given")

        else:
            reg1 = instruction[1].replace('$','')
            reg2 = instruction[2].replace('$','')
            anded = instruction[3]
            reg[reg1] = hex(int(reg[reg2],16)&int(anded,16))
            PC=PC+1

    elif(instruction[0]=='and'):

        if(len(instruction)!=4):
            print("Error in the given instruction. Missing or extra operand given")

        else:
            reg1 = instruction[1].replace('$','')
            reg2 = instruction[2].replace('$','')
            reg3 = instruction[3].replace('$','')
            reg[reg1] = hex(int(reg[reg2],16) & int(reg[reg3],16))
            PC = PC + 1
            
    return PC

def run_file():
    PC = 0
    while(PC!=len(data_and_text['main'])-1):

        PC = run_instruction(data_and_text['main'][PC],PC)

        # if(PC>len(data_and_text['main'])):
        #     print("Unexpected error occured.")
        #     break
    reg_list.delete(0, END)
    reg_list.insert(END, '%-10s %s'%('PC:', str(PC)))
    reg_list.insert(END, '')
    reg_list.insert(END, '')
    reg_list.insert(END, '')
    reg_list.insert(END, '')
    for register in reg:
        if(register != 'zero'):
            reg_list.insert(END, '%-10s %s'%(str(register) + ":", str(reg[register])))
        else:
            reg_list.insert(END, '%-10s %s'%(str(register) + ":", str(reg[register])))
        
    reg_list.insert(END, '')

    ic_list.delete(0, END)
    ic_list.insert(END, 'Data Segment')
    ic_list.insert(END, '')
    ic_list.insert(END, str(data['.word']))
    ic_list.insert(END, '')
    ic_list.insert(END, '')
    ic_list.insert(END, 'Text Segment')
    ic_list.insert(END, '')
    for i in data_and_text['main']:
        ic_list.insert(END, str(i))
        ic_list.insert(END, '')
    ic_list.insert(END, '')

def time_pass():
    print('It works for now!!!')

def addressfetch():
    app.filename = filedialog.askopenfilename(initialdir = '/CO', title = 'Select a File', filetypes = (('asm files', '*.asm'), ('s files', '*.s')))
    loadfile(app.filename)

def fileHandler(filename):

    file = open(filename,'r')
    result = []
    for line in file.readlines():
        result.append(line)
    return result


def parse(text):

    result = text.split()
    parsed = []

    for st in result:
        
        st = st.split(",")
        for x in st:
            if(x):
                parsed.append(x)

    return parsed

    
def read_instructions(instructions):

    parsed_list = []
    for ins in instructions:
        if(parse(ins)):
            parsed_list.append(parse(ins))

    return parsed_list

def loadfile(filename):
    instructions = read_instructions(fileHandler(filename))

    pos_data = 0
    pos_main = 0

    data_labels = []

    for i in range(len(instructions)):
        
        if(instructions[i][0]=='.data'):
            pos_data = i
        elif(instructions[i][0]=='main:'):
            pos_main = i

    for i in range(pos_data+1,pos_main):

        if(instructions[i][0]!='.text' and instructions[i][0]!='.globl'):
            data_and_text['data'].append(instructions[i])

    for i in range(pos_main+1,len(instructions)):
        data_and_text['main'].append(instructions[i])

    for dat in data_and_text['data']:
        if(len(dat)==1):
            data_labels.append(dat[0][:-1])

    count = 0
    label_count = 0

    for ins in data_and_text['data']:
        if(len(ins)==1):
            label_address[data_labels[label_count]] = count
            label_count+=1

        if(ins[0]=='.word'):
            for i in range(1,len(ins)):
                data['.word'].append(int(ins[i]))
                count+=1
    count = 0

    for ins in data_and_text['main']:
        if(len(ins)==1):
            ins[0] = ins[0][:-1]
            main[ins[0]]=count
        else:
            count+=1

    for ins in data_and_text['main']:
        if(ins[0] in main.keys()):
            data_and_text['main'].remove(ins)

    # label = Label(app, text = str(data['.word']))
    # label.grid(row = 1, column = 1)
    # ic_list = Listbox(app, height = 100, width = 80)
    # ic_list.grid(row = 1, column = 1, pady = 20, padx = 20, columnspan = 3, rowspan = 6)
    ic_list.delete(0, END)
    ic_list.insert(END, 'Data Segment')
    ic_list.insert(END, '')
    ic_list.insert(END, str(data['.word']))
    ic_list.insert(END, '')
    ic_list.insert(END, '')
    ic_list.insert(END, 'Text Segment')
    ic_list.insert(END, '')
    for i in data_and_text['main']:
        ic_list.insert(END, str(i))
        ic_list.insert(END, '')
    ic_list.insert(END, '')

#Buttons
load_btn = Button(app, text = 'Load File', width = 18, command = addressfetch)
load_btn.grid(row = 0, column = 0, pady = 20)
#Buttons
run_btn = Button(app, text = 'Run File', width = 18, command = run_file)
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
reg_list.insert(END, '%-10s %s'%('PC:', str(PC)))
reg_list.insert(END, '')
reg_list.insert(END, '')
reg_list.insert(END, '')
reg_list.insert(END, '')
for register in reg:
    if(register != 'zero'):
        reg_list.insert(END, '%-10s %s'%(str(register) + ":", str(reg[register])))
    else:
        reg_list.insert(END, '%-10s %s'%(str(register) + ":", str(reg[register])))
    
reg_list.insert(END, '')
# ListBox
ic_list = Listbox(app, height = 100, width = 80)
ic_list.grid(row = 1, column = 1, pady = 20, padx = 20, columnspan = 3, rowspan = 6)
ic_list.insert(END, 'Data Segment')
ic_list.insert(END, '')
ic_list.insert(END, '')
ic_list.insert(END, 'Text Segment')
ic_list.insert(END, '')
ic_list.insert(END, '')


app.mainloop()