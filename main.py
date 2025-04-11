# Imports various classes.
from libraryClass import Library
from bookManager import BookManager
from memberManager import MemberManager
from util import Util
from test import Test

# Initializes various classes.
util = Util()
library = Library(util)
book_manager = BookManager(library, util)
member_manager = MemberManager(library, util)
test = Test(library,book_manager,member_manager)

def prompt():
    """Prompts the user with all available features. Returns True or False, whether the user should be prompted again or not"""
    user_input = util.user_input().lower()
    # Matches the user's input against predefined options.
    match user_input:
        case "exit"|"stop"|"shutdown"|"end"|"close"|"quit":
            util.clear_print("Goodbye.")
            # Returns False to indicate the end of execution.
            return False

        case "help"|"help 1":
            util.clear_print("Prompts - Page 1\n  > help - Shows this list.\n  > exit - Shuts down the program.\n  > books - Prints a list of all books.\n  > members - Prints a list of all members.\n\nUse 'help 2' to go to the next page...")

        case "help 2":
            util.clear_print("Prompts - Page 2\n  > create - Create new books or members.\n  > delete - Delete books or members.\n  > update - Update books or members.\n\nUse 'help 3' to go to the next page...")

        case "help 3":
            util.clear_print("Prompts - Page 3\n  > rent - Rent a book.\n  > return - Return a book.")

        case "books":
            # Prints title.
            print("Zealand Library - Book Index. 'books -v' to show all details.")
            # Displays details about all books in the library.
            library.display_books()

        case "books -v"|"books verbose":
            # Displays a verbose list of all books in the library.
            display_books_verbose()

        case "members":
            # Prints title and all members and their details.
            print("Zealand Library - Member Index.")
            # Displays all members in the library.
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

        case "clear"|"cls"|"clean"|"":
            # Cleans the screen.
            util.clean()

        case _:
            util.clean(f"[Error] '{user_input}' is not a known command. Press enter to continue...")
    # Returns True to indicate continued execution.
    return True

def display_books_verbose():
    # Prints title.
    print("Zealand Library - Book Index.")
    # Iterates through all books in the library.
    for book in library.books:
        # Prints the book's details and 'Borrowed by:'.
        book.display_info(library)
        print("      | Borrowed by:")
        # Checks if the book is currently being borrowed by anyone.
        if library.is_borrowed(book):
            # Iterates through all members in the library.
            for member in library.members:
                # Checks if the member is currently borrowing the book, and prints their name if they're borrowing the book.
                if member.is_borrowed(book):
                    print(f"              [{member.member_id}] {member.name}")
            print("")
        # Prints 'None' if noone is currently borrowing the book.
        else:
            print("                    None\n")

