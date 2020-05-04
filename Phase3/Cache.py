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
            self.cache[i] = []
            for j in range(set_assoc):
                self.cache[i].append({})
                self.cache[i][j]['a'] = (0, ['']*block_size)
            

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

        valid = 0
        st = self.cache[modified_address['index']]
        for i in range(self.set_assoc):
            if(st[i].key() == 'a'):
                st[i][modified_address['tag']][1] = temp
                valid = 1
                break

        if(valid == 0):                       
            self.replace(temp, policy, modified_address)
    
    def search(self, modified_address, address):
        st = self.cache[modified_address['index']]
        found = 0
        for i in range(self.set_assoc):
            if(modified_address['tag'] == st[i].key()):
                found = 1
                return st[i][modified_address['tag']][1][modified_address['offset']]

        if(found == 0):
            self.miss_count += 1
            self.place_block(address, modified_address)
            return {}
    
    def write_value(self, value, modified_address, address):
        location = self.search(modified_address, address)
        if(location != {}):
            location = value                #either change or add the value at the exact location (using offset)
        else:
            self.place_block(address, modified_address)


    def write_block(self, address, modified_address):
        new_data = self.search(modified_address, address)
        # I think this new_data can never be empty as we will take care of it in new.py
        address = address - (address % self.block_size)
        data['.word'][address: address + self.block_size] = new_data

    def lru_policy(self, modified_address):
        
                
    def replace(self, new_block, policy, modified_address):
        if(policy == 'lru'):
            block = self.lru_policy(modified_address)
        

        block = new_block
    
    