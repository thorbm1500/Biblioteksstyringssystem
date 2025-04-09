from memberClass import Member

class MemberManager:

    current_id = 1

    def __init__(self, library, util):
        """Manager class for the Member class"""
        self.library = library
        self.util = util

    def new_member(self, name: str, borrowed_books=None, member_id=None):
        """Creates a new member. Returns the new member's ID"""
        if borrowed_books is None:
            borrowed_books = []

        # An ID from the standard order will be generated and given if no ID has been provided.
        if member_id is None:
            member_id = self._generate_id()
        else:
            # Attempts parsing input to an integer
            member_id = self.util.parse_integer(member_id)
            # If the parsing fails, the user will be informed, and the method will return False to indicate failure to update the book.
            if member_id is None:
                print(f"Error. {member_id} is not a valid member ID.")
                return False
            # If an ID has been provided, availability will be checked, and ensured.
            while not self.check_id_availability(member_id):
                member_id += 1

        member = Member(member_id, name, borrowed_books)
        self.library.add_member(member)
        return member_id

    def _generate_id(self):
        """Generates a new ID, and continues to do so until an available ID has been generated, to ensure no IDs overlap"""
        while not self.check_id_availability(self.current_id):
            self.current_id += 1
        # Returns the newly generated ID.
        return self.current_id

    def update_member_id(self, member_id=None):
        """Updates the current member ID.
        If no ID is provided, the current ID will be reset to 1"""
        if member_id is None: self.current_id = 1
        else:
            # Attempts parsing input to an integer
            member_id = self.util.parse_integer(member_id)
            # If the parsing fails, the user will be informed, and the method will return False to indicate failure to update the book.
            if member_id is None:
                print(f"Error. {member_id} is not a valid member ID.")
                return False
            self.current_id = member_id

    def delete_member(self, member_id: int):
        """Deletes the member with the given ID"""
        # Attempts parsing input to an integer
        member_id = self.util.parse_integer(member_id)
        # If the parsing fails, the user will be informed, and the method will return False to indicate failure to update the book.
        if member_id is None:
            print(f"Error. {member_id} is not a valid member ID.")
            return False
        # Returns True or False depending on if the removal was successful.
        return self.library.remove_member(member_id)


    def update_member(self, old_member_id: int, new_member_id: int, new_member_name: str):
        """Updates the member with the given ID with new details. Returns True or False depending on if the update was successful."""
        # Iterates through all members and compares IDs
        for member in self.library.members:
            # If a successful comparison has been made, the details of that member will be updated with the new details provided to the method.
            if member.member_id == old_member_id:
                member.member_id = new_member_id
                member.name = new_member_name
                return True
        print("Error. The member you're trying to update doesn't exist.")
        return False


    def check_id_availability(self, member_id: int):
        """Returns True or False, whether the given ID is available or not"""
        # Attempts parsing input to an integer
        member_id = self.util.parse_integer(member_id)
        # If the parsing fails, the user will be informed, and the method will return False to indicate that the ID isn't available.
        if member_id is None:
            print(f"Error. {member_id} is not a valid member ID.")
            return False

        # Returns True if an instance of a list isn't present, as the ID will then be available.
        if self.library.members is None:
            return True

        # Returns True if the length of the list is less than 1, as the ID will then be available.
        if len(self.library.members) < 1:
            return True

        # Iterates through all members and compares IDs. Returns False if a match is found.
        for member in self.library.members:
            if member.member_id == member_id:
                return False
        # Returns True as no more members are left to check and no matches have been found.
        return True