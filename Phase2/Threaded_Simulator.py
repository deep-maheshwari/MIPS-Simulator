import re
import time
from time import sleep
import threading
import os # Added for path manipulation

reg = {"zero":0, "r0":0, "at":0, "v0":0, "v1":0, "a0":0, "a1":0, "a2":0, "a3":0, "t0":0, "t1":0, "t2":0, "t3":0, "t4":0, "t5":0, "t6":0, "t7":0,"s0":0, "s1":0, "s2":0, "s3":0 ,"s4":0 ,"s5":0, "s6":0, "s7":0, "t8":0, "t9":0, "k0":0, "k1":0, "gp":0, "sp":0, "s8":0, "ra":0}
reg_flag = {"zero":['',''], "r0":['',''], "at":['',''], "v0":['',''], "v1":['',''], "a0":['',''], "a1":['',''], "a2":['',''], "a3":['',''], "t0":['',''], "t1":['',''], "t2":['',''], "t3":['',''], "t4":['',''], "t5":['',''], "t6":['',''], "t7":['',''],"s0":['',''], "s1":['',''], "s2":['',''], "s3":['',''] ,"s4":['',''] ,"s5":['',''], "s6":['',''], "s7":['',''], "t8":['',''], "t9":['',''], "k0":['',''], "k1":['',''], "gp":['',''], "sp":['',''], "s8":['',''], "ra":['','']}
base_address = 0x10010000
data_and_text = {'data':[],'main':[]}
data = {'.word':[],'.text':[]}
label_address = {}
main = {}
PC = 0
msg = ""
stalls = 0
stall_flag1 = False
stall_flag2 = False
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

def stllflg1_t(lock):
    global stall_flag1

    lock.acquire()
    stall_flag1 = True
    lock.release()

def stllflg1_f(lock):
    global stall_flag1

    lock.acquire()
    stall_flag1 = False
    lock.release()

def stllflg2_t(lock):
    global stall_flag2

    lock.acquire()
    stall_flag2 = True
    lock.release()

def stllflg2_f(lock):
    global stall_flag2

    lock.acquire()
    stall_flag2 = False
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
    
def fetch(lock):

    global PC
    global reg_flag
    global stall_flag1
    global bn_flag

    start = time.perf_counter()
    lock.acquire()
    try:
        # Read PC under lock
        current_pc_value = PC
        instr = data_and_text['main'][current_pc_value] 
    finally:
        lock.release()
    
    print(current_pc_value) # Debug print, value might be stale if PC changed by another thread immediately

    if((instr[0] in ins_type1) or (instr[0] in ins_type2) or (instr[0] in ins_type6)):
        regstr = instr[1].replace('$','')
        end = time.perf_counter()
        sleep(0.09-round(end-start,3))
        lock.acquire()
        try:
            reg_flag[regstr][0] = 'd'
            reg_flag[regstr][1] = 'e'
            PC = PC + 1
        finally:
            lock.release()

    elif(instr[0]=='lw'):
        regstr = instr[1].replace('$','')
        end = time.perf_counter()
        sleep(0.09-round(end-start,3))
        lock.acquire()
        try:
            reg_flag[regstr][0] = 'd'
            reg_flag[regstr][1] = 'm'
            PC = PC + 1
        finally:
            lock.release()

    elif(instr[0]=='sw'):
        lock.acquire()
        try:
            PC+=1
        finally:
            lock.release()

    elif(instr[0] in ins_type3):
        reg1 = instr[1].replace('$','')
        reg2 = instr[2].replace('$','')
        
        lock.acquire()
        try:
            #print(reg_flag[reg1],reg_flag[reg2])
            reg1_flag_0 = reg_flag[reg1][0]
            reg1_flag_1 = reg_flag[reg1][1]
            reg2_flag_0 = reg_flag[reg2][0]
            reg2_flag_1 = reg_flag[reg2][1]
        finally:
            lock.release()

        if(reg1_flag_0=='d' and reg1_flag_1=='m'):
            #take value from latch_m
            stllflg1_t(lock) # Uses lock internally
            bnflg_t(lock)    # Uses lock internally

        elif(reg2_flag_0=='d' and reg2_flag_1=='m'):
            #take value from latch_m
            stllflg1_t(lock) # Uses lock internally
            bnflg_t(lock)    # Uses lock internally

        elif(reg1_flag_0=='e' and reg1_flag_1=='m'):
            #take value from latch_m
            stllflg1_t(lock) # Uses lock internally

        elif(reg2_flag_0=='e' and reg2_flag_1=='m'):
            #take value from latch_m
            #print('hell')
            stllflg1_t(lock) # Uses lock internally

        elif(reg1_flag_0=='d' and reg1_flag_1=='e'):
            #take value from latch_e
            stllflg1_t(lock) # Uses lock internally

        elif(reg2_flag_0=='d' and reg2_flag_1=='e'):
            #take value from latch_e
            stllflg1_t(lock) # Uses lock internally

        #print(PC) # Reading PC here without lock, could be stale for debugging
    return instr

