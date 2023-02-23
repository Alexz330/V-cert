from pydantic import BaseModel

class Credenciales(BaseModel):
    username:str
    password:str