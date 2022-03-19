from emulator.cpu.cpu import CPU
from emulator.cpu.opcode_executor import OpcodeExecutor
import unittest

class testOpCodeExecutor(unittest.TestCase):
    def test_parameter2_retrieval(self):
        executor = OpcodeExecutor()
        executor.load_opcodes()
        for key_opc in executor.opcodes:
            cpu = CPU(10)
            cpu.memory.load_rom(0, bytearray("LD c,n", "UTF-8"))

            print(executor.opcodes[key_opc])
            print(executor.opcodes[key_opc].get_param2_value(cpu))
            print("=======")
