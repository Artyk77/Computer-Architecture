import sys
PRINT_BEEJ = 1
HALT = 2
PRINT_NUM = 3
SAVE = 4
PRINT_REGISTER = 5
ADD = 6
PUSH = 7
POP = 8

memory = [0] * 256
register = [0] * 8

SP = 7

pc = 0
running = True

def load_memory(filename):
    import sys
    try:
        address = 0
        with open(filename) as f:
            for line in f:
                comment_split = line.split("#")
                num = comment_split[0].strip()
                if num == "":
                    continue  # Ignore irrelevant lines
                value = int(num)
                memory[address] = value
                address += 1
    except FileNotFoundError:
        print(f"{sys.argv[0]}: {filename} Not Found")
        sys.exit(1)
if len(sys.argv) != 2:
    print("Usage: file.py filename", file=sys.stderr)
    sys.exit(1)
load_memory(sys.argv[1])
while running:
    command = memory[pc]
    if command == PRINT_BEEJ:
        print("BEEJ")
        pc += 1
    elif command == PRINT_NUM:
        num = memory[pc + 1]
        print(num)
        pc += 2
    elif command == HALT:
        running = False
        pc += 1
    elif command == SAVE:
        num = memory[pc + 1]
        reg = memory[pc + 2]
        register[reg] = num
        pc += 3
    elif command == ADD:
        reg_a = memory[pc + 1]
        reg_b = memory[pc + 2]
        register[reg_a] += register[reg_b]
        pc += 3
    elif command == PRINT_REGISTER:
        reg = memory[pc + 1]
        print(register[reg])
        pc += 2

    elif command == PUSH:
        reg = memory[pc + 1]
        val = register[reg]
        # decrement the SP
        register[SP] -= 1
        # copy the value from the given register to the address pointed to by the SP
        memory[register[SP]] = val
        # Increment PC by 2
        pc += 2

    elif command == POP:
        reg = memory[pc + 1]
        # copy the value from the address pointed to by SP to hte given register
        val = memory[register[SP]]
        register[reg] = val
        # increment SP
        register[SP] += 1
        # Increment PC by 2
        pc += 2

    else:
        print(f"Error: Unknown command: {command}")
        sys.exit(1)