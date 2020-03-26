#!/usr/bin/env python
# coding: utf-8

# In[106]:


instruction = ['add $s1,$s2,$s3','lui $s0,0x1001','lw $s2,0($s0)']
op_code = {'add':0}
r_type = ['sll','srl','jr','jalr','syscall','add','sub','and','or']
i_type = ['beq','bne','addi','ori','andi','lui','lw','sw']
j_type = ['j','jal']
reg = {"zero":0, "r0":0, "at":0, "v0":0, "v1":0, "a0":0, "a1":0, "a2":0, "a3":0, "t0":0, "t1":0, "t2":0, "t3":0, "t4":0, "t5":0, "t6":0, "t7":0,"s0":0, "s1":0, "s2":0, "s3":0 ,"s4":0 ,"s5":0, "s6":0, "s7":0, "t8":0, "t9":0, "k0":0, "k1":0, "gp":0, "sp":0, "s8":0, "ra":0}
data = {'.word':[10,1],'.text':[]}
base_address = 0x10010000


# In[25]:


def parse(text):
    result = text.split()
    parsed = []

    for st in result:

        st = st.split(",")
        for x in st:
            if(x):
                parsed.append(x)

    return parsed


# In[26]:


def fetch(instruction,i):
    parsed_ins = parse(instruction[i])
    return parsed_ins


# In[27]:


fetch(instruction,0)


# In[22]:


import re


# In[73]:


fetch(instruction,1)


# In[42]:


fetch(instruction,2)


# In[111]:


def decode(parsed_ins):
    
    if(parsed_ins[0]=='add' or parsed_ins[0]=='sub' or parsed_ins[0]=='and' or parsed_ins[0]=='or' or parsed_ins[0]=='slt'):
        return {'ins':parsed_ins[0],'rd':parsed_ins[1].replace('$',''),'rs':reg[parsed_ins[2].replace('$','')],'rt':reg[parsed_ins[3].replace('$','')]}
    elif(parsed_ins[0]=='sll' or parsed_ins[0]=='srl' or parsed_ins[0]=='andi' or parsed_ins[0]=='ori' or parsed_ins[0]=='addi'):
        return {'ins':parsed_ins[0],'rd':parsed_ins[1],'rs':parsed_ins[2],'amt':parsed_ins[3]}
    elif(parsed_ins[0]=='bne' or parsed_ins[0]=='beq'):
        return {'ins':parsed_ins[0],'rs':parsed_ins[1],'rt':parsed_ins[2],'addr':parsed_ins[3]}
    elif(parsed_ins[0]=='j' or parsed_ins[0]=='jal'):
        return {'ins':parsed_ins[0],'addr':parsed_ins[1]}
    elif(parsed_ins[0]=='lw' or parsed_ins[0]=='sw'):
        reg_pattern = re.search(r"\$[a-z0-9]*",parsed_ins[2],re.MULTILINE)
        offset_pattern = re.search(r"\w+",parsed_ins[2],re.MULTILINE)
        return {'ins':parsed_ins[0],'rt':parsed_ins[1].replace('$',''),'rm':reg_pattern.group(0).replace('$',''),'offset':int(offset_pattern.group(0))}
    elif(parsed_ins[0]=='lui'):
        return {'ins':parsed_ins[0],'rt':parsed_ins[1].replace('$',''),'addr':hex(int(parsed_ins[2]+'0000',16))}


# In[112]:


decode(fetch(instruction,1))


# In[113]:


decode(fetch(instruction,0))


# In[114]:


decode(fetch(instruction,2))


# In[70]:


def execute(decoded_ins):
    
    if(decoded_ins['ins']=='add'):
        return (decoded_ins['rt']+decoded_ins['rs'],decoded_ins['rd'])
    elif(decoded_ins['ins']=='sub'):
        return (decoded_ins['rt']-decoded_ins['rs'],decoded_ins['rd'])
    elif(decoded_ins['ins']=='and'):
        return (decoded_ins['rt'] and decoded_ins['rs'],decoded_ins['rd'])
    elif(decoded_ins['ins']=='or'):
        return (decoded_ins['rt'] or decoded_ins['rs'],decoded_ins['rd'])
    elif(decoded_ins['ins']=='slt'):
        if(decoded_ins['rt']<decoded_ins['rs']):
            return (1,decoded_ins['rd'])
        else:
            return (0,decoded_ins['rd'])
    elif(decoded_ins['ins']=='lui'):
        return (decoded_ins['addr'],decoded_ins['rt'])


# In[115]:


execute(decode(fetch(instruction,1)))


# In[101]:


def memory(decoded_ins):
    
    if('offset' in decoded_ins.keys()):
        reg1 = decoded_ins['rt']
        reg2 = decoded_ins['rm']
        offset = decoded_ins['offset']
        if(decoded_ins['ins']=='lw'):
            if(int(reg[reg2],16)-base_address>=0 and (int(reg[reg2],16)-base_address)%4==0 and offset%4==0):
                    index = int((int(reg[reg2],16)-base_address)/4 + offset/4)
                    reg[reg1] = data['.word'][index]
        elif(decoded_ins['ins']=='sw'):
            if(int(reg[reg2],16)>=base_address and (int(reg[reg2],16)-base_address)%4==0 and offset%4==0):
                    index = int((int(reg[reg2],16)-base_address)/4 + offset/4)
                    if(index>=len(data['.word'])):
                        count = index-len(data['.word'])
                        for i in range(count):
                            data['.word'].append(0)
                        data['.word'].append(reg[reg1])
                    else:
                        data['.word'][index] = self.reg[reg1]
    else:
        pass
    


# In[102]:


def writeback(result):
        regstr = result[1]
        value = result[0]
        reg[regstr] = value         


# In[107]:


writeback(execute(decode(fetch(instruction,1))))


# In[108]:


memory(decode(fetch(instruction,2)))


# In[109]:


reg


# In[ ]:




