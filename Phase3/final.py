import re
import math
import time
from time import sleep
import threading

l1d_blocks = 32
block_size = 64
l1d_assoc = 4

l2_blocks = 64
l2_assoc = 2

reg = {"zero":0, "r0":0, "at":0, "v0":0, "v1":0, "a0":0, "a1":0, "a2":0, "a3":0, "t0":0, "t1":0, "t2":0, "t3":0, "t4":0, "t5":0, "t6":0, "t7":0,"s0":0, "s1":0, "s2":0, "s3":0 ,"s4":0 ,"s5":0, "s6":0, "s7":0, "t8":0, "t9":0, "k0":0, "k1":0, "gp":0, "sp":0, "s8":0, "ra":0}
reg_flag = {"zero":['',''], "r0":['',''], "at":['',''], "v0":['',''], "v1":['',''], "a0":['',''], "a1":['',''], "a2":['',''], "a3":['',''], "t0":['',''], "t1":['',''], "t2":['',''], "t3":['',''], "t4":['',''], "t5":['',''], "t6":['',''], "t7":['',''],"s0":['',''], "s1":['',''], "s2":['',''], "s3":['',''] ,"s4":['',''] ,"s5":['',''], "s6":['',''], "s7":['',''], "t8":['',''], "t9":['',''], "k0":['',''], "k1":['',''], "gp":['',''], "sp":['',''], "s8":['',''], "ra":['','']}
reg_address = {'zero': 5000, 'r0': 5001, 'at': 5002, 'v0': 5003, 'v1': 5004, 'a0': 5005, 'a1': 5006, 'a2': 5007, 'a3': 5008, 't0': 5009, 't1': 5010, 't2': 5011, 't3': 5012, 't4': 5013, 't5': 5014, 't6': 5015, 't7': 5016, 's0': 5017, 's1': 5018, 's2': 5019, 's3': 5020, 's4': 5021, 's5': 5022, 's6': 5023, 's7': 5024, 't8': 5025, 't9': 5026, 'k0': 5027, 'k1': 5028, 'gp': 5029, 'sp': 5030, 's8': 5031, 'ra': 5032}
base_address = 0x10010000
data_and_text = {'data':[],'main':[]}
data = {'.word':[],'.text':[]}

#Creating cache
l1d = {}
for i in range(int(l1d_blocks/l1d_assoc)):
    l1d[i] = {}
    for j in range(l1d_assoc):
        l1d[i][j] = [None]*block_size

l1i = {}
l2 = {}
for i in range(int(l2_blocks/l2_assoc)):
    l2[i] = {}
    for j in range(l2_assoc):
        l2[i][j] = [None]*block_size

mm = []
index = int(math.log(l1d_blocks/l1d_assoc, 2))
offset = int(math.log(block_size, 2))
l1d_hit_count = 0
l1d_miss_count = 0

label_address = {}
main = {}
PC = 0
msg = ""
stalls = 0
stall_flag = False
bn_flag = False

ins_type1 = ['add','sub','and','or','slt']
ins_type2 = ['addi','andi','ori','sll','srl']
ins_type3 = ['bne','beq']
ins_type4 = ['lw','sw']
ins_type5 = ['j']
ins_type6 = ['lui']

latch_f = []
latch_d = {}
latch_e = 0
latch_m = 0

ins_queue = []

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

def read_instructions(instructions):    #

    parsed_list = []
    for ins in instructions:
        if(parse(ins)):
            parsed_list.append(parse(ins))

    return parsed_list

def ins_list(instructions,data_and_text,data,label_address,main):
    
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
                mm.append(int(ins[i]))
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
        mm.append(ins)
    print(mm)
    

def stllflg_t(lock):
    global stall_flag

    lock.acquire()
    stall_flag = True
    lock.release()

def stllflg_f(lock):
    global stall_flag

    lock.acquire()
    stall_flag = False
    lock.release()

def bnflg_t(lock):
    global bn_flag

    lock.acquire()
    bn_flag = True
    lock.release()

def bnflg_f(lock):
    global bn_flag

    lock.acquire()
    bn_flag = False
    lock.release()
    
