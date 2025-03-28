from libraryClass import Library
from bookManager import Manager

library = Library({},[])

manager = Manager(library)

def prompt():
    user_input = input("")

    if user_input == "exit":
        print("Goodbye.")
        return

    if user_input == "help":
        print("Prompts\n  help - Shows this list\n  books - Prints a list of all books")

    if user_input == "books":
        library.display_books()

    if user_input == "members":
        library.display_members()

    prompt()

def initialize_library():
    manager.new_book("Harry Potter","J.K. Rowling",32)
    manager.new_book("Game of Thrones","George R.R. Martin",512)
    manager.new_book("Twilight","Stephanie Mayers",363)

def main():
    initialize_library()
    prompt()

if __name__ == "__main__":
    print("Zealand Library\n\n")
    main()