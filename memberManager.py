from memberClass import Member

class MemberManager:

    member_id = 0

    def __init__(self, library):
        self.library = library

    def new_member(self, name, borrowed_books):
        self.member_id += 1
        member = Member(self.member_id, name, borrowed_books)
        self.library.add_member(member)
        return self.member_id