def fetch(lock):    #

    global PC
    global reg_flag
    global stall_flag
    global bn_flag
    global l1i_status
    global l1i_miss_count
    global l1i_hit_count

    l1i_hit_count = 0
    l1i_miss_count = 0

    instr = data_and_text['main'][PC]
    # print(data_and_text['main'].index(instr) == PC)

    # print(l1d)

    if(PC in l1i):
        l1i_status = 'hit'
        l1i_hit_count += 1
    else:
        l1i_status = 'miss'
        l1i_miss_count += 1
        l1i[PC] = instr
    # print(l1i)

    if((instr[0] in ins_type1) or (instr[0] in ins_type2) or (instr[0] in ins_type6)):
        regstr = instr[1].replace('$','')
        reg_flag[regstr][0] = 'd'
        reg_flag[regstr][1] = 'e'
        PC = PC + 1

    elif(instr[0]=='lw'):
        regstr = instr[1].replace('$','')
        reg_flag[regstr][0] = 'd'
        reg_flag[regstr][1] = 'm'
        PC = PC + 1

    elif(instr[0]=='sw'):
        PC+=1

    elif(instr[0] in ins_type3):
        reg1 = instr[1].replace('$','')
        reg2 = instr[2].replace('$','')

        if(reg_flag[reg1][0]=='d' and reg_flag[reg1][1]=='m'):
            #take value from latch_m
            stllflg_t(lock)
            bnflg_t(lock)
            sleep(2.0)

        elif(reg_flag[reg2][0]=='d' and reg_flag[reg2][1]=='m'):
            #take value from latch_m
            stllflg_t(lock)
            bnflg_t(lock)
            sleep(2.0)

        elif(reg_flag[reg1][0]=='e' and reg_flag[reg1][1]=='m'):
            #take value from latch_m
            stllflg_t(lock)
            bnflg_t(lock)
            sleep(2.0)

        elif(reg_flag[reg2][0]=='e' and reg_flag[reg2][1]=='m'):
            #take value from latch_m
            #print('hell')
            stllflg_t(lock)
            bnflg_t(lock)
            sleep(2.0)

        elif(reg_flag[reg1][0]=='d' and reg_flag[reg1][1]=='e'):
            #take value from latch_e
            stllflg_t(lock)
            sleep(1.0)

        elif(reg_flag[reg2][0]=='d' and reg_flag[reg2][1]=='e'):
            #take value from latch_e
            stllflg_t(lock)
            sleep(1.0)

        #print(PC)
    return instr