def return_books():
    # Prompts the user to select a method for selecting the member.
    user_input = util.user_input("Return a book\n\nSelect a member\n[ ID , Name ]\n\n")
    # Checks if the user wishes to cancel.
    if util.is_cancelled(user_input): return
    # Matches the user's input against predefined options.
    match user_input.lower():
        case "id":
            # Prompts the user to input an ID and only accepts integer.
            member_id = util.user_input_get_integer("Return a book\n\nSelect a member\n\nID: ")
            # Checks if an ID is present and otherwise returns as None indicates that the user wishes to exit to the main menu.
            if member_id is None: return
            # Gets the member from the library.
            member = library.get_member_from_id(member_id)
            # Checks if an instance of the member is present.
            if member is None:
                # Prompts the user with an option to retry.
                if util.retry("Return a book\n\nNo member found with that ID. Do you want to try again? [Y/N]\n\n"):
                    # Restarts the process for the user.
                    return_books()
                return

        case "name":
            # Prompts the user to input a name for the member they wish to select.
            name = util.user_input("Return a book\n\nSelect a member\n\nName: ")
            # Checks if the user wishes to cancel.
            if util.is_cancelled(name): return
            # Gets the member.
            member = library.get_member_from_string(name)
            # Checks if an instance of the member is present.
            if member is None:
                # Prompts the user with an option to retry.
                if util.retry("Return a book\n\nNo member found with that name. Do you want to try again? [Y/N]\n\n"):
                    # Restarts the process for the user.
                    return_books()
                return

        case _:
            # Prompts the user with an option to retry.
            if util.retry("Return a book\n\nUnknown selection. Do you want to try again? [Y/N]\n\n"):
                # Restarts the process for the user.
                return_books()
            return
    # Informs the user of the member that's been selected.
    user_input = util.user_input(f"Return a book\n\nMember selected: [{member.member_id}] {member.name}\nPress enter to continue...")
    # Checks if the user wishes to cancel.
    if util.is_cancelled(user_input): return
    # Checks if the member is currently borrowing any books
    if not member.is_borrowing():
        util.clean("Return a book\n\nThis member has not borrowed any books. Press enter to continue...")
        return
    # Prints a title.
    print("Return a book\n\nSelect a book")
    # Iterates
    for book in member.borrowed_books:
        print(f"  [{book.book_id}] {book.title} by {book.author}")
    # Prompts the user to input an ID and only accepts integer.
    book_id = util.user_input_get_integer("\nID: ")
    # Checks if an ID is present and otherwise returns as None indicates that the user wishes to exit to the main menu.
    if book_id is None: return
    # Gets the book from the library.
    book = library.get_book_from_id(book_id)
    # Checks if an instance of the book is present.
    if book is None:
        # Prompts the user with an option to retry.
        if util.retry("Return a book\n\nNo book found with that ID. Do you want to try again? [Y/N]\n\n"):
            # Restarts the process for the user.
            return_books()
        return
    # Checks if the member is currently borrowing the book before attempting to return it.
    if not member.is_borrowed(book):
        util.clean(f"Return a book\n\n[{book.book_id}] by {book.author} is currently not being borrowed by {member.name}. Press enter to continue...")
    else:
        # Returns the book
        library.return_book(book.book_id, member)
        util.clean(f"Return a book\n\n[{book.book_id}] by {book.author} has been returned from {member.name}. Press enter to continue...")
    return

def rent():
    # Prompts the user to select a method for choosing the member.
    user_input = util.user_input("Rent a book\n\nSelect a member\n[ ID , Name ]\n\n")
    # Checks if the user wishes to cancel.
    if util.is_cancelled(user_input): return
    # Matches the user's input against predefined options.
    match user_input.lower():
        case "id":
            # Prompts the user to input an ID and only accepts integer.
            member_id = util.user_input_get_integer("Rent a book\n\nSelect a member\n\nID: ")
            # Checks if an ID is present and otherwise returns as None indicates that the user wishes to exit to the main menu.
            if member_id is None: return
            # Gets the member from the library.
            member = library.get_member_from_id(member_id)
            # Checks if an instance of the member is present.
            if member is None:
                # Prompts the user with an option to retry.
                if util.retry("Rent a book\n\nNo member found with that ID. Do you want to try again? [Y/N]\n\n"):
                    # Restarts the process for the user.
                    rent()
                return

        case "name":
            # Prompts the user to input a name for the member they wish to select.
            name = util.user_input("Rent a book\n\nSelect a member\n\nName: ")
            # Checks if the user wishes to cancel.
            if util.is_cancelled(name): return
            # Gets the member from the library.
            member = library.get_member_from_string(name)
            # Checks if the member is present.
            if member is None:
                # Prompts the user with an option to retry.
                if util.retry("Rent a book\n\nNo member found with that name. Do you want to try again? [Y/N]\n\n"):
                    # Restarts the process for the user.
                    rent()
                return

        case _:
            # Prompts the user with an option to retry.
            if util.retry("Rent a book\n\nUnknown selection. Do you want to try again? [Y/N]\n\n"):
                # Restarts the process for the user.
                rent()
            return
    # Informs the user of the member they've selected.
    util.user_input(f"Rent a book\n\nMember selected: [{member.member_id}] {member.name}\nPress enter to continue...")
    # Prompts the user to select a method for choosing the book.
    user_input = util.user_input("Rent a book\n\nSelect a book\n[ ID , Name ]\n\n")
    # Checks if the user wishes to cancel.
    if util.is_cancelled(user_input): return
    # Matches the user's input against predefined options.
    match user_input.lower():
        case "id":
            book = None
            # Continues to prompt the user for a valid ID until they exit or provide a valid ID.
            while book is None:
                # Prompts the user to input an ID and only accepts integer.
                book_id = util.user_input_get_integer("Rent a book\n\nSelect a book\n\nID: ")
                # Checks if an ID is present and otherwise returns as None indicates that the user wishes to exit to the main menu.
                if book_id is None: return
                # Gets the book from the library.
                book = library.get_book_from_id(book_id)
                # Checks if an instance of the book is present.
                if book is None:
                    # Prompts the user with an option to retry.
                    if not util.retry("Rent a book\n\nNo book found with that ID. Do you want to try again? [Y/N]\n"): return

        case "name":
            title = util.user_input("Rent a book\n\nSelect a book\n\nName: ")
            # Checks if the user wishes to cancel.
            if util.is_cancelled(title): return
            # Gets the book from the library.
            book = library.get_book_from_string(title)
            # Checks if an instance of the book is present.
            if book is None:
                # Prompts the user with an option to retry.
                if util.retry("Rent a book\n\nNo book found with that name. Do you want to try again? [Y/N]\n\n"):
                    # Restarts the process for the user.
                    rent()
                return
        
        case _:
            # Prompts the user with an option to retry.
            if util.retry("Rent a book\n\nUnknown selection. Do you want to try again? [Y/N]\n\n"):
                # Restarts the process for the user.
                rent()
            return

    # Checks if any copies are available.
    if library.get_copies(book.book_id) < 1:
        util.clean(f"Rent a book\n\n[{book.book_id}] {book.title} has no available copies. Press enter to continue...")
        return

    # Checks if the member already has the book borrowed.
    if member.borrowed_books is not None and member.is_borrowed(book):
        util.clean(f"Rent a book\n\n{member.name} is already borrowing {book.title}. Press enter to continue...")
        return
    # Issues the selected book to the selected member.
    library.issue_book(book.book_id, member)
    # Informs the user of the completed action.
    util.clean(f"Rent a book\n\n[{member.member_id}] {member.name} has borrowed [{book.book_id}] {book.title}\n\nPress enter to continue...")

