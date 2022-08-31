class Program:
    def __init__(self) -> None:
        self.byte_count = 0
        self.functions = {}

    def instruction(self, instruction=None, arg1=None, arg2=None, func="main") -> None:
        if func not in self.functions:
            self.functions[func] = []

        if instruction != None:
            self.functions[func].append(instruction)
            self.byte_count += 1
        else:
            return

        if arg1 != None:
            self.functions[func].append(arg1)
            self.byte_count += 1

        if arg2 != None:
            self.functions[func].append(arg2)
            self.byte_count += 1
