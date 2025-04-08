from memberClass import Member

class MemberManager:

    member_id = 0

    def __init__(self, library):
        """Manager class for the Member class"""
        self.library = library

    def new_member(self, name, borrowed_books=None):
        """Creates a new member. Returns the new member's ID"""
        if borrowed_books is None:
            borrowed_books = []

        self._generate_id()

        member = Member(self.member_id, name, borrowed_books)
        self.library.add_member(member)
        return self.member_id

    def _generate_id(self):
        """Generates a new ID, to ensure no IDs overlap"""
        while True:
            self.member_id += 1
            for member in self.library.members:
                # Checks new ID number against all existing IDs
                if member.member_id == self.member_id: break
            return

    def update_member_id(self, _id=None):
        """Updates the current member ID"""
        if _id is None: self.reset_member_id()
        else: self.member_id = _id - 1

    def reset_member_id(self):
        """Resets the current member ID"""
        self.member_id = 0

    def delete_member(self, _id):
        """Deletes the member with the given ID"""
        if self.library.remove_member(int(_id)) is not None:
            self.update_member_id(_id)

    def update_member(self, old_member_id, new_member_id, new_member_name):
        """Updates the member with the given ID with new details"""
        for member in self.library.members:
            if member.member_id == old_member_id:
                member.member_id = new_member_id
                member.name = new_member_name


    def check_id_availability(self, member_id):
        """Returns True or False, whether the given ID is available or in use"""
        try:
            member_id = int(member_id)
        except:
            return False

        if member_id == -999: return False

        for member in self.library.members:
            if member.member_id == member_id:
                return False
        return True