def update():
    # Prompts the user to choose which object they want to update.
    user_input = input("Update Panel\n\nChoose an object\n[ Book , Member ]\n\n")
    # Checks if the user wishes to cancel.
    if util.is_cancelled(user_input): return
    # Matches the user's input against predefined options.
    match user_input.lower():
        case "book"|"books":
            update_book()

        case "member"|"members":
            update_member()

        case _:
            # Prompts the user with an option to retry.
            if util.retry("Update Panel\n\nUnknown selection. Do you want to try again? [Y/N]\n\n"):
                # Restarts the process for the user.
                update()
            return

def update_member():
    # Prompts the user to choose a method for choosing the member.
    user_input = util.user_input("Update Panel\n\nChoose an update method\n[ ID , Name ]\n\n")
    # Checks if the user wishes to cancel.
    if util.is_cancelled(user_input): return
    # Matches the user's input against predefined options.
    match user_input.lower():
        case "id":
            # Prompts the user to input an ID and only accepts integer.
            member_id = util.user_input_get_integer("Update Panel\n\nSelect a member\n\nID: ")
            # Checks if an ID is present and otherwise returns as None indicates that the user wishes to exit to the main menu.
            if member_id is None: return
            # Gets the member from the library.
            member = library.get_member_from_id(member_id)
            # Checks if an instance of the member is present.
            if member is None:
                # Prompts the user with an option to retry.
                if util.retry("Update Panel\n\nNo member found with that ID. Do you want to try again? [Y/N]\n\n"):
                    # Restarts the process for the user.
                    update_member()
                return

        case "name":
            # Prompts the user to input a name for the member they wish to select.
            name = util.user_input("Update Panel\n\nSelect a member\n\nName: ")
            # Checks if the user wishes to cancel.
            if util.is_cancelled(name): return
            # Gets the member from the library.
            member = library.get_member_from_string(name)
            # Checks if an instance of the member is present.
            if member is None:
                # Prompts the user with an option to retry.
                if util.retry("Update Panel\n\nNo member found with that name. Do you want to try again? [Y/N]\n\n"):
                    # Restarts the process for the user.
                    update_member()
                return
        
        case _:
            # Prompts the user with an option to retry.
            if util.retry("Update Panel\n\nUnknown selection. Do you want to try again? [Y/N]\n\n"):
                # Restarts the process for the user.
                update_member()
            return

    # Current and new member details
    old_member_id = new_member_id = member.member_id
    old_member_name = new_member_name = member.name
    # Informs the user of their member selection.
    user_input = util.user_input(f"Update Panel\n\nMember selected: [{old_member_id}] {old_member_name}\nPress enter to continue...")
    # Checks if the user wishes to cancel.
    if util.is_cancelled(user_input): return
    # Prompts the user to choose what they wish to update.
    user_input = util.user_input("Update Panel\n\nChoose a detail to update.\n[ ID , Name ]\n\n")
    # Checks if the user wishes to cancel.
    if util.is_cancelled(user_input): return
    # Matches the user's input against predefined options.
    match user_input.lower():
        case "id":
            # Prompts the user to input an ID and only accepts integer.
            new_member_id = util.user_input_get_integer(f"Update Panel\n\nOld ID: {old_member_id}\nNew ID: ")
            # Checks if an ID is present and otherwise returns as None indicates that the user wishes to exit to the main menu.
            if new_member_id is None: return
            # Continues to prompt the user for a valid ID until they either exit or provide a valid ID.
            while not member_manager.check_id_availability(new_member_id):
                # Prompts the user with an option to retry.
                if util.retry("Update Panel\n\nID is already in use. Do you want to try again? [Y/N]\n\n"):
                    # Prompts the user to input an ID and only accepts integer.
                    new_member_id = util.user_input_get_integer(f"Update Panel\n\nOld ID: {old_member_id}\nNew ID: ")
                    # Checks if an ID is present and otherwise returns as None indicates that the user wishes to exit to the main menu.
                    if new_member_id is None: return
                else: return

        case "name":
            # Prompts the user for a new name for the selected member.
            new_member_name = util.user_input(f"Update Panel\n\nOld name: {old_member_name}\nNew name: ")
            # Checks if the user wishes to cancel.
            if util.is_cancelled(new_member_name): return
    
        case _:
            # Prompts the user with an option to retry.
            if util.retry("Update Panel\n\nUnknown selection. Do you want to try again? [Y/N]\n\n"):
                # Restarts the process for the user.
                update_member()
            return
    
    confirm_changes = None
    # Continues to prompt the user to confirm the changes until they provide a valid response.
    while not util.legal_exec(confirm_changes):
        confirm_changes = util.user_input(f"Update Panel\n\nOld details: ID: {old_member_id}, Name: {old_member_name}\nNew Details: ID: {new_member_id}, Name: {new_member_name}\nConfirm changes [Y/N]\n\n")
    # Checks if the user wishes to cancel.
    if util.is_cancelled(confirm_changes): return
    # Matches the user's input against predefined options.
    match confirm_changes.lower():
        case "y"|"yes":
            # Updates the selected member with the provided new details.
            member_manager.update_member(old_member_id,new_member_id,new_member_name)
            util.clean(f"Update Panel\n\nNew details: ID: {new_member_id}, Name: {new_member_name}\nChanges saved. Press enter to continue...")

        case "n"|"no":
            util.clean(f"Update Panel\n\nNew details: ID: {new_member_id}, Name: {new_member_name}\nChanges discarded. Press enter to continue...")

        case _:
            util.clean()

