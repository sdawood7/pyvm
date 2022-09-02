from instruction import Instruction


class Program:
    def __init__(self) -> None:
        self.byte_count = 0
        self.functions = {}
        self.labels = {}

    def instruction(self, instruction=None, arg1=None, arg2=None, func="main", label=None) -> None:
        if func not in self.functions:
            self.functions[func] = []
            self.labels[func] = self.byte_count

        if instruction != None:
            self.functions[func].append(instruction)
            self.byte_count += 1
            if label != None and arg1 == None and arg2 == None:
                if label not in self.labels:
                    raise Exception("Label \"{}\" not yet declared".format(label))
                jump_address = self.labels[label]
                arg1 = (jump_address & 0xff00) >> 8
                arg2 = (jump_address & 0x00ff)
        else:
            return

        if arg1 != None:
            self.functions[func].append(arg1)
            self.byte_count += 1

        if arg2 != None:
            self.functions[func].append(arg2)
            self.byte_count += 1
