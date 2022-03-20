from audioop import add
from emulator.cpu.commands8bits import Commands8bits
from emulator.cpu.cpu import CPU
from emulator.cpu.opcode_executor import OpcodeExecutor
import unittest

from emulator.memory.memory_proxy import MemoryProxy
from emulator.tools.bit_tools import BitTools

class testOpCodeExecutorLD(unittest.TestCase):
    
    writtableMem = MemoryProxy.VRAM_END
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
        # For testing we need to be in a writtable part of the memory
        cpu.register.pc16 = testOpCodeExecutorLD.writtableMem

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

    def testLDfromRegisterAddress(self):
        cpu = self.init_cpu()
        
        address = testOpCodeExecutorLD.writtableMem + 10
        cpu.register.hl16 = address
        cpu.memory.write8(address, 0xBD)

        executor = OpcodeExecutor()
        executor.load_opcodes()
        # LD,"A,(HL)",0x7E,8
        cycles = executor.execute(cpu, 0x7E)
        self.assertEqual(cpu.register.hl16, address)
        self.assertEqual(cpu.register.a8, 0xBD)
        self.assertEqual(cycles, 8)
        
    def testLDtoRegisterAddress(self):
        cpu = self.init_cpu()

        address = testOpCodeExecutorLD.writtableMem
        cpu.register.hl16 = address
        cpu.memory.write8(address, 0xED)

        executor = OpcodeExecutor()
        executor.load_opcodes()
        # LD,"(HL),A",0x77,8
        cycles = executor.execute(cpu, 0x77)
        self.assertEqual(cpu.memory.read8(address), cpu.register.a8)
        self.assertEqual(cycles, 8)
        
    def testLDfromImmediate(self):
        cpu = self.init_cpu()

        cpu.memory.write8(cpu.register.pc16, 0xBF)

        executor = OpcodeExecutor()
        executor.load_opcodes()
        # copy from the immediate byte to register B
        # LD,"B,n",0x06,8
        cycles = executor.execute(cpu, 0x06)
        self.assertEqual(cpu.register.b8, 0xBF)
        self.assertEqual(cpu.register.pc16, testOpCodeExecutorLD.writtableMem + 1)
        self.assertEqual(cycles, 8)

    def testADD(self):
        cpu = self.init_cpu()

        executor = OpcodeExecutor()
        executor.load_opcodes()
        # ADD,"A,B",0x80,4
        cycles = executor.execute(cpu, 0x80)
        self.assertEqual(cpu.register.a8, 0x3)
        self.assertEqual(cpu.register.b8, 0x2)
        self.assertEqual(cpu.register.pc16, testOpCodeExecutorLD.writtableMem)
        self.assertEqual(cpu.register.z1, 0)
        self.assertEqual(cpu.register.n1, 0)
        self.assertEqual(cpu.register.h1, 0)
        self.assertEqual(cpu.register.cy1, 0)
        self.assertEqual(cycles, 4)

    def testSWAP(self):
        cpu = self.init_cpu()

        executor = OpcodeExecutor()
        executor.load_opcodes()
        # SWAP,"A,A",0xCB37,8
        cpu.register.a8 = 0b01101001
        cycles = executor.execute(cpu, 0xCB37)

        self.assertEqual(cpu.register.a8, 0b10010110)
        self.assertEqual(cycles, 8)

    def testBIT(self):
        cpu = self.init_cpu()

        executor = OpcodeExecutor()
        executor.load_opcodes()
        cpu.register.c8 = 0b00000010
        # BIT,"1,C",0xCB49,8
        executor.execute(cpu, 0xCB49)

        self.assertEqual(cpu.register.z1, 0b0)

        cpu.register.c8 = 0b11111101

        cycles = executor.execute(cpu, 0xCB49)
        print("wtf"+ str(cpu.register.z1))

        self.assertEqual(cpu.register.z1, 0b1)
        self.assertEqual(cycles, 8)

    def testHas4bitCarryOver(self):
        self.assertTrue(BitTools.has4bitCarryOver(0xF, 0x1))
        self.assertTrue(BitTools.has4bitCarryOver(0xA, 0x8))

        self.assertFalse(BitTools.has4bitCarryOver(0x5, 0x1))
        self.assertFalse(BitTools.has4bitCarryOver(0xA, 0x4))
        self.assertFalse(BitTools.has4bitCarryOver(0xF, 0x0))
        
    def testHas8bitCarryOver(self):
        self.assertTrue(BitTools.has8bitCarryOver(0xFF, 0x01))
        self.assertTrue(BitTools.has8bitCarryOver(0xFF, 0xFF))
        
        self.assertFalse(BitTools.has8bitCarryOver(0xAF, 0x41))
        self.assertFalse(BitTools.has8bitCarryOver(0xF, 0x01))
        self.assertFalse(BitTools.has8bitCarryOver(0x05, 0x01))
        self.assertFalse(BitTools.has8bitCarryOver(0xAF, 0x40))
        self.assertFalse(BitTools.has8bitCarryOver(0xFF, 0x00))
        

if __name__ == '__main__':
    unittest.main()      