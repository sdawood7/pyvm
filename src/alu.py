class ALU:
    def __init__(self):
        self.reset()

    def reset(self):
        self.overflow = False
        self.negative = False
        self.zero = True
        self.result = 0

    def compute(self, op, val1, val2=0) -> None: # Return accumulator value and flags
        self.reset()
        val1 = convert2scompl(val1)
        val2 = convert2scompl(val2)

        if op == "+":
            self.result = val1 + val2
        elif op == "-":
            self.result = val1 - val2
        elif op == "*":
            self.result = val1 * val2
        elif op == "/":
            if val2 == 0:
                raise Exception("Divide by 0 Error")
            self.result = val1 / val2
        elif op == "%":
            if val2 == 0:
                raise Exception("Modulo by 0 Error")
            self.result = val1 % val2
        elif op == "&":
            self.result = val1 & val2
        elif op == "|":
            self.result = val1 | val2
        elif op == "^":
            self.result = val1 ^ val2
        elif op == ">>":
            self.result = val1 >> val2
        elif op == "<<":
            self.result = val1 << val2
        elif op == "~":
            self.result = ~val1
        else:
            raise Exception("Unknown operator \"{}\" given".format(op))

        self.setFlags()

        def convert2scompl(n):
            n &= 0xFFFF # Convert to 16 bit
            if n >= 0x8000 and n <= 0xFFFF:
                return ~n + 1
            return n

        def setFlags():
            if self.result > 0xFFFF:
                self.overflow = True

            if self.result == 0:
                self.zero = True
                self.negative = False
            elif self.result < 0:
                self.zero = False
                self.negative = True
            else:
                self.zero = False
                self.negative = False
