from emulator.cpu.cpu import CPU
from emulator.cpu.opcode_executor import OpcodeExecutor
import unittest

from emulator.memory.memory_proxy import MemoryProxy

class testOpCodeExecutorLD(unittest.TestCase):
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
        # LD,"A,B",0x78,4
        cycles = executor.execute(cpu, 0x78)
        self.assertEqual(cpu.register.a8, 0x2)
        self.assertEqual(cpu.register.b8, 0x2)
        self.assertEqual(cycles, 4)

    def testLDsameRegister(self):
        cpu = self.init_cpu()
        executor = OpcodeExecutor()
        executor.load_opcodes()
        # LD,"A,A",0x7F,4
        cycles = executor.execute(cpu, 0x7F)
        self.assertEqual(cpu.register.a8, 0x1)
        self.assertEqual(cycles, 4)

    def testLDfromcombinedRegister(self):
        cpu = self.init_cpu()
        executor = OpcodeExecutor()
        executor.load_opcodes()
        # LD,"A,(HL)",0x7E,8
        cycles = executor.execute(cpu, 0x7E)
        self.assertEqual(cpu.register.hl16, 0x0708)
        self.assertEqual(cpu.register.a8, 0x08)
        self.assertEqual(cycles, 8)

    def testLDtocombinedRegister(self):
        cpu = self.init_cpu()
        executor = OpcodeExecutor()
        executor.load_opcodes()
        # LD,"(HL),A",0x77,8
        cycles = executor.execute(cpu, 0x77)
        self.assertEqual(cpu.register.a8, 0x01)
        self.assertEqual(cpu.register.hl16, 0x01)
        self.assertEqual(cycles, 8)
        
    def testLDtocombinedRegister(self):
        cpu = self.init_cpu()
        executor = OpcodeExecutor()
        executor.load_opcodes()
        # LD,"(HL),A",0x77,8
        cycles = executor.execute(cpu, 0x77)
        self.assertEqual(cpu.register.a8, 0x01)
        self.assertEqual(cpu.register.hl16, 0x01)
        self.assertEqual(cycles, 8)
        
    def testLDtocombinedRegister(self):
        cpu = self.init_cpu()
        executor = OpcodeExecutor()
        executor.load_opcodes()
        # copy from the memory to register B
        # LD,"B,n",0x06,8
        cycles = executor.execute(cpu, 0x06)
        self.assertEqual(cpu.register.b8, 0x0F)
        self.assertEqual(cpu.register.pc16, 1)
        self.assertEqual(cycles, 8)

if __name__ == '__main__':
    unittest.main()      