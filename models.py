from pydantic import BaseModel
class Restaraunt(BaseModel):
    id: int | None = None
    name: str
    adress: str


class chef(BaseModel):
    id: int | None = None
    name: str
    restaraunt_id: int
    
class pizza(BaseModel):
    id: int | None = None
    name: str | None = None
    cheese: str | None = None
    height: str | None = None
    ingr: str | None = None
    secret: str | None = None
    restaraunt_id: int | None = None

class review(BaseModel):
    id: int | None = None
    restaraunt_id: int
    rate: int
    text: str