from src.database.models.models import BetModel
from src.database.repositories.absctract_repository import AbstractRepository


class BetRepository(AbstractRepository[BetModel]):
    _model = BetModel
