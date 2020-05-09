import re
import pandas as pd
from Cache_interface import Cache

reg = {"zero":0, "r0":0, "at":0, "v0":0, "v1":0, "a0":0, "a1":0, "a2":0, "a3":0, "t0":0, "t1":0, "t2":0, "t3":0, "t4":0, "t5":0, "t6":0, "t7":0,"s0":0, "s1":0, "s2":0, "s3":0 ,"s4":0 ,"s5":0, "s6":0, "s7":0, "t8":0, "t9":0, "k0":0, "k1":0, "gp":0, "sp":0, "s8":0, "ra":0}
reg_flag = {"zero":['',''], "r0":['',''], "at":['',''], "v0":['',''], "v1":['',''], "a0":['',''], "a1":['',''], "a2":['',''], "a3":['',''], "t0":['',''], "t1":['',''], "t2":['',''], "t3":['',''], "t4":['',''], "t5":['',''], "t6":['',''], "t7":['',''],"s0":['',''], "s1":['',''], "s2":['',''], "s3":['',''] ,"s4":['',''] ,"s5":['',''], "s6":['',''], "s7":['',''], "t8":['',''], "t9":['',''], "k0":['',''], "k1":['',''], "gp":['',''], "sp":['',''], "s8":['',''], "ra":['','']}
base_address = 0x10010000
data_and_text = {'data':[],'main':[]}
data = {'.word':[],'.text':[]}
label_address = {}
main = {}
PC = 0
stalls = 0
mem_stalls = 0
write_stall = 0
stall_flag1 = False
stall_flag2 = False
stall_flag3 = False
bn_flag = False
ms_flag1 = False
ms_flag2 = False
wr_flag = False
# wr_flag1 = False
# wr_flag2 = False
# initializing caches
l1_block_size = 0
l1_set_assoc = 0
l1_blocks = 0
l2_block_size = 0
l2_set_assoc = 0
l2_blocks = 0
L1 = object()
L2 = object()

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

def reinitialize():
    global reg
    global reg_flag
    global base_address
    global data_and_text
    global data
    global label_address
    global main
    global PC
    global stalls
    global mem_stalls
    global write_stall
    global stall_flag1
    global stall_flag2
    global stall_flag3
    global bn_flag
    global ms_flag1
    global ms_flag2
    global wr_flag
    global latch_f
    global latch_d
    global latch_e
    global latch_m
    global ins_queue
    global l1_block_size
    global l1_set_assoc
    global l1_blocks
    global l2_block_size
    global l2_set_assoc
    global l2_blocks
    global L1
    global L2

    reg = {"zero":0, "r0":0, "at":0, "v0":0, "v1":0, "a0":0, "a1":0, "a2":0, "a3":0, "t0":0, "t1":0, "t2":0, "t3":0, "t4":0, "t5":0, "t6":0, "t7":0,"s0":0, "s1":0, "s2":0, "s3":0 ,"s4":0 ,"s5":0, "s6":0, "s7":0, "t8":0, "t9":0, "k0":0, "k1":0, "gp":0, "sp":0, "s8":0, "ra":0}
    reg_flag = {"zero":['',''], "r0":['',''], "at":['',''], "v0":['',''], "v1":['',''], "a0":['',''], "a1":['',''], "a2":['',''], "a3":['',''], "t0":['',''], "t1":['',''], "t2":['',''], "t3":['',''], "t4":['',''], "t5":['',''], "t6":['',''], "t7":['',''],"s0":['',''], "s1":['',''], "s2":['',''], "s3":['',''] ,"s4":['',''] ,"s5":['',''], "s6":['',''], "s7":['',''], "t8":['',''], "t9":['',''], "k0":['',''], "k1":['',''], "gp":['',''], "sp":['',''], "s8":['',''], "ra":['','']}
    base_address = 0x10010000
    data_and_text = {'data':[],'main':[]}
    data = {'.word':[],'.text':[]}
    label_address = {}
    main = {}
    PC = 0
    stalls = 0
    mem_stalls = 0
    write_stall = 0
    stall_flag1 = False
    stall_flag2 = False
    stall_flag3 = False
    bn_flag = False
    ms_flag1 = False
    ms_flag2 = False
    wr_flag = False
    latch_f = []
    latch_d = {}
    latch_e = 0
    latch_m = 0
    ins_queue = []
    l1_block_size = 0
    l1_set_assoc = 0
    l1_blocks = 0
    l2_block_size = 0
    l2_set_assoc = 0
    l2_blocks = 0
    L1 = object()
    L2 = object()

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

