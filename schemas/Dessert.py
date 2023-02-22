from pydantic import BaseModel

from schemas.Ingredient import Ingredient

class Dessert(BaseModel):
    name: str
    id_category: int

    def __str__(self) -> str:
        return f'name: {self.name} id_category: {self.id_category}'

class DessertGeneral(BaseModel):
    name: str
    ingredients: list[Ingredient]
    portion : float
    id_category: int