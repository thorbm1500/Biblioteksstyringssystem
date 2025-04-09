class Util:

    def __init__(self):
        """Utility class"""
        pass

    def clear(self):
        """ "Clears" the screen by sending 10 "end-of-line" """
        print("\n\n\n\n\n\n\n\n\n\n")

    def title(self):
        """Prints the title"""
        print("Zealand Library\nUse 'help' to get started.\n")

    def legal_exec(self, _input):
        """Checks if the given input is legal"""
        if _input is None: return False
        if self.is_cancelled(_input): return True
        match _input:
            case "y"|"yes"|"n"|"no":
                return True
            case _:
                return False

    def is_cancelled(self, _input):
        """Checks if an action has been canceled."""
        _input = str(_input)
        match _input.lower():
            case "exit"|"quit"|"cancel"|"stop"|"end":
                self.clean()
                return True
        return False

    def parse_integer(self, integer):
        """Parses integers from strings. Returns None if parsing fails"""
        try:
            integer = int(integer)
        except:
            return None
        return integer

    def retry(self, string):
        """Prompts the user with a retry"""
        match input(string).lower():
            case "y"|"yes": return True
        self.clean()
        return False

    def clean(self, string=""):
        """Cleans the screen and prints the title. Can be used with a string to delay the clearing of the screen"""
        if string == "":
            self.clear()
            self.title()
        else:
            input(string)
            self.clear()
            self.title()

    def user_input(self, string=""):
        """Prompts the user with a string and clears the screen after. Returns the user's input"""
        ui = input(string)
        self.clear()
        return ui

    def clear_print(self, string):
        """Clears the screen and prompts the user with an input after"""
        self.clear()
        print(string)

    def user_input_get_integer(self, string):
        """Prompts the user with an input and will continue to do so until the user inputs and integer or exits"""
        integer = self.parse_integer(self.user_input(string))

        while integer is None:
            if self.retry(f"Error. '{integer}' is not an integer. Do you want to try again? [Y/N]\n\n"):
                integer = self.parse_integer(self.user_input(string))

        if integer is None: self.clean()

        return integer