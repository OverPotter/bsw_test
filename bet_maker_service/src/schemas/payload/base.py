from pydantic import BaseModel


class BasePayload(BaseModel):
    class Config:
        alias_generator = "to_camel"
