from sys import exception
import random

class Test:

    def __init__(self, library, book_manager, member_manager):
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
            # Tests updating details of an existing book
            self.can_update_book()
            # Tests creation of a new member
            self.can_create_member()
            # Tests renting books
            #self.can_rent_books()todo
            # Tests updating details of an existing member
            self.can_update_member()
            # Tests returning books
            #self.can_return_books()todo
            # Tests removal of an existing member
            self.can_delete_member()
        except:
            print(exception())
            return False
        return True

    def can_create_book(self):
        """Tests creation of new books"""
        self.generate_book_id()
        self.book_manager.new_book("Test Book", "Test Author", 100, self.book_test_id)
        if self.library.get_book_from_id(self.book_test_id) is None:
            raise ValueError(f"Exception: Unsuccessful creation. Failed to create new book with ID: {self.book_test_id}.")

    def can_update_book(self):
        """Tests updating books' details"""
        book = self.library.get_book_from_id(self.book_test_id)

        self.generate_book_id()
        new_title = "Updated Test Title"
        new_author = "Updated Author"
        new_copies = 50

        old_test_id = book.book_id
        old_title = book.title
        old_author = book.author
        old_copies = self.library.get_copies(book.book_id)

        self.book_manager.update_book(old_test_id,self.book_test_id,new_title,new_author,new_copies)

        new_book = self.library.get_book_from_id(self.book_test_id)
        book_copies = self.library.get_copies(new_book.book_id)

        if new_book is None:
            raise ValueError(f"Exception: Unsuccessful update. Book with ID: {self.book_test_id}, could not be located with the new ID.")

        if new_book.title != new_title:
            raise AssertionError(f"Exception: Unsuccessful update. Book with ID: {self.book_test_id}. Expected title: {new_title}. Title found: {book.title}")

        if new_book.author != new_author:
            raise AssertionError(f"Exception: Unsuccessful update. Book with ID: {self.book_test_id}. Expected author: {new_author}. Author found: {book.author}")

        if book_copies != new_copies:
            raise AssertionError(f"Exception: Unsuccessful update. Book with ID: {self.book_test_id}. Expected copies: {new_copies}. Copies found: {book_copies}")

    def can_create_member(self):
        """Tests creation of new members"""
        self.generate_member_id()
        self.member_manager.new_member("John Doe", None, self.member_test_id)
        if self.library.get_member_from_id(self.member_test_id) is None:
            raise AssertionError(f"Exception: Unsuccessful creation. Failed to create new member with ID: {self.member_test_id}.")

    def can_update_member(self):
        """Tests updating members' details"""
        old_test_id = self.member_test_id
        self.generate_member_id()
        new_name = "Jane Doe"

        self.member_manager.update_member(old_test_id,self.member_test_id,new_name)

        member = self.library.get_member_from_id(self.member_test_id)

        if member is None:
            raise ValueError(f"Exception: Unsuccessful update. Member with ID: {self.member_test_id}, could not be located with the new ID.")

        if member.name != new_name:
            raise AssertionError(f"Exception: Unsuccessful update. Member with ID: {self.member_test_id}. Expected name: {new_name}. Name found: {member.name}")


    def can_delete_member(self):
        """Tests removal of members"""
        match self.library.remove_member(self.member_test_id):
            case None: raise ValueError(f"Exception: Failed to delete member. Member with ID: {self.member_test_id}, could not be found.")
            case True: return
            case False: raise AssertionError(f"Exception: Unsuccessful removal. Member with ID: {self.member_test_id}, found in member list after attempt of removal.")

    def generate_member_id(self):
        """Assigning test_id a random integer in the range of 1 to 1000, on every instance, ensuring an actual test will be carried out instead of running a test with fixed values."""
        self.member_test_id = random.randint(1, 1000)

    def generate_book_id(self):
        """Assigning test_id a random integer in the range of 1 to 1000, on every instance, ensuring an actual test will be carried out instead of running a test with fixed values."""
        self.book_test_id = random.randint(1, 1000)