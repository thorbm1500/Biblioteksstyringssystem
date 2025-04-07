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
                self.clean()
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
        match input(string).lower():
            case "y"|"yes": return True
        self.clean()
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

    def clear_print(self, string="This was left empty by mistake."):
        self.clear()
        print(string)

    def user_input_get_integer(self, string):
        integer = self.parse_integer(self.user_input(string))

        while integer is None:
            if self.retry("Error. '" + str(integer) + "' is not an integer. Do you want to try again? [Y/N]\n\n"):
                integer = self.parse_integer(self.user_input(string))

        if integer is None: self.clean()

        return integer