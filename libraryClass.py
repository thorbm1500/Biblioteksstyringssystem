class Library:

    # Dictionary storing all the library's books and how many copies are stored.
    books = {}

    # A list containing all the library's members
    members = []

    # Main method run when a new instance is created.
    def __init__(self, books, members):
        self.books = books
        self.members = members

    # Add a book to the library.
    def add_book(self, book, copies):
        self.books.add(book, copies)

    # Remove a book from the library
    def remove_book(self, book):
        self.books.pop(book)

    # Update a book in the library
    def update_book(self, book_id, book):
        old_book = self.get_book_from_id(book_id)

        if old_book is None:
            print("Error. The book you're trying to update doesn't exist.")
            return
        else:
            self.books.add(book, self.books.get(old_book))
            self.books.pop(old_book)

    def add_member(self, member):
        self.members.append(member)

    def remove_member(self, member):
        self.members.remove(member)

    def update_member(self, member):
        old_entry = self.get_member_from_id

        if old_entry is None:
            print("Error. The member you're trying to update doesn't exist.")
            return
        else:
            self.members.append(member)
            self.members.remove(old_entry)

    def issue_book(self, book_id, member):

    def return_book(self, book, member):

    def display_books(self):
        for book in self.books:
            book.display_info()

    # Prints all the members with their ID and Name
    def display_members(self):
        for member in self.members:
            member.display_info()

    # Get an instance of a book with the book's ID
    def get_book_from_id(self, book_id):
        for book in self.books:
            if book.book_id is book_id:
                return book

        # Returns None if no book was found
        return None

    # Get an instance of a member with the member's ID
    def get_member_from_id(self, member_id):
        for member in self.members:
            if member.member_id is member_id:
                return member

        # Returns None if no member was found
        return None