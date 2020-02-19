import sqlite3

class Database:
    def _init_(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute("""CREATE TABLE IF DOES NOT EXIST (
            print text
            )""")
        
        self.conn.commit()

        # data_and_text = {'data':[],'main':[],}
        # instructions = []
        # data = {'.word':[],'.text':[]}
        # label_address = {}
        # main = {}

    # def fileHandler(filename):

    #     file = open(filename,'r')
    #     result = []
    #     for line in file.readlines():
    #         result.append(line)
    #     return result

    # def loadfile(filename):
    #     instructions = read_instructions(fileHandler(filename))
        

    #     pos_data = 0
    #     pos_main = 0

    #     data_labels = []

    #     for i in range(len(instructions)):
            
    #         if(instructions[i][0]=='.data'):
    #             pos_data = i
    #         elif(instructions[i][0]=='main:'):
    #             pos_main = i

    #     for i in range(pos_data+1,pos_main):

    #         if(instructions[i][0]!='.text' and instructions[i][0]!='.globl'):
    #             data_and_text['data'].append(instructions[i])

    #     for i in range(pos_main+1,len(instructions)):
    #         data_and_text['main'].append(instructions[i])

    #     for dat in data_and_text['data']:
    #         if(len(dat)==1):
    #             data_labels.append(dat[0][:-1])

    #     count = 0
    #     label_count = 0

    #     for ins in data_and_text['data']:
    #         if(len(ins)==1):
    #             label_address[data_labels[label_count]] = count
    #             label_count+=1

    #         if(ins[0]=='.word'):
    #             for i in range(1,len(ins)):
    #                 data['.word'].append(int(ins[i]))
    #                 count+=1

    #     count = 0

    #     for ins in data_and_text['main']:
    #         if(len(ins)==1):
    #             ins[0] = ins[0][:-1]
    #             main[ins[0]]=count
    #         else:
    #             count+=1

    #     for ins in data_and_text['main']:
    #         if(ins[0] in main.keys()):
    #             data_and_text['main'].remove(ins)

    def time_pass(self):
        self.cur.execute("PRINT *")
        print('It works for now!!!')

    # def addressfetch(self):
    #     app.filename = filedialog.askopenfilename(initialdir = '/CO', title = 'Select a File', filetypes = (('asm files', '*.asm'), ('s files', '*.s')))
        # loadfile(app.filename)

    # def parse(text):

    #     result = text.split()
    #     parsed = []

    #     for st in result:
            
    #         st = st.split(",")
    #         for x in st:
    #             if(x):
    #                 parsed.append(x)

    #     return parsed

    # def read_instructions(instructions):

    #     parsed_list = []
    #     for ins in instructions:
    #         if(parse(ins)):
    #             parsed_list.append(parse(ins))

    #     return parsed_list
    def _del_(self):
        self.conn.close()