from pydantic import BaseModel

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


class LoginRequest(BaseModel):
    username: str
    password: str