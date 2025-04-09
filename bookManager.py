from bookClass import Book

class BookManager:

    book_id = 1

    def __init__(self, library):
        """Manager class for the Book class"""
        self.library = library

    def new_book(self, title, author, copies=0, _id=None):
        """Creates a new book"""
        if _id is None:
            _id = self._generate_id()
        else:
            while not self.check_id_availability(_id):
                _id += 1
        return self.library.add_book(Book(_id, title,author),copies)

    def latest_book(self):
        """Returns the ID of the latest book"""
        return self.book_id

    def _generate_id(self):
        """Generates a new ID, to ensure no IDs overlap"""
        while not self.check_id_availability(self.book_id):
            self.book_id += 1
        return self.book_id

    def update_book_id(self, _id):
        """Updates the current book ID"""
        if _id is None: self.reset_book_id()
        else: self.book_id = _id

    def reset_book_id(self):
        """Resets the current book ID"""
        self.book_id = 1

    def delete_book(self, book_id):
        """Removes the book with the given ID from the library and updates the current book ID"""
        if self.library.remove_book(book_id):
            self.update_book_id(book_id)

    def update_book(self, old_book_id, new_book_id, title, author, copies=None):
        """Updates the book with the given ID with new details"""
        new_book = Book(new_book_id, title, author)
        if copies is None:
            copies = self.library.get_copies(old_book_id)
        if self.library.update_book(old_book_id, new_book, copies) is None: return False
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
        book_id = book_id
        # If the parsing fails, the user will be informed, and the method will return False to indicate failure to update the book.
        if book_id is None:
            print(f"Error. {book_id} is not a valid book ID.")
            return False

        if self.library.books is None or len(self.library.books) < 1:
            return True

        for book in self.library.books:
            if book.book_id == book_id:
                return False
        return True