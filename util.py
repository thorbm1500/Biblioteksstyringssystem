class Util:

    def __init__(self):
        pass

    def clear(self):
        for i in range(10):
            print("\n")

    def title(self):
        print("Zealand Library\nUse 'help' to get started.\n")

    def legal_exec(self, _input):
        if self.is_cancelled(_input): return True
        match _input:
            case "y"|"yes"|"n"|"no":
                return True
            case _:
                return False

    # Used to check if an action has been cancelled.
    def is_cancelled(self, _input):
        _input = str(_input)
        match _input.lower():
            case "exit"|"quit"|"cancel"|"stop"|"end":
                self.clear()
                self.title()
                return True
        return False