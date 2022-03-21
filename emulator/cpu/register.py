from emulator.tools.bit_tools import BitTools


class Register:
    def __init__(self):
        self._a8 = 0x0
        self._f8 = 0x0 # flag register
        self._b8 = 0x0
        self._c8 = 0x0
        self._d8 = 0x0
        self._e8 = 0x0
        self._h8 = 0x0
        self._l8 = 0x0
        
        self.sp16 = 0x0
        self.pc16 = 0x0
    
    # Handling single byte registers
    @property
    def a8(self):
        return self._a8 
    
    @a8.setter
    def a8(self, value):
        self._a8 = value & 0xFF

    @property
    def f8(self):
        return self._f8 
    
    @f8.setter
    def f8(self, value):
        self._f8 = value & 0xFF
    
    
    @property
    def b8(self):
        return self._b8 
    
    @b8.setter
    def b8(self, value):
        self._b8 = value & 0xFF
    
    @property
    def c8(self):
        return self._c8 
    
    @c8.setter
    def c8(self, value):
        self._c8 = value & 0xFF

    @property
    def d8(self):
        return self._d8 
    
    @d8.setter
    def d8(self, value):
        self._d8 = value & 0xFF
    
    @property
    def e8(self):
        return self._e8 
    
    @e8.setter
    def e8(self, value):
        self._e8 = value & 0xFF
    
    @property
    def h8(self):
        return self._h8 
    
    @h8.setter
    def h8(self, value):
        self._h8 = value & 0xFF
    
    @property
    def l8(self):
        return self._l8 
    
    @l8.setter
    def l8(self, value):
        self._l8 = value & 0xFF
    
    # Handling the combined registers 
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
        return BitTools.get_bit(self.f8, 7)

    @z1.setter
    def z1(self, value):
        self.f8 = BitTools.set_bit(self.f8, 7, value)

    @property
    def n1(self):
        return BitTools.get_bit(self.f8, 6)

    @n1.setter
    def n1(self, value):
        self.f8 = BitTools.set_bit(self.f8, 6, value)

    @property
    def h1(self):
        return BitTools.get_bit(self.f8, 5)

    @h1.setter
    def h1(self, value):
        self.f8 = BitTools.set_bit(self.f8, 5, value)

    @property
    def cy1(self):
        return BitTools.get_bit(self.f8, 4)

    @cy1.setter
    def cy1(self, value):
        self.f8 = BitTools.set_bit(self.f8, 4, value)

    @property
    def nz1(self):
        return ~self.z1

    @nz1.setter
    def nz1(self, value):
        self.z1 = ~value

    @property
    def ncy1(self):
        return ~self.cy1

    @ncy1.setter
    def ncy1(self, value):
        self.cy1 = ~value

    def get_register_by_name(self, registerName):
        return Register.__getattribute__(self, registerName)
    
    def set_register_by_name(self, registerName, value):
        return Register.__setattr__(self, registerName, value)
