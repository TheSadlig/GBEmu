from atexit import register
import unittest
from emulator.cpu.register import Register

class testRegister(unittest.TestCase):
    def test_af(self):
        reg = Register() 
        self.assertEqual(reg.a8, 0)
        self.assertEqual(reg.f8, 0)
        reg.af16 = 0xFABC
        self.assertEqual(reg.a8, 0xFA)
        self.assertEqual(reg.f8, 0xBC)
        reg.af16 = 0xAF
        self.assertEqual(reg.a8, 0x00)
        self.assertEqual(reg.f8, 0xAF)

    def test_bc(self):
        reg = Register() 
        self.assertEqual(reg.b8, 0)
        self.assertEqual(reg.c8, 0)
        reg.bc16 = 0xFABC
        self.assertEqual(reg.b8, 0xFA)
        self.assertEqual(reg.c8, 0xBC)
        reg.bc16 = 0xAF
        self.assertEqual(reg.b8, 0x00)
        self.assertEqual(reg.c8, 0xAF)

    def test_de(self):
        reg = Register() 
        self.assertEqual(reg.d8, 0)
        self.assertEqual(reg.e8, 0)
        reg.de16 = 0xFABC
        self.assertEqual(reg.d8, 0xFA)
        self.assertEqual(reg.e8, 0xBC)
        reg.de16 = 0xAF
        self.assertEqual(reg.d8, 0x00)
        self.assertEqual(reg.e8, 0xAF)

    def test_hl(self):
        reg = Register() 
        self.assertEqual(reg.h8, 0)
        self.assertEqual(reg.l8, 0)
        reg.hl16 = 0xFABC
        self.assertEqual(reg.h8, 0xFA)
        self.assertEqual(reg.l8, 0xBC)
        reg.hl16 = 0xAF
        self.assertEqual(reg.h8, 0x00)
        self.assertEqual(reg.l8, 0xAF)

    def test_z(self):
        reg = Register() 
        self.assertEqual(reg.z1, 0)
        self.assertEqual(reg.f8, 0)
        reg.z1 = 0b1
        self.assertEqual(reg.z1, 0b1)
        self.assertEqual(reg.f8, 0b10000000)
        reg.f8 = 0b0
        self.assertEqual(reg.z1, 0)
        reg.f8 = 0b11111111
        self.assertEqual(reg.z1, 1)
        reg.z1 = 0
        self.assertEqual(reg.f8, 0b01111111)
    
    def test_register_by_name(self):
        reg = Register()
        reg.set_register_by_name("a1", 5)
        self.assertEqual(reg.a1, 5)
        self.assertEqual(reg.get_register_by_name("a1"), 5)
        
    def test_register_by_name_composite(self):
        reg = Register()
        reg.set_register_by_name("af16", 0xFE)
        self.assertEqual(reg.af16, 0xFE)
        self.assertEqual(reg.get_register_by_name("af16"), 0xFE)

if __name__ == '__main__':
    unittest.main()        
        
