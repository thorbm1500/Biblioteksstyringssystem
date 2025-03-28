from bookClass import Book

class Manager:

    book_id = 0

    def __init__(self, library):
        self.library = library

    def new_book(self, title, author, copies):
        book = Book(self.book_id, title,author)
        self.book_id += 1
        self.library.add_book(book,copies)