def stllflg1_t():
    global stall_flag1

    stall_flag1 = True

def stllflg1_f():
    global stall_flag1

    stall_flag1 = False

def stllflg2_t():
    global stall_flag2

    stall_flag2 = True

def stllflg2_f():
    global stall_flag2

    stall_flag2 = False

def stllflg3_t():
    global stall_flag2

    stall_flag3 = True

def stllflg3_f():
    global stall_flag2

    stall_flag3 = False

def bnflg_t():
    global bn_flag

    bn_flag = True

def bnflg_f():
    global bn_flag

    bn_flag = False
    
# def print_stages(lst):
#     flag = False
#     mark = 1
#     for i in range(5,len(lst)):
#         if(flag==False):
#             if(lst[i][0]!='w'):
#                 for _ in range(mark):
#                     lst[i].insert(0,' ')
#                 flag = True
#             else:
#                 for _ in range(mark):
#                     lst[i].insert(0,' ')
#                 mark+=1
#         else:
#             if(lst[i][0]=='w'):
#                 flag = False
#             for _ in range(mark):
#                 lst[i].insert(0," ")
#             mark+=1

#     cols = []
#     for i in range(174):
#         cols.append('c'+str(i+1))
#     df = pd.DataFrame(lst,columns=cols)
#     df.to_excel('new_new_cycles.xlsx',header=False,index=False)

def fetch():

    global PC
    global reg_flag
    global stall_flag1
    global stall_flag3
    global bn_flag

    instr = data_and_text['main'][PC]

    if((instr[0] in ins_type1) or (instr[0] in ins_type2) or (instr[0] in ins_type6)):
        regstr = instr[1].replace('$','')

        reg_flag[regstr][0] = 'f'
        reg_flag[regstr][1] = 'e'
        PC = PC + 1


    elif(instr[0]=='lw'):
        regstr = instr[1].replace('$','')

        reg_flag[regstr][0] = 'f'
        reg_flag[regstr][1] = 'm'
        PC = PC + 1


    elif(instr[0]=='sw'):
        PC+=1

    elif(instr[0] in ins_type3):
        reg1 = instr[1].replace('$','')
        reg2 = instr[2].replace('$','')
        bnflg_t()
        #print(reg_flag[reg1],reg_flag[reg2])
        if(reg_flag[reg1][0]=='d' and reg_flag[reg1][1]=='m'):
            #take value from latch_m
            stllflg3_t()

        elif(reg_flag[reg2][0]=='d' and reg_flag[reg2][1]=='m'):
            #take value from latch_m
            stllflg3_t()

        elif(reg_flag[reg1][0]=='e' and reg_flag[reg1][1]=='m'):
            #take value from latch_m
            stllflg1_t()

        elif(reg_flag[reg2][0]=='e' and reg_flag[reg2][1]=='m'):
            #take value from latch_m
            #print('hell')
            stllflg1_t()

        elif(reg_flag[reg1][0]=='d' and reg_flag[reg1][1]=='e'):
            #take value from latch_e
            stllflg1_t()

        elif(reg_flag[reg2][0]=='d' and reg_flag[reg2][1]=='e'):
            #take value from latch_e
            stllflg1_t()

    elif(instr[0] in ins_type5):
        bnflg_t()
        #print(PC)
    elif(instr[0]=='jr'):
        PC+=1

    return instr

