# # Python program to create a table 

from tkinter import *
from tkinter import ttk
import Cached_Simulator as Cache
# class Table: 
	
# 	def __init__(root, total_rows, total_columns, lst1): 
		
# 		# code for creating table 
# 		for i in range(total_rows): 
# 			for j in range(total_columns): 
				
# 				e = Label(root, width=20, fg='blue', 
# 							font=('Arial',16,'bold')) 
				
# 				e.grid(row=i, column=j) 
# 				e.insert(END, lst1[i][j]) 

# # take the data 
# ls2 = [[4, 5, 6],
#         [1, 2, 4]]

# ros = len(ls2)
# clms = len(ls2)
# root = Tk() 
# t1 = Table(root, ros, clms, ls2)

# ls = [(1, 'Raj','Mumbai', 19), 
# 	(2,'Aaryan','Pune',18), 
# 	(3,'Vaishnavi','Mumbai',20), 
# 	(4,'Rachna','Mumbai',21), 
# 	(5,'Shubham','Delhi',21)] 

# # find total number of rows and 
# # columns in list 
# rows = len(ls) 
# columns = len(ls[0]) 

# # create root window 

# t = Table(root, rows, columns, ls) 
# root.mainloop()

def take_inputs():

    inp = Tk()
    inp.geometry('450x300')

    def transfer_values():
        lst = [int(size1_entry.get()), int(assoc1_entry.get()), int(blocks1_entry.get()), int(size2_entry.get()), int(assoc2_entry.get()), int(blocks2_entry.get())]
        show_cache(lst)
        # print(lst)
        
    # l1_block_size = IntVar()
    # l1_set_assoc = IntVar()
    # l1_blocks = IntVar()
    # l2_block_size = IntVar()
    # l2_set_assoc = IntVar()
    # l2_blocks = IntVar()

    size1 = Label(inp, text = 'L1 Block Size: ', fg = 'blue')
    size1.grid(row = 0, column = 0, pady = 5, padx = 10, sticky = 'w')
    
    assoc1 = Label(inp, text = 'L1 Set Associativity: ', fg = 'blue')
    assoc1.grid(row = 1, column = 0, pady = 5, padx = 10, sticky = 'w')

    blocks1 = Label(inp, text = 'L1 Number of Blocks: ', fg = 'blue')
    blocks1.grid(row = 2, column = 0, pady = 5, padx = 10, sticky = 'w')

    size2 = Label(inp, text = 'L2 Block Size: ', fg = 'blue')
    size2.grid(row = 3, column = 0, pady = 5, padx = 10, sticky = 'w')

    assoc2 = Label(inp, text = 'L2 Set Associativity: ', fg = 'blue')
    assoc2.grid(row = 4, column = 0, pady = 5, padx = 10, sticky = 'w')

    blocks2 = Label(inp, text = 'L2 Number of Blocks: ', fg = 'blue')
    blocks2.grid(row = 5, column = 0, pady = 5, padx = 10, sticky = 'w')

    size1_entry = Entry(inp)
    size1_entry.grid(row = 0, column = 1, padx = 3, pady = 5)
    size1_entry.insert(0, '0')
    size1_entry.focus_set()

    assoc1_entry = Entry(inp)
    assoc1_entry.grid(row = 1, column = 1, padx = 3, pady = 5)
    assoc1_entry.insert(0, '0')
    assoc1.focus_set()

    blocks1_entry = Entry(inp)
    blocks1_entry.grid(row = 2, column = 1, padx = 3, pady = 5)
    blocks1_entry.insert(0, '0')
    blocks1_entry.focus_set()

    size2_entry = Entry(inp)
    size2_entry.grid(row = 3, column = 1, padx = 3, pady = 5)
    size2_entry.insert(0, '0')
    size2_entry.focus_set()

    assoc2_entry = Entry(inp)
    assoc2_entry.grid(row = 4, column = 1, padx = 3, pady = 5)
    assoc2_entry.insert(0, '0')
    assoc2_entry.focus()

    blocks2_entry = Entry(inp)
    blocks2_entry.grid(row = 5, column = 1, padx = 3, pady = 5)
    blocks2_entry.insert(0, '0')
    blocks2_entry.focus_set()

    ok = Button(inp, text = 'Done', width = 7, command = transfer_values)
    ok.grid(row = 6, column = 0, columnspan =2, pady = 10)

    exit_button = Button(inp, text = 'Exit', width = 5, command = inp.destroy)
    exit_button.grid(row = 6, column = 1, columnspan = 2, pady = 10)

    inp.mainloop()

