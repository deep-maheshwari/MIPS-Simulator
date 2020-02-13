# def parse():
#     text = input()

#     result = text.split()

#     parsed = []

#     for st in result:
        
#         st = st.split(",")
#         for x in st:
#             if(x):
#                 parsed.append(x)

#     print(parsed)

# parse()



def load_file():
    file = open("trial.asm", "r")
    parsed = parse(file)
    print("1.Run file\n2. Run step by step")
    todo3 = int(input())
    if(todo3 == 1):
        run_file(parsed)
    if(todo3 == 2):
        run_sbs(parsed)
    else:
        print("Enter valid option!!!")
    # for line in file:
    #     print(line)

def run_file(file):
    file = open("trial.asm", "r")
    parse(file)

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


def registers():
    reg = {"r0", "at", "v0", "v1", "a0", "a1", "a2", "a3", "t0", "t1", "t2", "t3", "t4", "t5", "t6", "t7", "s0", "s1", "s2", "s3", "s4" "s5", "s6", "s7", "t8", "t9", "k0", "k1", "gp", "sp", "s8", "ra"}
    

def data():
    

print("1. Load File\n2.Interactive Console")
todo1 = int(input())

if(todo1 == 1):
    load_file()

if(todo1 == 2):
    interactive_console()

else:
    print("Enter valid option!!!")