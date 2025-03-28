class Book:

    id = 0
    title = ""
    author = ""

    def __init__(self, book_id, title, author):
        self.book_id = book_id
        self.title = title
        self.author = author

    def display_info(self, library):
        if library is None:
            print("ID: " + str(self.book_id) + " | Title: " + self.title + " | Author: " + self.author)
        else:
            print("ID: " + str(self.book_id) + " | Title: " + self.title + " | Author: " + self.author + " | Copies: " + str(library.books.get(self)))