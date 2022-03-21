from emulator.cpu.cpu import CPU
from emulator.cpu.opcode import Opcode
from emulator.tools.bit_tools import BitTools

class Commands16bits:

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

    # Handles INC
    def INC16(cpu: CPU, opc: Opcode) -> int:
        value1 = opc.get_param1_value(cpu)
        opc.set_param1_value(cpu, value1 + 1)
        return opc.cycles

    # Handles DEC
    def DEC16(cpu: CPU, opc: Opcode) -> int:
        value1 = opc.get_param1_value(cpu)
        opc.set_param1_value(cpu, value1 - 1)
        return opc.cycles

    def _add_and_update_flags(cpu: CPU, value1: bytes, value2: bytes) -> bytes:
        # TODO We may need to handle the #FFFF + 1 case, as it should loop back to 0 (won't here)
        addition = value1 + value2

        # setting flags
        cpu.register.n1 = 0
        cpu.register.h1 = 1 if BitTools.has12bitCarryOver(value1, value2) else 0
        cpu.register.cy1 = 1 if BitTools.has16bitCarryOver(value1, value2) else 0
        return addition