class Member:

    def __init__(self, member_id: int, name: str, borrowed_books: list):
        """
            Member class

                Initialization (New instances of the class) should only be made through the Member Manager class
        """
        self.member_id = member_id
        self.name = name
        self.borrowed_books = borrowed_books

    def display_info(self):
        """Displays the member's details"""
        # Checks if the member is borrowing any books and prints 'None' if no books are currently being borrowed.
        if self.borrowed_books is None or len(self.borrowed_books)==0:
            print(f"ID: {self.member_id} | Name: {self.name} | Borrowed Books: None")
        else:
            # Collects information of all the books being borrowed, and prints it out all together after collecting.
            book_list = ""
            for book in self.borrowed_books:
                book_list = book_list + f"\n        [{book.book_id}] {book.title} by {book.author}"

            # Prints the info.
            print(f"ID: {self.member_id} | Name: {self.name} | Borrowed Books:{book_list}\n")

    def borrow_book(self, book):
        """Adds the given book to a list of borrowed books by the member"""
        # Checks if there's an instance of a list and if there is, the book is then appended to that list and otherwise a list is created with the book.
        if self.borrowed_books is None: self.borrowed_books = [ book ]
        else: self.borrowed_books.append(book)

    def return_book(self, book):
        """Removes the given book from the list of borrowed books by the member.

                Returns True or False, depending on if the removal of the book was performed successfully."""
        self.borrowed_books.remove(book)
        # Returns True or False, depending on if the member is still borrowing the book.
        return self.is_borrowed(book)

    def is_borrowed(self, book):
        """Returns True or False whether the given book is in the list of borrowed books by the member"""
        # Returns False if the list is None, as no books will then currently be borrowed.
        if self.borrowed_books is None: return False
        # Returns False if the length of the list is less than 1, as no books will then currently be borrowed.
        elif len(self.borrowed_books) < 1: return False
        else:
            # Iterates through all books in the list of borrowed books, and compares their IDs. Returns True if a match is found, as the checked book is then currently being borrowed by the member.
            for index in self.borrowed_books:
                if index.book_id == book.book_id:
                    return True
        # Should no match be found, the return statement below will fire, and return False, as the book is then not currently being borrowed by the member.
        return False