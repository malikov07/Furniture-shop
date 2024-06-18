from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, DateTime,Table,Float
from .connection import Base
from sqlalchemy.orm import relationship
import datetime

class User(Base):
    __tablename__ = "auth_user"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(60))
    last_name = Column(String(60))
    email = Column(String(60))
    username = Column(String(60))
    password = Column(String(60))
    is_staff = Column(Boolean(),default=False)
    is_active = Column(Boolean(),default=True)
    is_superuser = Column(Boolean(),default=False)
    date_joined = Column(DateTime(),default=datetime.datetime.now())

    carts = relationship("Cart")
    orders = relationship("Order")


class Category(Base):
    __tablename__ = "shop_category"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(60))
    created_date = Column(DateTime, nullable=False,default=datetime.datetime.now())

    def __repr__(self):
        return f"<Category(name={self.name})>"



class Product(Base):
    __tablename__ = "shop_product"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(60))
    description = Column(String, nullable=True)
    price = Column(Float(precision=2))
    image = Column(String)
    width = Column(Integer, default=50)
    height = Column(Integer, default=90)
    deep = Column(Integer, default=50)
    color = Column(String(10))
    material = Column(String(10))
    style = Column(String(10))
    company_name = Column(String(60), nullable=True)
    country = Column(String(60), nullable=True)
    warranty_duration = Column(Integer, nullable=True,default=12)
    slug = Column(String, unique=True, nullable=True)
    created_date = Column(DateTime, nullable=False,default=datetime.datetime.now())
    updated_date = Column(DateTime, nullable=False,default=datetime.datetime.now())

    images = relationship("ProductImage")
    categories = relationship("ProductCategory")
    carts = relationship("Cart")

    def __repr__(self):
        return f"<Product(name={self.name}, price={self.price})>"
    


class ProductImage(Base):
    __tablename__ = "shop_productimage"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('shop_product.id')) 
    image = Column(String)
    alt_text = Column(String, default="img not loaded", nullable=True)

    product = relationship("Product", back_populates="images")

    def __repr__(self):
        return f"<ProductImage(product={self.product.name}, id={self.id})>"


class ProductCategory(Base):
    __tablename__ = "shop_productcategory"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('shop_product.id'))
    category_id = Column(Integer, ForeignKey('shop_category.id'))

    product = relationship("Product", back_populates="categories")
    category = relationship("Category")

    def __repr__(self):
        return f"<ProductCategory(product={self.product.name}, category={self.category.name})>"

class Cart(Base):
    __tablename__ = "shop_cart"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('shop_product.id'))
    user_id = Column(Integer, ForeignKey('auth_user.id'))
    count = Column(Integer)

    product = relationship("Product", back_populates="carts")
    user = relationship("User", back_populates="carts")

    def __repr__(self):
        return f"<Cart(product={self.product.name}, user={self.user.username}, count={self.count})>"
    


order_products = Table('shop_order_products', Base.metadata,
    Column('order_id', Integer, ForeignKey('shop_order.id')),
    Column('product_id', Integer, ForeignKey('shop_product.id'))
)

class Order(Base):
    __tablename__ = "shop_order"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('auth_user.id'))
    total_amount = Column(Integer)
    status = Column(String(20))
    order_date = Column(DateTime, nullable=False)
    shipping_address = Column(String(200))
    payment_method = Column(String(50))
    tracking_number = Column(String(50), nullable=True)
    created_date = Column(DateTime, nullable=False,default=datetime.datetime.now())
    updated_date = Column(DateTime, nullable=False,default=datetime.datetime.now())

    user = relationship("User", back_populates="orders")
    products = relationship("Product", secondary=order_products)

    def __repr__(self):
        return f"<Order(user={self.user.username}, id={self.id}, total_amount={self.total_amount}, status={self.status})>"