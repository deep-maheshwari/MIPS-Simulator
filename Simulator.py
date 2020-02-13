# Simulator for phase 1
instructions = ["add","sub","lw","sw","bne"]
registers = ['s1','s2','s3','s4','s5','s6','s7']
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

    for items in parsed_list:
        print(items)
        
read_instructions(fileHandler("C:/Users/Admin/Desktop/programming/Assembly/bubble_sort.asm"))

#print(parse("add $s1, $s2, $s3"))
