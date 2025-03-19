from pydantic import BaseModel

# Modelo usado para criar uma pessoa (entrada)
class Pessoa(BaseModel):
    nome: str
    idade: int
    sexo: str
    email: str | None = None # Atributo opcional
