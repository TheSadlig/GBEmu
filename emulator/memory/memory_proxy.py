# This class routes the request to the correct memory based on its address
# It contains the whole gameboy memory (WRAM, VRAM, ROM)

from audioop import add
from xmlrpc.client import boolean
from emulator.memory.memory import Ram, Rom, Memory


class MemoryProxy:
    # 0000-3FFF   16KB ROM Bank 00     (in cartridge, fixed at bank 00)
    # 4000-7FFF   16KB ROM Bank 01..NN (in cartridge, switchable bank number)
    # 8000-9FFF   8KB Video RAM (VRAM) (switchable bank 0-1 in CGB Mode)
    # A000-BFFF   8KB External RAM     (in cartridge, switchable bank, if any)
    # C000-CFFF   4KB Work RAM Bank 0 (WRAM)
    # D000-DFFF   4KB Work RAM Bank 1 (WRAM)  (switchable bank 1-7 in CGB Mode)
    # E000-FDFF   Same as C000-DDFF (ECHO)    (typically not used)
    # FE00-FE9F   Sprite Attribute Table (OAM)
    # FEA0-FEFF   Not Usable
    # FF00-FF7F   I/O Ports
    # FF80-FFFE   High RAM (HRAM)
    # FFFF        Interrupt Enable Register
    ROM00_END = 0x3FFF
    ROMxx_END = 0x7FFF
    VRAM_END = 0x9FFF
    ERAM_END = 0XBFFF
    WRAM1_END = 0xCFFF
    WRAMx_END = 0xDFFF
    ECHO_END = 0xFDFF
    OAM_END = 0xFE9F
    NONUSABLE_END = 0xFEFF
    IO_END = 0xFF7F
    HRAM_END = 0xFFFE

    ADDRESSABLE_MEMORY_SIZE = 0xFFFF

    def __init__(self):
        self.addressable_memory = []
        self._add_memory_block(None, MemoryProxy.ROM00_END, True)
        self._add_memory_block(MemoryProxy.ROM00_END, MemoryProxy.ROMxx_END, True)
        self._add_memory_block(MemoryProxy.ROMxx_END, MemoryProxy.VRAM_END)
        self._add_memory_block(MemoryProxy.VRAM_END, MemoryProxy.ERAM_END)
        self._add_memory_block(MemoryProxy.ERAM_END, MemoryProxy.WRAM1_END)
        self._add_memory_block(MemoryProxy.WRAM1_END, MemoryProxy.WRAMx_END)
        self._add_memory_block(MemoryProxy.WRAMx_END, MemoryProxy.ECHO_END)
        self._add_memory_block(MemoryProxy.ECHO_END, MemoryProxy.OAM_END)
        self._add_memory_block(MemoryProxy.OAM_END, MemoryProxy.NONUSABLE_END)
        self._add_memory_block(MemoryProxy.NONUSABLE_END, MemoryProxy.IO_END)
        self._add_memory_block(MemoryProxy.IO_END, MemoryProxy.HRAM_END)

    def write8(self, address16: bytes, data8: bytes):
#        if len(data8) > 8:
#            raise MemoryAccessError("Cannot write more than 8 bits at a time. Tried to write: " + str(hex(data8)), address16)
        for memory_block in self.addressable_memory:
            if memory_block.is_adress_in_range(address16) and memory_block.is_writable():
                memory_block.write8(address16, data8)
                return
        raise MemoryAccessError("Could not write to address. Block is non-existent or readonly", address16)

    def read8(self, address16: bytes) -> bytes:
        for memory_block in self.addressable_memory:
            if memory_block.is_adress_in_range(address16):
                return memory_block.read8(address16) 
        raise MemoryAccessError("Could not read from address. Block is non-existent", address16)

    # loads a bytearray directly into a ROM address
    def load_cartridge(self, address16: bytes, memory_to_write: bytearray):
        for memory_block in self.addressable_memory:
            if memory_block.is_adress_in_range(address16) and not memory_block.is_writable():
                memory_block.load(memory_to_write)
                return
        raise MemoryAccessError("Could not write to address. Block is non-existent or readonly", address16)

    def _add_memory_block(self, previous_end: bytes, end_address: bytes, is_rom=False):
        if is_rom:
            self.addressable_memory.append(Rom(previous_end, end_address, MemoryProxy.ADDRESSABLE_MEMORY_SIZE))
        else:
            self.addressable_memory.append(Ram(previous_end, end_address, MemoryProxy.ADDRESSABLE_MEMORY_SIZE))


class MemoryAccessError(Exception):
    def __init__(self, message, address=None):
        self.message = message
        self.address = address
    
    def __str__(self):
        return str(self.message) + " - address: " + str(hex(self.address))