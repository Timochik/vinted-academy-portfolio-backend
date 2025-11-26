from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import Base, engine
from models import Item, User, Category
from schemas import ItemCreate, ItemOut, CategoryCreate, CategoryOut

from fastapi import HTTPException
from typing import Optional

from schemas import UserCreate, UserLogin, UserOut
from security import hash_password, verify_password, create_access_token, get_current_user

from fastapi.security import OAuth2PasswordRequestForm

from deps import get_db

from database import DATABASE_URL
print(">>> USING THIS DATABASE:", DATABASE_URL)

# create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/items", response_model=ItemOut)
def create_item(
    item: ItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_item = Item(
        title=item.title,
        description=item.description,
        price=item.price,
        condition=item.condition,
        category_id=item.category_id,
        photo_url=item.photo_url,
        owner_id=current_user.id,
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.get("/items", response_model=list[ItemOut])
def read_items(db: Session = Depends(get_db)):
    return db.query(Item).all()

@app.get("/items/filter", response_model=list[ItemOut])
def filter_items(
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    condition: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):

    query = db.query(Item)

    if min_price is not None:
        query = query.filter(Item.price >= min_price)

    if max_price is not None:
        query = query.filter(Item.price <= max_price)

    if condition:
        query = query.filter(Item.condition.ilike(f"%{condition}%"))

    if search:
        query = query.filter(Item.title.ilike(f"%{search}%"))

    return query.order_by(Item.id).all()

@app.get("/items/paginated", response_model=list[ItemOut])
def get_paginated_items(
    skip: int = 0, 
    limit: int = 10,
    db: Session = Depends(get_db)
):
    limit = min(limit, 50)  # safety limit

    return (
        db.query(Item)
        .order_by(Item.id)
        .offset(skip)
        .limit(limit)
        .all()
    )

@app.get("/items/{item_id}", response_model=ItemOut)
def read_item(item_id: int, db: Session = Depends(get_db)):
    return db.query(Item).filter(Item.id == item_id).first()

@app.put("/items/{item_id}", response_model=ItemOut)
def update_item(item_id: int, payload: ItemCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(404, "Item not found")
    if db_item.owner_id != current_user.id:
        raise HTTPException(403, "Not allowed")

    for key, value in payload.dict().items():
        setattr(db_item, key, value)

    db.commit()
    db.refresh(db_item)
    return db_item

@app.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(404, "Item not found")
    if db_item.owner_id != current_user.id:
        raise HTTPException(403, "Not allowed")

    db.delete(db_item)
    db.commit()
    return {"detail": "Item deleted"}

@app.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    # check if username already exists
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    # check email
    existing_email = db.query(User).filter(User.email == user.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already exists")

    hashed_pw = hash_password(user.password)
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_pw
    )
    print("RAW password:", user.password)
    print("TYPE:", type(user.password))
    print("ENCODED LENGTH:", len(user.password.encode("utf-8")))

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == form_data.username).first()

    if not db_user or not verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token({
        "sub": db_user.username,
        "user_id": db_user.id
    })

    return {"access_token": token, "token_type": "bearer"}


@app.post("/categories", response_model=CategoryOut)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    existing = db.query(Category).filter(Category.name == category.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Category already exists")

    new_category = Category(name=category.name)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category

@app.get("/categories", response_model=list[CategoryOut])
def list_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()