def update_book():
    # Prompts the user to choose what they wish to update.
    user_input = util.user_input("Update Panel\n\nChoose an update method\n[ ID , Title ]\n\n")
    # Checks if the user wishes to cancel.
    if util.is_cancelled(user_input): return
    # Matches the user's input against predefined options.
    match user_input.lower():
        case "id":
            # Prompts the user to input an ID and only accepts integer.
            book_id = util.user_input_get_integer("Update Panel\n\nSelect a book\n\nID: ")
            # Checks if an ID is present and otherwise returns as None indicates that the user wishes to exit to the main menu.
            if book_id is None: return
            # Gets the book from the library.
            book = library.get_book_from_id(book_id)
            # Checks if an instance of the book is present.
            if book is None:
                # Prompts the user with an option to retry.
                if util.retry("Update Panel\n\nNo book found with that ID. Do you want to try again? [Y/N]\n\n"):
                    # Restarts the process for the user.
                    update_book()
                return

        case "title"|"name":
            # Prompts the user to input a title for the book they wish to select.
            name = util.user_input("Update Panel\n\nSelect a book\n\nTitle: ")
            # Checks if the user wishes to cancel.
            if util.is_cancelled(name): return
            # Gets the book from the library.
            book = library.get_book_from_string(name)
            # Checks if an instance of the book is present.
            if book is None:
                # Prompts the user with an option to retry.
                if util.retry("Update Panel\n\nNo book found with that title. Do you want to try again? [Y/N]\n\n"):
                    # Restarts the process for the user.
                    update_book()
                return
        
        case _:
            # Prompts the user with an option to retry.
            if util.retry("Update Panel\n\nUnknown selection. Do you want to try again? [Y/N]\n\n"):
                # Restarts the process for the user.
                update_book()
            return

    # Current and new book details.
    old_book_id = new_book_id = book.book_id
    old_title = new_title = book.title
    old_author = new_author = book.author
    old_copies = new_copies = library.get_copies(old_book_id)
    # Informs the user of the book they've selected.
    user_input = util.user_input(f"Update Panel\n\nBook selected: [{old_book_id}] {old_title} by {old_author}\nPress enter to continue...")
    # Checks if the user wishes to cancel.
    if util.is_cancelled(user_input): return
    # Prompts the user to choose what they wish to update.
    user_input = util.user_input("Update Panel\n\nChoose a detail to update.\n[ ID , Title , Author , Copies ]\n")
    # Checks if the user wishes to cancel.
    if util.is_cancelled(user_input): return
    # Matches the user's input against predefined options.
    match user_input.lower():
        case "title":
            # Prompts the user to input a new title.
            new_title = util.user_input(f"Update Panel\n\nOld Title: {old_title}\nNew Title: ")
            # Checks if the user wishes to cancel.
            if util.is_cancelled(new_title): return

        case "author"|"authors":
            # Prompts the user to input a new author.
            new_author = util.user_input(f"Update Panel\n\nOld Author: {old_author}\nNew Author: ")
            # Checks if the user wishes to cancel.
            if util.is_cancelled(new_author): return

        case "copies":
            # Prompts the user to input a new number of available copies and only accepts integer.
            new_copies = util.user_input_get_integer(f"Update Panel\n\nOld Copies: {old_copies}\nNew Title: ")
            # Checks if an ID is present and otherwise returns as None indicates that the user wishes to exit to the main menu.
            if new_copies is None: return

        case "id":
            # Prompts the user to input a new ID and only accepts integer.
            new_book_id = util.user_input_get_integer(f"Update Panel\n\nOld ID: {old_book_id}\nNew ID: ")
            # Checks if an ID is present and otherwise returns as None indicates that the user wishes to exit to the main menu.
            if new_book_id is None: return
        
        case _:
            # Prompts the user with an option to retry.
            if util.retry("Update Panel\n\nUnknown selection. Do you want to try again? [Y/N]\n\n"):
                # Restarts the process for the user.
                update_book()
            return

    confirm_changes = None
    # Continues to prompt the user to confirm the changes until they provide a valid response.
    while not util.legal_exec(confirm_changes):
        confirm_changes = util.user_input(f"Update Panel\n\nOld book: Title: {old_title}, Author: {old_author}, Copies: {old_copies}\n"
            + f"New book: Title: {new_title}, Author: {new_author}, Copies: {new_copies}\nConfirm changes [Y/N]\n\n")
    # Checks if the user wishes to cancel.
    if util.is_cancelled(user_input): return
    # Matches the user's input against predefined options.
    match confirm_changes.lower():
        case "y"|"yes":
            # Updates the selected book with the new provided details.
            book_manager.update_book(old_book_id,new_book_id,new_title,new_author,new_copies)
            # Gets the book from the library.
            book = library.get_book_from_id(new_book_id)
            util.clean(f"Update Panel\n\nNew book: Title: {book.title}, Author: {book.author}, Copies: {library.get_copies(new_book_id)}\nChanges saved. Press enter to continue...")

        case "n"|"no":
            util.clean(f"Update Panel\n\nNew book: Title: {book.title}, Author: {book.author}, Copies: {library.get_copies(new_book_id)}\nChanges discarded. Press enter to continue...")
        
        case _:
            # Prompts the user with an option to retry.
            if util.retry("Update Panel\n\nUnknown selection. Do you want to try again? [Y/N]\n\n"):
                # Restarts the process for the user.
                update_book()
            return

