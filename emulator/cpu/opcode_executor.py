import csv
from xmlrpc.client import boolean
from emulator.cpu.cpu import CPU
from emulator.cpu.opcode import Opcode

class OpcodeExecutor:
    def load_opcodes(self):
        self.opcodes = dict()
        with open('opcodes_list.csv', newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) > 0 and not row[0].startswith("#"):
                    opcode_hex = int(row[2], 16)
                    opcode = Opcode(row[0], row[1], opcode_hex, int(row[3]))
                    self.opcodes[opcode_hex] = opcode
    
    # Executes the instruction and returns the number of cycles
    def execute(self, cpu: CPU, opc_hex: int):

        opcode = self.opcodes[opc_hex]
        print(opcode)
        if opcode.instruction == "LD":
            return OpcodeExecutor.LD8bits(cpu, opcode)
        elif opcode.instruction == "LDD":
            return OpcodeExecutor.LDD8bits(cpu, opcode)
        elif opcode.instruction == "LDI":
            return OpcodeExecutor.LDI8bits(cpu, opcode)
        elif opcode.instruction == "LDHL":
            return OpcodeExecutor.LDHL8bits(cpu, opcode)

    # Switches 8 bits from one place to another and returns the number of cycles
    def LD8bits(cpu, opc: Opcode) -> int:
        opc.set_param1_value(cpu, opc.get_param2_value(cpu))
        return opc.cycles

    # Handles `LDD (HL),A` and `LDD A,(HL)`
    def LDD8bits(cpu: CPU, opc: Opcode) -> int:
        opc.set_param1_value(cpu, opc.get_param2_value(cpu))
        # no matter the order, we want to decrement HL
        cpu.register.hl16 -= 1
        return opc.cycles
    
    # Handles `LDI (HL),A` and `LDI A,(HL)`
    def LDI8bits(cpu: CPU, opc: Opcode) -> int:
        opc.set_param1_value(cpu, opc.get_param2_value(cpu))
        # no matter the order, we want to decrement HL
        cpu.register.hl16 += 1
        return opc.cycles

    # Handles `LDHL SP,n`
    def LDHL8bits(cpu: CPU, opc: Opcode) -> int:
        immediateValue = opc.get_param2_value(cpu)
        spValue = cpu.register.sp16
        hlValue = immediateValue + spValue 
        opc.set_param1_value(cpu, opc.get_param2_value(cpu))
        # no matter the order, we want to decrement HL
        cpu.register.hl16 = hlValue
        cpu.register.z1 = 0
        cpu.register.n1 = 0
        cpu.register.h1 = 1 if OpcodeExecutor.hasHalfCarryOver(immediateValue, spValue) else 0
        cpu.register.cy1 = 1 if OpcodeExecutor.hasCarryOver(immediateValue, spValue) else 0
        return opc.cycles

    # returns true of there is a half carry over
    def hasHalfCarryOver(value1, value2) -> boolean:
        return ((( value1 & 0xf) + (value2 & 0xf)) & 0x10) == 0x10
    
    # returns true of there is a carry over
    def hasCarryOver(value1, value2) -> boolean:
        return ((( value1 & 0xFF) + (value2 & 0xFF)) & 0x100) == 0x100