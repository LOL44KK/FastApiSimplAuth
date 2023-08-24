from pydantic import BaseModel, Field

class UserLoginSchema(BaseModel):
    login: str = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "login": "login",
                "password": "any"
            }
        }

class UserRegisterSchema(BaseModel):
    login: str = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "login": "login",
                "password": "any"
            }
        }
