# reg = {"zero":0, "r0":0, "at":0, "v0":0, "v1":0, "a0":0, "a1":0, "a2":0, "a3":0, "t0":0, "t1":0, "t2":0, "t3":0, "t4":0, "t5":0, "t6":0, "t7":0,"s0":0, "s1":0, "s2":0, "s3":0 ,"s4":0 ,"s5":0, "s6":0, "s7":0, "t8":0, "t9":0, "k0":0, "k1":0, "gp":0, "sp":0, "s8":0, "ra":0}
# address = 0x10015000
# for val in reg:
#     reg[val] = address
#     address += 1

# print(reg)

# base_address = 0x10010000

# print(bin(int(str(5000), 16) + base_address))

# # 0b10000000000010101000000000000

# num = 171
# k = 5
# p = 2

# # convert number into binary first 
# binary = bin(num) 
# print (str(binary))

# # remove first two characters 
# binary = binary[2:]
# print (str(binary))

# end = len(binary) - p 
# start = end - k + 1
# print (str(end) + " " + str(start))
    
# # extract k bit sub-string 
# kBitSubStr = binary[start : end+1] 

# # convert extracted sub-string into decimal again 
# print (int(kBitSubStr,2))

# l1d = {
#         0: {0: [None]*64, 1: [None]*64, 2: [None]*64, 3: [None]*64, 4: [None]*64, 5: [None]*64, 6: [None]*64, 7: [None]*64, 8: [None]*64, 9: [None]*64, 10: [None]*64, 11: [None]*64, 12: [None]*64, 13: [None]*64, 14: [None]*64, 15: [None]*64},
#         1: {16: [None]*64, 17: [None]*64, 18: [None]*64, 19: [None]*64, 20: [None]*64, 21: [None]*64, 22: [None]*64, 23: [None]*64, 24: [None]*64, 25: [None]*64, 26: [None]*64, 27: [None]*64, 28: [None]*64, 29: [None]*64, 30: [None]*64, 31: [None]*64},
#         2: {32: [None]*64, 33: [None]*64, 34: [None]*64, 35: [None]*64, 36: [None]*64, 37: [None]*64, 38: [None]*64, 39: [None]*64, 40: [None]*64, 41: [None]*64, 42: [None]*64, 43: [None]*64, 44: [None]*64, 45: [None]*64, 46: [None]*64, 47: [None]*64},
#         3: {48: [None]*64, 49: [None]*64, 50: [None]*64, 51: [None]*64, 52: [None]*64, 53: [None]*64, 54: [None]*64, 55: [None]*64, 56: [None]*64, 57: [None]*64, 58: [None]*64, 59: [None]*64, 60: [None]*64, 61: [None]*64, 62: [None]*64, 63: [None]*64}
# }

l1d_blocks = 64
block_size = 4
l1d_assoc = 4

l1d = {}

for i in range(int(l1d_blocks/l1d_assoc)):
    l1d[i] = {}
    for j in range(l1d_assoc):
        l1d[i][j] = [None]*block_size

# l1d[0][0] = [None]*2

print(l1d)

{0: {0: [None, None, None, None], 1: [None, None, None, None], 2: [None, None, None, None], 3: [None, None, None, None]},
 1: {0: [None, None, None, None], 1: [None, None, None, None], 2: [None, None, None, None], 3: [None, None, None, None]}, 
 2: {0: [None, None, None, None], 1: [None, None, None, None], 2: [None, None, None, None], 3: [None, None, None, None]}, 
 3: {0: [None, None, None, None], 1: [None, None, None, None], 2: [None, None, None, None], 3: [None, None, None, None]}, 
 4: {0: [None, None, None, None], 1: [None, None, None, None], 2: [None, None, None, None], 3: [None, None, None, None]}, 
 5: {0: [None, None, None, None], 1: [None, None, None, None], 2: [None, None, None, None], 3: [None, None, None, None]}, 
 6: {0: [None, None, None, None], 1: [None, None, None, None], 2: [None, None, None, None], 3: [None, None, None, None]}, 
 7: {0: [None, None, None, None], 1: [None, None, None, None], 2: [None, None, None, None], 3: [None, None, None, None]}, 
 8: {0: [None, None, None, None], 1: [None, None, None, None], 2: [None, None, None, None], 3: [None, None, None, None]}, 
 9: {0: [None, None, None, None], 1: [None, None, None, None], 2: [None, None, None, None], 3: [None, None, None, None]}, 
 10: {0: [None, None, None, None], 1: [None, None, None, None], 2: [None, None, None, None], 3: [None, None, None, None]}, 
 11: {0: [None, None, None, None], 1: [None, None, None, None], 2: [None, None, None, None], 3: [None, None, None, None]}, 
 12: {0: [None, None, None, None], 1: [None, None, None, None], 2: [None, None, None, None], 3: [None, None, None, None]}, 
 13: {0: [None, None, None, None], 1: [None, None, None, None], 2: [None, None, None, None], 3: [None, None, None, None]}, 
 14: {0: [None, None, None, None], 1: [None, None, None, None], 2: [None, None, None, None], 3: [None, None, None, None]}, 
 15: {0: [None, None, None, None], 1: [None, None, None, None], 2: [None, None, None, None], 3: [None, None, None, None]}
}