def decode(parsed_ins,lock):

    global main
    global PC
    global reg_flag
    global stall_flag2
    global latch_m # For reading
    global latch_e # For reading
    global reg     # For reading
    start = time.perf_counter()

    if not parsed_ins: return {}


    if(parsed_ins[0]=='add' or parsed_ins[0]=='sub' or parsed_ins[0]=='and' or parsed_ins[0]=='or' or parsed_ins[0]=='slt'):
        regstr = parsed_ins[1].replace('$','')
        reg1 = parsed_ins[2].replace('$','')
        reg2 = parsed_ins[3].replace('$','')

        lock.acquire()
        try:
            reg1_flag_0 = reg_flag[reg1][0]
            reg1_flag_1 = reg_flag[reg1][1]
            reg2_flag_0 = reg_flag[reg2][0]
            reg2_flag_1 = reg_flag[reg2][1]
        finally:
            lock.release()

        if(reg1_flag_0=='e' and reg1_flag_1=='m'):
            stllflg2_t(lock) # Uses lock internally
        elif(reg2_flag_0=='e' and reg2_flag_1=='m'):
            stllflg2_t(lock) # Uses lock internally
        
        end = time.perf_counter()
        # Approximation of original sleep logic placement
        sleep_duration = 0.09 - round(end - start, 3)
        if sleep_duration > 0:
            sleep(sleep_duration)
            
        lock.acquire()
        try:
            reg_flag[regstr][0] = 'e'
        finally:
            lock.release()
        return {'ins':parsed_ins[0],'rd':parsed_ins[1].replace('$',''),'rs':parsed_ins[2].replace('$',''),'rt':parsed_ins[3].replace('$','')}
    
    elif(parsed_ins[0]=='sll' or parsed_ins[0]=='srl' or parsed_ins[0]=='andi' or parsed_ins[0]=='ori' or parsed_ins[0]=='addi'):
        regstr = parsed_ins[1].replace('$','')
        reg1 = parsed_ins[2].replace('$','')

        lock.acquire()
        try:
            reg1_flag_0 = reg_flag[reg1][0]
            reg1_flag_1 = reg_flag[reg1][1]
        finally:
            lock.release()

        if(reg1_flag_0=='e' and reg1_flag_1=='m'):
            stllflg2_t(lock) # Uses lock internally
        
        end = time.perf_counter()
        sleep_duration = 0.09 - round(end - start, 3)
        if sleep_duration > 0:
            sleep(sleep_duration)

        lock.acquire()
        try:
            reg_flag[regstr][0] = 'e'
        finally:
            lock.release()
        return {'ins':parsed_ins[0],'rd':parsed_ins[1].replace('$',''),'rs':parsed_ins[2].replace('$',''),'amt':parsed_ins[3]}
    
    elif(parsed_ins[0]=='bne' or parsed_ins[0]=='beq'):
        rs = parsed_ins[1].replace('$','')
        rt = parsed_ins[2].replace('$','')
        addr = parsed_ins[3]
        value1 = 0
        value2 = 0

        lock.acquire()
        try:
            #print(reg_flag[rs],reg_flag[rt])
            rs_reg_flag_w = reg_flag[rs][0]=='w'
            rs_reg_flag_m = reg_flag[rs][0]=='m'
            rt_reg_flag_w = reg_flag[rt][0]=='w'
            rt_reg_flag_m = reg_flag[rt][0]=='m'

            if rs_reg_flag_w:
                value1 = latch_m
            elif rs_reg_flag_m:
                value1 = latch_e
            else:
                value1 = reg[rs]

            if rt_reg_flag_w:
                value2 = latch_m
            elif rt_reg_flag_m:
                value2 = latch_e
            else:
                value2 = reg[rt]
        finally:
            lock.release() # Released after accessing reg_flag, latch_m, latch_e, reg

        lock.acquire()
        try:
            if(parsed_ins[0]=='bne'):
                if(value1 == value2): # value1, value2 are local copies
                    PC = PC + 1
                else:
                    PC = main[addr]
            else: #beq
                #print(value1,value2)
                if(value1 != value2): # value1, value2 are local copies
                    #print('in here')
                    PC = PC + 1
                else:
                    PC = main[addr]
        finally:
            lock.release() # Released after accessing PC
        
        return {'ins':parsed_ins[0],'rs':parsed_ins[1].replace('$',''),'rt':parsed_ins[2].replace('$',''),'addr':parsed_ins[3]}
    
    elif(parsed_ins[0]=='j'):
        addr = parsed_ins[1]
        lock.acquire()
        try:
            PC = main[addr]
        finally:
            lock.release()
        return {'ins':parsed_ins[0],'addr':parsed_ins[1]}

    elif(parsed_ins[0]=='lw' or parsed_ins[0]=='sw'):
        regstr = parsed_ins[1].replace('$','')

        reg_pattern = re.search(r"\$[a-z0-9]*",parsed_ins[2],re.MULTILINE)
        offset_pattern = re.search(r"\w+",parsed_ins[2],re.MULTILINE)

        reg1 = reg_pattern.group(0).replace('$','')
        
        lock.acquire()
        try:
            reg1_flag_0 = reg_flag[reg1][0]
            reg1_flag_1 = reg_flag[reg1][1]
        finally:
            lock.release()
        
        if(reg1_flag_0=='e' and reg1_flag_1=='m'):
            stllflg2_t(lock) # Uses lock internally

        if(parsed_ins[0]=='lw'):
            end = time.perf_counter()
            sleep_duration = 0.09 - round(end - start, 3)
            if sleep_duration > 0:
                sleep(sleep_duration)
            lock.acquire()
            try:
                reg_flag[regstr][0]='e'
            finally:
                lock.release()
        return {'ins':parsed_ins[0],'rt':parsed_ins[1].replace('$',''),'rm':reg_pattern.group(0).replace('$',''),'offset':int(offset_pattern.group(0))}

    elif(parsed_ins[0]=='lui'):
        regstr = parsed_ins[1].replace('$','')
        end = time.perf_counter()
        sleep_duration = 0.09 - round(end - start, 3)
        if sleep_duration > 0:
            sleep(sleep_duration)
        lock.acquire()
        try:
            reg_flag[regstr][0]='e'
        finally:
            lock.release()
        return {'ins':parsed_ins[0],'rd':parsed_ins[1].replace('$',''),'addr':hex(int(parsed_ins[2]+'0000',16))}

    elif(parsed_ins[0]=='jr'):
        return {'ins':parsed_ins[0]} # jr is effectively a NOP in this model's execute stage

