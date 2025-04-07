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
            rent()

        case "return"|"return book":
            #todo:Add returning books
            pass

        case _:
            print("Error. '" + user_input + "' is not a known command.")

    return True

def rent():
    util.clear()

    user_input = input("Rent a book\n\nSelect a member\n[ ID , Name ]\n\n")
    if util.is_cancelled(user_input): return

    member = None
    book = None

    util.clear()

    match user_input.lower():
        case "id":

            _id = input("Rent a book\n\nSelect a member\n\nID: ")

            try:
                _id = int(_id)
            except:
                user_input = input("Error. '" + str(_id) + "' is not an integer. Do you want to try again? [Y/N]\n\n")
                if user_input.lower().__contains__("y") or user_input.lower().__contains__("yes"):
                    rent()
                else:
                    util.clear()
                    util.title()
                return

            member = library.get_member_from_id(int(_id))

        case "name":
            name = input("Rent a book\n\nSelect a member\n\nName: ")

            member = library.get_member_from_string(name)

        case _:
            user_input = input("Rent a book\n\nUnknown selection. Do you want to try again? [Y/N]\n\n")
            if user_input.lower().__contains__("y") or user_input.lower().__contains__("yes"):
                rent()
            else:
                util.clear()
                util.title()
            return

    if member is None:
        user_input = input("Error. No member found with that ID. Do you want to try again? [Y/N]\n\n")
        if user_input.lower().__contains__("y") or user_input.lower().__contains__("yes"):
            delete_member()
        else:
            util.clear()
            util.title()
        return

    util.clear()

    user_input = input("Rent a book\n\nMember selected: [" + str(member.member_id) + "] " + member.name + "\nPress enter to continue...")
    if util.is_cancelled(user_input): return

    util.clear()

    user_input = input("Rent a book\n\nSelect a book\n[ ID , Name ]\n\n")
    if util.is_cancelled(user_input): return

    match user_input.lower():
        case "id":

            _id = input("Rent a book\n\nSelect a book\n\nID: ")

            try:
                _id = int(_id)
            except:
                user_input = input("Error. '" + str(_id) + "' is not an integer. Do you want to try again? [Y/N]\n\n")
                if user_input.lower().__contains__("y") or user_input.lower().__contains__("yes"):
                    rent()
                else:
                    util.clear()
                    util.title()
                return

            book = library.get_book_from_id(_id)

            if book is None:
                user_input = input("Error. No book found with that ID. Do you want to try again? [Y/N]\n\n")
                if user_input.lower().__contains__("y") or user_input.lower().__contains__("yes"):
                    update_book()
                else:
                    util.clear()
                    util.title()
                return

        case "name":
            name = input("Rent a book\n\nSelect a book\n\nName: ")

            book = library.get_book_from_string(name)

            if book is None:
                user_input = input("Error. No book found with that name. Do you want to try again? [Y/N]\n\n")
                if user_input.lower().__contains__("y") or user_input.lower().__contains__("yes"):
                    update_book()
                else:
                    util.clear()
                    util.title()
                return

    # Checks if any copies are available
    if library.get_copies(book.book_id) < 1:
        input("Rent a book\n\nThe chosen book '" + book.title + "' has no available copies. Press enter to continue...")
        util.clear()
        util.title()
        return

    # Checks if the member already has the book borrowed
    if member.borrowed_books is not None:
        if member.is_borrowed(book):
            input("Rent a book\n\nThis book has already been borrowed by this member. Press enter to continue...")
            util.clear()
            util.title()
            return

    member.borrow_book(book)

    util.clear()

    input("Rent a book\n\n[" + str(member.member_id) + "] " + member.name + " has borrowed [" + str(book.book_id) + "] " + book.title + "\n\nPress enter to continue...")

    util.clear()
    util.title()

