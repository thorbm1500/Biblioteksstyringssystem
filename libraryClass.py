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
        self.books[book] = copies

    # Remove a book from the library
    def remove_book(self, book_id):
        book = self.get_book_from_id(book_id)

        if book is None:
            print("Error. No book exists with ID: " + book_id)
            return

        self.books.pop(book)

    # Update a book in the library
    def update_book(self, book):
        book_id = book.book_id
        old_book = self.get_book_from_id(book_id)

        if old_book is None:
            print("Error. The book you're trying to update doesn't exist.")
            return
        else:
            self.books[book] = self.books.get(old_book)
            self.books.pop(old_book)

    def add_member(self, member):
        self.members.append(member)

    def remove_member(self, member_id):
        member = self.get_member_from_id(member_id)

        if member is None:
            print("Error. No member found with ID: " + member_id)
            return

        self.members.remove(member)

    def update_member(self, member):
        member_id = member.member_id
        old_entry = self.get_member_from_id(member_id)

        if old_entry is None:
            print("Error. The member you're trying to update doesn't exist.")
        else:
            self.members.append(member)
            self.members.remove(old_entry)

    def issue_book(self, book_id, member):
        book = self.get_book_from_id(book_id)
        copies = self.books.get(book)

        if book is None:
            print("Error. No book exists with ID: " + book_id)
            return

        if copies == 0:
            print("Error. No available copies found.")
            return

        member.borrow_book(book)
        self.books.put(book,copies-1)

    def return_book(self, book_id, member):
        book = self.get_book_from_id(book_id)
        copies = self.books.get(book)

        if book is None:
            print("Error. No book exists with ID: " + book_id)
            return

        if member.borrowed_books.contains(book) is not True:
            print("Error. The member is not currently borrowing this book.")
            return

        member.return_book(book)
        self.books.put(book, copies + 1)

    def display_books(self):
        for book in self.books:
            book.display_info(self)

    # Prints all the members with their ID and Name
    def display_members(self):
        for member in self.members:
            member.display_info()

    # Prints all info on a specific member
    def display_member(self, member_id):
        member = self.get_member_from_id(member_id)

        if member is None:
            print("Error. No member found with ID: " + member_id)
            return

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