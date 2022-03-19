class Memory:
    def __init__(self, range_start_exl, range_end, total_memory_size):
        self.range_start_exl = range_start_exl
        self.range_end = range_end
        # Careful, this is the total gameboy memory size
        # Part of that bytearray will be empty
        self.memory = bytearray(total_memory_size)

    def is_adress_in_range(self, address16):
        if self.range_start_exl == None:
            return address16 <= self.range_end
        return address16 > self.range_start_exl and address16 <= self.range_end
    
    def is_writable(self):
        return False


class Ram(Memory):
    def read8(self, address16):
        return self.memory[address16]
    
    def write8(self, address16, data8):
        self.memory[address16] = data8
    
    def is_writable(self):
        return True


class Rom(Memory):
    def read8(self, address16):
        return self.memory[address16]
 
    def load(self, memory: bytearray):
        self.memory = memory