def execute(decoded_ins, lock): # Added lock as parameter
    
    global reg_flag
    global reg
    global latch_e # For reading
    global latch_m # For reading
    start = time.perf_counter()

    if not decoded_ins or not decoded_ins.get('ins'): # Ensure decoded_ins and its 'ins' key exist
        return ()

    if(decoded_ins['ins']=='add'):
        regstr = decoded_ins['rd']
        reg1 = decoded_ins['rs']
        reg2 = decoded_ins['rt']
        value1, value2 = 0, 0
        reg_copy_for_return = {}
        lock.acquire()
        try:
            if(reg_flag[reg1][0]=='m'): value1 = latch_e
            elif(reg_flag[reg1][0]=='w'): value1 = latch_m
            else: value1 = reg[reg1]

            if(reg_flag[reg2][0]=='m'): value2 = latch_e
            elif(reg_flag[reg2][0]=='w'): value2 = latch_m
            else: value2 = reg[reg2]
            
            reg_flag[regstr][0] = 'm'
            reg_copy_for_return = reg.copy() # Copy reg under lock
        finally:
            lock.release()
        
        end = time.perf_counter()
        sleep_duration = 0.09 - round(end - start, 3)
        if sleep_duration > 0: sleep(sleep_duration)
        return (value1 + value2, reg_copy_for_return)


    elif(decoded_ins['ins']=='sub'):
        regstr = decoded_ins['rd']
        reg1 = decoded_ins['rs']
        reg2 = decoded_ins['rt']
        value1, value2 = 0, 0
        lock.acquire()
        try:
            if(reg_flag[reg1][0]=='m'): value1 = latch_e
            elif(reg_flag[reg1][0]=='w'): value1 = latch_m
            else: value1 = reg[reg1]

            if(reg_flag[reg2][0]=='m'): value2 = latch_e
            elif(reg_flag[reg2][0]=='w'): value2 = latch_m
            else: value2 = reg[reg2]
            reg_flag[regstr][0] = 'm'
        finally:
            lock.release()
        end = time.perf_counter()
        sleep_duration = 0.09-round(end-start,3)
        if sleep_duration > 0: sleep(sleep_duration)
        return (value1-value2,decoded_ins['rd'])

    elif(decoded_ins['ins']=='and'):
        regstr = decoded_ins['rd']
        reg1 = decoded_ins['rs']
        reg2 = decoded_ins['rt']
        value1, value2 = 0, 0
        lock.acquire()
        try:
            if(reg_flag[reg1][0]=='m'): value1 = latch_e
            elif(reg_flag[reg1][0]=='w'): value1 = latch_m
            else: value1 = reg[reg1]

            if(reg_flag[reg2][0]=='m'): value2 = latch_e
            elif(reg_flag[reg2][0]=='w'): value2 = latch_m
            else: value2 = reg[reg2]
            reg_flag[regstr][0] = 'm'
        finally:
            lock.release()
        end = time.perf_counter()
        sleep_duration = 0.09-round(end-start,3)
        if sleep_duration > 0: sleep(sleep_duration)
        return (value1 and value2 ,decoded_ins['rd'])

    elif(decoded_ins['ins']=='or'):
        regstr = decoded_ins['rd']
        reg1 = decoded_ins['rs']
        reg2 = decoded_ins['rt']
        value1, value2 = 0, 0
        lock.acquire()
        try:
            if(reg_flag[reg1][0]=='m'): value1 = latch_e
            elif(reg_flag[reg1][0]=='w'): value1 = latch_m
            else: value1 = reg[reg1]

            if(reg_flag[reg2][0]=='m'): value2 = latch_e
            elif(reg_flag[reg2][0]=='w'): value2 = latch_m
            else: value2 = reg[reg2]
            reg_flag[regstr][0] = 'm'
        finally:
            lock.release()
        end = time.perf_counter()
        sleep_duration = 0.09-round(end-start,3)
        if sleep_duration > 0: sleep(sleep_duration)
        return (value1 or value2 ,decoded_ins['rd'])

    elif(decoded_ins['ins']=='slt'):
        regstr = decoded_ins['rd']
        reg1 = decoded_ins['rs']
        reg2 = decoded_ins['rt']
        value1, value2 = 0,0
        lock.acquire()
        try:
            if(reg_flag[reg1][0]=='m'): value1 = latch_e
            elif(reg_flag[reg1][0]=='w'): value1 = latch_m
            else: value1 = reg[reg1]

            if(reg_flag[reg2][0]=='m'): value2 = latch_e
            elif(reg_flag[reg2][0]=='w'): value2 = latch_m
            else: value2 = reg[reg2]
            reg_flag[regstr][0] = 'm'
        finally:
            lock.release()
        end = time.perf_counter()
        sleep_duration = 0.09-round(end-start,3)
        if sleep_duration > 0: sleep(sleep_duration)
        if(value1 < value2): return (1,decoded_ins['rd'])
        else: return (0,decoded_ins['rd'])

    elif(decoded_ins['ins']=='lui'):
        regstr = decoded_ins['rd']
        end = time.perf_counter()
        sleep_duration = 0.09-round(end-start,3)
        if sleep_duration > 0: sleep(sleep_duration)
        lock.acquire()
        try:
            reg_flag[regstr][0] = 'm'
        finally:
            lock.release()
        return (decoded_ins['addr'],decoded_ins['rd'])

    elif(decoded_ins['ins']=='lw' or decoded_ins['ins']=='sw'):
        regstr = decoded_ins['rt'] # rt is target for lw, source for sw
        reg1 = decoded_ins['rm']   # rm is base address register
        value1 = 0 # For base address
        lock.acquire()
        try:
            if(reg_flag[reg1][0]=='m'): value1 = latch_e
            elif(reg_flag[reg1][0]=='w'): value1 = latch_m
            else: value1 = reg[reg1]

            if(decoded_ins['ins']=='lw'): # Only lw changes reg_flag for destination
                reg_flag[regstr][0] = 'm'
        finally:
            lock.release()
        
        offset = decoded_ins['offset']
        index = 0
        # This calculation does not involve shared state, can be outside lock
        if(int(str(value1),16)-base_address>=0 and (int(str(value1),16)-base_address)%4==0 and offset%4==0):
            index = int((int(str(value1),16)-base_address)/4 + offset/4)
        
        if(decoded_ins['ins']=='lw'): # Sleep is only for lw in original
            end = time.perf_counter()
            sleep_duration = 0.09-round(end-start,3)
            if sleep_duration > 0: sleep(sleep_duration)
        return (index,decoded_ins) # Return index and original instruction details

    elif(decoded_ins['ins']=='addi'):
        regstr = decoded_ins['rd']
        reg1 = decoded_ins['rs']
        value1 = 0
        lock.acquire()
        try:
            if(reg_flag[reg1][0]=='m'): value1 = latch_e
            elif(reg_flag[reg1][0]=='w'): value1 = latch_m
            else: value1 = reg[reg1]
            reg_flag[regstr][0] = 'm'
        finally:
            lock.release()
        
        end = time.perf_counter()
        sleep_duration = 0.09-round(end-start,3)
        if sleep_duration > 0: sleep(sleep_duration)
        addend = int(decoded_ins['amt'])
        if(type(value1)==str and value1[0:2]=='0x'): return(hex(int(value1,16)+addend),decoded_ins['rd'])
        else: return(value1+addend,decoded_ins['rd'])

    elif(decoded_ins['ins']=='ori'):
        regstr = decoded_ins['rd']
        reg1 = decoded_ins['rs']
        value1 = 0
        lock.acquire()
        try:
            if(reg_flag[reg1][0]=='m'): value1 = latch_e
            elif(reg_flag[reg1][0]=='w'): value1 = latch_m
            else: value1 = reg[reg1]
            reg_flag[regstr][0] = 'm'
        finally:
            lock.release()
        end = time.perf_counter()
        sleep_duration = 0.09-round(end-start,3)
        if sleep_duration > 0: sleep(sleep_duration)
        # Ensure amt is int for bitwise OR if value1 is int
        amt_val = int(decoded_ins['amt'])
        if isinstance(value1, str) and value1.startswith("0x"):
            return (hex(int(value1, 16) | amt_val), decoded_ins['rd'])
        return(value1 | amt_val ,decoded_ins['rd'])


    elif(decoded_ins['ins']=='andi'):
        regstr = decoded_ins['rd']
        reg1 = decoded_ins['rs']
        value1 = 0
        lock.acquire()
        try:
            if(reg_flag[reg1][0]=='m'): value1 = latch_e
            elif(reg_flag[reg1][0]=='w'): value1 = latch_m
            else: value1 = reg[reg1]
            reg_flag[regstr][0] = 'm'
        finally:
            lock.release()
        end = time.perf_counter()
        sleep_duration = 0.09-round(end-start,3)
        if sleep_duration > 0: sleep(sleep_duration)
        anded = decoded_ins['amt'] # Assuming anded is hex string like "0xff"
        # Ensure value1 is treated as hex string if it is one
        val1_int = int(str(value1),16) if isinstance(value1, str) and value1.startswith("0x") else int(value1)
        anded_int = int(anded,16)
        result = hex(val1_int & anded_int)
        return(result,decoded_ins['rd'])
    else:
        return () # Should not happen if decoded_ins is valid and checked
        
