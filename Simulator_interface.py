import re

class Simulator:

    reg = {"zero":0, "r0":0, "at":0, "v0":0, "v1":0, "a0":0, "a1":0, "a2":0, "a3":0, "t0":0, "t1":0, "t2":0, "t3":0, "t4":0, "t5":0, "t6":0, "t7":0,"s0":0, "s1":0, "s2":0, "s3":0 ,"s4":0 ,"s5":0, "s6":0, "s7":0, "t8":0, "t9":0, "k0":0, "k1":0, "gp":0, "sp":0, "s8":0, "ra":0}
    base_address = 0x10010000
    data_and_text = {'data':[],'main':[]}
    data = {'.word':[],'.text':[]}
    bne_flag = ''
    beq_flag = ''
    j_flag = ''
    label_address = {}
    main = {}
    instructions = []
    PC = 0
    msg = ""

    def run_instruction(self,instruction,PC):

        if(instruction[0]=='add'):
            if(len(instruction)!=4):
                msg = "Error in the given instruction. Missing or extra operand given"

            else:
                reg1 = instruction[1].replace('$','')
                reg2 = instruction[2].replace('$','')
                reg3 = instruction[3].replace('$','')
                self.reg[reg1] = self.reg[reg2]+self.reg[reg3]
                PC+=1

        elif(instruction[0]=='sub'):
            if(len(instruction)!=4):
                msg = "Error in the given instruction. Missing or extra operand given"

            else:
                reg1 = instruction[1].replace('$','')
                reg2 = instruction[2].replace('$','')
                reg3 = instruction[3].replace('$','')
                self.reg[reg1] = self.reg[reg2]-self.reg[reg3]
                PC+=1

        elif(instruction[0]=='lw'):
            if(len(instruction)!=3):
                msg = "Error in the given instruction. Missing or extra operand given"

            else:
                reg_pattern = re.search(r"\$[a-z0-9]*",instruction[2],re.MULTILINE)
                offset_pattern = re.search(r"\w+",instruction[2],re.MULTILINE)
                reg1 = instruction[1].replace('$','')
                reg2 = reg_pattern.group(0)
                reg2 = reg2.replace('$','')
                offset = int(offset_pattern.group(0))
                #print(int(reg[reg2],16)-base_address)
                if(int(self.reg[reg2],16)-self.base_address>=0 and (int(self.reg[reg2],16)-self.base_address)%4==0 and offset%4==0):
                    index = int((int(self.reg[reg2],16)-self.base_address)/4 + offset/4)
                    self.reg[reg1] = self.data['.word'][index]
                PC+=1

        elif(instruction[0]=='sw'):
            if(len(instruction)!=3):
                msg = "Error in the given instruction. Missing or extra operand given"

            else:
                reg_pattern = re.search(r"\$[a-z0-9]*",instruction[2],re.MULTILINE)
                offset_pattern = re.search(r"\w+",instruction[2],re.MULTILINE)
                reg1 = instruction[1].replace('$','')
                reg2 = reg_pattern.group(0)
                reg2 = reg2.replace('$','')
                offset = int(offset_pattern.group(0))

                if(int(self.reg[reg2],16)>=self.base_address and (int(self.reg[reg2],16)-self.base_address)%4==0 and offset%4==0):
                    index = int((int(self.reg[reg2],16)-self.base_address)/4 + offset/4)
                    if(index>=len(self.data['.word'])):
                        count = index-len(data['.word'])
                        for i in range(count):
                            self.data['.word'].append(0)
                        self.data['.word'].append(self.reg[reg1])
                    else:
                        self.data['.word'][index] = self.reg[reg1]
                PC+=1

        elif(instruction[0]=='bne'):

            if(len(instruction)!=4):
                msg = "Error in the given instruction. Missing or extra operand given"
            
            else:
                reg1 = instruction[1].replace('$','')
                reg2 = instruction[2].replace('$','')
                
                if(self.reg[reg1]!=self.reg[reg2]):
                    self.bne_flag = instruction[3]   
                    PC = self.main[self.bne_flag] 

                else:
                    self.bne_flag = ''
                    PC+=1

        elif(instruction[0]=='lui'):

            if(len(instruction)!=3):
                msg = msg + "Error in the given instruction. Missing or extra operand given"
                self.PC = len(self.instructions)+1

            else:
                reg1 = instruction[1].replace('$','')
                self.reg[reg1] = hex(int(instruction[2]+'0000',16))
                PC+=1

        elif(instruction[0]=='slt'):

            if(len(instruction)!=4):
                msg = "Error in the given instruction. Missing or extra operand given"

            else:
                reg1 = instruction[1].replace('$','')
                self.reg[reg1] = 0
                reg2 = instruction[2].replace('$','')
                reg3 = instruction[3].replace('$','')
                if(self.reg[reg2]<self.reg[reg3]):
                    self.reg[reg1] = 1
                PC+=1

        elif(instruction[0]=='beq'):

            if(len(instruction)!=4):
                msg = "Error in the given instruction. Missing or extra operand given"

            else:
                reg1 = instruction[1].replace('$','')
                if(instruction[2][0]=='$'):
                    reg2 = instruction[2].replace('$','')
                    if(self.reg[reg1]==self.reg[reg2]):
                        self.beq_flag = instruction[3]
                        PC = self.main[self.beq_flag]

                    else:
                        self.beq_flag = ''
                        PC+=1
                
                else:
                    reg2 = int(instruction[2])
                    if(self.reg[reg1]==reg2):
                        self.beq_flag = instruction[3]
                        PC = self.main[self.beq_flag]

                    else:
                        self.beq_flag = ''
                        PC+=1

        elif(instruction[0]=='j'):

            if(len(instruction)!=2):
                msg = "Error in the given instruction. Missing or extra operand given"

            else:
                self.j_flag = instruction[1]
                PC = self.main[self.j_flag]

        elif(instruction[0]=='addi'):

            if(len(instruction)!=4):
                msg = "Error in the given instruction. Missing or extra operand given"

            else:
                reg1 = instruction[1].replace('$','')
                reg2 = instruction[2].replace('$','')
                addend = int(instruction[3])
                if(type(self.reg[reg2])==str and self.reg[reg2][0:2]=='0x'):
                    self.reg[reg1] = hex(int(self.reg[reg2],16)+addend)
                else:
                    self.reg[reg1] = self.reg[reg2] + addend
                PC+=1
        elif(instruction[0]=='andi'):

            if(len(instruction)!=4):
                msg = "Error in the given instruction. Missing or extra operand given"

            else:
                reg1 = instruction[1].replace('$','')
                reg2 = instruction[2].replace('$','')
                anded = instruction[3]
                self.reg[reg1] = hex(int(self.reg[reg2],16)&int(anded,16))
                PC=PC+1

        elif(instruction[0]=='and'):

            if(len(instruction)!=4):
                msg = "Error in the given instruction. Missing or extra operand given"

            else:
                reg1 = instruction[1].replace('$','')
                reg2 = instruction[2].replace('$','')
                reg3 = instruction[3].replace('$','')
                self.reg[reg1] = hex(int(self.reg[reg2],16) & int(self.reg[reg3],16))
                PC = PC + 1
                
        return PC

    def fileHandler(self,filename):

        file = open(filename,'r')
        result = []
        for line in file.readlines():
            result.append(line)
        return result

    def parse(self,text):

        result = text.split()
        parsed = []

        for st in result:
            
            st = st.split(",")
            for x in st:
                if(x):
                    parsed.append(x)

        return parsed

        
    def read_instructions(self,instructions):

        parsed_list = []
        for ins in instructions:
            if(self.parse(ins)):
                parsed_list.append(self.parse(ins))

        return parsed_list

    def fetch_and_load_file(self,filepath):

        self.instructions = self.read_instructions(self.fileHandler(filepath))

    def load_data_and_text(self):

        pos_data = 0
        pos_main = 0

        for i in range(len(self.instructions)):
            
            if(self.instructions[i][0]=='.data'):
                pos_data = i
            elif(self.instructions[i][0]=='main:'):
                pos_main = i

        for i in range(pos_data+1,pos_main):
             if(self.instructions[i][0]!='.text' and self.instructions[i][0]!='.globl'):
                self.data_and_text['data'].append(self.instructions[i])

        for i in range(pos_main+1,len(self.instructions)):
            self.data_and_text['main'].append(self.instructions[i])

    def load_data(self):

        data_labels = []

        for dat in self.data_and_text['data']:
            if(len(dat)==1):
                data_labels.append(dat[0][:-1])
        
        count = 0
        label_count = 0

        for ins in self.data_and_text['data']:
            if(len(ins)==1):
                self.label_address[data_labels[label_count]] = count
                label_count+=1

            if(ins[0]=='.word'):
                for i in range(1,len(ins)):
                    self.data['.word'].append(int(ins[i]))
                    count+=1

    def load_main(self):

        self.main = {}
        count = 0
        for ins in self.data_and_text['main']:
            if(len(ins)==1):
                ins[0] = ins[0][:-1]
                self.main[ins[0]]=count
            else:
                count+=1

    def set_data_and_text(self):

        for ins in self.data_and_text['main']:
            if(len(ins)==1):
                self.data_and_text['main'].remove(ins)

    def print_reg(self):

        for register in self.reg.keys():
                print(register+": "+str(self.reg[register]))

    def print_data(self):

        for i in range(len(self.data['.word'])):
                print(hex((self.base_address+4*i))+": "+str(self.data['.word'][i]))

    def print_instructions(self):
        
        for ins in self.data_and_text['main']:
            print(ins)

    def Simulate_all(self):

        self.PC = 0

        # print('1.Run file')
        # print('2.Run file step by step')
        # print('Choose one of the above option')
        # option = int(input())

        while(self.PC!=len(self.data_and_text['main'])-1):
            print(self.PC)
            self.PC = self.run_instruction(self.data_and_text['main'][self.PC],self.PC)

            if(self.PC>len(self.data_and_text['main'])):
                msg = "Unexpected error occured."
                break
            
        # print(parse("add $s1, $s2, $s3"))
        #print(len(data_and_text['main']))

    def Simulate_step(self):

        # print('1.Run command\n2.Show registers\n3.Show Memory\n4.exit')

        # int_option = int(input())

        self.PC = self.run_instruction(self.data_and_text['main'][self.PC],self.PC)

        # elif(int_option==2):
        #     for register in self.reg.keys():
        #             print(register+": "+str(self.reg[register]))

        # elif(int_option==3):
        #     for i in range(len(self.data['.word'])):
        #         print(hex((self.base_address+4*i))+": "+str(self.data['.word'][i]))
        
        # elif(int_option==4):
        #     break

        # if(self.PC>len(self.data_and_text['main'])):
        #     print("Unexpected error occured.")
        #     break   
        
        # print('1.Run command\n2.Show registers\n3.Show Memory\n4.exit')


    def reinitialize(self):

        self.reg = {"zero":0, "r0":0, "at":0, "v0":0, "v1":0, "a0":0, "a1":0, "a2":0, "a3":0, "t0":0, "t1":0, "t2":0, "t3":0, "t4":0, "t5":0, "t6":0, "t7":0,"s0":0, "s1":0, "s2":0, "s3":0 ,"s4":0 ,"s5":0, "s6":0, "s7":0, "t8":0, "t9":0, "k0":0, "k1":0, "gp":0, "sp":0, "s8":0, "ra":0}
        self.base_address = 0x10010000
        self.data_and_text = {'data':[],'main':[],}
        self.data = {'.word':[],'.text':[]}
        self.label_address = {}
        self.main = {}
        self.instructions = []
        self.PC = 0
        self.msg = ""

    def print_all(self):

        self.print_reg()
        self.print_data()
        self.print_instructions()
        print(self.bne_flag)
        print(self.beq_flag)
        print(self.PC)
        print(self.label_address)
        print(self.main)


if __name__ == '__main__':

    Sim = Simulator()

    Sim.fetch_and_load_file()
    Sim.load_data_and_text()
    Sim.load_data()
    Sim.load_main()
    Sim.set_data_and_text()
    Sim.Simulate_all()
    