def show_cache(details):
    print(details)

    Cache.GUI_cache_input(details)
    Cache.Simulate()

    file = open('Cache.txt', 'r')
    cache_list = []
    for eac in file:
        cache_list.append(eac)

    l1 = []
    l2 = []

    i = 0
    cache_list[0] = list(cache_list[0].split(', '))
    cache_list[1] = list(cache_list[1].split(', '))

    for each in cache_list[0]:
        if('[' in each):
            each = each.replace('[', '')
        if(']' in each):
            each = each.replace(']', '')
        if("''" in each or "None" in each):
            each = ' '
        if('\n' in each):
            each = each.replace('\n', '')
        l1.append(each)

    for each in cache_list[1]:
        if('[' in each):
            each = each.replace('[', '')
        if(']' in each):
            each = each.replace(']', '')
        if("''" in each or "None" in each):
            each = ' '
        l2.append(each)

    # print(l1)
    # print("--------------------------------------------------")
    # print(l2)

    lst1 = []
    for _ in range(int(l1[2]) + 2):
        lst1.append([])

    for i in range(int(l1[0])):
        lst1[0].append('Set ' + str(i))

    for i in range(int(l1[1])):
        lst1[1].append('Tag ' + str(i))

    for i in range(int(l1[2])):
        for j in range(2 * int(l1[0]) * int(l1[1])):
            lst1[i+2].append(l1[2*int(l1[0])*int(l1[1])*i+j+3])

    lst2 = []
    for _ in range(int(l2[2]) + 2):
        lst2.append([])

    for i in range(int(l2[0])):
        lst2[0].append('Set ' + str(i))

    for i in range(int(l2[1])):
        lst2[1].append('Tag ' + str(i))

    for i in range(int(l2[2])):
        for j in range(2 * int(l2[0]) * int(l2[1])):
            lst2[i+2].append(l2[2*int(l2[0])*int(l2[1])*i+j+3])

    #Initializing Tk()
    cache = Tk()
    window_width = cache.winfo_screenwidth()
    window_height = cache.winfo_screenheight()
    cache.geometry(str(window_width) + "x" + str(window_height))
    cache.resizable(True, True) 

    #For L1
    frame1 = Canvas(cache, borderwidth = 2, width = window_width-10)
    frame1.grid(sticky = 'w')
    # head = Entry(frame1, fg='blue', font = ('Times', 20, 'bold'), bd = 0, bg = 'lightblue')
    # head.grid(row = 0, column = 0, columnspan = 2*len(lst1[0])*len(lst1[1]), sticky = 'we')
    # head.insert(END, 'L1 Cache:')
    # head.configure(state = 'readonly')
    head = Label(frame1, text = 'L1 Cache:', borderwidth = 1, relief = "ridge", fg='blue', font = ('Times', 20, 'bold'))
    head.grid()

    frame1.create_window(0, 0, anchor = NW, window = head)
    scroll1 = Scrollbar(cache, orient = 'horizontal', command = frame1.xview)
    frame1.configure(xscrollcommand = scroll1.set, scrollregion = (0, 0, 230*len(lst1[0]), 230*len(lst1[0])))
    scroll1.config(command = frame1.xview, bg = 'grey')
    scroll1.grid(row = 1, sticky = 'ew')

    e = Label(frame1, borderwidth = 1, relief = "ridge", text = 'Offset', width = 6, font = ('Times', 14), height = 3)
    e.grid(row = 1, column = 0, rowspan = 2, ipady = 12)
    frame1.create_window(0, 33, anchor = NW, window = e)
    # e.insert(END, 'Offset')

    y = []
    for i in range(int(l1[2])):
        e = Label(frame1, borderwidth = 1, relief = "ridge", text = i, width = 6, font = ('Times', 14))
        e.grid(row = i+3, column = 0)
        frame1.create_window(0, 84 + i * 25, anchor = NW, window = e)
        y.append(84 + i * 25)
        # e.insert(END, i)

    for i in range(int(l1[0])):
        e = Label(frame1, borderwidth = 1, relief = "ridge", text = lst1[0][i], width = 6*len(lst1[1]), font = ('Times', 14, 'bold'))
        e.grid(row = 1, column = 2*len(lst1[1])*i+1, columnspan = 2*len(lst1[1]))
        frame1.create_window(59 + i * 224, 33, anchor = NW, window = e)
        # e.insert(END, lst1[0][i])

    j = 0
    for i in range(len(lst1[0]) * len(lst1[1])):
        e = Label(frame1, borderwidth = 1, relief = "ridge", text = lst1[1][j], width = 5, font = ('Times', 15))
        e.grid(row = 2, column = 2*i + 1, columnspan = 2)
        frame1.create_window(59 + i * 56, 58, anchor = NW, window = e)
        # e.insert(END, lst1[1][j])
        j += 1
        if(j % len(lst1[1]) == 0):
            j = 0

    last_row = 0
    for i in range(int(l1[2])):
        for k in range(len(lst1[i+2])):
            e = Label(frame1, borderwidth = 1, relief = "ridge", text = lst1[i+2][k], width = 2, font = ('Times', 15))
            e.grid(row = 3+i, column = k+1)
            frame1.create_window(59 + k * 28, y[i], anchor = NW, window = e)
            # e.insert(END, lst1[i+2][k])
        last_row = 3 + i


    # For L2
    frame2 = Canvas(cache, borderwidth = 2, width = window_width-10)
    frame2.grid(row = 2, sticky = 'we')
    # last_row += 1
    head = Label(frame2, text = 'L2 Cache:', borderwidth = 1, relief = "ridge", fg='blue', font = ('Times', 20, 'bold'))
    head.grid()

    frame2.create_window(0, 0, anchor = NW, window = head)
    scroll2 = Scrollbar(cache, orient = 'horizontal', command = frame2.xview)
    frame2.configure(xscrollcommand = scroll2.set, scrollregion = (0, 0, 230*len(lst2[0]), 230*len(lst2[0])))
    scroll2.config(command = frame2.xview, bg = 'grey')
    scroll2.grid(row = 3, sticky = 'ew')

    e = Label(frame2, borderwidth = 1, relief = "ridge", text = 'Offset', width = 6, font = ('Times', 14), height = 3)
    e.grid(row = last_row+1, column = 0, rowspan = 2)
    frame2.create_window(0, 33, anchor = NW, window = e)
    # e.insert(END, 'Offset')

    y = []
    for i in range(int(l2[2])):
        e = Label(frame2, borderwidth = 1, relief = "ridge", text = i, width = 6, font = ('Times', 14))
        e.grid(row = last_row+i+3, column = 0)
        frame2.create_window(0, 84 + i * 25, anchor = NW, window = e)
        y.append(84 + i * 25)
        # e.insert(END, i)

    for i in range(int(l2[0])):
        e = Label(frame2, borderwidth = 1, relief = "ridge", text = lst2[0][i], width = 6*len(lst2[1]), font = ('Times', 14, 'bold'))
        e.grid(row = last_row+1, column = 2*len(lst2[1])*i+1, columnspan = 2*len(lst2[1]))
        frame2.create_window(59 + i * 224, 33, anchor = NW, window = e)
        # e.insert(END, lst1[0][i])

    j = 0
    for i in range(len(lst2[0]) * len(lst2[1])):
        e = Label(frame2, borderwidth = 1, relief = "ridge", text = lst2[1][j], width = 5, font = ('Times', 15))
        e.grid(row = last_row+2, column = 2*i + 1, columnspan = 2)
        frame2.create_window(59 + i * 56, 58, anchor = NW, window = e)
        # e.insert(END, lst1[1][j])
        j += 1
        if(j % len(lst2[1]) == 0):
            j = 0

    for i in range(int(l2[2])):
        for k in range(len(lst2[i+2])):
            e = Label(frame2, borderwidth = 1, relief = "ridge", text = lst2[i+2][k], width = 2, font = ('Times', 15))
            e.grid(row = last_row+3+i, column = k+1)
            frame2.create_window(59 + k * 28, y[i], anchor = NW, window = e)
            # e.insert(END, lst1[i+2][k])

    misses1 = Label(cache, text = 'L1 Miss Count: ' + str(Cache.return_data()[0]) + '       L2 Miss Count: ' + str(Cache.return_data()[2]), fg='blue', font = ('Times', 15))
    misses1.grid(row = 4, column = 0, sticky = 'w', pady = 15, padx = 5)

    hits1 = Label(cache, text = 'L1 Hit Count: ' + str(Cache.return_data()[1]) + '        L2 Hit Count: ' + str(Cache.return_data()[3]), fg='blue', font = ('Times', 15))
    hits1.grid(row = 5, column = 0, sticky = 'w', pady = 10, padx = 5)

    mm = Label(cache, text = 'Main memory: ' + str(Cache.return_data()[4]), fg = 'blue', font = ('Times', 15))
    mm.grid(row = 6, column = 0, sticky = 'w', padx = 5, pady = 10)

    cache.mainloop()

# def printtext():
#     global e
#     string = e.get() 
#     print(string)  

# from tkinter import *
# root = Tk()

# root.title('Name')

# e = Entry(root)
# e.pack()
# e.focus_set()

# b = Button(root,text='okay',command=printtext)
# b.pack(side='bottom')
# root.mainloop()