def decode(parsed_ins,lock):

    global main
    global PC
    global reg_flag
    global stall_flag

    if(parsed_ins[0]=='add' or parsed_ins[0]=='sub' or parsed_ins[0]=='and' or parsed_ins[0]=='or' or parsed_ins[0]=='slt'):
        regstr = parsed_ins[1].replace('$','')
        
        reg1 = parsed_ins[2].replace('$','')
        reg2 = parsed_ins[3].replace('$','')

        if(reg_flag[reg1][0]=='e' and reg_flag[reg1][1]=='m'):
            stllflg_t(lock)
        if(reg_flag[reg2][0]=='e' and reg_flag[reg2][1]=='m'):
            stllflg_t(lock)

        reg_flag[regstr][0] = 'e'
        return {'ins':parsed_ins[0],'rd':parsed_ins[1].replace('$',''),'rs':parsed_ins[2].replace('$',''),'rt':parsed_ins[3].replace('$','')}
    
    elif(parsed_ins[0]=='sll' or parsed_ins[0]=='srl' or parsed_ins[0]=='andi' or parsed_ins[0]=='ori' or parsed_ins[0]=='addi'):
        regstr = parsed_ins[1].replace('$','')

        reg1 = parsed_ins[2].replace('$','')

        if(reg_flag[reg1][0]=='e' and reg_flag[reg1][1]=='m'):
            stllflg_t(lock)

        reg_flag[regstr][0] = 'e'
        return {'ins':parsed_ins[0],'rd':parsed_ins[1].replace('$',''),'rs':parsed_ins[2].replace('$',''),'amt':parsed_ins[3]}
    
    elif(parsed_ins[0]=='bne' or parsed_ins[0]=='beq'):
        rs = parsed_ins[1].replace('$','')
        rt = parsed_ins[2].replace('$','')
        addr = parsed_ins[3]

        if(reg_flag[rs][0]=='w'):
            value1 = latch_m
        elif(reg_flag[rs][0]=='m'):
            value1 = latch_e
        else:
            value1 = reg[rs]

        if(reg_flag[rt][0]=='w'):
            value2 = latch_m
        elif(reg_flag[rt][0]=='m'):
            value2 = latch_e
        else:
            value2 = reg[rt]

        if(parsed_ins[0]=='bne'):
            if(value1 == value2):
                PC = PC + 1
            else:
                PC = main[addr]

        else:
            #print(value1,value2)
            if(value1 != value2):
                #print('in here')
                PC = PC + 1
            else:
                PC = main[addr]
        
        return {'ins':parsed_ins[0],'rs':parsed_ins[1].replace('$',''),'rt':parsed_ins[2].replace('$',''),'addr':parsed_ins[3]}
    
    elif(parsed_ins[0]=='j'):
        addr = parsed_ins[1]
        PC = main[addr]
        return {'ins':parsed_ins[0],'addr':parsed_ins[1]}

    elif(parsed_ins[0]=='lw' or parsed_ins[0]=='sw'):
        regstr = parsed_ins[1].replace('$','')

        reg_pattern = re.search(r"\$[a-z0-9]*",parsed_ins[2],re.MULTILINE)
        offset_pattern = re.search(r"\w+",parsed_ins[2],re.MULTILINE)
        
        reg1 = reg_pattern.group(0).replace('$','')
        if(reg_flag[reg1][0]=='e' and reg_flag[reg1][1]=='m'):
            stllflg_t(lock)

        reg_flag[regstr][0]='e'
        return {'ins':parsed_ins[0],'rt':parsed_ins[1].replace('$',''),'rm':reg_pattern.group(0).replace('$',''),'offset':int(offset_pattern.group(0))}

    elif(parsed_ins[0]=='lui'):
        regstr = parsed_ins[1].replace('$','')

        reg_flag[regstr][0]='e'
        return {'ins':parsed_ins[0],'rd':parsed_ins[1].replace('$',''),'addr':hex(int(parsed_ins[2]+'0000',16)),'stall_flag':False}