def create():
    # Prompts the user to choose which type of object they wish to create.
    user_input = util.user_input("Creation Panel\n\nChoose an object\n[ Book , Member ]\n\n")
    # Checks if the user wishes to cancel.
    if util.is_cancelled(user_input): return
    # Matches the user's input against predefined options.
    match user_input.lower():
        case "book"|"books":
            # Prompts the user to input details for the new book.
            title = util.user_input("Creation Panel\n\nChoose a title.\n\nTitle: ")
            author = util.user_input("Creation Panel\n\nChoose an author.\n\nAuthor: ")
            copies = util.user_input("Creation Panel\n\nChoose number of copies.\n\nCopies: ")
            # Creates the new book with the provided details.
            new_book_id = book_manager.new_book(title,author,copies)
            # Prints information that the book has been created and what it's details are.
            print("New book created.\n")
            library.display_book(new_book_id)
            util.clean("Press enter to continue...")

        case "member"|"members":
            # Prompts the user to select a name for the new member.
            name = util.user_input("Creation Panel\n\nChoose a name.\n\nName: ")
            # Creates the new member.
            new_member_id = member_manager.new_member(name)
            # Prints information that the member has been created and what it's details are.
            print("New member created.\n")
            library.display_member(new_member_id)
            util.clean("Press enter to continue...")

        case _:
            # Prompts the user with an option to retry.
            if util.retry("Creation Panel\n\nUnknown selection. Do you want to try again? [Y/N]\n\n"):
                # Restarts the process for the user.
                create()
            return

