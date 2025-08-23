class User:
    def __init__(self, user_id: str, google_id: str, given_name: str, family_name: str, email: str):
        self.user_id = user_id
        self.google_id = google_id
        self.given_name = given_name
        self.family_name = family_name
        self.email = email

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            user_id=data.get("user_id"),
            google_id=data.get("google_id"),
            given_name=data.get("given_name"),
            family_name=data.get("family_name"),
            email=data.get("email"),
        )