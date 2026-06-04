from database import engine, Base
from main import Restaurant, FoodItem, Customer, Order

Base.metadata.create_all(bind=engine)

print("Database tables created successfully!")