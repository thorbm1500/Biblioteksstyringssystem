from util import Util

util = Util()

class Library:
    def __init__(self, books=None, members=None):
        """Library class"""
        # Dictionary storing all the library's books and how many copies are stored
        # Creates a dictionary if one has not been provided
        if books is None: self.books = {}
        else: self.books = books

        # List containing all the library's members
        # Creates a list if one has not been provided
        if members is None: self.members = []
        else: self.members = members

    def add_book(self, book, copies):
        """Add a book to the library. Returns the ID of the book added to the library"""
        try:
            copies = int(copies)
        except:
            copies = 0
            print(f"Error. Unable to parse integer. Copies has been set to 0.")
        # Adds the given book with its copies to the dictionary of books
        self.books[book] = copies
        # Returns the ID of the new book
        return book.book_id

    def remove_book(self, book_id):
        """Removes the book with the given ID from the library"""
        book_id = util.parse_integer(book_id)
        if book_id is None:
            print(f"Error. {book_id} is not a valid book ID.")
            return False

        book = self.get_book_from_id(book_id)

        if book is None:
            print(f"Error. No book exists with ID: {book_id}")
            return False

        # Removes the book from all members that currently has it borrowed
        for member in self.members:
            if member.borrowed_books is None: continue
            for index in member.borrowed_books:
                if index.book_id == book.book_id:
                    member.borrowed_books.remove(book)

        # Removes the book along with its value (copies) from the dictionary
        self.books.pop(book)
        return True


    def update_book(self, book):
        """Updates the given book in the library"""
        old_book = self.get_book_from_id(book.book_id)

        if old_book is None:
            print("Error. The book you're trying to update doesn't exist.")
            return
        else:
            # Adds the new book to the dictionary of books with the copies from the old book
            self.books[book] = self.books.get(old_book)
            # Removes the old book from the dictionary
            self.books.pop(old_book)

    def add_member(self, member):
        """Adds the given member to the list of members"""
        self.members.append(member)

    def remove_member(self, member_id):
        """Removes the member with the given ID from the list of members"""
        member = self.get_member_from_id(member_id)

        if member is None:
            print("Error. No member found with ID: " + str(member_id))
            return

        self.members.remove(member)

    def update_member(self, member):
        """Updates the given member with new details"""
        member_id = member.member_id
        old_entry = self.get_member_from_id(member_id)

        if old_entry is None:
            print("Error. The member you're trying to update doesn't exist.")
        else:
            self.members.append(member)
            self.members.remove(old_entry)

    def issue_book(self, book_id, member):
        """Lends a copy of the book with the given ID to the given member"""
        book = self.get_book_from_id(book_id)
        copies = self.books.get(book)

        if book is None:
            print("Error. No book exists with ID: " + str(book_id))
            return

        if copies == 0:
            print("Error. The book is out of stock.")
            return

        member.borrow_book(book)
        self.books.put(book,copies-1)

    def return_book(self, book_id, member):
        """Returns the book with the given ID from the given member"""
        book = self.get_book_from_id(book_id)
        copies = self.books.get(book)

        if book is None:
            print("Error. No book exists with ID: " + str(book_id))
            return

        if member.borrowed_books.contains(book) is not True:
            print("Error. The member is not currently borrowing this book.")
            return

        member.return_book(book)
        self.books.put(book, copies + 1)

    def display_books(self):
        """Prints details on all books in the library"""
        for book in self.books:
            book.display_info(self)

    def display_book(self, book_id):
        """Prints details about the book with the given ID"""
        for book in self.books:
            if book.book_id == book_id:
                book.display_info(self)
                return
        print("Error. No book found with ID: " + str(book_id))

    def get_book_from_string(self, name):
        """Get the book with the given name"""
        for book in self.books:
            if book.title.lower() == name.lower():
                return book

        return None

    def get_member_from_string(self, name):
        """Get the member with the given name"""
        for member in self.members:
            if member.name.lower() == name.lower():
                return member

        return None

    def display_members(self):
        """Prints details on all members in the library"""
        for member in self.members:
            member.display_info()

    def display_member(self, member_id):
        """Prints details about the member with the given ID"""
        member = self.get_member_from_id(member_id)

        if member is None:
            print("Error. No member found with ID: " + str(member_id))
            return

        member.display_info()

    def get_book_from_id(self, book_id):
        """Returns the book with the given ID"""
        try:
            book_id = int(book_id)
        except:
            return None

        for book in self.books:
            if book.book_id == book_id:
                return book

        # Returns None if no book was found
        return None

    def get_member_from_id(self, member_id):
        """Returns the member with the given ID"""
        try:
            member_id = int(member_id)
        except:
            return None

        for member in self.members:
            if member.member_id is member_id:
                return member

        # Returns None if no member was found
        return None

    def get_copies(self, _id):
        """Returns the number of copies available of the book with the given ID in the library"""
        for book in self.books:
            if book.book_id == _id:
                return self.books.get(book)

    def update_book(self, old_book_id, book, copies):
        """Removes the book with the old ID given, and inserts the new book in the library"""
        self.remove_book(old_book_id)
        self.add_book(book, copies)

    def is_borrowed(self, book):
        """Returns True or False whether the given book is currently being lent to any members"""
        for member in self.members:
            if member.borrowed_books is None: return False
            for index in member.borrowed_books:
                if book.book_id == index.book_id: return True
            return False