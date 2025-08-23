from models.user import User

class SearchParticipant:
    def __init__(self, search_id: str, user_id: str, create_date: str, user: User):
        self.search_id = search_id
        self.user_id = user_id
        self.create_date = create_date
        self.user = user

    @classmethod
    def from_dict(cls, data: dict):
        user = User.from_dict(data["user"]) if "user" in data else None
        return cls(
            search_id=data.get("search_id"),
            user_id=data.get("user_id"),
            create_date=data.get("create_date"),
            user=user,
        )