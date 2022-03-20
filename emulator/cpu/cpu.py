from emulator.cpu.register import Register
from emulator.memory.memory_proxy import MemoryProxy

class CPU:
    def __init__(self, clock_speed):
        self.clock_speed = clock_speed
        self.register = Register()
        self.memory = MemoryProxy()
        self.clock_counter = 0
#        self.executor = OpcodeExecutor()

    def get_next_opcode(self):
        opcode = self.memory.read8(self.register.pc16)
        self.register.pc16 += 1
        return opcode

    def execute_next(self):
        inst = self.get_next_opcode()
#        self.executor.execute(self, inst)
    
    def run(self):
        i = 0
        max_loop = 100
        # Todo implement a real loop
        while i < max_loop:
            i += 1
            self.execute_next()

