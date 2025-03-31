from libraryClass import Library
from bookManager import BookManager
from memberManager import MemberManager
from util import Util

util = Util()

library = Library({},[])

book_manager = BookManager(library)
member_manager = MemberManager(library)

def prompt():
    user_input = input("")

    match user_input.lower():
        case "exit"|"stop"|"shutdown"|"end"|"close":
            print("Goodbye.")
            return False

        case "help"|"help 1":
            util.clear()
            print("Prompts - Page 1\n  > help - Shows this list.\n  > exit - Shuts down the program.\n  > books - Prints a list of all books.\n  > members - Prints a list of all members.\n\nUse 'help 2' to go to the next page...")

        case "help 2":
            util.clear()
            print("Prompts - Page 2\n  > create - Create new books or members.\n  > delete - Delete books or members")

        case "books":
            library.display_books()

        case "members":
            library.display_members()

        case "create":
            create()

        case "delete"|"del":
            delete()

        case _:
            print("Error. '" + user_input + "' is not a known command.")

    return True

def create():
    util.clear()

    user_input = input("Creation Panel\n\nChoose an object\n[ Book , Member ]\n\n")

    match user_input.lower():
        case "book"|"books":
            util.clear()
            title = input("Creation Panel\n\nChoose a title.\n\nTitle: ")
            util.clear()
            author = input("Creation Panel\n\nChoose an author.\n\nAuthor: ")
            util.clear()
            copies = input("Creation Panel\n\nChoose number of copies.\n\nCopies: ")
            util.clear()


            new_book_id = book_manager.new_book(title,author,copies)
            print("New book created.\n")
            library.display_book(new_book_id)
            input("Press enter to continue...")
            util.clear()
            util.title()

        case "member"|"members":
            util.clear()
            name = input("Creation Panel\n\nChoose a name.\n\nName: ")
            util.clear()

            print("New member created.")
            new_member_id = member_manager.new_member(name, None)
            library.display_member(new_member_id)
            input("Press enter to continue...")
            util.clear()
            util.title()

def delete():
    util.clear()

    user_input = input("Deletion Panel\n\nChoose an object\n[ Book , Member ]\n\n")

    match user_input.lower():
        case "book"|"books":
            util.clear()

        case "member"|"members":
            delete_member()

def delete_member():
    util.clear()

    name = input("Deletion Panel\n\nSelect a member\n\nName: ")
    member = library.get_member_from_string(name)
    if member is None:
        user_input = input("Error. No member found with that name. Do you want to try again? [Y/N]")
        if user_input.lower() == "y" or user_input.lower() == "yes":
            delete_member()
        else:
            util.clear()
            util.title()
            return

    library.remove_member(member.member_id)
    print("Member " + member.name + " with ID: " + str(member.member_id) + " has been deleted.")

def initialize_library():
    book_manager.new_book("Harry Potter","J.K. Rowling",32)
    book_manager.new_book("Game of Thrones","George R.R. Martin",512)
    book_manager.new_book("Twilight","Stephanie Mayers",363)

    member_manager.new_member("Thor M.",None)
    member_manager.new_member("John D.", None)
    member_manager.new_member("Jane D.", None)

def main():
    initialize_library()
    util.title()
    while prompt():
        pass

if __name__ == "__main__":
    main()