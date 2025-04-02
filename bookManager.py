from bookClass import Book

class BookManager:

    book_id = 0

    def __init__(self, library):
        self.library = library

    def new_book(self, title, author, copies):
        self.book_id += 1
        book = Book(self.book_id, title,author)
        self.library.add_book(book,int(copies))
        return self.book_id

    def latest_book(self):
        return self.book_id