def delete():
    # Prompts the user to choose which type of object they wish to delete.
    user_input = input("Removal Panel\n\nChoose an object\n[ Book , Member ]\n\n")
    # Checks if the user wishes to cancel.
    if util.is_cancelled(user_input): return
    # Matches the user's input against predefined options.
    match user_input.lower():
        case "book"|"books":
            delete_book()

        case "member"|"members":
            delete_member()

        case _:
            # Prompts the user with an option to retry.
            if util.retry("Removal Panel\n\nUnknown selection. Do you want to try again? [Y/N]\n\n"):
                # Restarts the process for the user.
                delete()
            return

def delete_book():
    # Prompts the user to choose a method for selecting the book.
    user_input = util.user_input("Removal Panel\n\nSelect a book\n[ ID , Name ]\n\n")
    # Checks if the user wishes to cancel.
    if util.is_cancelled(user_input): return
    # Matches the user's input against predefined options.
    match user_input.lower():
        case "id":
            # Prompts the user to input an ID and only accepts integer.
            book_id = util.user_input_get_integer("Removal Panel\n\nSelect a book\n\nID: ")
            # Checks if an ID is present and otherwise returns as None indicates that the user wishes to exit to the main menu.
            if book_id is None: return
            # Gets the book from the library.
            book = library.get_book_from_id(book_id)
            # Checks if an instance of the book is present.
            if book is None:
                # Prompts the user with an option to retry.
                if util.retry("Removal Panel\n\nNo book found with that ID. Do you want to try again? [Y/N]\n\n"):
                    # Restarts the process for the user.
                    delete_book()
                return

        case "name":
            # Prompts the user to input a name for the book they wish to select.
            name = util.user_input("Removal Panel\n\nSelect a book\n\nName: ")
            # Checks if the user wishes to cancel.
            if util.is_cancelled(name): return
            # Gets the book from the library.
            book = library.get_book_from_string(name)
            # Checks if an instance of the book is present.
            if book is None:
                # Prompts the user with an option to retry.
                if util.retry("Removal Panel\n\nNo book found with that name. Do you want to try again? [Y/N]\n\n"):
                    # Restarts the process for the user.
                    delete_book()
                return
        
        case _:
            # Prompts the user with an option to retry.
            if util.retry("Removal Panel\n\nUnknown selection. Do you want to try again? [Y/N]\n\n"):
                # Restarts the process for the user.
                delete_book()
            return
    # Deletes the book from the library and removes it from all members that may currently be borrowing it.
    book_manager.delete_book(book.book_id)
    util.clean(f"Book {book.title} with ID: {book.book_id} has been deleted.")

