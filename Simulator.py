# Simulator for phase 1
instructions = ["add","sub","lw","sw","bne"]
registers = ['s1','s2','s3','s4','s5','s6','s7']
base_address = 10010000

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

instructions = read_instructions(fileHandler("/home/tapish/CO/bub_sort.asm"))
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

print(data_and_text['main'])

#print(parse("add $s1, $s2, $s3"))