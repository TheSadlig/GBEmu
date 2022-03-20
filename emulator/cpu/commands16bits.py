from emulator.cpu.cpu import CPU
from emulator.cpu.opcode import Opcode

class Commands16bits:
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
    def ADD16(cpu: CPU, opc: Opcode) -> int:
        value1 = opc.get_param1_value(cpu)
        value2 = opc.get_param2_value(cpu)
        opc.set_param1_value(cpu, Commands16bits._add_and_update_flags(cpu, value1, value2))

        return opc.cycles

    # Handles ADD
    def ADD16SP(cpu: CPU, opc: Opcode) -> int:
        Commands16bits.ADD16(cpu, opc)
        cpu.register.z1 = 0
        return opc.cycles

    def _add_and_update_flags(cpu: CPU, value1: bytes, value2: bytes) -> bytes:
        # TODO We may need to handle the #FFFF + 1 case, as it should loop back to 0 (won't here)
        addition = value1 + value2

        # setting flags
        cpu.register.n1 = 0
        cpu.register.h1 = 1 if Commands16bits.has12bitCarryOver(value1, value2) else 0
        cpu.register.cy1 = 1 if Commands16bits.has16bitCarryOver(value1, value2) else 0
        return addition

    # returns true of there is a half carry over
    def has12bitCarryOver(value1, value2) -> bool:
        return ((( value1 & 0xFFF) + (value2 & 0xFFF)) & 0x1000) == 0x1000

    # returns true of there is a carry over
    def has16bitCarryOver(value1, value2) -> bool:
        return ((( value1 & 0xFFFF) + (value2 & 0xFFFF)) & 0x10000) == 0x10000