from fastapi import APIRouter, HTTPException, status,Depends
from database.schemas import OrderCreateModel
from database.connection import db
from database.models import Product, User, Order
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT
import datetime

order_router = APIRouter(prefix="/orders")


@order_router.post("/")
async def create_order(order: OrderCreateModel, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
        claims = Authorize.get_jwt_subject()
    except:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You're not allowed to do that")
    
    super_user = db.query(User).filter(User.username == claims).first()
    if not super_user or not super_user.is_staff:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You're not a superuser, so you're not allowed to create orders")
    
    user = db.query(User).filter(User.id == order.user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")
    
    products = db.query(Product).filter(Product.id.in_(order.product_ids)).all()
    if not products or len(products) != len(order.product_ids):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="One or more products not found")

    new_order = Order(
        user_id=order.user_id,
        total_amount=order.total_amount,
        status=order.status,
        shipping_address=order.shipping_address,
        payment_method=order.payment_method,
        tracking_number=order.tracking_number,
        order_date=datetime.datetime.now()
    )
    
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    for product in products:
        new_order.products.append(product)
    
    db.commit()
    db.refresh(new_order)

    response_order = {
        "id": new_order.id,
        "user_id": new_order.user_id,
        "total_amount": new_order.total_amount,
        "status": new_order.status,
        "shipping_address": new_order.shipping_address,
        "payment_method": new_order.payment_method,
        "tracking_number": new_order.tracking_number,
        "created_date": new_order.created_date.isoformat(),
        "updated_date": new_order.updated_date.isoformat(),
        "order_date": new_order.order_date.isoformat(),
        "products": [{"id": p.id, "name": p.name, "description": p.description, "price": p.price} for p in new_order.products]
    }

    return response_order
@order_router.get("/")
async def get_orders():
    orders = db.query(Order).all()
    response_orders = [
        {
            "id": order.id,
            "user_id": order.user_id,
            "total_amount": order.total_amount,
            "status": order.status,
            "shipping_address": order.shipping_address,
            "payment_method": order.payment_method,
            "tracking_number": order.tracking_number,
            "created_date": order.created_date.isoformat(),
            "updated_date": order.updated_date.isoformat(),
            "order_date": order.order_date.isoformat(),
            "products": [{"id": p.id, "name": p.name, "description": p.description, "price": p.price} for p in order.products]
        }
        for order in orders
    ]
    return response_orders

@order_router.get("/{id}")
async def get_order_by_id(id: int):
    order = db.query(Order).filter(Order.id == id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    
    response_order = {
        "id": order.id,
        "user_id": order.user_id,
        "total_amount": order.total_amount,
        "status": order.status,
        "shipping_address": order.shipping_address,
        "payment_method": order.payment_method,
        "tracking_number": order.tracking_number,
        "created_date": order.created_date.isoformat(),
        "updated_date": order.updated_date.isoformat(),
        "order_date": order.order_date.isoformat(),
        "products": [{"id": p.id, "name": p.name, "description": p.description, "price": p.price} for p in order.products]
    }
    return response_order

@order_router.put("/{id}")
async def update_order(id: int, order_update: OrderCreateModel):
    order = db.query(Order).filter(Order.id == id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    user = db.query(User).filter(User.id == order_update.user_id).first()
    print(user)
    if not user:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")
    if order_update.product_ids:
        products = db.query(Product).filter(Product.id.in_(order_update.product_ids)).all()
        

        if not products or len(products) != len(order_update.product_ids):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="One or more products not found")
        order.products = products

    for key, value in order_update.dict(exclude_unset=True).items():
        setattr(order, key, value)
    
    order.updated_date = datetime.datetime.now()
    db.commit()
    db.refresh(order)

    response_order = {
        "id": order.id,
        "user_id": order.user_id,
        "total_amount": order.total_amount,
        "status": order.status,
        "shipping_address": order.shipping_address,
        "payment_method": order.payment_method,
        "tracking_number": order.tracking_number,
        "created_date": order.created_date.isoformat(),
        "updated_date": order.updated_date.isoformat(),
        "order_date": order.order_date.isoformat(),
        "products": [{"id": p.id, "name": p.name, "description": p.description, "price": p.price} for p in order.products]
    }
    return response_order

@order_router.delete("/{id}", response_model=dict)
async def delete_order(id: int):
    order = db.query(Order).filter(Order.id == id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    
    db.delete(order)
    db.commit()
    
    return {"detail": "Order deleted successfully"}