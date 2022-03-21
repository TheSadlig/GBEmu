from emulator.cpu.cpu import CPU
from emulator.cpu.opcode import Opcode


class CommandsActions:
    def JP(cpu:CPU, opc: Opcode) -> int:
        # will contain 1 if we have to jump
        shouldJump = opc.get_param1_value(cpu)
        if shouldJump == 1:
            cpu.register.pc16 = opc.get_param2_value(cpu)

        return opc.cycles