def decode(parsed_ins):

    global main
    global PC
    global reg_flag
    global stall_flag2

    if(parsed_ins[0]=='add' or parsed_ins[0]=='sub' or parsed_ins[0]=='and' or parsed_ins[0]=='or' or parsed_ins[0]=='slt'):
        regstr = parsed_ins[1].replace('$','')
        
        reg1 = parsed_ins[2].replace('$','')
        reg2 = parsed_ins[3].replace('$','')

        if(reg_flag[reg1][0]=='e' and reg_flag[reg1][1]=='m'):
            stllflg2_t()
        elif(reg_flag[reg2][0]=='e' and reg_flag[reg2][1]=='m'):
            stllflg2_t()

        reg_flag[regstr][0] = 'd'

        return {'ins':parsed_ins[0],'rd':parsed_ins[1].replace('$',''),'rs':parsed_ins[2].replace('$',''),'rt':parsed_ins[3].replace('$','')}
    
    elif(parsed_ins[0]=='sll' or parsed_ins[0]=='srl' or parsed_ins[0]=='andi' or parsed_ins[0]=='ori' or parsed_ins[0]=='addi'):
        regstr = parsed_ins[1].replace('$','')

        reg1 = parsed_ins[2].replace('$','')

        if(reg_flag[reg1][0]=='e' and reg_flag[reg1][1]=='m'):
            stllflg2_t()

        reg_flag[regstr][0] = 'd'

        return {'ins':parsed_ins[0],'rd':parsed_ins[1].replace('$',''),'rs':parsed_ins[2].replace('$',''),'amt':parsed_ins[3]}
    
    elif(parsed_ins[0]=='bne' or parsed_ins[0]=='beq'):
        rs = parsed_ins[1].replace('$','')
        rt = parsed_ins[2].replace('$','')
        addr = parsed_ins[3]
        value1 = 0
        value2 = 0
        #print(reg_flag[rs],reg_flag[rt])
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
            stllflg2_t()

        if(parsed_ins[0]=='lw'):
            reg_flag[regstr][0]='d'

        return {'ins':parsed_ins[0],'rt':parsed_ins[1].replace('$',''),'rm':reg_pattern.group(0).replace('$',''),'offset':int(offset_pattern.group(0))}

    elif(parsed_ins[0]=='lui'):
        regstr = parsed_ins[1].replace('$','')
        reg_flag[regstr][0]='d'
        return {'ins':parsed_ins[0],'rd':parsed_ins[1].replace('$',''),'addr':hex(int(parsed_ins[2]+'0000',16))}

    elif(parsed_ins[0]=='jr'):
        return {'ins':parsed_ins[0]}

