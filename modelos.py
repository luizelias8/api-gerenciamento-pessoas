from pydantic import BaseModel, EmailStr

# Modelo usado para criar uma pessoa (entrada)
class Pessoa(BaseModel):
    nome: str
    idade: int
    sexo: str
    email: EmailStr | None = None # Atributo opcional
