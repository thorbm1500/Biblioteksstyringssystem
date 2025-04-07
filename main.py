from libraryClass import Library
from bookManager import BookManager
from memberManager import MemberManager
from util import Util

util = Util()

library = Library({},[])

book_manager = BookManager(library)
member_manager = MemberManager(library)

def prompt():
    user_input = util.user_input().lower()

    match user_input:
        case "exit"|"stop"|"shutdown"|"end"|"close"|"quit":
            util.clear_print("Goodbye.")
            return False

        case "help"|"help 1":
            util.clear_print("Prompts - Page 1\n  > help - Shows this list.\n  > exit - Shuts down the program.\n  > books - Prints a list of all books.\n  > members - Prints a list of all members.\n\nUse 'help 2' to go to the next page...")

        case "help 2":
            util.clear_print("Prompts - Page 2\n  > create - Create new books or members.\n  > delete - Delete books or members.\n  > update - Update books or members.\n\nUse 'help 3' to go to the next page...")

        case "help 3":
            util.clear_print("Prompts - Page 3\n  > rent - Rent a book.\n  > return - Return a book.")

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
            return_books()

        case _:
            util.clean("Error. '" + user_input + "' is not a known command. Press enter to continue...")

    return True

def return_books():
    user_input = util.user_input("Return a book\n\nSelect a member\n[ ID , Name ]\n\n")
    if util.is_cancelled(user_input): return

    match user_input.lower():
        case "id":
            member_id = util.user_input_get_integer("Return a book\n\nSelect a member\n\nID: ")
            if member_id is None: return

            member = library.get_member_from_id(member_id)

            if member is None:
                if util.retry("Return a book\n\nNo member found with that ID. Do you want to try again? [Y/N]\n\n"):
                    return_books()
                return

        case "name":
            name = util.user_input("Return a book\n\nSelect a member\n\nName: ")
            if util.is_cancelled(name): return

            member = library.get_member_from_string(name)

            if member is None:
                if util.retry("Return a book\n\nNo member found with that name. Do you want to try again? [Y/N]\n\n"):
                    return_books()
                return

        case _:
            if util.retry("Return a book\n\nUnknown selection. Do you want to try again? [Y/N]\n\n"):
                return_books()
            return

    user_input = util.user_input("Return a book\n\nMember selected: [" + str(member.member_id) + "] " + member.name + "\nPress enter to continue...")
    if util.is_cancelled(user_input): return

    if len(member.borrowed_books) < 1:
        util.clean("Return a book\n\nThis member has not borrowed any books. Press enter to continue...")
        return

    print("Return a book\n\nSelect a book")

    for book in member.borrowed_books:
        print("  [" + str(book.book_id) + "] " + book.title + " by " + book.author)

    book_id = util.user_input_get_integer("\nID: ")
    if book_id is None: return

    book = library.get_book_from_id(book_id)

    if book is None:
        if util.retry("Return a book\n\nNo book found with that ID. Do you want to try again? [Y/N]\n\n"):
            return_books()
        return

    if not member.is_borrowed(book):
        util.clean("Return a book\n\n[" + str(book.book_id) + "] by " + book.author + " is currently not being borrowed by " + member.name + ". Press enter to continue...")
    else:
        member.return_book(book)
        util.clean("Return a book\n\n[" + str(book.book_id) + "] by " + book.author + " has been returned from " + member.name + ". Press enter to continue...")
    return

