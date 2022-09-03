from pydantic import BaseModel


class AuthorBase(BaseModel):
    name: str


class AuthorCreate(AuthorBase):
    pass


class Author(BaseModel):
    pass

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
