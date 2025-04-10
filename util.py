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
        """Checks if the provided input is legal"""
        if _input is None: return False
        if self.is_cancelled(_input): return True
        match _input:
            case "y"|"yes"|"n"|"no":
                return True
            case _:
                return False

    def is_cancelled(self, _input: str):
        """Checks if an action has been canceled."""
        _input = str(_input)
        match _input.lower():
            case "exit"|"quit"|"cancel"|"stop"|"end":
                self.clean()
                return True
        return False

    def parse_integer(self, number):
        """Parses integers from strings. Returns None if parsing fails"""
        if isinstance(number, int): return number
        try:
            number = int(number)
        except:
            return None
        return number

    def retry(self, string: str):
        """Prompts the user with a retry"""
        match input(string).lower():
            case "y"|"yes":
                self.clear()
                return True
        self.clean()
        return False

    def clean(self, string=None):
        """Cleans the screen and prints the title. Can be used with a string to delay the clearing of the screen"""
        if string is None:
            self.clear()
            self.title()
        else:
            input(string)
            self.clear()
            self.title()

    def user_input(self, string=""):
        """Prompts the user with a string and clears the screen after. Returns the user's input"""
        user_input = input(string)
        self.clear()
        return user_input

    def clear_print(self, string:str):
        """Clears the screen and prompts the user with an input after"""
        self.clear()
        print(string)

    def user_input_get_integer(self, string:str):
        """Prompts the user with an input and will continue to do so until the user inputs and integer or exits"""
        user_input = self.user_input(string)
        integer = self.parse_integer(user_input)

        while integer is None:
            if self.retry(f"[Error] '{user_input}' is not an integer. Do you want to try again? [Y/N]\n\n"):
                user_input = self.user_input(string)
                integer = self.parse_integer(user_input)

        if integer is None: self.clean()
        else: return integer