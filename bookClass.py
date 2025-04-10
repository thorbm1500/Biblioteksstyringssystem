class Book:

    def __init__(self, book_id: int, title: str, author: str):
        """
            Book class

                Initialization (New instances of the class) should only be made through the Book Manager class
        """
        self.book_id = book_id
        self.title = title
        self.author = author

    def display_info(self, library=None):
        """Displays the book's details and copies should the library be provided"""
        if library is None: print(f"[{self.book_id}] {self.title} by {self.author}")
        else: print(f"[{self.book_id}] {self.title} by {self.author}. Available copies: {library.books.get(self)}")