def rent():
    user_input = util.user_input("Rent a book\n\nSelect a member\n[ ID , Name ]\n\n")
    if util.is_cancelled(user_input): return

    book = None

    match user_input.lower():
        case "id":
            member_id = util.user_input_get_integer("Rent a book\n\nSelect a member\n\nID: ")
            if member_id is None: return

            member = library.get_member_from_id(member_id)

            if member is None:
                if util.retry("Rent a book\n\nNo member found with that ID. Do you want to try again? [Y/N]\n\n"):
                    rent()
                return

        case "name":
            name = util.user_input("Rent a book\n\nSelect a member\n\nName: ")
            if util.is_cancelled(name): return
            member = library.get_member_from_string(name)

            if member is None:
                if util.retry("Rent a book\n\nNo member found with that name. Do you want to try again? [Y/N]\n\n"):
                    rent()
                return

        case _:
            if util.retry("Rent a book\n\nUnknown selection. Do you want to try again? [Y/N]\n\n"):
                rent()
            return

    util.clear_print("Rent a book\n\nMember selected: [" + str(member.member_id) + "] " + member.name + "\nPress enter to continue...")

    user_input = util.user_input("Rent a book\n\nSelect a book\n[ ID , Name ]\n\n")
    if util.is_cancelled(user_input): return

    match user_input.lower():
        case "id":
            book_id = util.user_input_get_integer("Rent a book\n\nSelect a book\n\nID: ")
            if book_id is None: return

            book = library.get_book_from_id(book_id)

            if book is None:
                if util.retry("Rent a book\n\nNo book found with that ID. Do you want to try again? [Y/N]\n\n"):
                    rent()
                return

        case "name":
            title = util.user_input("Rent a book\n\nSelect a book\n\nName: ")
            if util.is_cancelled(title): return

            book = library.get_book_from_string(title)

            if book is None:
                if util.retry("Rent a book\n\nNo book found with that name. Do you want to try again? [Y/N]\n\n"):
                    rent()
                return

    # Checks if any copies are available
    if library.get_copies(book.book_id) < 1:
        util.clean("Rent a book\n\nThe chosen book '" + book.title + "' has no available copies. Press enter to continue...")
        return

    # Checks if the member already has the book borrowed
    if member.borrowed_books is not None and member.is_borrowed(book):
        util.clean("Rent a book\n\nThis book has already been borrowed by this member. Press enter to continue...")
        return

    member.borrow_book(book)
    util.clean("Rent a book\n\n[" + str(member.member_id) + "] " + member.name + " has borrowed [" + str(book.book_id) + "] " + book.title + "\n\nPress enter to continue...")

def update():
    user_input = input("Update Panel\n\nChoose an object\n[ Book , Member ]\n\n")
    if util.is_cancelled(user_input): return

    match user_input.lower():
        case "book"|"books":
            update_book()

        case "member"|"members":
            update_member()

        case _:
            if util.retry("Update Panel\n\nUnknown selection. Do you want to try again? [Y/N]\n\n"):
                update()

def update_member():
    user_input = util.user_input("Update Panel\n\nChoose an update method\n[ ID , Name ]\n\n")
    if util.is_cancelled(user_input): return

    member = None

    match user_input.lower():
        case "id":
            member_id = util.user_input_get_integer("Update Panel\n\nSelect a member\n\nID: ")
            if member_id is None: return

            member = library.get_member_from_id(member_id)

            if member is None:
                if util.retry("Update Panel\n\nNo member found with that ID. Do you want to try again? [Y/N]\n\n"):
                    update_member()
                return

        case "name":
            name = util.user_input("Update Panel\n\nSelect a member\n\nName: ")
            if util.is_cancelled(name): return
            member = library.get_member_from_string(name)

            if member is None:
                if util.retry("Update Panel\n\nNo member found with that name. Do you want to try again? [Y/N]\n\n"):
                    update_member()
                return

    # Current and new member details
    old_member_id = new_member_id = member.member_id
    old_member_name = new_member_name = member.name

    user_input = util.user_input("Update Panel\n\nMember selected: [" + str(old_member_id) + "] " + str(old_member_name) + "\nPress enter to continue...")
    if util.is_cancelled(user_input): return

    user_input = util.user_input("Update Panel\n\nChoose a detail to update.\n[ ID , Name ]\n\n")
    if util.is_cancelled(user_input): return

    match user_input.lower():
        case "id":
            new_member_id = util.user_input_get_integer("Update Panel\n\nOld ID: " + str(old_member_id) + "\nNew ID: ")
            if new_member_id is None: return

            while not member_manager.check_id_availability(new_member_id):
                if util.retry("Update Panel\n\nID is already in use. Do you want to try again? [Y/N]\n\n"):
                    new_member_id = util.user_input_get_integer("Update Panel\n\nOld ID: " + str(old_member_id) + "\nNew ID: ")
                    if new_member_id is None: return
                else:
                    return

        case "name":
            util.clear()

            new_member_name = util.user_input("Update Panel\n\nOld name: " + old_member_name + "\nNew name: ")
            if util.is_cancelled(new_member_name): return

    confirm_changes = util.user_input("Update Panel\n\nOld details: ID: "
                                    + str(old_member_id) + ", Name: "
                                    + old_member_name + "\nNew Details: ID: "
                                    + str(new_member_id) + ", Name: "
                                    + new_member_name + "\nConfirm changes [Y/N]\n\n")

    if util.is_cancelled(confirm_changes): return

    while not util.legal_exec(confirm_changes):
        confirm_changes = util.user_input("Update Panel\n\nOld details: ID: "
                                    + str(old_member_id) + ", Name: "
                                    + old_member_name + "\nNew Details: ID: "
                                    + str(new_member_id) + ", Name: "
                                    + new_member_name + "\nConfirm changes [Y/N]\n\n")

    if util.is_cancelled(confirm_changes): return

    match confirm_changes.lower():
        case "y"|"yes":
            member_manager.update_member(old_member_id,new_member_id,new_member_name)
            util.clean("Update Panel\n\nNew details: ID: " + str(new_member_id) + ", Name: " + new_member_name + "\nChanges saved. Press enter to continue...")

        case "n"|"no":
            update()

        case _:
            util.clean()

