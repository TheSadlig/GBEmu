class BitTools:
    def clear_bit(byte, position):
        byte &= ~(1 << position) 
        return byte
    
    def set_bit(byte, position, value):
        byte = BitTools.clear_bit(byte, position)
        byte = (byte | (value << position)) 
        return byte

    def get_bit(byte, position):
        return (byte & 1 << position) >> position

    # returns true of there is a half carry over
    def has12bitCarryOver(value1, value2) -> bool:
        return ((( value1 & 0xFFF) + (value2 & 0xFFF)) & 0x1000) == 0x1000

    # returns true of there is a carry over
    def has16bitCarryOver(value1, value2) -> bool:
        return ((( value1 & 0xFFFF) + (value2 & 0xFFFF)) & 0x10000) == 0x10000

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
