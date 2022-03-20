from emulator.cpu.cpu import CPU
from emulator.cpu.opcode import Opcode

class Commands8bits:
    # Loads from one place to another and returns the number of cycles
    def LD(cpu:CPU, opc: Opcode) -> int:
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
        # no matter the order, we want to increment HL
        cpu.register.hl16 += 1
        return opc.cycles

    # Handles `LDHL SP,n`
    # This should be a 16 bits, but the behaviour on flags is closer to 8 bits
    def LDHL(cpu: CPU, opc: Opcode) -> int:
        immediateValue = opc.get_param2_value(cpu)
        spValue = cpu.register.sp16
        hlValue = immediateValue + spValue 
        opc.set_param1_value(cpu, opc.get_param2_value(cpu))

        cpu.register.hl16 = hlValue
        cpu.register.z1 = 0
        cpu.register.n1 = 0
        cpu.register.h1 = 1 if Commands8bits.has4bitCarryOver(immediateValue, spValue) else 0
        cpu.register.cy1 = 1 if Commands8bits.has8bitCarryOver(immediateValue, spValue) else 0
        return opc.cycles

    # Handles ADD
    def ADD(cpu: CPU, opc: Opcode) -> int:
        value1 = opc.get_param1_value(cpu)
        value2 = opc.get_param2_value(cpu)
        opc.set_param1_value(cpu, Commands8bits._add_and_update_flags(cpu, value1, value2))

        return opc.cycles

    # Handles ADC (also adds the carry flag)
    def ADC(cpu: CPU, opc: Opcode) -> int:
        value1 = opc.get_param1_value(cpu)
        value2 = opc.get_param2_value(cpu)
        opc.set_param1_value(cpu, Commands8bits._add_and_update_flags(cpu, value1, value2 + cpu.register.cy1))

        return opc.cycles

    # Handles SUB
    def SUB(cpu: CPU, opc: Opcode) -> int:
        value1 = opc.get_param1_value(cpu)
        value2 = opc.get_param2_value(cpu)
        opc.set_param1_value(cpu, Commands8bits._sub_and_update_flags(cpu, value1, value2))

        return opc.cycles

    # Handles SBC (also substracts the carry flag)
    def SBC(cpu: CPU, opc: Opcode) -> int:
        value1 = opc.get_param1_value(cpu)
        value2 = opc.get_param2_value(cpu)
        opc.set_param1_value(cpu, Commands8bits._sub_and_update_flags(cpu, value1, value2 + cpu.register.cy1))

        return opc.cycles

    # Handles AND
    def AND(cpu: CPU, opc: Opcode) -> int:
        value1 = opc.get_param1_value(cpu)
        value2 = opc.get_param2_value(cpu)
        res = value1 & value2 
        opc.set_param1_value(cpu, res)
        
        cpu.register.z1 = 1 if res == 0 else 0
        cpu.register.n1 = 0
        cpu.register.h1 = 1
        cpu.register.cy1 = 0
        return opc.cycles

    # Handles OR
    def OR(cpu: CPU, opc: Opcode) -> int:
        value1 = opc.get_param1_value(cpu)
        value2 = opc.get_param2_value(cpu)
        res = value1 | value2 
        opc.set_param1_value(cpu, res)
        
        cpu.register.z1 = 1 if res == 0 else 0
        cpu.register.n1 = 0
        cpu.register.h1 = 0
        cpu.register.cy1 = 0
        return opc.cycles

    # Handles XOR
    def XOR(cpu: CPU, opc: Opcode) -> int:
        value1 = opc.get_param1_value(cpu)
        value2 = opc.get_param2_value(cpu)
        res = value1 ^ value2 
        opc.set_param1_value(cpu, res)
        
        cpu.register.z1 = 1 if res == 0 else 0
        cpu.register.n1 = 0
        cpu.register.h1 = 0
        cpu.register.cy1 = 0
        return opc.cycles

   # Handles CP (compare) - works like a SUB, but we don't store the result, only flags get updated
    def CP(cpu: CPU, opc: Opcode) -> int:
        value1 = opc.get_param1_value(cpu)
        value2 = opc.get_param2_value(cpu)
        Commands8bits._sub_and_update_flags(cpu, value1, value2)

        return opc.cycles

   # Handles INC
    def INC(cpu: CPU, opc: Opcode) -> int:
        value1 = opc.get_param1_value(cpu)
        
        # The Cy flag should not be affected
        cy_back = cpu.register.cy1
        opc.set_param1_value(cpu, Commands8bits._add_and_update_flags(cpu, value1, 1))

        cpu.register.cy1 = cy_back

        return opc.cycles

    # Handles DEC
    def DEC(cpu: CPU, opc: Opcode) -> int:
        value1 = opc.get_param1_value(cpu)

        # The Cy flag should not be affected
        cy_back = cpu.register.cy1
        opc.set_param1_value(cpu, Commands8bits._sub_and_update_flags(cpu, value1, 1))

        cpu.register.cy1 = cy_back
        
        return opc.cycles

    # Handles SWAP (swaps the 4 upper bits with the 4 lower bits)
    def SWAP(cpu: CPU, opc: Opcode) -> int:
        value = opc.get_param1_value(cpu)
        upper_nibble = (value & 0xF0) >> 4
        lower_nibble = value & 0x0F
        
        res = (lower_nibble << 4) | upper_nibble
        
        opc.set_param1_value(cpu, res)
        
        cpu.register.z1 = 1 if res == 0 else 0
        cpu.register.n1 = 0
        cpu.register.h1 = 0
        cpu.register.cy1 = 0
        return opc.cycles

    # Handles DAA (Decimal adjust register A)
    # Each nibble of register A will represent a different decimal (See Binary Coded Decimal)
    def DAA(cpu: CPU, opc: Opcode) -> int:
        value = opc.get_param1_value(cpu)
        
        print("before" + str(hex(value)))
        if cpu.register.n1 != 1:
            # Previous operation was addition
            if cpu.register.h1 == 1 or (value & 0xF) > 0x9:
                value += 0x6
            if cpu.register.cy1 == 1 or (value > 0x9F):
                value += 0x60
                cpu.register.cy1 = 1
        else:
            # Previous operation was substraction
            if cpu.register.h1 == 1:
                value -= 0x6
            if cpu.register.cy1 == 1:
                value -= 0x60
        
        cpu.register.z1 = 1 if value & 0xFF == 0 else 0
        cpu.register.n1 = 0
        print("res" + str(hex(value)))
        opc.set_param1_value(cpu, value)

    # Handles CPL (flips all bits from register A)
    def CPL(cpu: CPU, opc: Opcode) -> int:
        value = opc.get_param1_value(cpu)

        opc.set_param1_value(cpu, (~value) & 0xFF )
        
        cpu.register.z1 = 0
        cpu.register.n1 = 1
        cpu.register.h1 = 1
        return opc.cycles

    # Handles CCF (flips bit for Carry register Cy)
    def CCF(cpu: CPU, opc: Opcode) -> int:
        cpu.register.cy1 = ~cpu.register.cy1 & 0b1
        cpu.register.n1 = 0
        cpu.register.h1 = 0
        return opc.cycles

    # Handles SCF (set carry flag Cy)
    def SCF(cpu: CPU, opc: Opcode) -> int:
        cpu.register.cy1 = 1
        cpu.register.n1 = 0
        cpu.register.h1 = 0
        return opc.cycles

    # Handles DI (disable interrupts after next operation)
    def DI(cpu: CPU, opc: Opcode) -> int:
        cpu.interrupts.disable_interrupts_after_next = 1
        return opc.cycles

    # Handles EI (enable interrupts after next operation)
    def EI(cpu: CPU, opc: Opcode) -> int:
        cpu.interrupts.enable_interrupts_after_next = 1
        return opc.cycles

    # Rotates register left
    def RLC(cpu: CPU, opc:Opcode) -> int:
        value = opc.get_param1_value(cpu)
        removedbit = (value & 0b10000000) >> 7
        cpu.register.cy1 = removedbit
        value = (value << 1) | removedbit
        cpu.register.n1 = 0 
        cpu.register.h1 = 0
        cpu.register.z1 = 1 if value == 0 else 0
        
        opc.set_param1_value(value)
        return opc.cycles

    # Rotates register left through cy1
    def RL(cpu: CPU, opc:Opcode) -> int:
        value = opc.get_param1_value(cpu)
        removedbit = (value & 0b10000000) >> 7
        oldcy1 = cpu.register.cy1
        cpu.register.cy1 = removedbit
        value = (value << 1) | oldcy1
        cpu.register.n1 = 0 
        cpu.register.h1 = 0
        cpu.register.z1 = 1 if value == 0 else 0
        
        opc.set_param1_value(value)
        return opc.cycles

    # Rotates register right
    def RRC(cpu: CPU, opc:Opcode) -> int:
        value = opc.get_param1_value(cpu)
        removedbit = value & 0b00000001
        cpu.register.cy1 = removedbit
        value = (value >> 1) | (removedbit << 7)
        cpu.register.n1 = 0 
        cpu.register.h1 = 0
        cpu.register.z1 = 1 if value == 0 else 0
        
        opc.set_param1_value(value)
        return opc.cycles

    # Rotates A right through cy1
    def RR(cpu: CPU, opc:Opcode) -> int:
        value = opc.get_param1_value(cpu)
        removedbit = value & 0b00000001
        oldcy1 = cpu.register.cy1
        cpu.register.cy1 = removedbit
        value = (value >> 1) | (oldcy1 << 7)
        cpu.register.n1 = 0 
        cpu.register.h1 = 0
        cpu.register.z1 = 1 if value == 0 else 0
        
        opc.set_param1_value(value)
        return opc.cycles

    def _add_and_update_flags(cpu: CPU, value1: bytes, value2: bytes) -> bytes:
        # TODO We may need to handle the #FF + 1 case, as it loop back to 0 (won't here)
        addition = value1 + value2

        # setting flags
        cpu.register.z1 = 1 if addition == 0 else 0
        cpu.register.n1 = 0
        cpu.register.h1 = 1 if Commands8bits.has4bitCarryOver(value1, value2) else 0
        cpu.register.cy1 = 1 if Commands8bits.has8bitCarryOver(value1, value2) else 0
        return addition

    def _sub_and_update_flags(cpu: CPU, value1: bytes, value2: bytes) -> bytes:
        sub = value1 - value2

        # setting flags
        cpu.register.z1 = 1 if sub == 0 else 0
        cpu.register.n1 = 1
        cpu.register.h1 = 1 if Commands8bits.has4bitBorrow(value1, value2) else 0
        cpu.register.cy1 = 1 if Commands8bits.has8bitBorrow(value1, value2) else 0
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
