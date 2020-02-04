# Simulator for phase 1
instructions = ["add","sub","lw","sw","bne"]
registers = ['s1','s2','s3','s4','s5','s6','s7']
def fileHandler(filename):
    file = open(filename,'r')
    for line in file.readlines():
        print(line)
    
def parse(text):
    raw = []

    for st in text:
        raw.append(st.split(","))

    parsed = []

    for item in raw:
        for st in item:
            if(st):
                parsed.append(st)

    print(parsed)

fileHandler("C:/Users/Admin/Desktop/programming/Assembly/question6.s")
    
    