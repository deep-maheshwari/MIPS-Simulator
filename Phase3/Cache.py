import math

class Cache:

    block_size = 0
    set_assoc = 0
    blocks = 0
    miss_penalty = 0 #time to fetch_from cache to it's next level
    miss_count = 0
    cache_lat = 0 #time taken to fetch from cache
    hit_count = 0
    cache = {}

    def __init__(self,block_size,set_assoc,blocks):
        self.block_size = block_size
        self.blocks = blocks
        self.set_assoc = set_assoc

        for i in range(int(blocks/set_assoc)):
            self.cache[i] = {}
            for j in range(set_assoc):
                self.cache[i][j] = (0, ['']*block_size)
            

    def Cache_controller(self, address):
        address = bin(address)[2:]
        index_bits = int(math.log(self.blocks/self.set_assoc, 2))
        offset_bits = int(math.log(self.block_size, 2))
        return {'offset': int(address[(len(address)-offset_bits):], 2),
                'index': int(address[(len(address)-(offset_bits + index_bits)): len(address)-offset_bits], 2), 
                'tag': int(address[:(len(address)-(offset_bits + index_bits))], 2)}

    def place_block(self, address, modified_address):
        address = address - (address % self.block_size)
        temp = []
        count = 0
        while(count < self.block_size):
            if(address + count > len(data['.word'])):
                temp.append('')
            else:
                temp.append(data['.word'][address + count])
        location = self.cache[modified_address['index']][modified_address['tag']][1]
        if(location != ['']*self.block_size):                       #check
            self.replace(temp, policy, modified_address)
        else:
            location = temp
    
    def search(self, modified_address, address):
        location = self.cache[modified_address['index']][modified_address['tag']][1][modified_address['offset']]
        if(location == ''):
            self.miss_count += 1
            self.place_block(address, modified_address)
            return {}
        else:
            return location
    
    def write_block(self, address, modified_address):
        location = self.cache[modified_address['index']][modified_address['tag']][1]
        address = address - (address % self.block_size)
        data['.word'][address: address + self.block_size] = location

    def lru_policy(self, modified_address):
        tag = 0
        min = self.cache[modified_address['index'][tag][0]]
        for i in range(self.set_assoc):                                     #depends on how the tags are, change it if required
            if(min > self.cache[modified_address['index']][i][0]):
                min = self.cache[modified_address['index']][i][0]
                tag = i
        return self.cache[modified_address['index']][tag][1]
                
    def replace(self, new_block, policy, modified_address):
        if(policy == 'lru'):
            block = self.lru_policy(modified_address)
        

        block = new_block
    
    