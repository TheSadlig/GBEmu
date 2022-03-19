import unittest

from emulator.cpu.cpu import CPU
from emulator.memory.memory_proxy import MemoryProxy
from emulator.cpu.opcode_executor import Opcode

class testOpCodeGet(unittest.TestCase):
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

    # 8 bits immediate (retrieve from memory)
    def test_parameter2_retrieval_register_immediate8(self):
        opcode = Opcode("XX", "B,(n)", 'XX', 4)
        cpu = self.init_cpu()
        self.assertEqual(0xF, opcode.get_param2_value(cpu))
        self.assertEqual(1, cpu.register.pc16)
        
        self.assertEqual(0xE, opcode.get_param2_value(cpu))
        self.assertEqual(2, cpu.register.pc16)

    # 16 bits immediate (retrieve from memory)
    def test_parameter2_retrieval_register_immediate16(self):
        opcode = Opcode("XX", "B,(nn)", 'XX', 4)
        cpu = self.init_cpu()
        self.assertEqual(0x0F0E, opcode.get_param2_value(cpu))
        self.assertEqual(2, cpu.register.pc16)
        self.assertEqual(0x0D0C, opcode.get_param2_value(cpu))
        self.assertEqual(4, cpu.register.pc16)

    # Retrieve from Address + register ($FF00+C)
    def test_parameter2_retrieval_address_register(self):
        opcode = Opcode("XX", "B,($FF00+C)", 'XX', 4)
        cpu = self.init_cpu()
        cpu.memory.write8(0xFF00 + 0x3, 0xAB)
        self.assertEqual(0xAB, opcode.get_param2_value(cpu))
        self.assertEqual(0, cpu.register.pc16)
    
    # Simple registers:
    def test_parameter2_retrieval_registerA(self):
        opcode = Opcode("XX", "B,A", 'XX', 4)
        cpu = self.init_cpu()
        self.assertEqual(0x1, opcode.get_param2_value(cpu))
        self.assertEqual(0, cpu.register.pc16)

    def test_parameter2_retrieval_registerB(self):
        opcode = Opcode("XX", "B,B", 'XX', 4)
        cpu = self.init_cpu()
        self.assertEqual(0x2, opcode.get_param2_value(cpu))
        self.assertEqual(0, cpu.register.pc16)

    def test_parameter2_retrieval_registerC(self):
        opcode = Opcode("XX", "B,C", 'XX', 4)
        cpu = self.init_cpu()
        self.assertEqual(0x3, opcode.get_param2_value(cpu))
        self.assertEqual(0, cpu.register.pc16)

        
    def test_parameter2_retrieval_registerD(self):
        opcode = Opcode("XX", "B,D", 'XX', 4)
        cpu = self.init_cpu()
        self.assertEqual(0x4, opcode.get_param2_value(cpu))
        self.assertEqual(0, cpu.register.pc16)
        
    def test_parameter2_retrieval_registerE(self):
        opcode = Opcode("XX", "B,E", 'XX', 4)
        cpu = self.init_cpu()
        self.assertEqual(0x5, opcode.get_param2_value(cpu))
        self.assertEqual(0, cpu.register.pc16)
        
    def test_parameter2_retrieval_registerF(self):
        opcode = Opcode("XX", "B,F", 'XX', 4)
        cpu = self.init_cpu()
        self.assertEqual(0x6, opcode.get_param2_value(cpu))
        self.assertEqual(0, cpu.register.pc16)
        
    def test_parameter2_retrieval_registerH(self):
        opcode = Opcode("XX", "B,H", 'XX', 4)
        cpu = self.init_cpu()
        self.assertEqual(0x7, opcode.get_param2_value(cpu))
        self.assertEqual(0, cpu.register.pc16)


    def test_parameter2_retrieval_registerL(self):
        opcode = Opcode("XX", "B,L", 'XX', 4)
        cpu = self.init_cpu()
        self.assertEqual(0x8, opcode.get_param2_value(cpu))
        self.assertEqual(0, cpu.register.pc16)

    # Combined registers:
    def test_parameter2_retrieval_registerAF(self):
        opcode = Opcode("XX", "B,(AF)", 'XX', 4)
        cpu = self.init_cpu()
        self.assertEqual(cpu.register.af16, opcode.get_param2_value(cpu))
        self.assertEqual(0, cpu.register.pc16)

    def test_parameter2_retrieval_registerBC(self):
        opcode = Opcode("XX", "B,(BC)", 'XX', 4)
        cpu = self.init_cpu()
        self.assertEqual(cpu.register.bc16, opcode.get_param2_value(cpu))
        self.assertEqual(0, cpu.register.pc16)

    def test_parameter2_retrieval_registerDE(self):
        opcode = Opcode("XX", "B,(DE)", 'XX', 4)
        cpu = self.init_cpu()
        self.assertEqual(cpu.register.de16, opcode.get_param2_value(cpu))
        self.assertEqual(0, cpu.register.pc16)

    def test_parameter2_retrieval_registerHL(self):
        opcode = Opcode("XX", "B,(HL)", 'XX', 4)
        cpu = self.init_cpu()
        self.assertEqual(cpu.register.hl16, opcode.get_param2_value(cpu))
        self.assertEqual(0, cpu.register.pc16)


if __name__ == '__main__':
    unittest.main()        
        
