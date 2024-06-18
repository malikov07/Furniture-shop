from pydantic import BaseModel, HttpUrl
from typing import List, Optional
from datetime import datetime

class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    created_date: datetime

    class Config:
        orm_mode = True

class ProductImageBase(BaseModel):
    image: str
    alt_text: Optional[str]

class ProductImageCreate(ProductImageBase):
    pass

class ProductImage(ProductImageBase):
    id: int
    product_id: int

    class Config:
        orm_mode = True

class ProductCategoryBase(BaseModel):
    product_id: int
    category_id: int

class ProductCategoryCreate(ProductCategoryBase):
    pass

class ProductCategory(ProductCategoryBase):
    id: int

    class Config:
        orm_mode = True

class CartBase(BaseModel):
    product_id: int
    user_id: int
    count: int

class CartCreate(CartBase):
    pass

class Cart(CartBase):
    id: int

    class Config:
        orm_mode = True

class ProductBase(BaseModel):
    name: str
    description: Optional[str]
    price: float
    image: str
    width: int = 50
    height: int = 90
    deep: int = 50
    color: str
    material: str
    style: str
    company_name: Optional[str]
    country: Optional[str]
    warranty_duration: Optional[int]
    slug: str

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    images: List[ProductImage]
    categories: List[Category]

    class Config:
        orm_mode = True


class OrderBase(BaseModel):
    user_id: int
    total_amount: int
    status: str
    order_date: datetime
    shipping_address: str
    payment_method: str
    tracking_number: Optional[str]

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: int
    products: List[ProductBase]

    class Config:
        orm_mode = True

class RegisterModel(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: str
    password: str
    is_staff: bool
    is_superuser: bool

    class Config:
        orm_mode = True


class LoginModel(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True


class JwtModel(BaseModel):
    authjwt_secret_key: str = '3ab42577ea4c274120ac14a8cd6d9b307f0b17f94d39a074b5073efe9c9fdbcb'


class OrderModel(BaseModel):
    user_id: int
    total_amount: float
    status: str
    shipping_address: str
    payment_method: str
    tracking_number: Optional[str] = None
    products: List[ProductBase]

    class Config:
        orm_mode = True

class OrderCreateModel(BaseModel):
    user_id: int
    total_amount: float
    status: str
    shipping_address: str
    payment_method: str
    tracking_number: Optional[str] = None
    product_ids: List[int]

    class Config:
        orm_mode = True