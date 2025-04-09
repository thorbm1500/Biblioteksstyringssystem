class Book:

    def __init__(self, book_id, title, author):
        """Book class"""
        self.book_id = book_id
        self.title = title
        self.author = author

    def display_info(self, library=None):
        """Displays the book's details and copies should the library be provided"""
        if library is None: print(f"ID: {self.book_id} | Title: {self.title} | Author: {self.author}")
        else: print(f"ID: {self.book_id} | Title: {self.title} | Author: {self.author} | Copies: {library.books.get(self)}")