def update():
    util.clear()

    user_input = input("Update Panel\n\nChoose an object\n[ Book , Member ]\n\n")
    if util.is_cancelled(user_input): return

    match user_input.lower():
        case "book"|"books":
            update_book()

        case "member"|"members":
            #todo:Add updating for members
            pass

        case _:
            input("Object: '" + str(user_input) + "' is unknown. Press enter to continue...")
            util.clear()
            util.title()
            return

def update_book():
    util.clear()

    user_input = input("Update Panel\n\nChoose an update method\n[ ID , Name ]\n\n")
    if util.is_cancelled(user_input): return

    book = None

    util.clear()

    match user_input.lower():
        case "id":
            _id = input("Update Panel\n\nSelect a book\n\nID: ")
            if util.is_cancelled(_id): return
            book = library.get_book_from_id(_id)

            if book is None:
                user_input = input("Error. No book found with that ID. Do you want to try again? [Y/N]\n\n")
                if user_input.lower().__contains__("y") or user_input.lower().__contains__("yes"):
                    update_book()
                else:
                    util.clear()
                    util.title()
                return

        case "name":
            name = input("Update Panel\n\nSelect a book\n\nName: ")
            if util.is_cancelled(name): return
            book = library.get_book_from_string(name)

            if book is None:
                user_input = input("Error. No book found with that name. Do you want to try again? [Y/N]\n\n")
                if user_input.lower().__contains__("y") or user_input.lower().__contains__("yes"):
                    update_book()
                else:
                    util.clear()
                    util.title()
                return

    util.clear()

    # Current and new book details
    old_book_id = new_book_id = book.book_id
    old_title = new_title = book.title
    old_author = new_author = book.author
    old_copies = new_copies = library.get_copies(old_book_id)

    user_input = input("Update Panel\n\nChoose a detail to update.\n[ ID , Title , Author , Copies ]\n")
    if util.is_cancelled(user_input): return

    match user_input.lower():
        case "title":
            util.clear()

            new_title = input("Update Panel\n\nOld Title: " + old_title + "\nNew Title: ")
            if util.is_cancelled(new_title): return

        case "author"|"authors":
            util.clear()

            new_author = input("Update Panel\n\nOld Author: " + old_author + "\nNew Author: ")
            if util.is_cancelled(new_author): return

        case "copies":
            util.clear()

            new_copies = input("Update Panel\n\nOld Copies: " + old_copies + "\nNew Title: ")
            if util.is_cancelled(new_copies): return

            try:
                new_copies = int(new_copies)
            except:
                user_input = input("Error. '" + str(new_copies) + "' is not an integer. Do you want to try again? [Y/N]\n\n")
                if user_input.lower().__contains__("y" or "yes"):
                    update()
                else:
                    util.clear()
                    util.title()
                return

        case "id":
            util.clear()

            new_book_id = input("Update Panel\n\nOld ID: " + str(old_book_id) + "\nNew ID: ")
            if util.is_cancelled(new_book_id): return

            try:
                new_book_id = int(new_book_id)
            except:
                user_input = input("Error. '" + str(new_book_id) + "' is not an integer. Do you want to try again? [Y/N]\n\n")
                if user_input.lower().__contains__("y" or "yes"):
                    update()
                else:
                    util.clear()
                    util.title()
                return

    util.clear()

    confirm_changes = input("Update Panel\n\nOld book: Title: "
                                    + old_title + ", Author: "
                                    + old_author + ", Copies: "
                                    + str(old_copies) + "\nNew book: Title: "
                                    + new_title + ", Author: " + new_author + ", Copies: "
                                    + str(new_copies) + "\nConfirm changes [Y/N]\n\n")

    while not util.legal_exec(confirm_changes):
        util.clear()
        confirm_changes = input("Update Panel\n\nOld book: Title: "
                                + old_title + ", Author: "
                                + old_author + ", Copies: "
                                + str(old_copies) + "\nNew book: Title: "
                                + new_title + ", Author: " + new_author + ", Copies: "
                                + str(new_copies) + "\nConfirm changes [Y/N]\n\n")

    if util.is_cancelled(user_input): return

    match confirm_changes.lower():
        case "y"|"yes":
            util.clear()
            book_manager.update_book(old_book_id,new_book_id,new_title,new_author,new_copies)
            book = library.get_book_from_id(new_book_id)
            input("Update Panel\n\nNew book: Title: " + book.title + ", Author: " + book.author + ", Copies: " + str(library.get_copies(new_book_id)) + "\nChanges saved. Press enter to continue...")
            util.clear()
            util.title()

        case "n"|"no":
            update()

    return

