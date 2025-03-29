from bookClass import Book

class BookManager:

    book_id = 1

    def __init__(self, library):
        self.library = library

    def new_book(self, title, author, copies):
        book = Book(self.book_id, title,author)
        self.book_id += 1
        self.library.add_book(book,int(copies))
        return self.book_id - 1

    def latest_book(self):
        return self.book_id