class Library:

    def __init__(self, util, books=None, members=None):
        """Library class"""
        self.util = util
        # A dictionary storing all the library's books and how many copies are stored
        # Creates a dictionary if one hasn't been provided
        if books is None: self.books = {}
        else: self.books = books

        # A list containing all the library's members
        # Creates a list if one hasn't been provided
        if members is None: self.members = []
        else: self.members = members

    def add_book(self, book, copies: int):
        """Add a book to the library. Returns the ID of the book added to the library"""
        # Attempts parsing input to an integer.
        # If the parsing fails, the number of copies will be set to '0', and the user will be informed.
        # If the parsing doesn't fail, copies will be set to the number provided.
        if self.util.parse_integer(copies) is None:
            print(f"[Error] Unable to parse '{copies}' to an integer. Copies has been set to '0'.")
            copies = 0
        else: copies = self.util.parse_integer(copies)
        # Adds the provided book with its copies to the dictionary of books.
        self.books[book] = copies
        # Returns the ID of the new book.
        return book.book_id

    def remove_book(self, book_id: int):
        """Removes the book with the provided ID from the library"""
        # Attempts parsing input to an integer.
        # If the parsing fails, the user will be informed, and the method will return False to indicate failure to remove the book.
        if self.util.parse_integer(book_id) is None:
            print(f"[Error] {book_id} is not a valid book ID.")
            return False
        # Parses the ID to an integer.
        book_id = self.util.parse_integer(book_id)
        # Gets the book with the provided ID.
        book = self.get_book_from_id(book_id)

        # If no book exists with the provided ID, the user will be informed and the method will return None to indicate failure to remove the book.
        if book is None:
            print(f"[Error] No book exists with ID: {book_id}")
            return None

        # Iterates through all members and their borrowed books to see if there's a match for the book. If there is, the book will be removed from their borrowed books, to ensure the book is removed completely.
        for member in self.members:
            if member.borrowed_books is None: continue
            for index in member.borrowed_books:
                if index.book_id == book.book_id:
                    member.borrowed_books.remove(book)

        # Removes the key(book) along with its value(copies) from the dictionary.
        self.books.pop(book)
        # Returns True to indicate successful execution.
        return True


    def update_book(self, old_book_id: int, book, copies: int):
        """Updates the provided book in the library"""
        # Attempts parsing input to an integer.
        # If the parsing fails, the user will be informed, and the method will return False to indicate failure to update the book.
        if self.util.parse_integer(old_book_id) is None:
            print(f"[Error] {old_book_id} is not a valid book ID.")
            return False

        # Gets the old book with the provided ID.
        old_book = self.get_book_from_id(self.util.parse_integer(old_book_id))

        # If no book exists with the provided ID, the user will be informed and the method will return False to indicate failure to update the book.
        if old_book is None:
            print("[Error] The book you're trying to update doesn't exist.")
            return False
        else:
            # Adds the new and updated version of the book to the dictionary of books with the copies from the old book.
            self.books[book] = copies
            # Removes the old book from the dictionary.
            self.books.pop(old_book)
        # Returns True to indicate successful execution.
        return True

    def add_member(self, member):
        """Adds the provided member to the list of members"""
        self.members.append(member)

    def remove_member(self, member_id: int):
        """Removes the member with the provided ID from the list of members"""
        # Attempts parsing input to an integer
        # If the parsing fails, the user will be informed, and the method will return False to indicate failure to update the book.
        if self.util.parse_integer(member_id) is None:
            print(f"[Error] {member_id} is not a valid member ID.")
            return False
        # Parses the ID to an integer.
        member_id = self.util.parse_integer(member_id)

        # Gets the member with the provided ID.
        member = self.get_member_from_id(member_id)

        # If no member exists with the provided ID, the user will be informed and the method will return None to indicate failure to locate member with the provided ID.
        if member is None:
            print(f"[Error] No member found with ID: {member_id}")
            return None

        # Removes the member from the list
        self.members.remove(member)

        # Returns True or False, depending on if the removal was successful
        if self.get_member_from_id(member_id) is None: return True
        else: return False

    def issue_book(self, book_id, member):
        """Lends a copy of the book with the provided ID to the provided member"""
        # Attempts parsing ID to an integer.
        # If the parsing fails, the user will be informed, and the method will return False to indicate failure to update the book.
        if self.util.parse_integer(book_id) is None:
            print(f"[Error] {book_id} is not a valid book ID.")
            return False
        # Parses the ID to an integer.
        book_id = self.util.parse_integer(book_id)
        book = self.get_book_from_id(book_id)

        # Checks if a book with the provided ID exists.
        if book is None:
            print(f"[Error] No book exists with ID: {book_id}")
            return

        # Checks if the member is already borrowing the book before attempting to borrow it.
        if member.is_borrowed(book):
            print("[Error] The member is already borrowing this book.")
            return

        # Gets the number of copies available.
        copies = self.books.get(book)

        # Checks if any copies are available.
        if copies == 0:
            print(f"[Error] Book with ID: {book_id}, is out of stock.")
            return

        # Adds the book to the member's list of borrowed books, and remove 1 from available copies.
        member.borrow_book(book)
        self.books[book] = copies-1

    def return_book(self, book_id, member):
        """Returns the book with the provided ID from the provided member"""
        # Attempts parsing ID to an integer.
        # If the parsing fails, the user will be informed, and the method will return False to indicate failure to update the book.
        if self.util.parse_integer(book_id) is None:
            print(f"[Error] {book_id} is not a valid book ID.")
            return False
        # Parses the ID to an integer.
        book_id = self.util.parse_integer(book_id)
        book = self.get_book_from_id(book_id)

        # Checks if a book with the provided ID exists.
        if book is None:
            print(f"[Error] No book exists with ID: {book_id}")
            return

        # Checks if the member is currently borrowing the book before attempting to return it.
        if not member.is_borrowed(book):
            print("[Error] The member is not currently borrowing this book.")
            return

        # Gets the number of copies available.
        copies = self.books.get(book)

        # Removes the book from the member's list of borrowed books and adds 1 to available copies.
        member.return_book(book)
        self.books[book] = copies + 1

    def display_books(self):
        """Prints details on all books in the library"""
        # Checks if the library contains any books.
        if not self.contain_books(): return
        # Iterates through all books and prints their details.
        for book in self.books:
            book.display_info(self)

    def display_book(self, book_id):
        """Prints details about the book with the provided ID"""
        # Checks if the library contains any books.
        if not self.contain_books(): return
        # Iterates through all books and compares IDs to find a match.
        for book in self.books:
            if book.book_id == book_id:
                book.display_info(self)
                return
        # Informs that no match was found.
        print(f"[Error] No book found with ID: {book_id}")

    def get_book_from_string(self, name):
        """Get the book with the provided name"""
        # Checks if the library contains any books.
        if not self.contain_books(): return None
        # Iterates through all books and compares names to find a match.
        for book in self.books:
            if book.title.lower() == name.lower():
                return book
        # Returns None to indicate that no book was found with the name provided.
        return None

    def get_member_from_string(self, name):
        """Get the member with the provided name"""
        # Checks if the library contains any members.
        if not self.contain_members(): return
        # Iterates through all members and compares names to find a match.
        for member in self.members:
            if member.name.lower() == name.lower():
                return member
        return None

    def display_members(self):
        """Prints details on all members in the library"""
        # Checks if the library contains any members.
        if not self.contain_members(): return
        # Iterates through all members and prints their details.
        for member in self.members:
            member.display_info()

    def display_member(self, member_id):
        """Prints details about the member with the provided ID"""
        # Gets the member.
        member = self.get_member_from_id(member_id)
        # Checks if an instance of the member is present.
        if member is None:
            print(f"[Error] No member found with ID: {member_id}")
            return

        member.display_info()

    def get_book_from_id(self, book_id):
        """Returns the book with the provided ID"""
        # Attempts parsing the ID to an integer.
        book_id = self.util.parse_integer(book_id)
        # Returns None if the parsing fails.
        if book_id is None: return None

        # Checks if the library contains any books.
        if not self.contain_books(): return None
        for book in self.books:
            if book.book_id == book_id:
                return book

        # Returns None if no book was found
        return None

    def get_member_from_id(self, member_id: int):
        """Returns the member with the provided ID"""
        # Attempts parsing the ID to an integer.
        member_id = self.util.parse_integer(member_id)
        # Returns None if the parsing fails.
        if member_id is None: return None

        # Checks if the library contains any members.
        if not self.contain_members(): return
        # Iterates through all members and compares IDs. Returns the member if they're found, otherwise returns None
        for member in self.members:
            if member.member_id == member_id:
                return member

        # Returns None if no member was found
        return None

    def get_copies(self, book_id):
        """Returns the number of copies available of the book with the provided ID in the library"""
        # Attempts parsing the ID to an integer.
        book_id = self.util.parse_integer(book_id)
        # Returns None if the parsing fails.
        if book_id is None: return None
        # Checks if the library contains any books.
        if not self.contain_books(): return
        for book in self.books:
            if book.book_id == book_id:
                return self.books.get(book)
        return 0

    def is_borrowed(self, book):
        """Returns True or False whether the provided book is currently being lent to any members"""
        # Checks if the library contains any members.
        if not self.contain_members(): return
        for member in self.members:
            # Checks if an instance of the list is present.
            if member.borrowed_books is None: return False
            # Iterates through all books in the list and compares IDs to find a match.
            for index in member.borrowed_books:
                if book.book_id == index.book_id: return True
            return False

    def contain_books(self):
        """Checks if any books are present in the library."""
        # Checks if an instance of the list is present.
        if self.books is None:
            return False
        # Checks if any books are present in the list of books.
        if len(self.books)<1:
            return False
        # Returns True as both previous statements were False, hence indicating that the library does contain books.
        return True

    def contain_members(self):
        """Checks if any members are present in the library."""
        # Checks if an instance of the dictionary is present.
        if self.members is None:
            return False
        # Checks if any members are present in the dictionary of members.
        if len(self.members)<1:
            return False
        # Returns True as both previous statements were False, hence indicating that the library does contain members.
        return True