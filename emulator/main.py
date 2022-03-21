import sys, getopt
from emulator.cpu.opcode_executor import OpcodeExecutor
from emulator.cpu.cpu import CPU

class MainLoop:
    CLOCK_SPEED = 4194304
    FRAME_RATE = 60 # Video frame rate
    def __init__(self, cartridge_bytes):
        self._cpu = CPU(cartridge_bytes)
        self._executor = OpcodeExecutor()
        self._executor.load_opcodes()
        # init programm counter to 0x100
        self._cpu.register.pc16 = 0x100
        self._cpu.register.sp16 = 0xFFFE

    def step(self):
        instruction = self._cpu.get_next_opcode()
        self._executor.execute(self._cpu, instruction)

def main(argv):
    try:   
        opts, args = getopt.getopt(argv,"i:",["ifile="])
    except getopt.GetoptError:  
        print("test.py -i <inputfile>")
        sys.exit(2)

    inputfile = 'cartridges/cpu_instrs.gb'
    for opt, arg in opts:
        if opt in ("-i", "--ifile"):
            inputfile = arg
    if inputfile != None:
        f = open(inputfile, "rb")
        loop = MainLoop(f.read())
        while True:
            input("Press Enter to continue...")
            loop.step()
    else:
        sys.exit(2)
        

if __name__ == '__main__':
   main(sys.argv[1:])