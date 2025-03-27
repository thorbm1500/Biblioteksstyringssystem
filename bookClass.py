class Book:

    id = 0
    title = ""
    author = ""

    def __init__(self, book_id, title, author, copies):
        self.book_id = book_id
        self.title = title
        self.author = author

    def display_info(self):
        print("ID: " + self.book_id + " | Title: " + self.title + " | Author: " + self.author)