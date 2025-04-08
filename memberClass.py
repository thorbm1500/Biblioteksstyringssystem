class Member:

    name = ""
    borrowed_books = []

    def __init__(self, member_id, name, borrowed_books):
        """
            Member class

                Initialization (New instances of the class) should only be made through the Member Manager class
        """
        self.member_id = member_id
        self.name = name
        self.borrowed_books = borrowed_books

    def display_info(self):
        """Displays the member's details"""
        if self.borrowed_books is None or len(self.borrowed_books)==0:
            print("ID: " + str(self.member_id) + " | Name: " + self.name + " | Borrowed Books: None")
        else:
            book_list = ""
            for book in self.borrowed_books:
                book_list = book_list + "\n        [" + str(book.book_id) + "] " + book.title + " by " + book.author

            print("ID: " + str(self.member_id) + " | Name: " + self.name + " | Borrowed Books:" + book_list)

    def borrow_book(self, book):
        """Adds the given book to a list of borrowed books by the member"""
        if self.borrowed_books is None: self.borrowed_books = [ book ]
        else: self.borrowed_books.append(book)

    def return_book(self, book):
        """Removes the given book from the list of borrowed books by the member"""
        self.borrowed_books.remove(book)

    def is_borrowed(self, checked_book):
        """Returns True or False whether the given book is in the list of borrowed books by the member"""
        if self.borrowed_books is None: return False
        else:
            for book in self.borrowed_books:
                if book.book_id == checked_book.book_id:
                    return True
        return False