def memory(execute_result, lock): # Added lock parameter, renamed execute to execute_result
    
    global reg_flag
    global data # For data['.word']
    global reg  # For reg[reg1] in sw
    global latch_m # For reading in sw
    start = time.perf_counter()

    if not execute_result: return ()
    
    # execute_result contains (value, instruction_details_dict) or (value, dest_reg_string)
    # We need instruction_details_dict for lw/sw.
    # For other ops, it might be just dest_reg_string.
    
    # Check if execute_result[1] is a dictionary (implies lw/sw or similar detailed structure)
    if isinstance(execute_result[1], dict) and 'ins' in execute_result[1]:
        instruction_details = execute_result[1]
        current_ins_type = instruction_details['ins']

        if current_ins_type == 'lw':
            index = execute_result[0] # This is the calculated memory index
            rt_reg = instruction_details['rt'] # Destination register
            data_val = 0
            
            end = time.perf_counter() # Sleep timing from original
            sleep_duration = 0.09 - round(end - start, 3)
            if sleep_duration > 0: sleep(sleep_duration)

            lock.acquire()
            try:
                reg_flag[rt_reg][0] = 'w'
                data_val = data['.word'][index] # Read from data['.word']
            finally:
                lock.release()
            return (data_val, rt_reg)

        elif current_ins_type == 'sw':
            index = execute_result[0] # This is the calculated memory index
            rt_reg = instruction_details['rt'] # Source register for sw
            value_to_store = 0
            
            lock.acquire()
            try:
                # Determine value to store (forwarding or from register)
                if reg_flag[rt_reg][0] == 'w': # Check reg_flag for the source register rt_reg
                    value_to_store = latch_m
                # elif reg_flag[rt_reg][0] == 'm': # This case seems unlikely for sw source in typical forwarding
                #    value_to_store = latch_e 
                else:
                    value_to_store = reg[rt_reg] # Read from reg

                # Store value into data['.word']
                if index >= len(data['.word']):
                    # Extend data['.word'] if index is out of bounds
                    for _ in range(index - len(data['.word'])):
                        data['.word'].append(0)
                    data['.word'].append(value_to_store)
                else:
                    data['.word'][index] = value_to_store
            finally:
                lock.release()
            return () # sw does not return a value to writeback stage typically
        else: # Not lw or sw, but execute_result[1] was a dict. Pass through.
              # This handles cases like add where execute_result[1] was the whole reg dict (now fixed to be a copy)
              # or other non-R/I type instructions if they follow this structure.
              # However, based on current execute, only add returns reg dict.
              # For safety, we assume such instructions might need their reg_flag updated.
            if isinstance(execute_result[1], str): # If it's ('val', 'reg_name_str')
                dest_reg_str = execute_result[1]
                end = time.perf_counter()
                sleep_duration = 0.09 - round(end - start, 3)
                if sleep_duration > 0: sleep(sleep_duration)
                lock.acquire()
                try:
                    reg_flag[dest_reg_str][0] = 'w'
                finally:
                    lock.release()
            return execute_result


    # This 'else' handles cases from execute like (value, dest_reg_string) for R-type, I-type (non-lw)
    elif isinstance(execute_result[1], str): # execute_result[1] is dest_reg string
        dest_reg = execute_result[1]
        end = time.perf_counter() # Sleep timing from original
        sleep_duration = 0.09 - round(end - start, 3)
        if sleep_duration > 0: sleep(sleep_duration)
        
        lock.acquire()
        try:
            reg_flag[dest_reg][0] = 'w'
        finally:
            lock.release()
        return execute_result # Pass through (value, dest_reg_string)
    
    return () # Default return if no conditions met