def update_book():
    user_input = util.user_input("Update Panel\n\nChoose an update method\n[ ID , Title ]\n\n")
    if util.is_cancelled(user_input): return

    book = None

    match user_input.lower():
        case "id":
            book_id = util.user_input_get_integer("Update Panel\n\nSelect a book\n\nID: ")
            if book_id is None: return

            book = library.get_book_from_id(book_id)

            if book is None:
                if util.retry("Update Panel\n\nNo book found with that ID. Do you want to try again? [Y/N]\n\n"):
                    update_book()
                return

        case "title"|"name":
            name = util.user_input("Update Panel\n\nSelect a book\n\nTitle: ")
            if util.is_cancelled(name): return

            book = library.get_book_from_string(name)

            if book is None:
                if util.retry("Update Panel\n\nNo book found with that title. Do you want to try again? [Y/N]\n\n"):
                    update_book()
                return

    # Current and new book details
    old_book_id = new_book_id = book.book_id
    old_title = new_title = book.title
    old_author = new_author = book.author
    old_copies = new_copies = library.get_copies(old_book_id)

    user_input = util.user_input("Update Panel\n\nBook selected: [" + str(old_book_id) + "] " + str(old_title) + " by " + old_author + "\nPress enter to continue...")
    if util.is_cancelled(user_input): return

    user_input = util.user_input("Update Panel\n\nChoose a detail to update.\n[ ID , Title , Author , Copies ]\n")
    if util.is_cancelled(user_input): return

    match user_input.lower():
        case "title":
            new_title = util.user_input("Update Panel\n\nOld Title: " + old_title + "\nNew Title: ")
            if util.is_cancelled(new_title): return

        case "author"|"authors":
            new_author = util.user_input("Update Panel\n\nOld Author: " + old_author + "\nNew Author: ")
            if util.is_cancelled(new_author): return

        case "copies":
            new_copies = util.user_input_get_integer("Update Panel\n\nOld Copies: " + old_copies + "\nNew Title: ")
            if new_copies is None: return

        case "id":
            new_book_id = util.user_input_get_integer("Update Panel\n\nOld ID: " + str(old_book_id) + "\nNew ID: ")
            if new_book_id is None: return

    confirm_changes = util.user_input("Update Panel\n\nOld book: Title: "
                                    + old_title + ", Author: "
                                    + old_author + ", Copies: "
                                    + str(old_copies) + "\nNew book: Title: "
                                    + new_title + ", Author: " + new_author + ", Copies: "
                                    + str(new_copies) + "\nConfirm changes [Y/N]\n\n"),

    if util.is_cancelled(user_input): return

    while not util.legal_exec(confirm_changes):
        confirm_changes = util.user_input("Update Panel\n\nOld book: Title: "
                                + old_title + ", Author: "
                                + old_author + ", Copies: "
                                + str(old_copies) + "\nNew book: Title: "
                                + new_title + ", Author: " + new_author + ", Copies: "
                                + str(new_copies) + "\nConfirm changes [Y/N]\n\n")

    if util.is_cancelled(user_input): return

    match confirm_changes.lower():
        case "y"|"yes":
            book_manager.update_book(old_book_id,new_book_id,new_title,new_author,new_copies)
            book = library.get_book_from_id(new_book_id)
            util.clean("Update Panel\n\nNew book: Title: " + book.title + ", Author: " + book.author + ", Copies: " + str(library.get_copies(new_book_id)) + "\nChanges saved. Press enter to continue...")

        case "n"|"no":
            update()

