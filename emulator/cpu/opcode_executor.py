import csv
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
            return OpcodeExecutor.LD(cpu, opcode)
        elif opcode.instruction == "LDD":
            return OpcodeExecutor.LDD(cpu, opcode)
        elif opcode.instruction == "LDI":
            return OpcodeExecutor.LDI(cpu, opcode)
        elif opcode.instruction == "LDHL":
            return OpcodeExecutor.LDHL(cpu, opcode)
        elif opcode.instruction == "PUSH":
            return OpcodeExecutor.PUSH(cpu, opcode)
        elif opcode.instruction == "POP":
            return OpcodeExecutor.POP(cpu, opcode)
        elif opcode.instruction == "ADD":
            return OpcodeExecutor.ADD(cpu, opcode)
        elif opcode.instruction == "ADC":
            return OpcodeExecutor.ADC(cpu, opcode)
        elif opcode.instruction == "SUB":
            return OpcodeExecutor.SUB(cpu, opcode)

    # Loads from one place to another and returns the number of cycles
    def LD(cpu, opc: Opcode) -> int:
        opc.set_param1_value(cpu, opc.get_param2_value(cpu))
        return opc.cycles

    # Handles `LDD (HL),A` and `LDD A,(HL)`
    def LDD(cpu: CPU, opc: Opcode) -> int:
        opc.set_param1_value(cpu, opc.get_param2_value(cpu))
        # no matter the order, we want to decrement HL
        cpu.register.hl16 -= 1
        return opc.cycles
    
    # Handles `LDI (HL),A` and `LDI A,(HL)`
    def LDI(cpu: CPU, opc: Opcode) -> int:
        opc.set_param1_value(cpu, opc.get_param2_value(cpu))
        # no matter the order, we want to decrement HL
        cpu.register.hl16 += 1
        return opc.cycles

    # Handles `LDHL SP,n`
    def LDHL(cpu: CPU, opc: Opcode) -> int:
        immediateValue = opc.get_param2_value(cpu)
        spValue = cpu.register.sp16
        hlValue = immediateValue + spValue 
        opc.set_param1_value(cpu, opc.get_param2_value(cpu))
        # no matter the order, we want to decrement HL
        cpu.register.hl16 = hlValue
        cpu.register.z1 = 0
        cpu.register.n1 = 0
        cpu.register.h1 = 1 if OpcodeExecutor.has4bitCarryOver(immediateValue, spValue) else 0
        cpu.register.cy1 = 1 if OpcodeExecutor.has8bitCarryOver(immediateValue, spValue) else 0
        return opc.cycles

    # Handles PUSH
    def PUSH(cpu: CPU, opc: Opcode) -> int:
        value = opc.get_param2_value(cpu)
        cpu.memory.write8(cpu.register.sp16, (value & 0xFF00) >> 8)
        cpu.register.sp16 -= 1
        cpu.memory.write8(cpu.register.sp16, (value & 0xFF))
        cpu.register.sp16 -= 1
        return opc.cycles

    # Handles POP
    def POP(cpu: CPU, opc: Opcode) -> int:
        value = opc.get_param2_value(cpu)
        cpu.register.sp16 += 1
        cpu.memory.write8(cpu.register.sp16, 0x0)
        cpu.register.sp16 += 1
        cpu.memory.write8(cpu.register.sp16, 0x0)
        return opc.cycles

    # Handles ADD
    def ADD(cpu: CPU, opc: Opcode) -> int:
        value1 = opc.get_param1_value(cpu)
        value2 = opc.get_param2_value(cpu)
        opc.set_param1_value(cpu, OpcodeExecutor._add_and_update_flags(cpu, value1, value2))

        return opc.cycles

    # Handles ADC (also adds the carry flag)
    def ADC(cpu: CPU, opc: Opcode) -> int:
        value1 = opc.get_param1_value(cpu)
        value2 = opc.get_param2_value(cpu)
        opc.set_param1_value(cpu, OpcodeExecutor._add_and_update_flags(cpu, value1, value2 + cpu.register.cy1))

        return opc.cycles

    # Handles SUB
    def SUB(cpu: CPU, opc: Opcode) -> int:
        value1 = opc.get_param1_value(cpu)
        value2 = opc.get_param2_value(cpu)
        opc.set_param1_value(cpu, OpcodeExecutor._sub_and_update_flags(cpu, value1, value2))

        return opc.cycles

    # Handles SBC (also substracts the carry flag)
    def SBC(cpu: CPU, opc: Opcode) -> int:
        value1 = opc.get_param1_value(cpu)
        value2 = opc.get_param2_value(cpu)
        opc.set_param1_value(cpu, OpcodeExecutor._sub_and_update_flags(cpu, value1, value2 + cpu.register.cy1))

        return opc.cycles

    def _add_and_update_flags(cpu: CPU, value1: bytes, value2: bytes) -> bytes:
        # TODO We may need to handle the #FFFF + 1 case, as it loop back to 0 (won't here)
        addition = value1 + value2

        # setting flags
        cpu.register.z1 = 1 if addition == 0 else 0
        cpu.register.n1 = 0
        cpu.register.h1 = 1 if OpcodeExecutor.has4bitCarryOver(value1, value2) else 0
        cpu.register.cy1 = 1 if OpcodeExecutor.has8bitCarryOver(value1, value2) else 0
        return addition

    def _sub_and_update_flags(cpu: CPU, value1: bytes, value2: bytes) -> bytes:
        sub = value1 - value2

        # setting flags
        cpu.register.z1 = 1 if sub == 0 else 0
        cpu.register.n1 = 1
        cpu.register.h1 = 1 if OpcodeExecutor.has4bitBorrow(value1, value2) else 0
        cpu.register.cy1 = 1 if OpcodeExecutor.has8bitBorrow(value1, value2) else 0
        return sub

    # returns true of there is a half carry over
    def has4bitCarryOver(value1, value2) -> bool:
        return ((( value1 & 0xf) + (value2 & 0xf)) & 0x10) == 0x10
    
    # returns true of there is a carry over
    def has8bitCarryOver(value1, value2) -> bool:
        return ((( value1 & 0xFF) + (value2 & 0xFF)) & 0x100) == 0x100

    # returns true if in value1 - value 2, value2 > value 1 for 4 bits
    def has4bitBorrow(value1, value2) -> bool:
        return (value2  & 0xFF) > (value1 & 0xFF)

    # returns true if in value1 - value 2, value2 > value 1 for 8 bits
    def has8bitBorrow(value1, value2) -> bool:
        return (value2  & 0xFFFF) > (value1 & 0xFFFF)