def delete_member():
    # Prompts the user to choose a method for selecting the member.
    user_input = util.user_input("Removal Panel\n\nSelect a member\n[ ID , Name ]\n\n")
    # Checks if the user wishes to cancel.
    if util.is_cancelled(user_input): return
    # Matches the user's input against predefined options.
    match user_input.lower():
        case "id":
            # Prompts the user to input an ID and only accepts integer.
            member_id = util.user_input_get_integer("Removal Panel\n\nSelect a member\n\nID: ")
            # Checks if an ID is present and otherwise returns as None indicates that the user wishes to exit to the main menu.
            if member_id is None: return
            # Gets the member from the library.
            member = library.get_member_from_id(member_id)
            # Checks if an instance of the member is present.
            if member is None:
                # Prompts the user with an option to retry.
                if util.retry("Removal Panel\n\nNo member found with that ID. Do you want to try again? [Y/N]\n\n"):
                    # Restarts the process for the user.
                    delete_member()
                return

        case "name":
            # Prompts the user to input a name for the member they wish to select.
            name = util.user_input("Removal Panel\n\nSelect a member\n\nName: ")
            # Checks if the user wishes to cancel.
            if util.is_cancelled(user_input): return
            # Gets the member from the library.
            member = library.get_member_from_string(name)
            # Checks if an instance of the member is present.
            if member is None:
                # Prompts the user with an option to retry.
                if util.retry("Removal Panel\n\nNo member found with that name. Do you want to try again? [Y/N]\n\n"):
                    # Restarts the process for the user.
                    delete_member()
                return
        
        case _:
            # Prompts the user with an option to retry.
            if util.retry("Removal Panel\n\nUnknown selection. Do you want to try again? [Y/N]\n\n"):
                # Restarts the process for the user.
                delete_member()
            return
    # Deletes the member selected and informs the user of the completed action.
    member_manager.delete_member(member.member_id)
    util.clean(f"Member {member.name} with ID: {member.member_id} has been deleted.")

def initialize_library():
    # Resets the current ID in the Book Manager.
    book_manager.update_book_id()
    # Creates all the default books the library comes with.
    book_manager.new_book("Harry Potter","J.K. Rowling",32)
    book_manager.new_book("Game of Thrones","George R.R. Martin",512)
    book_manager.new_book("Twilight","Stephanie Mayers",363)
    book_manager.new_book("The Great Gatsby", "F. Scott Fitzgerald", 786)
    book_manager.new_book("One Hundred Years of Solitude", "Gabriel García Márquez", 13)
    book_manager.new_book("Don Quixote", "Miguel de Cervantes", 6023)
    book_manager.new_book("The Lord of the Rings", "J. R. R. Tolkien", 2345)
    # Resets the current ID in the Member Manager.
    member_manager.update_member_id()
    # Creates all the default members the library comes with.
    member_manager.new_member("Thor Møller")
    member_manager.new_member("Emily Brontë")
    member_manager.new_member("Leo Tolstoy")
    member_manager.new_member("Fyodor Dostoevsky")
    member_manager.new_member("William Faulkner")
    member_manager.new_member("Albert Camus")

def main():
    # Runs the pre-test for the program and exits the program if the test fails.
    if not test.run():
        input("\n\nPre-testing failed. Program stopped. Press enter to exit...")
        return
    # Initializes the library with default values.
    initialize_library()
    # Prints the title.
    util.title()
    # Prompts the user and continues to do so, until the user decides to exit the program.
    while prompt():
        pass

if __name__ == "__main__":
    main()