def execute(decoded_ins):
    
    global reg_flag
    global reg
    global l1d_status
    global l1d_hit_count
    global l1d_miss_count

    index = int(math.log(l1d_blocks/l1d_assoc, 2))
    offset = int(math.log(block_size, 2))

    if(decoded_ins['ins']=='add'):
        regstr = decoded_ins['rd']
        reg1 = decoded_ins['rs']
        reg2 = decoded_ins['rt']

        binary1 = bin(base_address + int(str(reg_address[reg1]), 16))[2:]
        index11 = int(binary1[(len(binary1)-(offset + index)): len(binary1)-offset], 2)
        index12 = int((int(binary1[:(len(binary1)-(offset + index))-1], 2)) % (l1d_blocks/index))
        index13 = int(binary1[(len(binary1)-offset):], 2)

        #forwarding value if already in use
        if(reg_flag[reg1][0]=='m'):
            value1 = latch_e
        elif(reg_flag[reg1][0]=='w'):
            value1 = latch_m
        #directly using value
        else:
            # value1 = reg[reg1]
            if(l1d[index11][index12][index13] == None):
                l1d_status = 'miss'
                l1d_miss_count += 1
                l1d[index11][index12][index13] = reg[reg1]
                value1 = l1d[index11][index12][index13]
            else:
                l1d_status = 'hit'
                l1d_hit_count += 1
                value1 = l1d[index11][index12][index13]

        binary2 = bin(base_address + int(str(reg_address[reg2]), 16))[2:]
        index21 = int(binary2[(len(binary2)-(offset + index)): len(binary2)-offset], 2)
        index22 = (int(binary2[:(len(binary2)-(offset + index))-1], 2)) % (l1d_blocks/index)
        index23 = int(binary2[(len(binary2)-offset):], 2)

        #forwarding value if already in use
        if(reg_flag[reg2][0]=='m'):
            value2 = latch_e
        elif(reg_flag[reg2][0]=='w'):
            value2 = latch_m
        #directly using value
        else:
            # value2 = reg[reg2]
            if(l1d[index21][index22][index23] == None):
                l1d_status = 'miss'
                l1d_miss_count += 1
                l1d[index21][index22][index23] = reg[reg1]
                value2 = l1d[index21][index22][index23]
            else:
                l1d_status = 'hit'
                l1d_hit_count += 1
                value2 = l1d[index21][index22][index23]

        reg_flag[regstr][0] = 'm'
        return (value1+value2,reg)

    elif(decoded_ins['ins']=='sub'):
        regstr = decoded_ins['rd']
        reg1 = decoded_ins['rs']
        reg2 = decoded_ins['rt']

        binary1 = bin(base_address + int(str(reg_address[reg1]), 16))[2:]
        index11 = int(binary1[(len(binary1)-(offset + index)): len(binary1)-offset], 2)
        index12 = int((int(binary1[:(len(binary1)-(offset + index))-1], 2)) % (l1d_blocks/index))
        index13 = int(binary1[(len(binary1)-offset):], 2)

        #forwarding value if already in use
        if(reg_flag[reg1][0]=='m'):
            value1 = latch_e
        elif(reg_flag[reg1][0]=='w'):
            value1 = latch_m
        #directly using value
        else:
            # value1 = reg[reg1]
            if(l1d[index11][index12][index13] == None):
                l1d_status = 'miss'
                l1d_miss_count += 1
                l1d[index11][index12][index13] = reg[reg1]
                value1 = l1d[index11][index12][index13]
            else:
                l1d_status = 'hit'
                l1d_hit_count += 1
                value1 = l1d[index11][index12][index13]

        binary2 = bin(base_address + int(str(reg_address[reg2]), 16))[2:]
        index21 = int(binary2[(len(binary2)-(offset + index)): len(binary2)-offset], 2)
        index22 = (int(binary2[:(len(binary2)-(offset + index))-1], 2)) % (l1d_blocks/index)
        index23 = int(binary2[(len(binary2)-offset):], 2)

        #forwarding value if already in use
        if(reg_flag[reg2][0]=='m'):
            value2 = latch_e
        elif(reg_flag[reg2][0]=='w'):
            value2 = latch_m
        #directly using value
        else:
            # value2 = reg[reg2]
            if(l1d[index21][index22][index23] == None):
                l1d_status = 'miss'
                l1d_miss_count += 1
                l1d[index21][index22][index23] = reg[reg1]
                value2 = l1d[index21][index22][index23]
            else:
                l1d_status = 'hit'
                l1d_hit_count += 1
                value2 = l1d[index21][index22][index23]

        reg_flag[regstr][0] = 'm'
        return (value1-value2,decoded_ins['rd'])

    elif(decoded_ins['ins']=='and'):
        regstr = decoded_ins['rd']
        reg1 = decoded_ins['rs']
        reg2 = decoded_ins['rt']

        binary1 = bin(base_address + int(str(reg_address[reg1]), 16))[2:]
        index11 = int(binary1[(len(binary1)-(offset + index)): len(binary1)-offset], 2)
        index12 = int((int(binary1[:(len(binary1)-(offset + index))-1], 2)) % (l1d_blocks/index))
        index13 = int(binary1[(len(binary1)-offset):], 2)

        #forwarding value if already in use
        if(reg_flag[reg1][0]=='m'):
            value1 = latch_e
        elif(reg_flag[reg1][0]=='w'):
            value1 = latch_m
        #directly using value
        else:
            # value1 = reg[reg1]
            if(l1d[index11][index12][index13] == None):
                l1d_status = 'miss'
                l1d_miss_count += 1
                l1d[index11][index12][index13] = reg[reg1]
                value1 = l1d[index11][index12][index13]
            else:
                l1d_status = 'hit'
                l1d_hit_count += 1
                value1 = l1d[index11][index12][index13]

        binary2 = bin(base_address + int(str(reg_address[reg2]), 16))[2:]
        index21 = int(binary2[(len(binary2)-(offset + index)): len(binary2)-offset], 2)
        index22 = (int(binary2[:(len(binary2)-(offset + index))-1], 2)) % (l1d_blocks/index)
        index23 = int(binary2[(len(binary2)-offset):], 2)

        #forwarding value if already in use
        if(reg_flag[reg2][0]=='m'):
            value2 = latch_e
        elif(reg_flag[reg2][0]=='w'):
            value2 = latch_m
        #directly using value
        else:
            # value2 = reg[reg2]
            if(l1d[index21][index22][index23] == None):
                l1d_status = 'miss'
                l1d_miss_count += 1
                l1d[index21][index22][index23] = reg[reg1]
                value2 = l1d[index21][index22][index23]
            else:
                l1d_status = 'hit'
                l1d_hit_count += 1
                value2 = l1d[index21][index22][index23]

        reg_flag[regstr][0] = 'm'
        return (value1 and value2 ,decoded_ins['rd'])

    elif(decoded_ins['ins']=='or'):
        regstr = decoded_ins['rd']
        reg1 = decoded_ins['rs']
        reg2 = decoded_ins['rt']

        binary1 = bin(base_address + int(str(reg_address[reg1]), 16))[2:]
        index11 = int(binary1[(len(binary1)-(offset + index)): len(binary1)-offset], 2)
        index12 = int((int(binary1[:(len(binary1)-(offset + index))-1], 2)) % (l1d_blocks/index))
        index13 = int(binary1[(len(binary1)-offset):], 2)

        #forwarding value if already in use
        if(reg_flag[reg1][0]=='m'):
            value1 = latch_e
        elif(reg_flag[reg1][0]=='w'):
            value1 = latch_m
        #directly using value
        else:
            # value1 = reg[reg1]
            if(l1d[index11][index12][index13] == None):
                l1d_status = 'miss'
                l1d_miss_count += 1
                l1d[index11][index12][index13] = reg[reg1]
                value1 = l1d[index11][index12][index13]
            else:
                l1d_status = 'hit'
                l1d_hit_count += 1
                value1 = l1d[index11][index12][index13]

        binary2 = bin(base_address + int(str(reg_address[reg2]), 16))[2:]
        index21 = int(binary2[(len(binary2)-(offset + index)): len(binary2)-offset], 2)
        index22 = (int(binary2[:(len(binary2)-(offset + index))-1], 2)) % (l1d_blocks/index)
        index23 = int(binary2[(len(binary2)-offset):], 2)

        #forwarding value if already in use
        if(reg_flag[reg2][0]=='m'):
            value2 = latch_e
        elif(reg_flag[reg2][0]=='w'):
            value2 = latch_m
        #directly using value
        else:
            # value2 = reg[reg2]
            if(l1d[index21][index22][index23] == None):
                l1d_status = 'miss'
                l1d_miss_count += 1
                l1d[index21][index22][index23] = reg[reg1]
                value2 = l1d[index21][index22][index23]
            else:
                l1d_status = 'hit'
                l1d_hit_count += 1
                value2 = l1d[index21][index22][index23]

        reg_flag[regstr][0] = 'm'
        return (value1 or value2 ,decoded_ins['rd'])

    elif(decoded_ins['ins']=='slt'):
        regstr = decoded_ins['rd']
        reg1 = decoded_ins['rs']
        reg2 = decoded_ins['rt']

        binary1 = bin(base_address + int(str(reg_address[reg1]), 16))[2:]
        index11 = int(binary1[(len(binary1)-(offset + index)): len(binary1)-offset], 2)
        index12 = int((int(binary1[:(len(binary1)-(offset + index))-1], 2)) % (l1d_blocks/index))
        index13 = int(binary1[(len(binary1)-offset):], 2)

        #forwarding value if already in use
        if(reg_flag[reg1][0]=='m'):
            value1 = latch_e
        elif(reg_flag[reg1][0]=='w'):
            value1 = latch_m
        #directly using value
        else:
            # value1 = reg[reg1]
            if(l1d[index11][index12][index13] == None):
                l1d_status = 'miss'
                l1d_miss_count += 1
                l1d[index11][index12][index13] = reg[reg1]
                value1 = l1d[index11][index12][index13]
            else:
                l1d_status = 'hit'
                l1d_hit_count += 1
                value1 = l1d[index11][index12][index13]

        binary2 = bin(base_address + int(str(reg_address[reg2]), 16))[2:]
        index21 = int(binary2[(len(binary2)-(offset + index)): len(binary2)-offset], 2)
        index22 = (int(binary2[:(len(binary2)-(offset + index))-1], 2)) % (l1d_blocks/index)
        index23 = int(binary2[(len(binary2)-offset):], 2)

        #forwarding value if already in use
        if(reg_flag[reg2][0]=='m'):
            value2 = latch_e
        elif(reg_flag[reg2][0]=='w'):
            value2 = latch_m
        #directly using value
        else:
            # value2 = reg[reg2]
            if(l1d[index21][index22][index23] == None):
                l1d_status = 'miss'
                l1d_miss_count += 1
                l1d[index21][index22][index23] = reg[reg1]
                value2 = l1d[index21][index22][index23]
            else:
                l1d_status = 'hit'
                l1d_hit_count += 1
                value2 = l1d[index21][index22][index23]

        reg_flag[regstr][0] = 'm'
        #print(value1,value2)
        if(value1 < value2):
            return (1,decoded_ins['rd'])
        else:
            return (0,decoded_ins['rd'])

    elif(decoded_ins['ins']=='lui'):    
        regstr = decoded_ins['rd']
        reg_flag[regstr][0] = 'm'
        return (decoded_ins['addr'],decoded_ins['rd'])

    elif(decoded_ins['ins']=='lw' or decoded_ins['ins']=='sw'):     #
        regstr = decoded_ins['rt']
        reg1 = decoded_ins['rm']

        binary1 = bin(base_address + int(str(reg_address[reg1]), 16))[2:]
        index11 = int(binary1[(len(binary1)-(offset + index)): len(binary1)-offset], 2)
        index12 = int((int(binary1[:(len(binary1)-(offset + index))-1], 2)) % (l1d_blocks/index))
        index13 = int(binary1[(len(binary1)-offset):], 2)

        #forwarding value if already in use
        if(reg_flag[reg1][0]=='m'):
            value1 = latch_e
        elif(reg_flag[reg1][0]=='w'):
            value1 = latch_m
        #directly using value
        else:
            # value1 = reg[reg1]
            if(l1d[index11][index12][index13] == None):
                l1d_status = 'miss'
                l1d_miss_count += 1
                l1d[index11][index12][index13] = reg[reg1]
                value1 = l1d[index11][index12][index13]
            else:
                l1d_status = 'hit'
                l1d_hit_count += 1
                value1 = l1d[index11][index12][index13]

        # print(value1)
        offset = decoded_ins['offset']
        index = 0
        if(int(str(value1),16)-base_address>=0 and (int(str(value1),16)-base_address)%4==0 and offset%4==0):
            index = int((int(str(value1),16)-base_address)/4 + offset/4)
        reg_flag[regstr][0] = 'm'
        # print(index,decoded_ins)
        return (index,decoded_ins)

    elif(decoded_ins['ins']=='addi'):
        regstr = decoded_ins['rd']
        reg1 = decoded_ins['rs']

        binary1 = bin(base_address + int(str(reg_address[reg1]), 16))[2:]
        index11 = int(binary1[(len(binary1)-(offset + index)): len(binary1)-offset], 2)
        index12 = int((int(binary1[:(len(binary1)-(offset + index))-1], 2)) % (l1d_blocks/index))
        index13 = int(binary1[(len(binary1)-offset):], 2)

        if(reg_flag[reg1][0]=='m'):
            value1 = latch_e
        elif(reg_flag[reg1][0]=='w'):
            value1 = latch_m
        #directly using value
        else:
            # value1 = reg[reg1]
            if(l1d[index11][index12][index13] == None):
                l1d_status = 'miss'
                l1d_miss_count += 1
                l1d[index11][index12][index13] = reg[reg1]
                value1 = l1d[index11][index12][index13]
            else:
                l1d_status = 'hit'
                l1d_hit_count += 1
                value1 = l1d[index11][index12][index13]

        reg_flag[regstr][0] = 'm'
        addend = int(decoded_ins['amt'])

        if(type(value1)==str and value1[0:2]=='0x'):
            return(hex(int(value1,16)+addend),decoded_ins['rd'])
        else:
            return(value1+addend,decoded_ins['rd'])

    elif(decoded_ins['ins']=='ori'):
        regstr = decoded_ins['rd']
        reg1 = decoded_ins['rs']

        binary1 = bin(base_address + int(str(reg_address[reg1]), 16))[2:]
        index11 = int(binary1[(len(binary1)-(offset + index)): len(binary1)-offset], 2)
        index12 = int((int(binary1[:(len(binary1)-(offset + index))-1], 2)) % (l1d_blocks/index))
        index13 = int(binary1[(len(binary1)-offset):], 2)

        if(reg_flag[reg1][0]=='m'):
            value1 = latch_e
        elif(reg_flag[reg1][0]=='w'):
            value1 = latch_m
        #directly using value
        else:
            # value1 = reg[reg1]
            if(l1d[index11][index12][index13] == None):
                l1d_status = 'miss'
                l1d_miss_count += 1
                l1d[index11][index12][index13] = reg[reg1]
                value1 = l1d[index11][index12][index13]
            else:
                l1d_status = 'hit'
                l1d_hit_count += 1
                value1 = l1d[index11][index12][index13]

        reg_flag[regstr][0] = 'm'
        return(value1 or decoded_ins['amt'],decoded_ins['rd'])

    elif(decoded_ins['ins']=='andi'):
        regstr = decoded_ins['rd']
        reg1 = decoded_ins['rs']

        binary1 = bin(base_address + int(str(reg_address[reg1]), 16))[2:]
        index11 = int(binary1[(len(binary1)-(offset + index)): len(binary1)-offset], 2)
        index12 = int((int(binary1[:(len(binary1)-(offset + index))-1], 2)) % (l1d_blocks/index))
        index13 = int(binary1[(len(binary1)-offset):], 2)

        if(reg_flag[reg1][0]=='m'):
            value1 = latch_e
        elif(reg_flag[reg1][0]=='w'):
            value1 = latch_m
        #directly using value
        else:
            # value1 = reg[reg1]
            if(l1d[index11][index12][index13] == None):
                l1d_status = 'miss'
                l1d_miss_count += 1
                l1d[index11][index12][index13] = reg[reg1]
                value1 = l1d[index11][index12][index13]
            else:
                l1d_status = 'hit'
                l1d_hit_count += 1
                value1 = l1d[index11][index12][index13]

        reg_flag[regstr][0] = 'm'
        anded = decoded_ins['amt']
        result = hex(int(value1,16)&int(anded,16))
        return(result,decoded_ins['rd'])

    else:
        return ()
        
