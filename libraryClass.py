class Library:
    def __init__(self, util, books=None, members=None):
        """Library class"""
        self.util = util
        # A dictionary storing all the library's books and how many copies are stored
        # Creates a dictionary if one hasn't been provided
        if books is None: self.books = {}
        else: self.books = books

        # A list containing all the library's members
        # Creates a list if one hasn't been provided
        if members is None: self.members = []
        else: self.members = members

    def add_book(self, book, copies):
        """Add a book to the library. Returns the ID of the book added to the library"""
        # Attempts parsing input to an integer
        copies = self.util.parse_integer(copies)
        # If the parsing fails, the number of copies will be set to '0', and the user will be informed
        if copies is None:
            print(f"Error. Unable to parse '{copies}' to an integer. Copies has been set to '0'.")
            copies = 0
        # Adds the given book with its copies to the dictionary of books
        self.books[book] = copies
        # Returns the ID of the new book
        return book.book_id

    def remove_book(self, book_id):
        """Removes the book with the given ID from the library"""
        # Attempts parsing input to an integer
        book_id = self.util.parse_integer(book_id)
        # If the parsing fails, the user will be informed, and the method will return False to indicate failure to remove the book.
        if book_id is None:
            print(f"Error. {book_id} is not a valid book ID.")
            return False

        # Gets the book with the given ID
        book = self.get_book_from_id(book_id)

        # If no book exists with the given ID, the user will be informed and the method will return False to indicate failure to remove the book.
        if book is None:
            print(f"Error. No book exists with ID: {book_id}")
            return False

        # Iterates through all members and their borrowed books to see if there's a match for the book. If there is, the book will be removed from their borrowed books, to ensure the book is removed completely.
        for member in self.members:
            if member.borrowed_books is None: continue
            for index in member.borrowed_books:
                if index.book_id == book.book_id:
                    member.borrowed_books.remove(book)

        # Removes the book along with its value (copies) from the dictionary and returns True to indicate successful removal.
        self.books.pop(book)
        return True


    def update_book(self, old_book_id, book, copies):
        """Updates the given book in the library"""
        # Attempts parsing input to an integer.
        old_book_id = self.util.parse_integer(old_book_id)
        # If the parsing fails, the user will be informed, and the method will return False to indicate failure to update the book.
        if old_book_id is None:
            print(f"Error. {old_book_id} is not a valid book ID.")
            return False

        # Gets the old book with the given ID.
        old_book = self.get_book_from_id(old_book_id)

        # If no book exists with the given ID, the user will be informed and the method will return False to indicate failure to update the book.
        if old_book is None:
            print("Error. The book you're trying to update doesn't exist.")
            return None
        else:
            # Adds the new and updated version of the book to the dictionary of books with the copies from the old book.
            self.books[book] = copies
            # Removes the old book from the dictionary.
            self.books.pop(old_book)

    def add_member(self, member):
        """Adds the given member to the list of members"""
        self.members.append(member)

    def remove_member(self, member_id):
        """Removes the member with the given ID from the list of members"""
        # Gets the member with the given ID. member will be None if no member with the given ID could be found.
        member = self.get_member_from_id(member_id)

        # If no member exists with the given ID, the user will be informed and the method will return None to indicate failure to locate member with given ID.
        if member is None:
            print(f"Error. No member found with ID: {member_id}")
            return None

        # Removes the member from the list
        self.members.remove(member)

        # Returns True or False, depending on if the removal was successful
        if self.get_member_from_id(member_id) is None: return True
        else: return False

    def issue_book(self, book_id, member):
        """Lends a copy of the book with the given ID to the given member"""
        book = self.get_book_from_id(book_id)
        copies = self.books.get(book)

        if book is None:
            print(f"Error. No book exists with ID: {book_id}")
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
            print(f"Error. No book exists with ID: {book_id}")
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
        print(f"Error. No book found with ID: {book_id}")

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
            print(f"Error. No member found with ID: {member_id}")
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

        # Iterates through all members and compares IDs. Returns the member if they're found, otherwise returns None
        for member in self.members:
            if member.member_id == member_id:
                return member

        # Returns None if no member was found
        return None

    def get_copies(self, book_id):
        """Returns the number of copies available of the book with the given ID in the library"""
        for book in self.books:
            if book.book_id == book_id:
                return self.books.get(book)
        return 0

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