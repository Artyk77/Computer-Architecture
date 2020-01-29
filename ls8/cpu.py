"""CPU functionality."""
import sys
class CPU:
    """Main CPU class."""
    def __init__(self):
        """Construct a new CPU."""
        self.registers = [0] * 8
        self.ram = [0] * 256
        self.pc = 0
        self.sp = 7

    def load(self, filename):
        """Load a program into memory."""
        address = 0
        # For now, we've just hardcoded a program:
        program = []
        try:
            address = 0
            with open(filename) as f:
                for line in f:
                    comment_split = line.split("#")
                    num = comment_split[0].strip()
                    if num == "":
                        continue  # Ignore irrelevant lines
                    value = int(num, 2)
                    program.append(value)
        except FileNotFoundError:
            print(f"{sys.argv[0]}: {filename} Not Found")
            sys.exit(1)
        for instruction in program:
            self.ram[address] = instruction
            address += 1
    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        elif op == "MUL":
            self.registers[reg_a] *= self.registers[reg_b]
        else:
            raise Exception("Unsupported ALU operation")
    def ram_read(self, MAR):
        return self.ram[MAR]
    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR
    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """
        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')
        for i in range(8):
            print(" %02X" % self.reg[i], end='')
        print()
    def run(self):
        """Run the CPU."""
        running = True
        HLT = 0b00000001
        LDI = 0b10000010
        PRN = 0b01000111
        MUL = 0b10100010
        PUSH = 0b01000101
        POP = 0b01000110

        while running:
            IR = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            if IR == HLT:
                print("Exiting program...")
                running = False
                print("Program exited")
            elif IR == LDI:
                self.registers[operand_a] = operand_b
                self.pc += 3
            elif IR == PRN:
                print(self.registers[operand_a])
                self.pc += 2
            elif IR == MUL:
                product = self.alu("MUL", operand_a, operand_b)
                self.pc += 3
            elif IR == PUSH:
                reg = self.ram_read(self.pc + 1)
                val = self.registers[reg]
                self.registers[self.sp] -= 1
                self.ram_write(self.registers[self.sp], val)
                self.pc += 2
            elif IR == POP:
                reg = self.ram_read(self.pc + 1)
                val = self.ram_read(self.registers[self.sp])
                self.registers[reg] = val
                self.registers[self.sp] += 1
                self.pc += 2