def memory(execute):
    
    global reg_flag
    global data
    global reg
    global l1d_status
    global l1d_hit_count
    global l1d_miss_count

    # print(execute)
    if(execute):
        if (type(execute[1]) is dict and 'offset' in execute[1].keys()):
            index1 = execute[0]
            binary1 = bin(base_address + int(str(index1*4), 16))[2:]
            index11 = int(binary1[(len(binary1)-(offset + index)): len(binary1)-offset], 2)
            index12 = int((int(binary1[:(len(binary1)-(offset + index))-1], 2)) % (l1d_blocks/index))
            index13 = int(binary1[(len(binary1)-offset):], 2)

            if(execute[1]['ins']=='lw'):
                reg_flag[execute[1]['rt']][0] = 'w'
                # print((data['.word'][index],execute[1]['rt']))
                if(l1d[index11][index12][index13] == None):
                    l1d_status = 'miss'
                    l1d_miss_count += 1
                    l1d[index11][index12][index13] = mm[index1]
                    # print(mm[index1])
                    value1 = l1d[index11][index12][index13]
                else:
                    l1d_status = 'hit'
                    l1d_hit_count += 1
                    value1 = l1d[index11][index12][index13]
                # print(value1)

                return (value1, execute[1]['rt'])

            elif(execute[1]['ins']=='sw'):
                reg1 = execute[1]['rt']

                binary1 = bin(base_address + int(str(reg_address[reg1]), 16))[2:]
                index11 = int(binary1[(len(binary1)-(offset + index)): len(binary1)-offset], 2)
                index12 = int((int(binary1[:(len(binary1)-(offset + index))-1], 2)) % (l1d_blocks/index))
                index13 = int(binary1[(len(binary1)-offset):], 2)

                if(reg_flag[reg1][0]=='w'):
                    value = latch_m
                else:
                    # value = reg[reg1]
                    if(l1d[index11][index12][index13] == None):
                        l1d_status = 'miss'
                        l1d_miss_count += 1
                        l1d[index11][index12][index13] = reg[reg1]
                        value = l1d[index11][index12][index13]
                        # print("reg " + str(reg[reg1]))
                    else:
                        l1d_status = 'hit'
                        l1d_hit_count += 1
                        value = l1d[index11][index12][index13]
                    # print(value)

                if(index1>=len(data['.word'])):
                    count = index1-len(data['.word'])
                    for i in range(count):
                        data['.word'].append(0)
                    data['.word'].append(value)
                    print(data['.word'])
                    return ()
                else:
                    data['.word'][index1] = value
                    return ()
        else:
            reg_flag[execute[1]][0] = 'w'
            return execute
    else:
        return ()

