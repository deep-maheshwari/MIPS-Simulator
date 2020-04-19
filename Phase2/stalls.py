instruction_lst = [][]

def data_hazard(instruction1, instruction2):

    if(instruction1[1] == instruction2[2] || instruction1[1] == instruction2[3]):
        return True
    else:
        return False


    def stall(instruction_lst):
    for i in range(len(instruction_lst)):
        if(data_hazard):
            if((instruction_lst[i][0] == 'add' && instruction_lst[i+1][0] == 'sub') || (instruction_lst[i][0] == 'add' && instruction_lst[i+1][0] == 'add') || (instruction_lst[i][0] == 'sub' && instruction_lst[i+1][0] == 'add') || (instruction_lst[i][0] == 'sub' && instruction_lst[i+1][0] == 'sub') || (instruction_lst[i][0] == 'add' && instruction_lst[i+1][0] == 'lw') || (instruction_lst[i][0] == 'sub' && instruction_lst[i+1][0] == 'lw')):
                return False
            else:
                return True
        
        if(instruction_lst[i][0] == 'bne' || instruction_lst[i][0] == 'beq'):
            return True


    for i in range(len(instruction_lst)):
        if((instruction_lst[i][0] == 'add' && instruction_lst[i+1][0] == 'sub') || (instruction_lst[i][0] == 'add' && instruction_lst[i+1][0] == 'add') || (instruction_lst[i][0] == 'sub' && instruction_lst[i+1][0] == 'add') || (instruction_lst[i][0] == 'sub' && instruction_lst[i+1][0] == 'sub') || (instruction_lst[i][0] == 'add' && instruction_lst[i+1][0] == 'lw') || (instruction_lst[i][0] == 'sub' && instruction_lst[i+1][0] == 'lw')):
            data_hazard(instruction_lst[i], instruction_lst[i+1])


numberOfStalls = 0
for i in range(len(instruction_lst)):
    if(stall(instruction_lst)):
        numberOfStalls+=1
