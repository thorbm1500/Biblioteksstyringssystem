class Member:

    id = 0
    name = ""
    borrowed_books = []

    def __init__(self, member_id, name, borrowed_books):
        self.member_id = member_id
        self.name = name
        self.borrowed_books = borrowed_books

    def display_info(self):
        print("ID: " + self.member_id + " | Name: " + self.name + " | Borrowed Books: " + self.borrowed_books)

    def borrow_book(self, book):
        self.borrowed_books.append(book)

    def return_book(self, book):
        self.borrowed_books.remove(book)