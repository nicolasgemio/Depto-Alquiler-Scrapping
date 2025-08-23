from typing import List
from models.search_participant import SearchParticipant
from models.search_filter import SearchFilter


class Search:
    def __init__(
        self,
        search_id: str,
        title: str,
        user_id: str,
        create_date: str,
        search_participants: List[SearchParticipant],
        search_filters: List[SearchFilter],
    ):
        self.search_id = search_id
        self.title = title
        self.user_id = user_id
        self.create_date = create_date
        self.search_participants = search_participants
        self.search_filters = search_filters

    @classmethod
    def from_dict(cls, data: dict):
        participants = [SearchParticipant.from_dict(p) for p in data.get("search_participants", [])]
        filters = [SearchFilter.from_dict(f) for f in data.get("search_filters", [])]
        return cls(
            search_id=data.get("search_id"),
            title=data.get("title"),
            user_id=data.get("user_id"),
            create_date=data.get("create_date"),
            search_participants=participants,
            search_filters=filters,
        )