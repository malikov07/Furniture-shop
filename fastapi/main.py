from fastapi import FastAPI
from database.schemas import JwtModel
from fastapi_jwt_auth import AuthJWT
from routers.auth import auth_router
from routers.products import product_router
from routers.categories import category_router
from routers.orders import order_router

@AuthJWT.load_config
def config():
    return JwtModel()

app = FastAPI()
app.include_router(auth_router)
app.include_router(product_router)
app.include_router(category_router)
app.include_router(order_router)

