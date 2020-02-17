# Simulator for phase 1
reg = ["r0", "at", "v0", "v1", "a0", "a1", "a2", "a3", "t0", "t1", "t2", "t3", "t4", "t5", "t6", "t7", "s0", "s1", "s2", "s3", "s4" "s5", "s6", "s7", "t8", "t9", "k0", "k1", "gp", "sp", "s8", "ra"]
register = {"r0": 0, "at": 0, "v0": 0, "v1": 0, "a0": 0, "a1": 0, "a2": 0, "a3": 0, "t0": 0, "t1": 0, "t2": 0, "t3": 0, "t4": 0, "t5": 0, "t6": 0, "t7": 0, "s0": 0, "s1": 0, "s2": 0, "s3": 0, "s4": 0 "s5": 0, "s6": 0, "s7": 0, "t8": 0, "t9": 0, "k0": 0, "k1": 0, "gp": 0, "sp": 0, "s8": 0, "ra": 0}

def parse():


def parse_particular():



def load_file():
    file = open("trial.asm", "r")
    parsed = parse(file)                        #check
    print("1.Run file\n2. Run step by step")
    todo3 = int(input())
    if(todo3 == 1):
        run_file(parsed)
    if(todo3 == 2):
        run_sbs(parsed)
    else:
        print("Enter valid option!!!")


def run_file(file):
    file = open("trial.asm", "r")
    data = parse(file).data                    #new
    main = parse(file).main                    #new

    word_list = []
    for word in data:
        word_list.append(word)
    
    pc = 0;
    for instruction in main:
        
        pc = pc + 4


def run_sbs(file):


def interactive_console():
    todo2 = 0
    while(True):
        print("1. Instructions\n2.Registers or Memory\n3.Data Segment\n4. Quit")
        todo2 = int(input())
        if(todo2 == 1):
            instructions()
        if(todo2 == 2):
            registers()
        if(todo2 == 3):
            data()
        if(todo2 == 4):
            break
        else:
            print("Enter valid option!!!")
    
def instructions():
    pc = 0;
    instr = list(input())
    parsed_instr = parse_particular(instr)          #new


def registers():
    
    print("PC: " + pc)                              #new
    count = 0
    for i in reg:
        print("R" + count + " [" + i + "]: " + register["'" + i + "'"])   #check if it works
        count = count + 1
    

def data(data):
    print("User Data Segment [10000000]..[10040000]")
    print("[10000000]..[1000ffff]  00000000")
    
    print("[10010000]   ")
    for d in data:
        print(d + " ",)             #check if it works

print("1. Load File\n2.Interactive Console")
todo1 = int(input())

if(todo1 == 1):
    load_file()

if(todo1 == 2):
    interactive_console()

else:
    print("Enter valid option!!!")