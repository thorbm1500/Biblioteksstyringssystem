from bookClass import Book

class BookManager:

    book_id = 0

    def __init__(self, library):
        """Manager class for the Book class"""
        self.library = library

    def new_book(self, title, author, copies=0):
        """Creates a new book"""
        self._generate_id()
        return self.library.add_book(Book(self.book_id, title,author),copies)

    def latest_book(self):
        """Returns the ID of the latest book"""
        return self.book_id

    def _generate_id(self):
        """Generates a new ID, to ensure no IDs overlap"""
        while True:
            self.book_id += 1
            for book in self.library.books:
                # Checks new ID number against all existing IDs
                if book.book_id == self.book_id: break
            return

    def update_book_id(self, _id):
        """Updates the current book ID"""
        if _id is None: self.reset_book_id()
        else: self.book_id = _id

    def reset_book_id(self):
        """Resets the current book ID"""
        self.book_id = 0

    def delete_book(self, book_id):
        """Removes the book with the given ID from the library and updates the current book ID"""
        if self.library.remove_book(book_id):
            self.update_book_id(book_id)

    def update_book(self, old_book_id, new_book_id, title, author, copies):
        """Updates the book with the given ID with new details"""
        new_book = Book(new_book_id, title, author)
        self.library.update_book(old_book_id, new_book, copies)
        for member in self.library.members:
            if member.borrowed_books is None:
                continue
            for book in member.borrowed_books:
                if book.book_id == old_book_id:
                    member.borrowed_books.remove(book)
                    break
            member.borrow_book(new_book)
