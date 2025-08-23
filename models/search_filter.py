class SearchFilter:
    def __init__(self, search_filter_id: str, name: str, filter_value: str, search_id: str):
        self.search_filter_id = search_filter_id
        self.name = name
        self.filter_value = filter_value
        self.search_id = search_id

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            search_filter_id=data.get("search_filter_id"),
            name=data.get("name"),
            filter_value=data.get("filter_value"),
            search_id=data.get("search_id"),
        )