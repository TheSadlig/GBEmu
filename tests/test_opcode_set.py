from atexit import register
import unittest

from emulator.cpu.cpu import CPU
from emulator.memory.memory_proxy import MemoryProxy
from emulator.cpu.opcode_executor import Opcode

class testOpCodeSet(unittest.TestCase):

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
        cpu.register.pc16 = testOpCodeSet.writtableMem

        return cpu
    
    # Write to Address + register ($FF00+C)
    def test_parameter1_write_address_register(self):
        opcode = Opcode("XX", "($FF00+C),B", 'XX', 4)
        cpu = self.init_cpu()
        opcode.set_param1_value(cpu, 0xAB)

        expectedAddress = 0xFF00 + cpu.register.c8
        self.assertEqual(0xAB, cpu.memory.read8(expectedAddress))
        self.assertEqual(testOpCodeSet.writtableMem, cpu.register.pc16)

    # Simple registers:
    def test_parameter1_set_registerA(self):
        opcode = Opcode("XX", "A,B", 'XX', 4)
        cpu = self.init_cpu()
        opcode.set_param1_value(cpu, 0xF)
        self.assertEqual(cpu.register.a8, 0xF)
        self.assertEqual(testOpCodeSet.writtableMem, cpu.register.pc16)

    def test_parameter1_set_registerB(self):
        opcode = Opcode("XX", "B,B", 'XX', 4)
        cpu = self.init_cpu()
        opcode.set_param1_value(cpu, 0xF)
        self.assertEqual(cpu.register.b8, 0xF)
        self.assertEqual(testOpCodeSet.writtableMem, cpu.register.pc16)

    def test_parameter1_set_registerC(self):
        opcode = Opcode("XX", "C,B", 'XX', 4)
        cpu = self.init_cpu()
        opcode.set_param1_value(cpu, 0xF)
        self.assertEqual(cpu.register.c8, 0xF)
        self.assertEqual(testOpCodeSet.writtableMem, cpu.register.pc16)

    def test_parameter1_set_registerD(self):
        opcode = Opcode("XX", "D,B", 'XX', 4)
        cpu = self.init_cpu()
        opcode.set_param1_value(cpu, 0xF)
        self.assertEqual(cpu.register.d8, 0xF)
        self.assertEqual(testOpCodeSet.writtableMem, cpu.register.pc16)

    def test_parameter1_set_registerE(self):
        opcode = Opcode("XX", "E", 'XX', 4)
        cpu = self.init_cpu()
        opcode.set_param1_value(cpu, 0xF)
        self.assertEqual(cpu.register.e8, 0xF)
        self.assertEqual(testOpCodeSet.writtableMem, cpu.register.pc16)

    def test_parameter1_set_registerF(self):
        opcode = Opcode("XX", "F,B", 'XX', 4)
        cpu = self.init_cpu()
        opcode.set_param1_value(cpu, 0xF)
        self.assertEqual(cpu.register.f8, 0xF)
        self.assertEqual(testOpCodeSet.writtableMem, cpu.register.pc16)

    def test_parameter1_set_registerH(self):
        opcode = Opcode("XX", "H,B", 'XX', 4)
        cpu = self.init_cpu()
        opcode.set_param1_value(cpu, 0xF)
        self.assertEqual(cpu.register.h8, 0xF)
        self.assertEqual(testOpCodeSet.writtableMem, cpu.register.pc16)

    def test_parameter1_set_registerL(self):
        opcode = Opcode("XX", "L,B", 'XX', 4)
        cpu = self.init_cpu()
        opcode.set_param1_value(cpu, 0xF)
        self.assertEqual(cpu.register.l8, 0xF)
        self.assertEqual(testOpCodeSet.writtableMem, cpu.register.pc16)

    # Combined registers:
    def test_parameter1_set_registerAF(self):
        opcode = Opcode("XX", "(AF),B", 'XX', 4)
        cpu = self.init_cpu()
        address = testOpCodeSet.writtableMem + 10
        cpu.register.af16 = address

        opcode.set_param1_value(cpu, 0xF)
        
        self.assertEqual(cpu.register.af16, address)
        self.assertEqual(cpu.memory.read8(address), 0xF)
    

    def test_parameter1_set_registerBC(self):
        opcode = Opcode("XX", "(BC),B", 'XX', 4)
        cpu = self.init_cpu()
        address = testOpCodeSet.writtableMem + 10
        cpu.register.bc16 = address

        opcode.set_param1_value(cpu, 0xF)
        
        self.assertEqual(cpu.register.bc16, address)
        self.assertEqual(cpu.memory.read8(address), 0xF)
    
    def test_parameter1_set_registerDE(self):
        opcode = Opcode("XX", "(DE),B", 'XX', 4)
        cpu = self.init_cpu()
        address = testOpCodeSet.writtableMem + 10
        cpu.register.de16 = address

        opcode.set_param1_value(cpu, 0xF)
        
        self.assertEqual(cpu.register.de16, address)
        self.assertEqual(cpu.memory.read8(address), 0xF)
        
    def test_parameter1_set_registerHL(self):
        opcode = Opcode("XX", "(HL),B", 'XX', 4)
        cpu = self.init_cpu()
        address = testOpCodeSet.writtableMem + 10
        cpu.register.hl16 = address

        opcode.set_param1_value(cpu, 0xF)
        
        self.assertEqual(cpu.register.hl16, address)
        self.assertEqual(cpu.memory.read8(address), 0xF)

if __name__ == '__main__':
    unittest.main()        
        
