import re
from pydantic import BaseModel, validator

class User(BaseModel):
    username: str
    password: str

    @validator('username')
    def validator_username(cls, value):
        if not re.match('^[a-z][0-9]|@)+$', value):
            raise ValueError('Usernamae format invalid')
        return value
    
