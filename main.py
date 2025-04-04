from libraryClass import Library
from bookManager import BookManager
from memberManager import MemberManager
from util import Util

util = Util()

library = Library({},[])

book_manager = BookManager(library)
member_manager = MemberManager(library)

def prompt():
    user_input = input()

    match user_input.lower():
        case "exit"|"stop"|"shutdown"|"end"|"close"|"quit":
            print("Goodbye.")
            return False

        case "help"|"help 1":
            util.clear()
            print("Prompts - Page 1\n  > help - Shows this list.\n  > exit - Shuts down the program.\n  > books - Prints a list of all books.\n  > members - Prints a list of all members.\n\nUse 'help 2' to go to the next page...")

        case "help 2":
            util.clear()
            print("Prompts - Page 2\n  > create - Create new books or members.\n  > delete - Delete books or members.\n  > update - Update books or members.\n\nUse 'help 3' to go to the next page...")

        case "help 3":
            util.clear()
            print("Prompts - Page 3\n  > rent - Rent a book.\n  > return - Return a book.")

        case "books":
            library.display_books()

        case "members":
            library.display_members()

        case "create":
            create()

        case "delete"|"del":
            delete()

        case "update":
            update()

        case "rent"|"rent book"|"issue"|"issue book":
            #todo:Add renting books
            pass

        case "return"|"return book":
            #todo:Add returning books
            pass

        case _:
            print("Error. '" + user_input + "' is not a known command.")

    return True

def update():
    util.clear()

    user_input = input("Update Panel\n\nChoose an object\n[ Book , Member ]\n\n")

    match user_input.lower():
        case "book"|"books":
            update_book()

        case "member"|"members":
            pass

def update_book():
    util.clear()

    user_input = input("Update Panel\n\nChoose an update method\n[ ID , Name ]\n\n")
    book = None

    util.clear()

    match user_input.lower():
        case "id":
            _id = input("Update Panel\n\nSelect a book\n\nID: ")
            book = library.get_book_from_id(_id)

            if book is None:
                user_input = input("Error. No book found with that ID. Do you want to try again? [Y/N]\n")
                if user_input.lower() == "y" or user_input.lower() == "yes":
                    update_book()
                else:
                    util.clear()
                    util.title()
                return

        case "name":
            name = input("Update Panel\n\nSelect a book\n\nName: ")
            book = library.get_book_from_string(name)

            if book is None:
                user_input = input("Error. No book found with that name. Do you want to try again? [Y/N]\n")
                if user_input.lower() == "y" or user_input.lower() == "yes":
                    delete_member()
                else:
                    util.clear()
                    util.title()
                return

    util.clear()

    # Current book details
    book_id = book.book_id
    title = book.title
    author = book.author
    copies = library.get_copies(book.book_id)

    user_input = input("Update Panel\n\nChoose a detail to update.\n[ Title , Author , Copies ]\n")

    match user_input.lower():
        case "title":
            util.clear()

            new_title = input("Update Panel\n\nOld Title: " + title + "\nNew Title: ")

            util.clear()

            confirm_changes = input("Update Panel\n\nOld book: Title: "
                                    + title + ", Author: "
                                    + author + ", Copies: "
                                    + str(copies) + "\nNew book: Title: "
                                    + new_title + ", Author: " + author + ", Copies: " + str(copies) + "\nConfirm changes [Y/N]\n")

            match confirm_changes.lower():
                case "exit"|"quit"|"cancel":
                    util.clear()
                    util.title()

                case "y"|"yes":
                    util.clear()
                    book_manager.update_book(book_id,new_title,author,copies)
                    input("Update Panel\n\nNew book: Title: " + title + ", Author: " + author + ", Copies: " + str(copies) + "\nChanges saved. Press enter to continue...")
                    util.clear()
                    util.title()

                case "n"|"no":
                    update_book()

        case "author"|"authors":
            #todo:Add logic
            pass

        case "copies":
            # todo:Add logic
            pass

        case "id":
            # todo:Add logic
            pass

    return

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
            delete_book()

        case "member"|"members":
            delete_member()

def delete_book():
    util.clear()

    user_input = input("Deletion Panel\n\nChoose a deletion method\n[ ID , Name ]\n\n")
    book = None

    match user_input.lower():
        case "id":
            _id = input("Deletion Panel\n\nSelect a book\n\nID: ")
            book = library.get_book_from_id(_id)

            if book is None:
                user_input = input("Error. No book found with that ID. Do you want to try again? [Y/N]")
                if user_input.lower() == "y" or user_input.lower() == "yes":
                    delete_book()
                else:
                    util.clear()
                    util.title()
                return
        case "name":
            name = input("Deletion Panel\n\nSelect a book\n\nName: ")
            book = library.get_book_from_string(name)

            if book is None:
                user_input = input("Error. No book found with that name. Do you want to try again? [Y/N]")
                if user_input.lower() == "y" or user_input.lower() == "yes":
                    delete_book()
                else:
                    util.clear()
                    util.title()
                return

    book_manager.delete_book(book.book_id)
    print("Book " + book.name + " with ID: " + str(book.book_id) + " has been deleted.")

def delete_member():
    util.clear()

    user_input = input("Deletion Panel\n\nChoose a deletion method\n[ ID , Name ]\n\n")
    member = None

    match user_input.lower():
        case "id":
            _id = input("Deletion Panel\n\nSelect a member\n\nID: ")
            member = library.get_member_from_id(_id)

            if member is None:
                user_input = input("Error. No member found with that ID. Do you want to try again? [Y/N]")
                if user_input.lower() == "y" or user_input.lower() == "yes":
                    delete_member()
                else:
                    util.clear()
                    util.title()
                return
        case "name":
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

    member_manager.delete_member(member.member_id)
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