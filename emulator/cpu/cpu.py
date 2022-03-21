from emulator.cpu.register import Register
from emulator.cpu.interrupts import Interrupts
from emulator.memory.memory_proxy import MemoryProxy

class CPU:
    def __init__(self, cartridge_bytes):
        self.register = Register()
        self.interrupts = Interrupts()
        self.memory = MemoryProxy()
        self.memory.load_cartridge(0x0, cartridge_bytes)
        self.clock_counter = 0

    def get_next_opcode(self):
        opcode = self.memory.read8(self.register.pc16)
        self.register.pc16 += 1
        return opcode

    def push_16bits_to_stack(self, data16: bytes) -> int:
        self.push_8bits_to_stack(data16 >> 8)
        self.push_8bits_to_stack(data16 & 0xFF)
        return self.register.sp16

    def push_8bits_to_stack(self, data8: bytes) -> int:
        self.memory.write8(self.register.sp16, data8)
        self.register.sp16 -= 1
        return self.register.sp16 

    def pop_8bits_from_stack(self) -> bytes:
        self.register.sp16 += 1
        return self.memory.read8(self.register.sp16)

    def pop_16bits_from_stack(self) -> bytes:
        low = self.pop_8bits_from_stack()
        high = self.pop_8bits_from_stack()
        return (high << 8) | low

    def run(self):
        i = 0
        max_loop = 100
        # Todo implement a real loop
        while i < max_loop:
            i += 1
            self.execute_next()

    def __str__(self) -> str:
        return "Register: \n"+str(self.register) + "\nInterrupts\n" + str(self.interrupts) + "\nMemory\n" + str(self.memory)
