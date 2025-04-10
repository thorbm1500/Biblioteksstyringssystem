from bookClass import Book

class BookManager:

    current_id = 1

    def __init__(self, library, util):
        """Manager class for the Book class"""
        self.library = library
        self.util = util

    def new_book(self, title, author, copies=0, book_id=None):
        """Creates a new book"""
        # An ID from the standard order will be generated and given if no ID has been provided.
        if book_id is None:
            book_id = self._generate_id()
        else:
            # Attempts parsing input to an integer
            book_id = self.util.parse_integer(book_id)
            # If the parsing fails, the user will be informed, and the method will return False to indicate failure to update the book.
            if book_id is None:
                print(f"[Error] {book_id} is not a valid book ID.")
                return False
            # If an ID has been provided, availability will be checked, and ensured.
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
            book_id = self.util.parse_integer(book_id)
            # If the parsing fails, the user will be informed, and the method will return False to indicate failure to update the current ID.
            if book_id is None:
                print(f"[Error] {book_id} is not a valid book ID.")
                return False
            self.current_id = book_id

    def delete_book(self, book_id):
        """Removes the book with the given ID from the library and updates the current book ID"""
        # Attempts parsing input to an integer
        book_id = self.util.parse_integer(book_id)
        # If the parsing fails, the user will be informed, and the method will return False to indicate failure to update the book.
        if book_id is None:
            print(f"[Error] {book_id} is not a valid book ID.")
            return False
        # Returns True or False depending on if the removal was successful.
        return self.library.remove_book(book_id)

    def update_book(self, old_book_id: int, new_book_id: int, title: str, author: str, copies=None):
        """Updates the book with the given ID with new details"""
        # Attempts parsing input to an integer
        new_book_id = self.util.parse_integer(new_book_id)
        # If the parsing fails, the user will be informed, and the method will return False to indicate failure to update the book.
        if new_book_id is None:
            print(f"[Error] {new_book_id} is not a valid book ID.")
            return False
        # Creates a new instance of a Book with the provided details
        new_book = Book(new_book_id, title, author)
        # Checks if a value for 'Copies' have been provided. If not, the copies will be taken from the old version of the book.
        if copies is None:
            copies = self.library.get_copies(old_book_id)

        if not self.library.update_book(old_book_id, new_book, copies):
            print(f"[Error] No book found with ID: {old_book_id}.")
            return False

        for member in self.library.members:
            if member.borrowed_books is None:
                continue
            for book in member.borrowed_books:
                if book.book_id == old_book_id:
                    member.borrowed_books.remove(book)
                    member.borrow_book(new_book)
        return True

    def check_id_availability(self, book_id):
        """Returns True or False, whether the given ID is available or not"""
        # Attempts parsing input to an integer
        book_id = self.util.parse_integer(book_id)
        # If the parsing fails, the user will be informed, and the method will return False to indicate failure to update the book.
        if book_id is None:
            print(f"[Error] {book_id} is not a valid book ID.")
            return False

        if self.library.books is None or len(self.library.books) < 1:
            return True

        for book in self.library.books:
            if book.book_id == book_id:
                return False
        return True