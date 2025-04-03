from bookClass import Book

class BookManager:

    book_id = 0

    def __init__(self, library):
        self.library = library

    def new_book(self, title, author, copies):
        while self._generate_id():
            pass
        book = Book(self.book_id, title,author)
        self.library.add_book(book,int(copies))
        return self.book_id

    # Returns the ID of the latest book.
    def latest_book(self):
        return self.book_id

    # Used for generating a new ID.
    def _generate_id(self):
        self.book_id += 1
        for book in self.library.books:
            # Checks new ID number against all existing ID numbers to avoid overlap.
            if book.book_id == self.book_id:
                return True
        return False

    # Used for updating the member ID.
    def update_book_id(self, _id):
        if _id is None:
            self.book_id = 0
        else:
            self.book_id = _id

    # Used for resetting the member ID.
    def reset_book_id(self):
        self.book_id = 0

    def delete_book(self, _id):
        if self.library.remove_book(int(_id)) is not None:
            self.update_book_id(_id)