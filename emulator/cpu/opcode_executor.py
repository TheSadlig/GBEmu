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
                    opcode_hex = int(row[2], 16)
                    opcode = Opcode(row[0], row[1], opcode_hex, int(row[3]))
                    self.opcodes[opcode_hex] = opcode
    
    # Executes the instruction and returns the number of cycles
    def execute(self, cpu: CPU, opc_hex: int):

        opcode = self.opcodes[opc_hex]
        print(opcode)
        if opcode.instruction == "LD":
            return OpcodeExecutor.LD8bits(cpu, opcode)
    
    # Switches 8 bits from one place to another and returns the number of cycles
    def LD8bits(cpu, opc: Opcode) -> int:
        opc.set_param1_value(cpu, opc.get_param2_value(cpu))
        return opc.cycles