def writeback(result):
        global reg_flag
        global reg

        if(result):
            regstr = result[1]
            value = result[0]
            reg[regstr] = value
            reg_flag[regstr] = ['','']             

def pipeline(lock):

    global PC
    global latch_f
    global latch_e
    global latch_d
    global latch_m
    global stall_flag

    print(PC)
    print(data)
    print("hits", l1d_hit_count)

    #fetch cycle
    start = time.perf_counter()
    f = fetch(lock)
    if(f):
        lock.acquire()
        latch_f = f
        lock.release()
    end = time.perf_counter()
    if(end-start<1):
        sleep(1.0-round(end-start,2))
    else:
        sleep(1.0)
    if(stall_flag==True):
        sleep(1.0)
        stllflg_f(lock)
    #decode cycle
    sleep(0.5)
    start = time.perf_counter()
    d = decode(f,lock)
    if(d):
        lock.acquire()
        latch_d = d
        lock.release()
    end = time.perf_counter()
    sleep(0.5-round(end-start,2))
    if(stall_flag==True):
        sleep(1.0)
        stllflg_f(lock)
    #execute cycle
    start = time.perf_counter()
    e = execute(d)
    if(e):
        lock.acquire()
        latch_e = e[0]
        lock.release()
    end = time.perf_counter()
    sleep(1.0-round(end-start,2))
    #memory cycle
    start = time.perf_counter()
    m = memory(e)
    if(m):
        lock.acquire()
        latch_m = m[0]
        lock.release()
    end = time.perf_counter()
    sleep(1.0-round(end-start,2))
    #writeback cycle
    start = time.perf_counter()
    w = writeback(m)
    end = time.perf_counter()
    sleep(1.0-round(end-start,2))
    
