from memberClass import Member

class MemberManager:

    current_id = 1

    def __init__(self, library, util):
        """Manager class for the Member class"""
        self.library = library
        self.util = util

    def new_member(self, name: str, borrowed_books=None, member_id=None):
        """Creates a new member. Returns the new member's ID"""
        # Checks if a list of borrowed books has been provided. If no list has been provided, a new one will be created.
        if borrowed_books is None:
            borrowed_books = []

        # An ID from the standard order will be generated and given if no ID has been provided.
        if member_id is None: member_id = self._generate_id()
        else:
            # Attempts parsing the ID to an integer.
            # If the parsing fails, the user will be informed, and the method will return False to indicate failure to create a new member.
            if self.util.parse_integer(member_id) is None:
                print(f"[Error] {member_id} is not a valid member ID.")
                return False
            # Parses the ID to an integer.
            member_id = self.util.parse_integer(member_id)
            # If an ID has been provided, availability will be checked, and ensured.
            while not self.check_id_availability(member_id):
                member_id += 1
        # Creates a new member and adds the member to the library.
        self.library.add_member(Member(member_id, name, borrowed_books))
        # Returns the ID of the newly created member.
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
            # Attempts parsing input to an integer.
            # If the parsing fails, the user will be informed, and the method will return False to indicate failure to update the current ID.
            if self.util.parse_integer(member_id) is None:
                print(f"[Error] {member_id} is not a valid member ID.")
                return False
            # Parses the ID to an integer and updates the current ID.
            self.current_id = self.util.parse_integer(member_id)

    def delete_member(self, member_id: int):
        """Deletes the member with the provided ID"""
        # Attempts parsing input to an integer.
        # If the parsing fails, the user will be informed, and the method will return False to indicate failure to delete the member.
        if self.util.parse_integer(member_id) is None:
            print(f"[Error] {member_id} is not a valid member ID.")
            return False
        # Returns True or False depending on if the removal was successful.
        return self.library.remove_member(self.util.parse_integer(member_id))

    def update_member(self, old_member_id: int, new_member_id: int, new_member_name: str):
        """Updates the member with the provided ID with new details. Returns True or False depending on if the update was successful."""
        # Attempts parsing the IDs to integers.
        # If the parsing fails, the user will be informed, and the method will return False to indicate failure to update the member.
        if self.util.parse_integer(old_member_id) is None:
            print(f"[Error] {old_member_id} is not a valid member ID.")
            return False
        if self.util.parse_integer(new_member_id) is None:
            print(f"[Error] {new_member_id} is not a valid member ID.")
            return False
        # Parses IDs to integers.
        old_member_id = self.util.parse_integer(old_member_id)
        new_member_id = self.util.parse_integer(new_member_id)
        # Iterates through all members and compares IDs.
        for member in self.library.members:
            # If a successful comparison has been made, the details of that member will be updated with the new details provided to the method.
            if member.member_id == old_member_id:
                member.member_id = new_member_id
                member.name = new_member_name
                # Returns True to indicate successful execution.
                return True
        # Informs the user of failure.
        print("[Error] The member you're trying to update doesn't exist.")
        # Returns False to indicate unsuccessful execution.
        return False

    def check_id_availability(self, member_id: int):
        """Returns True or False, whether the provided ID is available or not"""
        # Attempts parsing input to an integer.
        # If the parsing fails, the user will be informed, and the method will return False to indicate that the ID isn't available.
        if self.util.parse_integer(member_id) is None:
            print(f"[Error] {member_id} is not a valid member ID.")
            return False
        # Parses the ID to an integer.
        member_id = self.util.parse_integer(member_id)
        # Checks if the ID is negative and returns False if that's the case as IDs cant be negative.
        if member_id < 0:
            print("[Error] Negative values are not allowed.")
            return False
        # Checks if the library contains any members, and returns True if not to indicate that the ID is available.
        if self.library.contain_members() is None:
            return True
        # Iterates through all members and compares IDs. Returns False if a match is found, to indicate that the ID is already in use.
        for member in self.library.members:
            if member.member_id == member_id:
                return False
        # Returns True to indicate that the ID is available.
        return True