def writeback(result, lock): # Added lock parameter
        global reg_flag
        global reg
        start = time.perf_counter()
        if result and isinstance(result[1], str): # Ensure result is not None and result[1] is reg name
            regstr = result[1]
            value = result[0]
            
            lock.acquire()
            try:
                reg[regstr] = value
                reg_flag[regstr] = ['','']  
            finally:
                lock.release()

            end = time.perf_counter()
            sleep_duration = 0.09-(round(end-start,3)) # Original: start-end
            if sleep_duration > 0:
                 sleep(sleep_duration)
        # If result[1] is not a string (e.g. the reg dict from old 'add'), it's ignored.
        # This is consistent with original behavior where 'add's second element (reg dict) wasn't used as regstr.


def pipeline(lock):

    global PC # Read by fetch
    global latch_f # Written here, read by Simulate
    global latch_d # Written here, read by execute/decode (forwarding)
    global latch_e # Written here, read by execute/decode (forwarding)
    global latch_m # Written here, read by execute/decode (forwarding)
    global stall_flag1 # Read here
    global stall_flag2 # Read here
    global bn_flag # Read here

    #fetch cycle
    # Sleep outside lock, represents hardware delay
    sleep(0.10) 
    start_fetch = time.perf_counter()
    # fetch() handles its internal locking for PC, reg_flag
    # instr_from_fetch is local to this thread's pipeline instance.
    instr_from_fetch = fetch(lock) 
    
    # Update global latch_f, which is read by Simulate()
    if instr_from_fetch: 
        lock.acquire()
        try:
            latch_f = instr_from_fetch 
        finally:
            lock.release()
    
    end_fetch = time.perf_counter()
    fetch_duration = end_fetch - start_fetch
    if 0.100 > fetch_duration:
         sleep(0.100 - fetch_duration)
    
    # Stall logic based on global flags (read under lock)
    lock.acquire()
    try:
        s_flag2 = stall_flag2 
    finally:
        lock.release()
    if s_flag2: 
        sleep(0.05)
        stllflg2_f(lock) # Helper handles its own lock
        sleep(0.05)

    lock.acquire()
    try:
        s_flag1 = stall_flag1 
        b_flag = bn_flag         
    finally:
        lock.release()
    if s_flag1 and b_flag: 
        sleep(0.100)
        stllflg1_f(lock) 
        bnflg_f(lock)    
        sleep(0.100)
    elif s_flag1: 
        sleep(0.05)
        stllflg1_f(lock) 
        sleep(0.05)
    
    sleep(0.10) 
    #decode cycle
    start_decode = time.perf_counter()
    # instr_from_fetch (local var) is passed to decode
    # decode() handles its internal locking for PC, reg_flag, and reads latch_e/latch_m
    decoded_output = decode(instr_from_fetch, lock) 
    
    if decoded_output: 
        lock.acquire()
        try:
            latch_d = decoded_output # Update global latch_d
        finally:
            lock.release()
    
    end_decode = time.perf_counter()
    decode_duration = end_decode - start_decode
    if 0.100 > decode_duration:
        sleep(0.100 - decode_duration)

    lock.acquire()
    try:
        s_flag2_after_decode = stall_flag2 
    finally:
        lock.release()
    if s_flag2_after_decode: 
        sleep(0.05)
        stllflg2_f(lock) 
        sleep(0.05)
    
    sleep(0.10) 
    #execute cycle
    start_execute = time.perf_counter()
    # decoded_output (local var) is passed to execute
    # execute() handles its internal locking for reg_flag, reg, and reads latch_e/latch_m
    executed_data = execute(decoded_output, lock) 
    
    if executed_data: 
        lock.acquire()
        try:
            # executed_data is typically (value, reg_name_or_reg_dict_copy)
            latch_e = executed_data[0] # Update global latch_e with the value part
        finally:
            lock.release()
        
    end_execute = time.perf_counter()
    execute_duration = end_execute - start_execute
    if 0.100 > execute_duration:
        sleep(0.100 - execute_duration)
    
    sleep(0.10) 
    #memory cycle
    start_memory = time.perf_counter()
    # executed_data (local var) is passed to memory
    # memory() handles its internal locking for reg_flag, data['.word'], reg, and reads latch_m
    data_from_memory = memory(executed_data, lock) 
    
    if data_from_memory: 
        lock.acquire()
        try:
            # data_from_memory is typically (value, dest_reg_name) for lw
            latch_m = data_from_memory[0] # Update global latch_m with the value part
        finally:
            lock.release()

    end_memory = time.perf_counter()
    memory_duration = end_memory - start_memory
    if 0.100 > memory_duration:
        sleep(0.100 - memory_duration)
    
    sleep(0.10) 
    #writeback cycle
    start_writeback = time.perf_counter()
    # data_from_memory (local var) is passed to writeback
    # writeback() handles its internal locking for reg, reg_flag
    writeback(data_from_memory, lock) 
    end_writeback = time.perf_counter()
    writeback_duration = end_writeback - start_writeback
    if 0.100 > writeback_duration:
        sleep(0.100 - writeback_duration)
    
