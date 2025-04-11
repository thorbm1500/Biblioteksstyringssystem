from bookClass import Book

class BookManager:

    current_id = 1

    def __init__(self, library, util):
        """Manager class for the Book class"""
        self.library = library
        self.util = util

    def new_book(self, title:str, author:str, copies=0, book_id=None):
        """Creates a new book"""
        # An ID from the standard order will be generated and given if no ID has been provided.
        if book_id is None:
            book_id = self._generate_id()
        else:
            # Attempts parsing input to an integer
            # If the parsing fails, the user will be informed, and the method will return False to indicate failure to create the book.
            if self.util.parse_integer(book_id) is None:
                print(f"[Error] {book_id} is not a valid book ID.")
                return False
            # Parses the ID to an integer.
            book_id = self.util.parse_integer(book_id)
            # Availability will be checked and ensured.
            while not self.check_id_availability(book_id):
                book_id += 1
        # The new book is created, and its ID is returned, provided by the 'add_book' method in the library class.
        return self.library.add_book(Book(book_id, title,author),copies)

    def latest_book(self):
        """Returns the ID of the latest book"""
        return self.current_id

    def _generate_id(self):
        """Generates a new ID, and continues to do so until an available ID has been generated, to ensure no IDs overlap"""
        while not self.check_id_availability(self.current_id):
            self.current_id += 1
        # Returns the newly generated ID.
        return self.current_id

    def update_book_id(self, book_id=None):
        """Updates the current book ID.
        If no ID is provided, the current ID will be reset to 1"""
        if book_id is None: self.current_id = 1
        else:
            # Attempts parsing input to an integer
            # If the parsing fails, the user will be informed, and the method will return False to indicate failure to update the current ID.
            if self.util.parse_integer(book_id) is None:
                print(f"[Error] {book_id} is not a valid book ID.")
                return False
            # Parses the ID to an integer and updates the current ID.
            self.current_id = self.util.parse_integer(book_id)

    def delete_book(self, book_id):
        """Removes the book with the provided ID from the library and updates the current book ID"""
        # Attempts parsing input to an integer
        # If the parsing fails, the user will be informed, and the method will return False to indicate failure to remove the book.
        if self.util.parse_integer(book_id) is None:
            print(f"[Error] {book_id} is not a valid book ID.")
            return False
        # Parses the ID to an integer.
        book_id = self.util.parse_integer(book_id)
        # Returns True or False depending on if the removal was successful.
        return self.library.remove_book(book_id)

    def update_book(self, old_book_id: int, new_book_id: int, title: str, author: str, copies=None):
        """Updates the book with the provided ID with new details"""
        # Attempts parsing the provided ID to an integer.
        # If the parsing fails, the user will be informed, and the method will return False to indicate failure to update the book.
        if self.util.parse_integer(new_book_id) is None:
            print(f"[Error] {new_book_id} is not a valid book ID.")
            return False
        # Creates a new instance of a Book with the provided details
        new_book = Book(self.util.parse_integer(new_book_id), title, author)
        # Checks if a value for 'copies' have been provided. If not, the copies will be taken from the old version of the book.
        if copies is None:
            copies = self.library.get_copies(old_book_id)
        # Attempts to update the book and checks if update was successful. If the update fails, the user will be notified.
        if not self.library.update_book(old_book_id, new_book, copies):
            print(f"[Error] No book found with ID: {old_book_id}.")
            return False
        if not self.library.contain_members():
            # Skips checking all members to update the book as no members are present. Returns True to indicate successful execution.
            return True
        # Iterates through all members in the library.
        for member in self.library.members:
            # Checks if the member is currently borrowing any books.
            if not member.is_borrowing():
                continue
            # Iterates through all books in the list and compares IDs. Is a match found, the old book will be removed, and the new book will be inserted.
            for book in member.borrowed_books:
                if book.book_id == old_book_id:
                    member.borrowed_books.remove(book)
                    member.borrow_book(new_book)
        # Returns True to indicate successful execution.
        return True

    def check_id_availability(self, book_id: int):
        """Returns True or False, whether the provided ID is available or not"""
        # Attempts parsing the provided ID to an integer.
        # If the parsing fails, the user will be informed, and the method will return False to indicate that the ID is invalid.
        if self.util.parse_integer(book_id) is None:
            print(f"[Error] {book_id} is not a valid book ID.")
            return False
        # Parses the ID to an integer.
        book_id = self.util.parse_integer(book_id)
        # Checks if the ID is negative and returns False if that's the case as IDs cant be negative.
        if book_id < 0:
            print("[Error] Negative values are not allowed.")
            return False
        # Checks if the library contains any books.
        if self.library.contain_books() is None:
            return True
        # Iterates through all books in the list and compares IDs to find a match.
        for book in self.library.books:
            if book.book_id == book_id:
                return False
        # Returns True to indicate that the ID is available.
        return True