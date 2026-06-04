from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import Session
from pydantic import BaseModel

from database import engine, SessionLocal, Base

# ---------------- INIT ----------------
Base.metadata.create_all(bind=engine)
app = FastAPI()

# ---------------- DB SESSION ----------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------- MODELS ----------------

class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    location = Column(String)
    contact_number = Column(String)


class FoodItem(Base):
    __tablename__ = "food_items"

    id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    name = Column(String)
    price = Column(Float)
    category = Column(String)


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    phone = Column(String)


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    food_item_id = Column(Integer, ForeignKey("food_items.id"))
    quantity = Column(Integer)
    total_amount = Column(Float)
    status = Column(String, default="Pending")

# ---------------- SCHEMAS ----------------

class RestaurantCreate(BaseModel):
    name: str
    location: str
    contact_number: str


class FoodItemCreate(BaseModel):
    restaurant_id: int
    name: str
    price: float
    category: str


class CustomerCreate(BaseModel):
    name: str
    email: str
    phone: str


class OrderCreate(BaseModel):
    customer_id: int
    food_item_id: int
    quantity: int

# ---------------- HOME ----------------

@app.get("/")
def home():
    return {"message": "Online Food Ordering System Running"}

# ---------------- RESTAURANTS ----------------

@app.post("/restaurants")
def add_restaurant(data: RestaurantCreate, db: Session = Depends(get_db)):
    obj = Restaurant(**data.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@app.get("/restaurants")
def get_restaurants(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    return db.query(Restaurant).offset(skip).limit(limit).all()

@app.put("/restaurants/{id}")
def update_restaurant(id: int, data: RestaurantCreate, db: Session = Depends(get_db)):
    obj = db.query(Restaurant).filter(Restaurant.id == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    obj.name = data.name
    obj.location = data.location
    obj.contact_number = data.contact_number

    db.commit()
    return {"message": "Updated successfully"}


@app.delete("/restaurants/{id}")
def delete_restaurant(id: int, db: Session = Depends(get_db)):
    obj = db.query(Restaurant).filter(Restaurant.id == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    obj.is_deleted = True
    db.commit()
    return {"message": "Deleted successfully"}

# ---------------- FOOD ITEMS ----------------

@app.post("/food-items")
def add_food(data: FoodItemCreate, db: Session = Depends(get_db)):

    restaurant = db.query(Restaurant).filter(Restaurant.id == data.restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    obj = FoodItem(**data.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@app.get("/food-items")
def get_foods(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    return db.query(FoodItem).offset(skip).limit(limit).all()


@app.put("/food-items/{id}")
def update_food(id: int, data: FoodItemCreate, db: Session = Depends(get_db)):
    obj = db.query(FoodItem).filter(FoodItem.id == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Food item not found")

    obj.restaurant_id = data.restaurant_id
    obj.name = data.name
    obj.price = data.price
    obj.category = data.category

    db.commit()
    return {"message": "Updated successfully"}


@app.delete("/food-items/{id}")
def delete_food(id: int, db: Session = Depends(get_db)):
    obj = db.query(FoodItem).filter(FoodItem.id == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Food item not found")

    db.delete(obj)
    db.commit()
    return {"message": "Deleted successfully"}

# ---------------- CUSTOMERS ----------------

@app.post("/customers")
def add_customer(data: CustomerCreate, db: Session = Depends(get_db)):
    obj = Customer(**data.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@app.get("/customers")
def get_customers(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    return db.query(Customer).offset(skip).limit(limit).all()


@app.get("/restaurants/search")
def search_restaurant(name: str, db: Session = Depends(get_db)):
    return db.query(Restaurant).filter(
        Restaurant.name.contains(name)
    ).all()


@app.get("/food-items/search")
def search_food(name: str, db: Session = Depends(get_db)):
    return db.query(FoodItem).filter(
        FoodItem.name.contains(name)
    ).all()

# ---------------- ORDERS ----------------

@app.post("/orders")
def place_order(data: OrderCreate, db: Session = Depends(get_db)):

    customer = db.query(Customer).filter(Customer.id == data.customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    food = db.query(FoodItem).filter(FoodItem.id == data.food_item_id).first()
    if not food:
        raise HTTPException(status_code=404, detail="Food item not found")

    total = food.price * data.quantity

    order = Order(
        customer_id=data.customer_id,
        food_item_id=data.food_item_id,
        quantity=data.quantity,
        total_amount=total,
        status="Pending"
    )

    db.add(order)
    db.commit()
    db.refresh(order)

    return {
        "message": "Order placed successfully",
        "order_id": order.id,
        "total_amount": order.total_amount
    }


@app.get("/orders")
def get_orders(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    return db.query(Order).offset(skip).limit(limit).all()

@app.put("/orders/{order_id}")
def update_order(order_id: int, status: str, db: Session = Depends(get_db)):

    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if order.status == "Cancelled":
        raise HTTPException(status_code=400, detail="Cancelled order cannot be modified")

    order.status = status
    db.commit()

    return {"message": "Order updated successfully"}


@app.delete("/orders/{order_id}")
def cancel_order(order_id: int, db: Session = Depends(get_db)):

    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    order.status = "Cancelled"
    db.commit()

    return {"message": "Order cancelled successfully"}

print("Creating tables...")
Base.metadata.create_all(bind=engine)
print("Tables created")

