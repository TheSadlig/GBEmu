from emulator.cpu.cpu import CPU
from emulator.cpu.opcode import Opcode


class CommandsActions:

    # Handles PUSH
    def PUSH(cpu: CPU, opc: Opcode) -> int:
        value = opc.get_param2_value(cpu)
        cpu.push_8bits_to_stack((value | 0xFF00) >> 8)
        cpu.push_8bits_to_stack(value | 0xFF)
        return opc.cycles

    # Handles POP
    def POP(cpu: CPU, opc: Opcode) -> int:
        opc.set_param1_value(cpu.pop_16bits_from_stack())
        return opc.cycles

    def JP(cpu:CPU, opc: Opcode) -> int:
        # will contain 1 if we have to jump
        shouldJump = opc.get_param1_value(cpu)
        if shouldJump == 1:
            cpu.register.pc16 = opc.get_param2_value(cpu)

        return opc.cycles
        
    def JR(cpu:CPU, opc: Opcode) -> int:
        #   will contain 1 if we have to jump
        shouldJump = opc.get_param1_value(cpu)
        if shouldJump == 1:
            add_to_address = opc.get_param2_value(cpu)
            cpu.register.pc16 = opc.get_param2_value(cpu) + add_to_address

        return opc.cycles

    def CALL(cpu:CPU, opc: Opcode) -> int:
        shouldCall = opc.get_param1_value(cpu)
        if shouldCall == 1:
            jumpAddress = opc.get_param2_value(cpu)
            nextAddress = cpu.register.pc16 + 1
            cpu.push_16bits_to_stack(nextAddress)
            cpu.register.pc16 = jumpAddress
        return opc.cycles

    def RST(cpu:CPU, opc: Opcode) -> int:
        jumpAddress = opc.get_param2_value(cpu)
        cpu.push_16bits_to_stack(cpu.register.pc16)
        cpu.register.pc16 = jumpAddress # $0000 + n
        return opc.cycles

    def RET(cpu:CPU, opc: Opcode) -> int:
        shouldJump = opc.get_param1_value(cpu)
        if (shouldJump):
            jumpAddress = cpu.pop_16bits_from_stack()
            cpu.register.pc16 = jumpAddress
        return opc.cycles
