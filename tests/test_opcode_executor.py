from emulator.cpu.cpu import CPU
from emulator.cpu.opcode_executor import OpcodeExecutor
import unittest

from emulator.memory.memory_proxy import MemoryProxy

class testOpCodeExecutor(unittest.TestCase):
    def init_cpu(self) -> CPU:
        cpu = CPU(1)
        cpu.register.a8 = 0x1
        cpu.register.b8 = 0x2
        cpu.register.c8 = 0x3
        cpu.register.d8 = 0x4
        cpu.register.e8 = 0x5
        cpu.register.f8 = 0x6
        cpu.register.h8 = 0x7
        cpu.register.l8 = 0x8
        cpu.register.sp16 = MemoryProxy.HRAM_END
        cpu.register.pc16 = 0x0

        cpu.memory.load_rom(0, bytearray([0x0F,0x0E,0x0D,0x0C]))
        return cpu
    
    def testLDsimpleRegister(self):
        cpu = self.init_cpu()
        executor = OpcodeExecutor()
        executor.load_opcodes()
        # Copy reg B in reg A
        # LD,"A,B",0x78,4
        cycles = executor.execute(cpu, 0x78)
        self.assertEqual(cpu.register.a8, 0x2)
        self.assertEqual(cpu.register.b8, 0x2)
        self.assertEqual(cycles, 4)

    def testLDsameRegister(self):
        cpu = self.init_cpu()
        executor = OpcodeExecutor()
        executor.load_opcodes()
        # Copy reg A in reg A
        # LD,"A,A",0x7F,4
        cycles = executor.execute(cpu, 0x7F)
        self.assertEqual(cpu.register.a8, 0x1)
        self.assertEqual(cycles, 4)

if __name__ == '__main__':
    unittest.main()      