# Simulator for phase 1
#instructions = ["add","sub","lw","sw","bne"]
import re

reg = {"r0":0, "at":0, "v0":0, "v1":0, "a0":0, "a1":0, "a2":0, "a3":0, "t0":0, "t1":0, "t2":0, "t3":0, "t4":0, "t5":0, "t6":0, "t7":0,"s0":0, "s1":1, "s2":3, "s3":0 ,"s4":0 ,"s5":0, "s6":0, "s7":0, "t8":0, "t9":0, "k0":0, "k1":0, "gp":0, "sp":0, "s8":0, "ra":0}
base_address = 10010000
bne_flag = ''

def run_instruction(instruction):

    if(instruction[0]=='add'):
        if(len(instruction)!=4):
            print("Error in the given instruction. Missing or extra operand given")

        else:
            reg1 = instruction[1].replace('$','')
            reg2 = instruction[2].replace('$','')
            reg3 = instruction[3].replace('$','')
            reg[reg1] = reg[reg2]+reg[reg3]

    elif(instruction[0]=='sub'):
        if(len(instruction)!=4):
            print("Error in the given instruction. Missing or extra operand given")

        else:
            reg1 = instruction[1].replace('$','')
            reg2 = instruction[2].replace('$','')
            reg3 = instruction[3].replace('$','')
            reg[reg1] = reg[reg2]-reg[reg3]

    elif(instruction[0]=='lw'):
        if(len(instruction)!=3):
            print("Error in the given instruction. Missing or extra operand given")

        else:
            reg1 = instruction[1].replace('$','')
            reg2 = reg_pattern.group(0)
            reg2 = reg2.replace('$','')
            offset = offset_pattern.group(0)
            
    elif(instruction[0]=='sw'):
        if(len(instruction)!=3):
            print("Error in the given instruction. Missing or extra operand given")

        else:
            reg_pattern = re.search(r"\$[a-z0-9]*",instruction[2],re.MULTILINE)
            offset_pattern = re.search(r"\w+",instruction[2],re.MULTILINE)
            reg1 = instruction[1]
            reg2 = reg_pattern.group(0)
            reg2 = reg2.replace('$','')
            offset = offset_pattern.group(0)

    elif(instruction[0]=='bne'):

        if(len(instruction)!=4):
            print("Error in the given instruction. Missing or extra operand given")
        
        else:
            reg1 = instruction[1].replace('$','')
            reg2 = instruction[2].replace('$','')
            
        if(reg[reg1]!=reg[reg2]):
            bne_flag = instruction[3]   

        else:
            bne_flag = ''

#result = re.match(r"\d+","34($s0)")

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

instructions = read_instructions(fileHandler("C:/Users/Admin/Desktop/programming/Assembly/bubble_sort.asm"))
data_and_text = {'data':[],'main':[],}

pos_data = 0
pos_main = 0

data_labels = []
main_labels = []

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
        data_labels.append(dat[0])

data = {'.word':[],'.text':[]}

label_address = {}

count = 0
label_count = 0

for ins in data_and_text['data']:
    if(len(ins)==1):
        label_address[data_labels[label_count]] = count
        label_count+=1

    if(ins[0]=='.word'):
        for i in range(1,len(ins)):
            data['.word'].append(ins[i])
            count+=1

main = {}

count = 0

for ins in data_and_text['main']:
    if(len(ins)==1):
        main[ins[0]]=count+1
    else:
        count+=1

for key in main.keys():
    for ins in data_and_text['main']:
        if(key in ins):
            data_and_text['main'].remove(ins)
            break


# print(data)
# print(label_address)
# print(main)
# print(parse("add $s1, $s2, $s3"))