def create():
    user_input = util.user_input("Creation Panel\n\nChoose an object\n[ Book , Member ]\n\n")
    if util.is_cancelled(user_input): return

    match user_input.lower():
        case "book"|"books":
            title = util.user_input("Creation Panel\n\nChoose a title.\n\nTitle: ")
            author = util.user_input("Creation Panel\n\nChoose an author.\n\nAuthor: ")
            copies = util.user_input("Creation Panel\n\nChoose number of copies.\n\nCopies: ")

            new_book_id = book_manager.new_book(title,author,copies)
            print("New book created.\n")
            library.display_book(new_book_id)
            util.clean("Press enter to continue...")

        case "member"|"members":
            name = util.user_input("Creation Panel\n\nChoose a name.\n\nName: ")
            new_member_id = member_manager.new_member(name)
            print("New member created.\n")
            library.display_member(new_member_id)
            util.clean("Press enter to continue...")

        case _:
            if util.retry("Creation Panel\n\nUnknown selection. Do you want to try again? [Y/N]\n\n"):
                create()
            return

def delete():
    user_input = input("Deletion Panel\n\nChoose an object\n[ Book , Member ]\n\n")
    if util.is_cancelled(user_input): return

    match user_input.lower():
        case "book"|"books":
            delete_book()

        case "member"|"members":
            delete_member()

        case _:
            if util.retry("Deletion Panel\n\nUnknown selection. Do you want to try again? [Y/N]\n\n"):
                delete()
            return

def delete_book():
    user_input = util.user_input("Deletion Panel\n\nChoose a deletion method\n[ ID , Name ]\n\n")
    if util.is_cancelled(user_input): return

    book = None

    match user_input.lower():
        case "id":
            book_id = util.user_input_get_integer("Deletion Panel\n\nSelect a book\n\nID: ")
            if book_id is None: return

            book = library.get_book_from_id(book_id)

            if book is None:
                if util.retry("Deletion Panel\n\nNo book found with that ID. Do you want to try again? [Y/N]\n\n"):
                    delete_book()
                return

        case "name":
            name = util.user_input("Deletion Panel\n\nSelect a book\n\nName: ")
            if util.is_cancelled(name): return

            book = library.get_book_from_string(name)

            if book is None:
                if util.retry("Deletion Panel\n\nNo book found with that name. Do you want to try again? [Y/N]\n\n"):
                    delete_book()
                return

    book_manager.delete_book(book.book_id)
    util.clean("Book " + book.title + " with ID: " + str(book.book_id) + " has been deleted.")

def delete_member():
    user_input = util.user_input("Deletion Panel\n\nChoose a deletion method\n[ ID , Name ]\n\n")
    if util.is_cancelled(user_input): return

    member = None

    match user_input.lower():
        case "id":
            member_id = util.user_input_get_integer("Deletion Panel\n\nSelect a member\n\nID: ")
            if member_id is None: return

            member = library.get_member_from_id(member_id)

            if member is None:
                if util.retry("Deletion Panel\n\nNo member found with that ID. Do you want to try again? [Y/N]\n\n"):
                    delete_member()
                return

        case "name":
            name = util.user_input("Deletion Panel\n\nSelect a member\n\nName: ")
            if util.is_cancelled(user_input): return

            member = library.get_member_from_string(name)

            if member is None:
                if util.retry("Deletion Panel\n\nNo member found with that name. Do you want to try again? [Y/N]\n\n"):
                    delete_member()
                return

    member_manager.delete_member(member.member_id)
    util.clean("Member " + member.name + " with ID: " + str(member.member_id) + " has been deleted.")

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