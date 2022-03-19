class Register:
    def __init__(self):
        # For once we will keep everything public. There will be a lot of operations on those
        self.a8 = 0x0
        self.f8 = 0x0 # flag register
        self.b8 = 0x0
        self.c8 = 0x0
        self.d8 = 0x0
        self.e8 = 0x0
        self.h8 = 0x0
        self.l8 = 0x0
        
        self.sp16 = 0x0
        self.pc16 = 0x0
    
    @property
    def af16(self):
        return self.a8 << 8 | self.f8

    @af16.setter
    def af16(self, value):
        self.a8 = (value & 0xFF00) >> 8
        self.f8 = value & 0x00FF

    @property
    def bc16(self):
        return self.b8 << 8 | self.c8

    @bc16.setter
    def bc16(self, value):
        self.b8 = (value & 0xFF00) >> 8 
        self.c8 = value & 0x00FF

    @property
    def de16(self):
        return self.d8 << 8 | self.e8

    @de16.setter
    def de16(self, value):
        self.d8 = (value & 0xFF00) >> 8
        self.e8 = value & 0x00FF

    @property
    def hl16(self):
        return self.h8 << 8 | self.l8

    @hl16.setter
    def hl16(self, value):
        self.h8 = (value & 0xFF00) >> 8 
        self.l8 = value & 0x00FF

    @property
    def z1(self):
        return Register.get_bit(self.f8, 7)

    @z1.setter
    def z1(self, value):
        self.f8 = Register.set_bit(self.f8, 7, value)

    @property
    def n1(self):
        return Register.get_bit(self.f8, 6)

    @n1.setter
    def n1(self, value):
        self.f8 = Register.set_bit(self.f8, 6, value)

    @property
    def h1(self):
        return Register.get_bit(self.f8, 5)

    @h1.setter
    def h1(self, value):
        self.f8 = Register.set_bit(self.f8, 5, value)

    @property
    def cy1(self):
        return Register.get_bit(self.f8, 4)

    @cy1.setter
    def cy1(self, value):
        self.f8 = Register.set_bit(self.f8, 4, value)


    def clear_bit(byte, position):
        byte &= ~(1 << position) 
        return byte
    
    def set_bit(byte, position, value):
        byte = Register.clear_bit(byte, position)
        byte = (byte | (value << 7)) 
        return byte

    def get_bit(byte, position):
        return (byte & 1 << position) >> position

    def get_register_by_name(self, registerName):
        return Register.__getattribute__(self, registerName)
    
    def set_register_by_name(self, registerName, value):
        return Register.__setattr__(self, registerName, value)
