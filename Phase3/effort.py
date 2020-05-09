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
scroll1.config(command = frame1.xview)
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
scroll2.config(command = frame2.xview)
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

cache.mainloop()

# import tkinter as tk
# from tkinter import ttk

# root = tk.Tk()

# mytext = tk.StringVar(value='test ' * 30)

# myframe = ttk.Frame(root)
# myentry = ttk.Entry(myframe, textvariable=mytext, state='readonly')
# myscroll = ttk.Scrollbar(myframe, orient='horizontal', command=myentry.xview)
# myentry.config(xscrollcommand=myscroll.set)

# myframe.grid()
# myentry.grid(row=1, sticky='ew')
# myscroll.grid(row=2, sticky='ew')

# root.mainloop()