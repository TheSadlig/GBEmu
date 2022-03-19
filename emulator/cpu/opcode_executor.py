import csv
from emulator.cpu.cpu import CPU
from emulator.cpu.opcode import Opcode

class OpcodeExecutor:
    def load_opcodes(self):
        self.opcodes = dict()
        with open('opcodes_list.csv', newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                if not row[0].startswith("#"):
                    opcode = Opcode(row[0], row[1], row[2], row[3])
                    self.opcodes[str(row[2])] = opcode
                    print(opcode)
            print(self.opcodes['0E'])
    
executor = OpcodeExecutor()
executor.load_opcodes()

for key_opc in executor.opcodes:
    cpu = CPU(10)
    cpu.memory.load_rom(0, bytearray("LD c,n", "UTF-8"))

    print(executor.opcodes[key_opc])
    print(executor.opcodes[key_opc].get_param2_value(cpu))
    print("=======")