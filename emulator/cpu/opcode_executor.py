import csv
from emulator.cpu.commands_16bits import Commands16bits
from emulator.cpu.commands_8bits import Commands8bits
from emulator.cpu.commands_actions import CommandsActions
from emulator.cpu.cpu import CPU
from emulator.cpu.opcode import Opcode

class OpcodeExecutor:
    def load_opcodes(self):
        self.opcodes = dict()
        with open('opcodes_list.csv', newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) > 0 and not row[0].startswith("#"):
                    opcode_hex = int(row[2], 16)
                    opcode = Opcode(row[0], row[1], opcode_hex, int(row[3]))
                    self.opcodes[opcode_hex] = opcode
    
    # Executes the instruction and returns the number of cycles
    # Assumes that if opc_hex starts with CB, the next Byte is already retrieved !
    def execute(self, cpu: CPU, opc_hex: int):    
        opcode = self.opcodes[opc_hex]
        if opcode.instruction == "LD":
            return Commands8bits.LD(cpu, opcode)
        elif opcode.instruction == "LDD":
            return Commands8bits.LDD(cpu, opcode)
        elif opcode.instruction == "LDI":
            return Commands8bits.LDI(cpu, opcode)
        elif opcode.instruction == "LDHL":
            return Commands8bits.LDHL(cpu, opcode)
        elif opcode.instruction == "ADD":
            return Commands8bits.ADD(cpu, opcode)
        elif opcode.instruction == "ADC":
            return Commands8bits.ADC(cpu, opcode)
        elif opcode.instruction == "SUB":
            return Commands8bits.SUB(cpu, opcode)
        elif opcode.instruction == "SBC":
            return Commands8bits.SBC(cpu, opcode)
        elif opcode.instruction == "AND":
            return Commands8bits.AND(cpu, opcode)
        elif opcode.instruction == "OR":
            return Commands8bits.OR(cpu, opcode)
        elif opcode.instruction == "XOR":
            return Commands8bits.XOR(cpu, opcode)
        elif opcode.instruction == "CP":
            return Commands8bits.CP(cpu, opcode)
        elif opcode.instruction == "INC":
            return Commands8bits.INC(cpu, opcode)
        elif opcode.instruction == "DEC":
            return Commands8bits.DEC(cpu, opcode)
        elif opcode.instruction == "SWAP":
            return Commands8bits.SWAP(cpu, opcode)
        elif opcode.instruction == "DAA":
            return Commands8bits.DAA(cpu, opcode)
        elif opcode.instruction == "RLC":
            return Commands8bits.RLC(cpu, opcode)
        elif opcode.instruction == "RL":
            return Commands8bits.RL(cpu, opcode)
        elif opcode.instruction == "RRC":
            return Commands8bits.RRC(cpu, opcode)
        elif opcode.instruction == "RR":
            return Commands8bits.RR(cpu, opcode)
        elif opcode.instruction == "SLA":
            return Commands8bits.SLA(cpu, opcode)
        elif opcode.instruction == "SRA":
            return Commands8bits.SRA(cpu, opcode)
        elif opcode.instruction == "SRL":
            return Commands8bits.SRL(cpu, opcode)
        elif opcode.instruction == "BIT":
            return Commands8bits.BIT(cpu, opcode)
        elif opcode.instruction == "BIT":
            return Commands8bits.SET(cpu, opcode)
        elif opcode.instruction == "SET":
            return Commands8bits.RES(cpu, opcode)
        elif opcode.instruction == "RES":
            return Commands8bits.CPL(cpu, opcode)
        elif opcode.instruction == "CCF":
            return Commands8bits.CCF(cpu, opcode)
        elif opcode.instruction == "SCF":
            return Commands8bits.SCF(cpu, opcode)
        elif opcode.instruction == "NOP":
            # No operation
            return
        elif opcode.instruction == "HALT":
            # TODO: evaluate whether we need to do something for that ?
            return
        elif opcode.instruction == "STOP":
            # TODO: evaluate whether we need to do something for that ?
            return
        elif opcode.instruction == "JP":
            return CommandsActions.JP(cpu, opcode)
        # 16 bits
        elif opcode.instruction == "PUSH":
            return Commands16bits.PUSH(cpu, opcode)
        elif opcode.instruction == "POP":
            return Commands16bits.POP(cpu, opcode)
        elif opcode.instruction == "ADD16":
            return Commands16bits.ADD16(cpu, opcode)
        elif opcode.instruction == "ADD16SP":
            return Commands16bits.ADD16SP(cpu, opcode)
        elif opcode.instruction == "INC16":
            return Commands16bits.INC16(cpu, opcode)
        elif opcode.instruction == "DEC16":
            return Commands16bits.DEC16(cpu, opcode)
        