def Simulate():

    global PC
    global reg
    global data
    global latch_d
    global latch_f
    global latch_e
    global latch_m
    global reg_flag
    global stall_flag
    global bn_flag

    instructions = read_instructions(fileHandler("/home/tapish/CO/Project_Phase 1/COproj_phase1/Phase1/trial.asm"))
    ins_list(instructions,data_and_text,data,label_address,main)

    process_list = []
    lock = threading.Lock()
    instruction = data_and_text['main']
    
    start1 = time.perf_counter()
    count = 0

    while(PC<len(instruction)-1):
        start = time.perf_counter()
        if(stall_flag==True and bn_flag==True):
            sleep(2.0)
            stllflg_f(lock)
            bnflg_f(lock)

        elif(stall_flag==True):
            sleep(1.0)
            stllflg_f(lock)

        if(len(latch_f)>0):
            if(latch_f[0] in ins_type5 or latch_f[0] in ins_type3):
                sleep(1.0)
        
        p = threading.Thread(target=pipeline,args=(lock,))
        process_list.append(p)
        if(count>=5):
            process_list[count-5].join()
        process_list[count].start()
        count+=1
        end = time.perf_counter()
        if(round(end-start,2)<1.0):
            sleep(1.0-round(end-start,2))
        else:
            sleep(1.0-round((end-start)/10,2))
        # print(reg)
        # print(data['.word'])

    for i in range(count-4,count):
        process_list[i].join()

    # for ins in instruction:
    #     pipeline(ins)

    end1 = time.perf_counter()
    print(round(end1-start1,3))
    print(count)
    print()
    print(reg)
    print(data['.word'])



if __name__== "__main__":
    Simulate()