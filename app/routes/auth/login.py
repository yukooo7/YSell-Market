from database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, APIRouter
from schemas.login import ResponseLogin, RequestToken
from cruds.auth_crud import login_crud


api_route = APIRouter()


@api_route.post('/login', response_model=RequestToken)
async def login_route(data:ResponseLogin, db:AsyncSession = Depends(get_db)):
    try:
        user = await login_crud.login(data, db)
        return RequestToken(access_token=user.access_token, refresh_token=user.refresh_token, token_type='bearer')
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))