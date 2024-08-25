from pydantic import BaseModel


class BaseResponse(BaseModel):
    class Config:
        from_attributes = True
        alias_generator = "to_camel"