def create():
    util.clear()

    user_input = input("Creation Panel\n\nChoose an object\n[ Book , Member ]\n\n")
    if util.is_cancelled(user_input): return

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
    if util.is_cancelled(user_input): return

    match user_input.lower():
        case "book"|"books":
            delete_book()

        case "member"|"members":
            delete_member()

def delete_book():
    util.clear()

    user_input = input("Deletion Panel\n\nChoose a deletion method\n[ ID , Name ]\n\n")
    if util.is_cancelled(user_input): return

    book = None

    match user_input.lower():
        case "id":
            _id = input("Deletion Panel\n\nSelect a book\n\nID: ")
            book = library.get_book_from_id(_id)

            if book is None:
                user_input = input("Error. No book found with that ID. Do you want to try again? [Y/N]\n\n")
                if user_input.lower().__contains__("y") or user_input.lower().__contains__("yes"):
                    delete_book()
                else:
                    util.clear()
                    util.title()
                return
        case "name":
            name = input("Deletion Panel\n\nSelect a book\n\nName: ")
            book = library.get_book_from_string(name)

            if book is None:
                user_input = input("Error. No book found with that name. Do you want to try again? [Y/N]\n\n")
                if user_input.lower().__contains__("y") or user_input.lower().__contains__("yes"):
                    delete_book()
                else:
                    util.clear()
                    util.title()
                return

    book_manager.delete_book(book.book_id)
    print("Book " + book.title + " with ID: " + str(book.book_id) + " has been deleted.")

def delete_member():
    util.clear()

    user_input = input("Deletion Panel\n\nChoose a deletion method\n[ ID , Name ]\n\n")
    if util.is_cancelled(user_input): return

    member = None

    match user_input.lower():
        case "id":
            _id = input("Deletion Panel\n\nSelect a member\n\nID: ")
            member = library.get_member_from_id(_id)

            if member is None:
                user_input = input("Error. No member found with that ID. Do you want to try again? [Y/N]\n\n")
                if user_input.lower().__contains__("y") or user_input.lower().__contains__("yes"):
                    delete_member()
                else:
                    util.clear()
                    util.title()
                return
        case "name":
            name = input("Deletion Panel\n\nSelect a member\n\nName: ")
            member = library.get_member_from_string(name)

            if member is None:
                user_input = input("Error. No member found with that name. Do you want to try again? [Y/N]\n\n")
                if user_input.lower().__contains__("y") or user_input.lower().__contains__("yes"):
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
    book_manager.new_book("The Great Gatsby", "F. Scott Fitzgerald", 786)
    book_manager.new_book("One Hundred Years of Solitude", "Gabriel García Márquez", 13)
    book_manager.new_book("Don Quixote", "Miguel de Cervantes", 6023)
    book_manager.new_book("The Lord of the Rings", "J. R. R. Tolkien", 2345)

    member_manager.new_member("Thor Møller")
    member_manager.new_member("Emily Brontë")
    member_manager.new_member("Leo Tolstoy")
    member_manager.new_member("Fyodor Dostoevsky")
    member_manager.new_member("William Faulkner")
    member_manager.new_member("Albert Camus")

def main():
    initialize_library()
    util.title()
    while prompt():
        pass

if __name__ == "__main__":
    main()