from pydantic import BaseModel


class AuthorBase(BaseModel):
    first_name: str
    last_name: str


class AuthorCreate(AuthorBase):
    pass


class Author(BaseModel):
    pass

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
