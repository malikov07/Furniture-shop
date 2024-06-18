from fastapi import APIRouter, HTTPException, status,Depends
from database.schemas import ProductBase
from database.connection import db
from database.models import Product, Category,User
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT

product_router = APIRouter(prefix="/products")


@product_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductBase, Auth: AuthJWT = Depends()):
    try:
        Auth.jwt_required()
        claims = Auth.get_jwt_subject()
    except:
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token is required!!!!!")
    user = db.query(User).filter(User.username == claims).first()
    print(user.is_superuser)
    if user.is_superuser:
        product_data = product.dict()
        new_product = Product(**product_data)
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        return new_product
    else:
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You're not superuser so you're not allowed'!!!!!")


@product_router.get("/")
async def get_products():
    products = db.query(Product).all()
    context = [
        {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "image": product.image,
            "width": product.width,
            "height": product.height,
            "deep": product.deep,
            "color": product.color,
            "material": product.material,
            "style": product.style,
            "company_name": product.company_name,
            "country": product.country,
            "warranty_duration": product.warranty_duration,
            "created_date": product.created_date,
            "updated_date": product.updated_date,
            "slug": product.slug
        }
        for product in products
    ]
    return jsonable_encoder(context)


@product_router.get("/{id}")
async def product_detail(id:int):
    product = db.query(Product).filter(Product.id == id).first()
    if not product:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="not found")
    return jsonable_encoder(product)


@product_router.put("/{id}")
async def update_product(id:int, product:ProductBase, Auth: AuthJWT = Depends()):
    try:
        Auth.jwt_required()
        claims = Auth.get_jwt_subject()
    except:
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token is required!!!!!")
    user = db.query(User).filter(User.username == claims).first()
    print(user.is_superuser)
    if user.is_superuser:
        product_check = db.query(Product).filter(Product.id == id).first()
        if not product_check:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="product not found")


        for key, value in product.dict().items():
            setattr(product_check, key, value)

        db.add(product_check)
        db.commit()
        return HTTPException(status_code=status.HTTP_200_OK,detail="updated")
    else:
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You're not superuser so you're not allowed'!!!!!")

@product_router.delete("/{id}")
async def delete_product(id:int, Auth: AuthJWT = Depends()):
    try:
        Auth.jwt_required()
        claims = Auth.get_jwt_subject()
    except:
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token is required!!!!!")
    user = db.query(User).filter(User.username == claims).first()
    print(user.is_superuser)
    if user.is_superuser:
        product_check = db.query(Product).filter(Product.id == id).first()
        if not product_check:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="not found")
        db.delete(product_check)
        db.commit()
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="deleted")
    else:
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You're not superuser so you're not allowed'!!!!!")