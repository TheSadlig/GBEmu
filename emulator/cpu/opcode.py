import opcode
from emulator.cpu.cpu import CPU

class Opcode:
    def __init__(self, instruction: str, params: str, opcode: int, cycles: int):
        self.instruction = instruction
        self.params = params.split(',')
        self.opcode = opcode
        self.cycles = cycles

    def _clean_param(self, param: str) -> str:
        param = param.removeprefix("(")
        param = param.removesuffix(")")
        param = param.lower()
        return param 
        

    # returns the value for the FIRST param, based on the current state (CPU, registers and/or memory)
    def get_param1_value(self, cpu: CPU) -> bytes:
        if self.params[0].isnumeric(): # For some operations, the spec will contain numbers (BIT)
            return int(self.params[0])

        is_param1_address = self.params[0].startswith("(")

        param = self._clean_param(self.params[0])
        if param == 'n' or param == 'nn':
            # Raising an exception because if we had n or nn, the code would increase the cp16 register which we don't want
            raise WrongOpcodeError("`n` and `nn` are unsupported as first parameters", self.opcode)
        
        value = self._get_from_reg(cpu, param)
        
        if is_param1_address:
            return cpu.memory.read8(value)
        else:
            return value

    # returns the value for the SECOND param, based on the current state (CPU, registers and/or memory)
    # If the parameter is "n" or "nn" (immediate), it will increase the program counter accordingly
    def get_param2_value(self, cpu: CPU) -> bytes:
        is_param2_address = self.params[1].startswith("(")

        param = self._clean_param(self.params[1])
        value = self._get_from_reg(cpu, param)
        
        if is_param2_address:
            return cpu.memory.read8(value)
        else:
            return value

    def _get_from_reg(self, cpu: CPU, param:str) -> bytes:
        register = cpu.register
        if (param.startswith('$')):
            # we need to handle a hardcoded address: e.g. $FFEE+C
            param_splitted = param.split('+')
            param_address1 = int(param_splitted[0].removeprefix('$'), 16)
            if len(param_splitted) == 2:
                param_address2 = self._get_from_reg(cpu, param_splitted[1])
                return param_address1 + param_address2
            return param_address1
        elif (param == 'n'):
            # 8 bit immediate
            previousPcValue = register.pc16
            register.pc16 += 1
            return cpu.memory.read8(previousPcValue)
        elif (param == 'nn'):
            # 16 bits immediate
            # get_param2_value may get the value from the returned address (if "(nn)" and not "nn")
            previousPcValue = register.pc16
            register.pc16 += 2
            return cpu.memory.read8(previousPcValue) | cpu.memory.read8(previousPcValue + 1) << 8 
        elif (param == "cy"):
            return register.cy1
        elif (param == "ncy"):
            return register.ncy1 
        elif (param == "z"):
            return register.z1
        elif (param == "nz"):
            return register.nz1
        elif (len(param) == 1): 
            # Single letter, simple 8b register
            param = param + "8" 
            print("Getting register " + param)
            return register.get_register_by_name(param)
        elif (len(param) == 2):
            # two letters, combine two register
            param = param + "16"
            print("Getting register " + param)
            return register.get_register_by_name(param)
        else:
            raise WrongOpcodeError("Unsupported opcode parameter:" + param, self.opcode)

    # Sets the given value to the proper place/register
    def set_param1_value(self, cpu:CPU, value:hex):
        is_param1_address = self.params[0].startswith("(")
        param = self._clean_param(self.params[0])

        if (is_param1_address):
            address = self._get_from_reg(cpu, param)
            cpu.memory.write8(address, value)
        else:
            self._set_value_from_param(cpu, param, value)

    def _set_value_from_param(self, cpu: CPU, param:str, value:hex):
        register = cpu.register
        if (len(param) == 1):
            # Single letter, simple 8b register
            param = param + "8" 
            print("setting register " + param + " = " + str(value))
            register.set_register_by_name(param, value)
        elif (len(param) == 2):
            # two letters, combine two register
            param = param + "16"
            print("setting register " + param + " = " + str(hex(value)))
            register.set_register_by_name(param, value)
        else:
            raise WrongOpcodeError("Unsupported opcode parameter:" + param, self.opcode)

    def __str__(self) -> str:
        params_str = self.params[0]
        if len(self.params) == 2:
            params_str += "," + self.params[1] 
        return self.instruction + " " + params_str + "   # " + str(hex(self.opcode)) + " - " + str(self.cycles)


class WrongOpcodeError(Exception):
    def __init__(self, message, opcode: Opcode):
        self.message = message
        self.opcode = opcode

    def __str__(self):
        return str(self.message) + " - " + str(self.opcode)