def execute(decoded_ins):
    
    global reg_flag
    global reg

    if(decoded_ins['ins']=='add'):
        regstr = decoded_ins['rd']
        reg1 = decoded_ins['rs']
        reg2 = decoded_ins['rt']

        #forwarding value if already in use
        if(reg_flag[reg1][0]=='m'):
            value1 = latch_e
        elif(reg_flag[reg1][0]=='w'):
            value1 = latch_m
        #directly using value
        else:
            value1 = reg[reg1]

        #forwarding value if already in use
        if(reg_flag[reg2][0]=='m'):
            value2 = latch_e
        elif(reg_flag[reg2][0]=='w'):
            value2 = latch_m
        #directly using value
        else:
            value2 = reg[reg2]

        reg_flag[regstr][0] = 'e'
        return (value1+value2,reg)

    elif(decoded_ins['ins']=='sub'):
        regstr = decoded_ins['rd']
        reg1 = decoded_ins['rs']
        reg2 = decoded_ins['rt']

        #forwarding value if already in use
        if(reg_flag[reg1][0]=='m'):
            value1 = latch_e
        elif(reg_flag[reg1][0]=='w'):
            value1 = latch_m
        #directly using value
        else:
            value1 = reg[reg1]

        #forwarding value if already in use
        if(reg_flag[reg2][0]=='m'):
            value2 = latch_e
        elif(reg_flag[reg2][0]=='w'):
            value2 = latch_m
        #directly using value
        else:
            value2 = reg[reg2]
        reg_flag[regstr][0] = 'e'
        return (value1-value2,decoded_ins['rd'])

    elif(decoded_ins['ins']=='and'):
        regstr = decoded_ins['rd']
        reg1 = decoded_ins['rs']
        reg2 = decoded_ins['rt']

        #forwarding value if already in use
        if(reg_flag[reg1][0]=='m'):
            value1 = latch_e
        elif(reg_flag[reg1][0]=='w'):
            value1 = latch_m
        #directly using value
        else:
            value1 = reg[reg1]

        #forwarding value if already in use
        if(reg_flag[reg2][0]=='m'):
            value2 = latch_e
        elif(reg_flag[reg2][0]=='w'):
            value2 = latch_m
        #directly using value
        else:
            value2 = reg[reg2]
        reg_flag[regstr][0] = 'e'
        return (value1 and value2 ,decoded_ins['rd'])

    elif(decoded_ins['ins']=='or'):
        regstr = decoded_ins['rd']
        reg1 = decoded_ins['rs']
        reg2 = decoded_ins['rt']

        #forwarding value if already in use
        if(reg_flag[reg1][0]=='m'):
            value1 = latch_e
        elif(reg_flag[reg1][0]=='w'):
            value1 = latch_m
        #directly using value
        else:
            value1 = reg[reg1]

        #forwarding value if already in use
        if(reg_flag[reg2][0]=='m'):
            value2 = latch_e
        elif(reg_flag[reg2][0]=='w'):
            value2 = latch_m
        #directly using value
        else:
            value2 = reg[reg2]
        reg_flag[regstr][0] = 'e'
        return (value1 or value2 ,decoded_ins['rd'])

    elif(decoded_ins['ins']=='slt'):
        regstr = decoded_ins['rd']
        reg1 = decoded_ins['rs']
        reg2 = decoded_ins['rt']
        value1 = 0
        value2 = 0
        #forwarding value if already in use
        if(reg_flag[reg1][0]=='m'):
            value1 = latch_e
        elif(reg_flag[reg1][0]=='w'):
            value1 = latch_m
        #directly using value
        else:
            value1 = reg[reg1]

        #forwarding value if already in use
        if(reg_flag[reg2][0]=='m'):
            value2 = latch_e
        elif(reg_flag[reg2][0]=='w'):
            value2 = latch_m
        #directly using value
        else:
            value2 = reg[reg2]

        reg_flag[regstr][0] = 'e'
        #print(value1,value2)
        if(value1 < value2):
            return (1,decoded_ins['rd'])
        else:
            return (0,decoded_ins['rd'])

    elif(decoded_ins['ins']=='lui'):
        regstr = decoded_ins['rd']
        reg_flag[regstr][0] = 'e'
        return (decoded_ins['addr'],decoded_ins['rd'])

    elif(decoded_ins['ins']=='lw' or decoded_ins['ins']=='sw'):
        regstr = decoded_ins['rt']
        reg1 = decoded_ins['rm']

        #forwarding value if already in use
        if(reg_flag[reg1][0]=='m'):
            value1 = latch_e
        elif(reg_flag[reg1][0]=='w'):
            value1 = latch_m
        #directly using value
        else:
            value1 = reg[reg1]

        #print(value1)
        offset = decoded_ins['offset']
        index = 0
        if(int(str(value1),16)-base_address>=0 and (int(str(value1),16)-base_address)%4==0 and offset%4==0):
            index = int((int(str(value1),16)-base_address)/4 + offset/4)
        if(decoded_ins['ins']=='lw'):
            reg_flag[regstr][0] = 'e'
        #print(index,decoded_ins)
        return (index,decoded_ins)

    elif(decoded_ins['ins']=='addi'):
        regstr = decoded_ins['rd']
        reg1 = decoded_ins['rs']
        value1 = 0
        value2 = 0
        if(reg_flag[reg1][0]=='m'):
            value1 = latch_e
        elif(reg_flag[reg1][0]=='w'):
            value1 = latch_m
        #directly using value
        else:
            value1 = reg[reg1]

        reg_flag[regstr][0] = 'e'
        addend = int(decoded_ins['amt'])

        if(type(value1)==str and value1[0:2]=='0x'):
            return(hex(int(value1,16)+addend),decoded_ins['rd'])
        else:
            return(value1+addend,decoded_ins['rd'])

    elif(decoded_ins['ins']=='ori'):
        regstr = decoded_ins['rd']
        reg1 = decoded_ins['rs']
        if(reg_flag[reg1][0]=='m'):
            value1 = latch_e
        elif(reg_flag[reg1][0]=='w'):
            value1 = latch_m
        #directly using value
        else:
            value1 = reg[reg1]
        reg_flag[regstr][0] = 'e'
        return(value1 or decoded_ins['amt'],decoded_ins['rd'])

    elif(decoded_ins['ins']=='andi'):
        regstr = decoded_ins['rd']
        reg1 = decoded_ins['rs']
        value1 = 0
        value2 = 0
        if(reg_flag[reg1][0]=='m'):
            value1 = latch_e
        elif(reg_flag[reg1][0]=='w'):
            value1 = latch_m
        #directly using value
        else:
            value1 = reg[reg1]

        reg_flag[regstr][0] = 'e'
        anded = decoded_ins['amt']
        result = hex(int(value1,16)&int(anded,16))
        return(result,decoded_ins['rd'])

    elif(decoded_ins['ins'] in ins_type3 or decoded_ins['ins'] in ins_type5):
        return ('','done')

    else:
        return ()
        
