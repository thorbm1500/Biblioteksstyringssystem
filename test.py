from sys import exception
import random

class Test:
    def __init__(self, library, book_manager, member_manager):
        """Test class for testing basic functions"""
        self.library = library
        self.book_manager = book_manager
        self.member_manager = member_manager
        self.member_test_id = None
        self.book_test_id = None

    def run(self):
        """Runs through all the different tests and returns True if all tests are completed successfully"""
        try:
            # Tests creation of a new book
            self.can_create_book()
            # Tests creation of a new member
            self.can_create_member()
            # Tests renting books
            self.can_rent_book()
            # Tests updating details of an existing book
            self.can_update_book()
            # Tests updating details of an existing member
            self.can_update_member()
            # Tests returning books
            self.can_return_book()
            # Tests removal of an existing member
            self.can_delete_member()
            # Tests removal of an existing book
            self.can_delete_book()
        except:
            print(exception())
            return False
        return True

    def can_create_book(self):
        """Tests creation of new books"""
        # Generates a new random ID.
        self.generate_book_id()
        # Creates a new book.
        self.book_manager.new_book("Test Book", "Test Author", 100, self.book_test_id)
        # Checks if the book was created successfully.
        if self.library.get_book_from_id(self.book_test_id) is None:
            raise ValueError(f"[Exception] Unsuccessful creation. Failed to create new book with ID: {self.book_test_id}.")

    def can_update_book(self):
        """Tests updating books' details"""
        # Gets the book.
        book = self.library.get_book_from_id(self.book_test_id)
        # Checks if an instance of the book is present.
        if book is None:
            raise ValueError(f"[Exception] Unsuccessful update. Book with ID: {self.book_test_id}, could not be located with the new ID. Make sure a book exists before trying to update its details.")
        # Generates a new random ID for the book.
        self.generate_book_id()
        new_title = "Updated Test Title"
        new_author = "Updated Author"
        new_copies = 50
        old_test_id = book.book_id
        # Attempts to update the book and checks if the update was executed successfully.
        if not self.book_manager.update_book(old_test_id,self.book_test_id,new_title,new_author,new_copies):
            raise ValueError(f"[Exception] Unsuccessful update. Book with ID: {old_test_id}, could not be located with the new ID.")
        # Gets the newly updated book and its copies.
        new_book = self.library.get_book_from_id(self.book_test_id)
        book_copies = self.library.get_copies(new_book.book_id)
        # Checks if an instance of the book is present.
        if new_book is None:
            raise ValueError(f"[Exception] Unsuccessful update. Book with ID: {self.book_test_id}, could not be located with the new ID.")
        # Checks if the title matches with the new title.
        if new_book.title != new_title:
            raise AssertionError(f"[Exception] Unsuccessful update. Book with ID: {self.book_test_id}. Expected title: {new_title}. Title found: {book.title}")
        # Checks if the author matches with the new author.
        if new_book.author != new_author:
            raise AssertionError(f"[Exception] Unsuccessful update. Book with ID: {self.book_test_id}. Expected author: {new_author}. Author found: {book.author}")
        # Checks if the copies match with the new copies.
        if book_copies != new_copies:
            raise AssertionError(f"[Exception] Unsuccessful update. Book with ID: {self.book_test_id}. Expected copies: {new_copies}. Copies found: {book_copies}")

    def can_create_member(self):
        """Tests creation of new members"""
        # Generates a new random ID.
        self.generate_member_id()
        # Creates a new member.
        self.member_manager.new_member("John Doe", None, self.member_test_id)
        # Checks if the member was created successfully.
        if self.library.get_member_from_id(self.member_test_id) is None:
            raise AssertionError(f"[Exception] Unsuccessful creation. Failed to create new member with ID: {self.member_test_id}.")

    def can_rent_book(self):
        """Tests renting books"""
        # Gets an instance of both the book and member.
        member = self.library.get_member_from_id(self.member_test_id)
        book = self.library.get_book_from_id(self.book_test_id)
        # Checks if an instance of the member is present.
        if member is None:
            raise ValueError(f"[Exception] Unsuccessful renting. Member with ID: {self.member_test_id}, could not be located.")
        # Checks if an instance of the book is present.
        if book is None:
            raise ValueError(f"[Exception] Unsuccessful renting. Book with ID: {self.book_test_id}, could not be located.")
        # Issues the book to the member.
        self.library.issue_book(book.book_id,member)
        # Checks if the member has successfully borrowed the book.
        if not member.is_borrowed(book):
            raise AssertionError(f"[Exception] Unsuccessful renting. Failed to rent book with ID: {self.book_test_id}, for member with ID: {self.member_test_id}.")

    def can_update_member(self):
        """Tests updating members' details"""
        old_test_id = self.member_test_id
        # Generates a new random ID.
        self.generate_member_id()
        new_name = "Jane Doe"

        # Attempts to update the member and checks if the update was executed successfully.
        if not self.member_manager.update_member(old_test_id,self.member_test_id,new_name):
            raise ValueError(f"[Exception] Unsuccessful update. Failed to update book with ID: {old_test_id}.")

        # Gets the member
        member = self.library.get_member_from_id(self.member_test_id)
        # Checks if an instance of the member is present.
        if member is None:
            raise ValueError(f"[Exception] Unsuccessful update. Member with ID: {self.member_test_id}, could not be located with the new ID.")
        # Checks if the name was successfully updated.
        if member.name != new_name:
            raise AssertionError(f"[Exception] Unsuccessful update. Member with ID: {self.member_test_id}. Expected name: {new_name}. Name found: {member.name}")

    def can_return_book(self):
        """Tests returning books"""
        # Gets both the member and book
        member = self.library.get_member_from_id(self.member_test_id)
        book = self.library.get_book_from_id(self.book_test_id)
        # Checks if an instance of the member is present.
        if member is None:
            raise ValueError(f"[Exception] Unsuccessful returning. Member with ID: {self.member_test_id}, could not be located.")
        # Checks if an instance of the book is present.
        if book is None:
            raise ValueError(f"[Exception] Unsuccessful returning. Book with ID: {self.book_test_id}, could not be located.")
        # Attempts to return the book.
        self.library.return_book(book.book_id,member)
        # Checks if the book was returned successfully.
        if member.is_borrowed(book):
            raise AssertionError(f"[Exception] Unsuccessful returning. Failed to return book with ID: {self.book_test_id}, for member with ID: {self.member_test_id}.")

    def can_delete_member(self):
        """Tests removal of members"""
        # Attempts to remove the member and checks the execution.
        match self.library.remove_member(self.member_test_id):
            case None: raise ValueError(f"[Exception] Failed to delete member. Member with ID: {self.member_test_id}, could not be found.")
            case True: return
            case False: raise AssertionError(f"[Exception] Unsuccessful removal. Member with ID: {self.member_test_id}, found in member list after attempt of removal.")

    def can_delete_book(self):
        """Tests removal of members"""
        # Attempts to remove the book and checks the execution.
        match self.library.remove_book(self.book_test_id):
            case None: raise ValueError(f"[Exception] Failed to delete book. Book with ID: {self.book_test_id}, could not be found.")
            case True: return
            case False: raise ValueError(f"[Exception] Failed to delete book. {self.book_test_id} is not a valid ID.")

    def generate_member_id(self):
        """Assigning test_id a random integer in the range of 1 to 1000, on every instance, ensuring an actual test will be carried out instead of running a test with fixed values."""
        self.member_test_id = random.randint(1, 1000)

    def generate_book_id(self):
        """Assigning test_id a random integer in the range of 1 to 1000, on every instance, ensuring an actual test will be carried out instead of running a test with fixed values."""
        self.book_test_id = random.randint(1, 1000)