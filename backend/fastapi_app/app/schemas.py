from pydantic import BaseModel, EmailStr, Field, constr, validator
from typing import Optional
from pydantic import BaseModel, validator, constr
import re


class Settings(BaseModel):
    authjwt_secret_key: str = "6a7f1238b2e109452be655e8691b90a1449ef2c45d2378f570252a48a9fd5995"


class UserRegisterSchema(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    username: Optional[str]
    email: Optional[str]
    phone: constr(regex=r'^\+?\d{9,15}$')
    password: constr(min_length=8)

    @validator('password')
    def validate_password(cls, value):
        if not re.search(r"[A-Za-z]", value) or not re.search(r"\d", value):
            raise ValueError("Password must contain both letters and numbers.")
        return value

    @validator('first_name', 'last_name')
    def strip_names(cls, value):
        return value.strip()

    class Config:
        orm_mode = True
        schema_extra = {
            "first_name": "John",
            "last_name": "Doe",
            "username": "johndoe",
            "email": "john@example.com",
            "phone": "+1234567890",
            "password": "Password123"
        }


class UserLoginSchema(BaseModel):
    username: Optional[str]
    password: Optional[str]

    class Config:
        orm_mode = True
        schema_extra = {
            "username": "johndoe",
            "password": "Password123"
        }


class PasswordResetSchema(BaseModel):
    password: Optional[str]
    password_2: Optional[str]

    class Config:
        orm_mode = True
        schema_extra = {
            "password": "Password123",
            "password_2": "Password123"
        }


class ClientRegisterSchema(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    username: Optional[str]
    email: Optional[str]
    password: constr(min_length=8)

    @validator('password')
    def validate_password(cls, value):
        if not re.search(r"[A-Za-z]", value) or not re.search(r"\d", value):
            raise ValueError("Password must contain both letters and numbers.")
        return value

    @validator('first_name', 'last_name')
    def strip_names(cls, value):
        return value.strip()

    class Config:
        orm_mode = True
        schema_extra = {
            "first_name": "John",
            "last_name": "Doe",
            "username": "johndoe",
            "email": "john@example.com",
            "password": "Password123"
        }


class ClientLoginSchema(BaseModel):
    username: Optional[str]
    password: Optional[str]

    class Config:
        orm_mode = True
        schema_extra = {
            "username": "johndoe",
            "password": "Password123"
        }


class PasswordResetSchema(BaseModel):
    password: Optional[str]
    password_2: Optional[str]

    class Config:
        orm_mode = True
        schema_extra = {
            "password": "Password123",
            "password_2": "Password123"
        }


class FurnitureCreateSchema(BaseModel):
    name: Optional[str]
    description: Optional[str]
    price: Optional[int]
    quantity: Optional[int]
    image_url: Optional[str]

    class Config:
        orm_mode = True
        schema_extra = {
            "name": "chair",
            "description": "this is a chair",
            "price": 45,
            "quantity": 50,
            "image_url": "https://cdn0.divan.by/img/v1/p6zGYcUmfU4jylci300Lssq1qRvBkRd2qksF6wCllRQ/t:0::0:0/pd:60:60:60:60/rs:fit:1148:720:0:1:ce:0:0/g:ce:0:0/bg:f5f3f1/q:85/czM6Ly9kaXZhbi9wcm9kdWN0LzUwOTY4NDMucG5n.jpg"
        }


class FurnitureUpdateSchema(BaseModel):
    name: Optional[str]
    description: Optional[str]
    price: Optional[int]
    quantity: Optional[int]
    image_url: Optional[str]

    class Config:
        orm_mode = True
        schema_extra = {
            "name": "chair",
            "description": "this is a chair",
            "price": 45,
            "quantity": 50,
            "image_url": "https://cdn0.divan.by/img/v1/p6zGYcUmfU4jylci300Lssq1qRvBkRd2qksF6wCllRQ/t:0::0:0/pd:60:60:60:60/rs:fit:1148:720:0:1:ce:0:0/g:ce:0:0/bg:f5f3f1/q:85/czM6Ly9kaXZhbi9wcm9kdWN0LzUwOTY4NDMucG5n.jpg"
        }



class OrderCreateSchema(BaseModel):
    order_status: Optional[str]
    furniture_id: Optional[str]
    quantity: Optional[int]
    total_price: Optional[float]

    class Config:
        orm_mode = True
        schema_extra = {
            "order_status": "pn",
            "furniture_id": "str",
            "quantity": 50,
            "total_price": 23.1
        }


class OrderUpdateSchema(BaseModel):
    order_status: Optional[str]
    furniture_id: Optional[str]
    quantity: Optional[int]
    total_price: Optional[float]

    class Config:
        orm_mode = True
        schema_extra = {
            "order_status": "pn",
            "furniture_id": "str",
            "quantity": 50,
            "total_price": 23.1
        }


class PaymentCreateSchema(BaseModel):
    order_id: Optional[str]
    amount: Optional[str]
    payment_status: Optional[str]
    payment_type: Optional[str]

    class Config:
        orm_mode = True
        schema_extra = {
            "amount": "str",
            "payment_status": "pn",
            "payment_type": "str",
            "order_id": "str"
        }


class PaymentUpdateSchema(BaseModel):
    order_id: Optional[str]
    amount: Optional[str]
    payment_status: Optional[str]
    payment_type: Optional[str]

    class Config:
        orm_mode = True
        schema_extra = {
            "amount": "str",
            "payment_status": "pn",
            "payment_type": "str",
            "order_id": "str"
        }



class CargoCreateSchema(BaseModel):
    order_id: Optional[str]
    delivery_address: Optional[str]
    delivery_status: Optional[str]

    class Config:
        orm_mode = True
        schema_extra = {
            "order_id": "str",
            "delivery_status": "pn",
            "delivery_address": "str"
        }


class CargoUpdateSchema(BaseModel):
    order_id: Optional[str]
    delivery_address: Optional[str]
    delivery_status: Optional[str]

    class Config:
        orm_mode = True
        schema_extra = {
            "order_id": "str",
            "delivery_status": "pn",
            "delivery_address": "str"
        }

class CommentCreateSchema(BaseModel):
    client_id: Optional[str]
    furniture_id: Optional[str]
    content: Optional[str]

    class Config:
        orm_mode = True
        schema_extra = {
            "client_id": 0,
            "furniture_id": 0,
            "content": "bir nima"
        }


class CommentUpdateSchema(BaseModel):
    furniture_id: Optional[str]
    content: Optional[str]

    class Config:
        orm_mode = True
        schema_extra = {
            "client_id": 0,
            "furniture_id": 0,
            "content": "bir nima"
        }