def memory(execute):
    
    global reg_flag
    global data
    global reg
    global ms_flag1
    global ms_flag2
    global wr_flag

    if(execute):
        if (type(execute[1]) is dict and 'offset' in execute[1].keys()):
            index = execute[0]
            if(execute[1]['ins']=='lw'):
                reg_flag[execute[1]['rt']][0] = 'm'
                if(L1.search(index)):
                    return (L1.search(index),execute[1]['rt'])
                if(L2.search(index)):
                    L1.place_block(index,data)
                    ms_flag1 = True
                    return (L2.search(index),execute[1]['rt'])
                L1.place_block(index,data)
                L2.place_block(index,data)
                ms_flag2 = True
                return (data['.word'][index],execute[1]['rt'])
                # return (data['.word'][index],execute[1]['rt'])

            elif(execute[1]['ins']=='sw'):
                reg1 = execute[1]['rt']
                if(reg_flag[reg1][0]=='w'):
                    value = latch_m
                else:
                    value = reg[reg1]

                if(index >= len(data['.word'])):
                    count = index-len(data['.word'])
                    for i in range(count):
                        data['.word'].append(0)
                    data['.word'].append(value)
                    L1.place_block(index,data)
                    L2.place_block(index,data)
                    wr_flag = True
                    return ()

                else:
                    if(L1.search(index)):
                        L1.write_through(index,value)
                        L2.write_through(index,value)
                        data['.word'][index] = value
                        return ('','done')
                    if(L2.search(index)):
                        L2.write_through(index,value)
                        data['.word'][index] = value
                        L1.place_block(index,data)
                        return ('','done')
                    data['.word'][index] = value
                    L2.place_block(index,data)
                    L1.place_block(index,data)
                    return ('','done')

        elif(execute[1]!='done'):
            reg_flag[execute[1]][0] = 'm'
            return execute
        else:
            return execute
    else:
        return ()

def writeback(result):
        global reg_flag
        global reg

        if(result and result[1]!='done'):
            regstr = result[1]
            value = result[0]
            reg[regstr] = value
            reg_flag[regstr] = 'w'
            return result[1]             

        return ''

