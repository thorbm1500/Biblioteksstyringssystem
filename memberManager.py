from memberClass import Member

class MemberManager:

    member_id = 0

    def __init__(self, library):
        self.library = library

    def new_member(self, name, borrowed_books=None):
        if borrowed_books is None:
            borrowed_books = []

        while self._generate_id():
            pass

        member = Member(self.member_id, name, borrowed_books)
        self.library.add_member(member)
        return self.member_id

    # Used for generating a new ID.
    def _generate_id(self):
        self.member_id += 1
        for member in self.library.members:
            # Checks new ID number against all existing ID numbers to avoid overlap.
            if member.member_id == self.member_id:
                return True
        return False

    # Used for updating the member ID.
    def update_member_id(self, _id):
        if _id is None:
            self.member_id = 0
        else:
            self.member_id = _id

    # Used for resetting the member ID.
    def reset_member_id(self):
        self.member_id = 0

    def delete_member(self, _id):
        if self.library.remove_member(int(_id)) is not None:
            self.update_member_id(_id)