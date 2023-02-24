from pydantic import BaseModel, validator

class Credenciales(BaseModel):
    username: str
    password: str
    env: str
    
    @validator('env')
    def validate_env(cls, env_value):
        if env_value not in ('prod', 'sandbox'):
            raise ValueError('El valor del atributo env debe ser "prod" o "sandbox"')
        return env_value