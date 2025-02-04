import datetime
from uuid import UUID
from typing import Optional
from fastapi import APIRouter, HTTPException, status, Depends, Path
from fastapi.encoders import jsonable_encoder
from fastapi_app.app.schemas import FurnitureCreateSchema, FurnitureUpdateSchema
from fastapi_app.app.database import Session, ENGINE
from fastapi_app.app.models import Furniture, Admin, Client
from fastapi_jwt_auth.auth_jwt import AuthJWT
from fastapi_app.app.helpers import Get_info
from werkzeug.datastructures.auth import Authorization
from werkzeug.security import check_password_hash, generate_password_hash

session = Session(bind=ENGINE)

furnitures_router = APIRouter(prefix="/furniture", tags=["Furniture"])


@furnitures_router.get('/search/{q}')
async def get_furniture(q: Optional[str] = Path(..., min_length=1), authorization: AuthJWT = Depends()):
    try:
        authorization.jwt_required()
        check_user = session.query(Client).filter(Client.username == authorization.get_jwt_subject()).first()
        if not check_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Users not found")
        if q:
            furnitures = session.query(Furniture).filter(
                (Furniture.name.ilike(f"%{q}%"))
            ).all()
        else:
            furnitures = session.query(Furniture).all()
        if not furnitures:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No users found")
        return jsonable_encoder(furnitures)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


@furnitures_router.get('/')
async def get_furniture(Authorization: AuthJWT = Depends()):
    try:
        Authorization.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    # Get user from token
    check_user = session.query(Client).filter(Client.username == Authorization.get_jwt_subject()).first()

    if check_user:
        furnitures = session.query(Furniture).all()  # Fetch all furniture data
        data = [{
            "status": 200,
            "product": {
                "name": furniture.name,
                "description": furniture.description,
                "price": furniture.price,
                "quantity": furniture.quantity,
                "image": furniture.image_url,
                "id": ''.join(map(lambda part: part[-3:], str(furniture.id).split("-")))
            }
        } for furniture in furnitures]

        return jsonable_encoder(data)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Furniture not found')


@furnitures_router.get('/furniture/{id}')
async def furniture_detail(id: str, Authorization: AuthJWT = Depends()):
    try:
        Authorization.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Token')
    check_user = session.query(Admin).filter(Admin.username == Authorization.get_jwt_subject()).first()
    if check_user:
        check_furniture = session.query(Furniture).all()
        for from_database2 in check_furniture:
            from_database1 = ''.join(map(lambda part: part[-3:], str(from_database2.id).split("-")))
            check_id = Get_info(id)
            if check_id.get_from_id(from_database1) == "successfully":
                if from_database2 is not None:
                    data = {
                        "status": 200,
                        "product": {
                            "id": id,
                            "name": from_database2.name,
                            "description": from_database2.description,
                            "price": from_database2.price,
                            "quantity": from_database2.quantity,
                            "image": from_database2.image_url
                        }
                    }
                return jsonable_encoder(data)
            return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')


@furnitures_router.post("/create")
async def create_furniture(furniture: FurnitureCreateSchema, Authorization: AuthJWT = Depends()):
    try:
        Authorization.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Token')
    check_user = session.query(Admin).filter(Admin.username == Authorization.get_jwt_subject()).first()
    if check_user:
        try:
            if check_user.is_admin:
                new_furniture = Furniture(
                    name=furniture.name,
                    admin_id=check_user.id,
                    description=furniture.description,
                    price=furniture.price,
                    quantity=furniture.quantity,
                    image_url=furniture.image_url
                )
                session.query(Furniture)
                session.add(new_furniture)
                session.commit()
                data = {
                    "code": 200,
                    "success": True,
                    "id": new_furniture.id,
                    "message": "Successfully created furniture"
                }
                return jsonable_encoder(data)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Adminlik xuquqiga emassiz')


@furnitures_router.put("/update/{id}")
async def update_router(id: str, furniture: FurnitureUpdateSchema, Authorization: AuthJWT = Depends()):
    try:
        Authorization.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Token')
    check_user = session.query(Admin).filter(Admin.username == Authorization.get_jwt_subject()).first()
    if check_user:
        check_furniture = session.query(Furniture).all()
        for from_database2 in check_furniture:
            from_database1 = ''.join(map(lambda part: part[-3:], str(from_database2.id).split("-")))
            check_id = Get_info(id)
            if check_id.get_from_id(from_database1) == "successfully":
                if from_database2 is not None:
                    for key, value in furniture.dict().items():
                        setattr(from_database2, key, value)
                        data = {
                            "code": 200,
                            "success": True,
                            "message": "Successfully updated furniture",
                            "object": {
                                "id": id,
                                "name": from_database2.name,
                                "description": from_database2.description,
                                "price": from_database2.price,
                                "quantity": from_database2.quantity,
                                "image_url": from_database2.image_url,
                            }
                        }
                        session.add(from_database2)
                        session.commit()
                        return jsonable_encoder(data)
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')


@furnitures_router.delete("/delete/{id}")
async def delete_furniture(id: str, Authorization: AuthJWT = Depends()):
    try:
        Authorization.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Token')
    check_user = session.query(Admin).filter(Admin.username == Authorization.get_jwt_subject()).first()
    if check_user:
        furniture_id = UUID(id)
        check_furniture = session.query(Furniture).filter(Furniture.id == furniture_id).first()
        if check_furniture:
            session.delete(check_furniture)
            session.commit()
            return jsonable_encoder({"code": 200, "message": "Successfully deleted furniture"})

        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="furniture not found")
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