def pipeline(ins):

    global PC
    global stall_flag1
    global stall_flag2
    global stall_flag3
    global wr_flag
    global ms_flag1
    global ms_flag2
    global stalls
    global mem_stalls
    global reg_flag
    global latch_f
    global latch_d
    global latch_e
    global latch_m
    global write_stall

    f = []
    d = {}
    e = ()
    m = ()
    w = ''

    result = []
    cycles = -1
    count = 0

    while(PC<len(ins)):
        cycles+=1
        result.append([])
        if(ms_flag1==True):
            mem_stalls+=1
            ms_flag1 = False
            reg[cycles] = ['ms','ms','ms','ms','ms']
            continue
        elif(ms_flag2==True):
            if(count==0):
                mem_stalls+=1
                count+=1
            elif(count==1):
                mem_stalls+=1
                count = 0
                ms_flag2 = False
            reg[cycles] = ['ms','ms','ms','ms','ms']
            continue
        if(wr_flag==True):
            wr_flag = False
            write_stall+=1
            reg[cycles] = ['ws','ws','ws','ws','ws']
            continue
        #writeback cycle
        if(m):
            w = writeback(m)
            if(w):
                reg_flag[w]=['','']
            result[cycles].append('w')
        #memory cycle
        if(e):
            m = memory(e)
            if(m):
                latch_m = m[0]
            result[cycles].append('m')
        else:
            m = ()
        #execute cycle
        if(stall_flag2==True):
            e = ()
            stalls+=1
            stllflg2_f()
            result[cycles].append('s')
            result[cycles].append('s')
            result[cycles].append('s')
            continue

        if(d):
            e = execute(d)
            if(e):
                latch_e = e[0]
            result[cycles].append('e')
        else:
            e = ()
        #decode cycle
        if(stall_flag1==True):
            d = {}
            stalls+=1
            stllflg1_f()
            result[cycles].append('s')
            result[cycles].append('s')
            continue
        elif(stall_flag3==True):
            if(count==0):
                d = {}
                stalls+=1
                count+=1
                result[cycles].append('s')
                result[cycles].append('s')
            elif(count==1):
                stalls+=1
                count = 0
                result[cycles].append('s')
                stllflg3_f()
            continue
        if(f):
            d = decode(f)
            latch_d = d
            result[cycles].append('d')
        else: 
            d = {}
        #fetch cycle
        if(bn_flag==True):
            f = []
            stalls+=1
            result[cycles].append('s')
            bnflg_f()
            continue
        f = fetch()
        latch_f = f
        result[cycles].append('f')
        
    return (result,cycles+1)

def Simulate():
    global stalls

    file = open("loaded_file.txt", "r")
    file_address = file.read()

    instructions = read_instructions(fileHandler(str(file_address)))
    ins_list(instructions,data_and_text,data,label_address,main)

    process = ()
    instruction = data_and_text['main']

    process = pipeline(instruction)
    print('Number of Cycles in total = '+str(process[1]))
    # print_stages(process[0])
    print('--------------------------------------')
    L1.print_cache()
    L2.print_cache()
    print('--------------------------------------')
    print('Number of memory stalls = '+str(mem_stalls))
    print('--------------------------------------')
    print('Number of write stalls = '+str(write_stall))
    print('--------------------------------------')
    print('Number of stalls = '+ str(stalls))
    print('--------------------------------------')
    print('Instructions per cycle = '+str(round((process[1]-stalls)/process[1],3)))
    print(data['.word'])

    print('--------------------------------------')

    print("For L1 Cache, Miss Count= " + str(L1.miss_count))
    print("For L2 Cache, Miss Count= " + str(L2.miss_count))
    print("For L1 Cache, Hit Count= " + str(L1.hit_count))
    print("For L2 Cache, Hit Count= " + str(L2.hit_count))

    file = open("Cache.txt", 'w')
    file.write(str(L1.store_cache()))   
    file.write("\n")
    file.write(str(L2.store_cache()))
    file.close()

def Cache_input():
    global l1_block_size
    global l1_set_assoc
    global l1_blocks
    global l2_block_size
    global l2_set_assoc
    global l2_blocks
    global L1
    global L2

    l1_block_size = int(input("Enter the block size for L1 Cache: "))
    l1_set_assoc = int(input("Enter the set associativity of L1 Cache: "))
    l1_blocks = int(input("Enter the number of blocks in L1 Cache: "))

    l2_block_size = int(input("Enter the block size for L2 Cache: "))
    l2_set_assoc = int(input("Enter the set associativity of L2 Cache: "))
    l2_blocks = int(input("Enter the number of blocks in L2 Cache: "))

    L1 = Cache(l1_block_size, l1_set_assoc, l1_blocks, {})
    L2 = Cache(l2_block_size, l2_set_assoc, l2_blocks, {})

if __name__== "__main__":
    Cache_input()
    Simulate()
    
