import math

class Cache:

    #miss_penalty = 0 #time to fetch_from cache to it's next level
    miss_count = 0
    #cache_lat = 0 #time taken to fetch from cache
    hit_count = 0
    #cache = {}

    def __init__(self,block_size,set_assoc,blocks,cache):
        self.block_size = block_size
        self.blocks = blocks
        self.set_assoc = set_assoc
        self.cache = cache
        
        #print(block_size)
        for i in range(int(blocks/set_assoc)):
            self.cache[i] = []
            for j in range(set_assoc):
                self.cache[i].append({})
                self.cache[i][j]['a'] = [0, [None]*self.block_size]
            
    def print_cache(self):
        for i in range(int(self.blocks/self.set_assoc)):
            print(i,self.cache[i])
        print('-----------------------------------')

    def store_cache(self):
        output = []
        output.append(int(self.blocks/self.set_assoc))
        output.append(self.set_assoc)
        output.append(self.block_size)
        for k in range(self.block_size):
            for i in range(int(self.blocks/self.set_assoc)):
                for j in range(self.set_assoc):
                    output.append([self.cache[i][j][next(iter(self.cache[i][j]))][0], self.cache[i][j][next(iter(self.cache[i][j]))][1][k]])
        
        return output

    def Cache_controller(self, address):
        address = '{:032b}'.format(address)
        #print(address)
        index_bits = int(math.log(self.blocks/self.set_assoc, 2))
        offset_bits = int(math.log(self.block_size, 2))
        return {'offset': int('0b'+ address[(len(address)-offset_bits):], 2),
                'index': int('0b' + address[(len(address)-(offset_bits + index_bits)): len(address)-offset_bits], 2), 
                'tag': int('0b' + address[:(len(address)-(offset_bits + index_bits))], 2)}

    def place_block(self, address, data):
        if(self.search(address)=={}):
            modified_address = self.Cache_controller(address)
            address = address - (address % self.block_size)
            temp = []
            count = 0
            while(count < self.block_size):
                # print(address, count, len(data['.word']))
                if(address + count >= len(data['.word'])):
                    temp.append('')
                else:
                    temp.append(data['.word'][address + count])
                count+=1

            valid = 0
            st = self.cache[modified_address['index']]
            for i in range(self.set_assoc):
                if(next(iter(st[i])) == 'a'):
                    valid = 1
                    c_bit = st[i]['a'][0]
                    st.pop(i)
                    tag = modified_address['tag']
                    st.insert(i,{tag:[c_bit,temp]})
                    # modifying LRU bits
                    self.modify_lrub(modified_address,i)
                    break

            if(valid == 0):
                policy = 'LRU'                       
                self.replace(temp, policy, modified_address)

    def search(self, address):
        modified_address = self.Cache_controller(address)
        st = self.cache[modified_address['index']]
        found = 0
        for i in range(self.set_assoc):
            #print(modified_address['tag'],next(iter(st[i])))
            if(modified_address['tag'] == next(iter(st[i]))):
                found = 1
                self.hit_count += 1
                # modifying LRU bits
                self.modify_lrub(modified_address,i)
                return st[i][modified_address['tag']][1][modified_address['offset']]

        if(found == 0):
            self.miss_count += 1
            return {}
    
    def write_through(self,address,value):
        modified_address = self.Cache_controller(address)
        st = self.cache[modified_address['index']]
        for i in range(self.set_assoc):
            tag = next(iter(st[i]))
            if(tag==modified_address['tag']):
                #print(st[i])
                st[i][tag][1][modified_address['offset']] = value
                self.modify_lrub(modified_address,i)
                break

    def lru_policy(self, modified_address):
        st = self.cache[modified_address['index']]
        maxi = 0
        key2 = next(iter(st[maxi]))
        for i in range(1,len(st)):
            key1 = next(iter(st[i]))
            key2 = next(iter(st[maxi]))
            if(st[maxi][key2][0]<st[i][key1][0]):
                maxi =  i
        return maxi
                
    def replace(self, new_block, policy, modified_address):
        block = []
        tag = modified_address['tag']
        st = self.cache[modified_address['index']]
        if(policy == 'LRU'):
            block_index = self.lru_policy(modified_address)
            #print(block_index)
            c_bit = st[block_index][next(iter(st[block_index]))][0]
            st.pop(block_index)
            st.insert(block_index,{tag:[c_bit,new_block]})
            # modifying LRU bits
            self.modify_lrub(modified_address,block_index)

    def modify_lrub(self,modified_address,index):
        # modifying LRU bit
        st = self.cache[modified_address['index']]
        var = st[index][modified_address['tag']][0]
        tag = modified_address['tag']
        #print(var)
        for j in range(self.set_assoc):
            if(next(iter(st[j]))==tag):
                st[j][next(iter(st[j]))][0] = 0
            elif(st[j][next(iter(st[j]))][0] <= var):
                st[j][next(iter(st[j]))][0] += 1
        # modified LRU bits