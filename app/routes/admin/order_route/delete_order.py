from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from cruds.admin_cruds.order.delete_orders import delete_order
from database import get_db
from services.permission import requered
from models.user import User
from enums import Role

api_route = APIRouter()


#  Роут для удаление User полнсятя удалить может только сам Admin
@api_route.delete('/delete_order/{order_id}')
async def delete_order_route(order_id:int, db:AsyncSession = Depends(get_db), current_user:User = Depends(requered(Role.ADMIN))):

    deleted_order = await delete_order(order_id, db)

    if not deleted_order:
        raise HTTPException(status_code=401, detail="не удалось удалить заказ")
    return {"message": "Удаление успешно"}