class Util:

    def __init__(self):
        pass

    def clear(self):
        for i in range(10):
            print("\n")

    def title(self):
        print("Zealand Library\nUse 'help' to get started.\n")

    def legal_exec(self, _input):
        match _input:
            case "exit"|"quit"|"cancel"|"y"|"yes"|"n"|"no":
                return True
            case _:
                return False