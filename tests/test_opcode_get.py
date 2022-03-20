import unittest

from emulator.cpu.cpu import CPU
from emulator.memory.memory_proxy import MemoryProxy
from emulator.cpu.opcode_executor import Opcode

class testOpCodeGet(unittest.TestCase):

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
        cpu.register.pc16 = testOpCodeGet.writtableMem

        return cpu

    # 8 bits immediate (retrieve from memory)
    def test_parameter2_retrieval_register_immediate8(self):
        opcode = Opcode("XX", "B,n", 'XX', 4)
        cpu = self.init_cpu()
        cpu.memory.write8(cpu.register.pc16, 0xF)
        cpu.memory.write8(cpu.register.pc16 + 1, 0xE)

        self.assertEqual(0xF, opcode.get_param2_value(cpu))
        self.assertEqual(testOpCodeGet.writtableMem + 1, cpu.register.pc16)
        
        self.assertEqual(0xE, opcode.get_param2_value(cpu))
        self.assertEqual(testOpCodeGet.writtableMem + 2, cpu.register.pc16)

    # 16 bits immediate (retrieve from memory)
    def test_parameter2_retrieval_register_immediate16(self):
        # this command will get the address in the immediate 16 bits
        # THEN copy the data present at this address to the B registry
        opcode = Opcode("XX", "B,(nn)", 'XX', 4)
        cpu = self.init_cpu()
        
        copiedAddress = testOpCodeGet.writtableMem + 10
        cpu.memory.write8(cpu.register.pc16, (copiedAddress & 0xFF00) >> 8)
        cpu.memory.write8(cpu.register.pc16 + 1, copiedAddress & 0x00FF)

        cpu.memory.write8(copiedAddress, 0x84)

        self.assertEqual(0x84, opcode.get_param2_value(cpu))
        self.assertEqual(testOpCodeGet.writtableMem + 2, cpu.register.pc16)

    # Retrieve from Address + register ($FF00+C)
    def test_parameter2_retrieval_address_register(self):
        opcode = Opcode("XX", "B,($FF00+C)", 'XX', 4)
        cpu = self.init_cpu()
        cpu.memory.write8(0xFF00 + 0x3, 0xAB)
        self.assertEqual(0xAB, opcode.get_param2_value(cpu))
        self.assertEqual(testOpCodeGet.writtableMem, cpu.register.pc16)
    
    # Simple registers:
    def test_parameter2_retrieval_registerA(self):
        opcode = Opcode("XX", "B,A", 'XX', 4)
        cpu = self.init_cpu()
        self.assertEqual(0x1, opcode.get_param2_value(cpu))
        self.assertEqual(testOpCodeGet.writtableMem, cpu.register.pc16)

    def test_parameter2_retrieval_registerB(self):
        opcode = Opcode("XX", "B,B", 'XX', 4)
        cpu = self.init_cpu()
        self.assertEqual(0x2, opcode.get_param2_value(cpu))
        self.assertEqual(testOpCodeGet.writtableMem, cpu.register.pc16)

    def test_parameter2_retrieval_registerC(self):
        opcode = Opcode("XX", "B,C", 'XX', 4)
        cpu = self.init_cpu()
        self.assertEqual(0x3, opcode.get_param2_value(cpu))
        self.assertEqual(testOpCodeGet.writtableMem, cpu.register.pc16)

        
    def test_parameter2_retrieval_registerD(self):
        opcode = Opcode("XX", "B,D", 'XX', 4)
        cpu = self.init_cpu()
        self.assertEqual(0x4, opcode.get_param2_value(cpu))
        self.assertEqual(testOpCodeGet.writtableMem, cpu.register.pc16)
        
    def test_parameter2_retrieval_registerE(self):
        opcode = Opcode("XX", "B,E", 'XX', 4)
        cpu = self.init_cpu()
        self.assertEqual(0x5, opcode.get_param2_value(cpu))
        self.assertEqual(testOpCodeGet.writtableMem, cpu.register.pc16)
        
    def test_parameter2_retrieval_registerF(self):
        opcode = Opcode("XX", "B,F", 'XX', 4)
        cpu = self.init_cpu()
        self.assertEqual(0x6, opcode.get_param2_value(cpu))
        self.assertEqual(testOpCodeGet.writtableMem, cpu.register.pc16)
        
    def test_parameter2_retrieval_registerH(self):
        opcode = Opcode("XX", "B,H", 'XX', 4)
        cpu = self.init_cpu()
        self.assertEqual(0x7, opcode.get_param2_value(cpu))
        self.assertEqual(testOpCodeGet.writtableMem, cpu.register.pc16)


    def test_parameter2_retrieval_registerL(self):
        opcode = Opcode("XX", "B,L", 'XX', 4)
        cpu = self.init_cpu()
        self.assertEqual(0x8, opcode.get_param2_value(cpu))
        self.assertEqual(testOpCodeGet.writtableMem, cpu.register.pc16)

    # Combined registers:
    def test_parameter2_retrieval_registerAF(self):
        opcode = Opcode("XX", "B,(AF)", 'XX', 4)
        cpu = self.init_cpu()
        
        cpu.register.af16 = testOpCodeGet.writtableMem
        cpu.memory.write8(cpu.register.af16, 0xAF)

        self.assertEqual(0xAF, opcode.get_param2_value(cpu))
        self.assertEqual(testOpCodeGet.writtableMem, cpu.register.pc16)

    def test_parameter2_retrieval_registerBC(self):
        opcode = Opcode("XX", "B,(BC)", 'XX', 4)
        cpu = self.init_cpu()

        cpu.register.bc16 = testOpCodeGet.writtableMem
        cpu.memory.write8(cpu.register.bc16, 0xAF)

        self.assertEqual(0xAF, opcode.get_param2_value(cpu))
        self.assertEqual(testOpCodeGet.writtableMem, cpu.register.pc16)

    def test_parameter2_retrieval_registerDE(self):
        opcode = Opcode("XX", "B,(DE)", 'XX', 4)
        cpu = self.init_cpu()

        cpu.register.de16 = testOpCodeGet.writtableMem
        cpu.memory.write8(cpu.register.de16, 0xAF)

        self.assertEqual(0xAF, opcode.get_param2_value(cpu))
        self.assertEqual(testOpCodeGet.writtableMem, cpu.register.pc16)

    def test_parameter2_retrieval_registerHL(self):
        opcode = Opcode("XX", "B,(HL)", 'XX', 4)
        cpu = self.init_cpu()

        cpu.register.hl16 = testOpCodeGet.writtableMem
        cpu.memory.write8(cpu.register.hl16, 0xAF)
        
        self.assertEqual(0xAF, opcode.get_param2_value(cpu))
        self.assertEqual(testOpCodeGet.writtableMem, cpu.register.pc16)


if __name__ == '__main__':
    unittest.main()