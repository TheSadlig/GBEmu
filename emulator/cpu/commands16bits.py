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
