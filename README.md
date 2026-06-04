Online Food Ordering System

Objective

A backend application built using FastAPI, SQLAlchemy, and SQLite to manage restaurants, food items, customers, and orders.

Tech Stack

* Python 3.x
* FastAPI
* SQLAlchemy
* Pydantic
* SQLite

Features

Restaurant Management

* Add Restaurant
* View Restaurants
* Update Restaurant
* Delete Restaurant

Food Item Management

* Add Food Item
* View Food Items
* Update Food Item
* Delete Food Item

Customer Management

* Add Customer
* View Customers

Order Management

* Place Order
* View Orders
* Update Order Status
* Cancel Order

Business Rules

* Customer must exist before placing an order.
* Food item must exist before ordering.
* Order total amount is calculated automatically.
* Cancelled orders cannot be modified.

Bonus Features

* Login API
* Pagination
* Search APIs
* Swagger Documentation

API Endpoints

Restaurants

* POST /restaurants
* GET /restaurants
* PUT /restaurants/{id}
* DELETE /restaurants/{id}

Food Items

* POST /food-items
* GET /food-items
* PUT /food-items/{id}
* DELETE /food-items/{id}

Customers

* POST /customers
* GET /customers

Orders

* POST /orders
* GET /orders
* PUT /orders/{order_id}
* DELETE /orders/{order_id}

Login

* POST /login

Run Project

Install Dependencies

pip install fastapi uvicorn sqlalchemy pydantic

Start Server

uvicorn main:app --reload

Swagger Documentation

http://127.0.0.1:8000/docs
