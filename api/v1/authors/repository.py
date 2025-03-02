from db.base_repository import BaseRepository
from db.models import Author


class AuthorRepository(BaseRepository[Author]):
    def __init__(self):
        super().__init__(Author)