def Simulate():

    global PC
    global reg
    global data
    # latch_d, latch_e, latch_m are primarily pipeline stage boundaries internal to a pipeline thread's flow
    # but are global. Reads for forwarding are handled in decode/execute.
    global latch_f    # Written by pipeline threads, read by Simulate thread
    global reg_flag   # Accessed by pipeline threads
    global stall_flag1 # Written by pipeline (helpers), read by Simulate & pipeline threads
    global stall_flag2 # Written by pipeline (helpers), read by Simulate & pipeline threads
    global bn_flag     # Written by pipeline (helpers), read by Simulate & pipeline threads
    global stalls      # Written and Read by Simulate thread

    # Setup is single-threaded, no lock needed for these initial modifications of data/data_and_text
    # Determine the correct path to bubble_sort.asm relative to this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Path assumes Phase1 and Phase2 are sibling directories
    asm_file_path = os.path.join(script_dir, "..", "Phase1", "bubble_sort.asm")
    # Verify if the path exists, otherwise try from repo root perspective
    if not os.path.exists(asm_file_path):
        # This path assumes the script is run from the repository root
        asm_file_path = os.path.join("Phase1", "bubble_sort.asm")

    instructions_raw = fileHandler(asm_file_path)
    instructions_parsed = read_instructions(instructions_raw)
    ins_list(instructions_parsed, data_and_text, data, label_address, main)


    process_list = []
    lock = threading.Lock() 
    instruction_memory = data_and_text['main'] # Local reference
    
    sim_start_time = time.perf_counter() # Renamed from start1
    instruction_count_executed = 0 # Renamed from count

    while True:
        lock.acquire()
        try:
            current_pc_val = PC
        finally:
            lock.release()
        
        if not (current_pc_val < len(instruction_memory) -1): 
            break

        loop_iter_start_time = time.perf_counter()
        
        s_flag2_sim, s_flag1_sim, b_flag_sim, local_latch_f_sim = False, False, False, []
        lock.acquire()
        try:
            s_flag2_sim = stall_flag2 
            s_flag1_sim = stall_flag1 
            b_flag_sim = bn_flag     
            # Make a shallow copy of latch_f for safe access after releasing lock
            if latch_f: local_latch_f_sim = list(latch_f) 
        finally:
            lock.release()

        if s_flag2_sim:
            lock.acquire()
            try:
                stalls+=1 
            finally:
                lock.release()
            sleep(0.100)

        if s_flag1_sim and b_flag_sim:
            lock.acquire()
            try:
                stalls+=2 
            finally:
                lock.release()
            sleep(0.200)
        elif s_flag1_sim:
            lock.acquire()
            try:
                stalls+=1 
            finally:
                lock.release()
            sleep(0.100)

        if local_latch_f_sim: # Check if the local copy is not empty
            if (local_latch_f_sim[0] in ins_type5) or (local_latch_f_sim[0] in ins_type3):
                lock.acquire()
                try:
                    stalls+=1 
                finally:
                    lock.release()
                sleep(0.100)
        
        p = threading.Thread(target=pipeline,args=(lock,))
        process_list.append(p)
        # Original code joins before starting the current thread, which is unusual.
        # Typically, you start and then join later, or manage a pool.
        # For now, matching original structure:
        if instruction_count_executed >= 5: 
            if process_list[instruction_count_executed-5].is_alive():
                 process_list[instruction_count_executed-5].join()
        
        p.start() 
        instruction_count_executed += 1
        
        loop_iter_end_time = time.perf_counter()
        loop_iter_elapsed = loop_iter_end_time - loop_iter_start_time
        
        # This sleep logic in the main loop tries to pace the simulation.
        # It's not directly related to individual pipeline stage timing.
        if round(loop_iter_elapsed,3) >= 0.100: 
             sleep(0.300)
        else:
             sleep(0.300 - loop_iter_elapsed)
        
        # Debug prints (optional, keep locked if used)
        # lock.acquire()
        # print(f"Simulate Loop: PC={PC}, Stalls={stalls}, Executed Count={instruction_count_executed}")
        # print(f"Regs: {reg}")
        # print(f"Data: {data['.word']}")
        # lock.release()

    # Join any remaining threads after the main loop
    # The original code joins only up to instruction_count_executed - 1 from count-4
    # A more robust way is to iterate through all threads that were started.
    for i in range(len(process_list)):
        if process_list[i].is_alive():
            process_list[i].join()
    
    sim_end_time = time.perf_counter() # Renamed from end1
    
    lock.acquire()
    try:
        final_stalls_val = stalls 
        final_reg_val = reg.copy() 
        final_data_word_val = list(data['.word']) 
    finally:
        lock.release()

    print(f"Execution Time: {sim_end_time - sim_start_time:.3f} seconds")
    print('cycles taken to execute are '+str(instruction_count_executed + 4 + final_stalls_val)) # +4 for pipeline flush
    print('stalls = '+str(final_stalls_val))
    
    total_cycles_for_ipc = instruction_count_executed + 4 + final_stalls_val
    ipc = 0
    if total_cycles_for_ipc > 0:
        ipc = round(instruction_count_executed / total_cycles_for_ipc, 3)
    print('INSTRUCTIONS PER CYCLE = '+str(ipc))
    print("Final Registers:", final_reg_val)
    print("Final Data Memory:", final_data_word_val)

if __name__== "__main__":
    Simulate()