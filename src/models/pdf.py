from datetime import datetime

class PDF:
    def __init__(self, title: str, date: datetime, path: str):
        self.title = title
        self.date = date
        self.path = path