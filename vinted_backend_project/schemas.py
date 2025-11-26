from pydantic import BaseModel, EmailStr

class ItemBase(BaseModel):
    title: str
    description: str
    price: float
    condition: str
    category_id: int | None = None
    photo_url: str | None = None

class ItemCreate(ItemBase):
    pass

class ItemOut(ItemBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        orm_mode = True


class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class CategoryOut(CategoryBase):
    id: int

    class Config:
        orm_mode = True
