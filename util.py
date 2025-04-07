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

    # Used to parse integers from strings
    def parse_integer(self, integer):
        try:
            integer = int(integer)
        except:
            return None
        return integer

    def retry(self, string):
        user_input = input(string)

        match user_input.lower():
            case "y"|"yes": return True

        return False

    def clean(self, string=""):
        if string == "":
            self.clear()
            self.title()
        else:
            input(string)
            self.clear()
            self.title()

    def user_input(self, string=""):
        ui = input(string)
        self.clear()
        return ui