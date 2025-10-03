from fastapi import FastAPI
from database import engine, Base
from routes.auth.login import api_route as login_route
from routes.auth.registr import api_route as register_route
from routes.auth.logout import api_route as logout_route
from routes.auth.refresh_token import api_route as refresh_token
from routes.admin.user_route.delete import api_route as delete_user
from routes.admin.user_route.get_user_by_id import api_route as get_user_by_id
from routes.admin.user_route.get_user import api_route as get_users
from routes.admin.user_route.update_user import api_route as update_user
# from routes.admin.poduct_route.delete_products import api_route as delete_product
# from routes.admin.poduct_route.get_product_by_id import api_route as get_product_by_id
# from routes.admin.poduct_route.get_products import api_route as get_producs
# from routes.admin.poduct_route.update_product import api_route as update_product
from routes.admin.order_route.delete_order_r import api_route as delete_order
from routes.admin.order_route.get_orders import api_route as get_orders
from routes.admin.order_route.reserve_order_status import api_route as reserve_order_status
from routes.admin.stats_route import api_route as get_stats
from routes.buyyer.get_product import buyyer_route as get_product_buyyer_route
from routes.buyyer.get_me import buyyer_route as get_me_route
from routes.buyyer.get_cart import buyyer_route as get_cart_route
from routes.buyyer.delete_cart import buyyer_route as delete_cart_route
from routes.buyyer.create_order import buyyer_route as create_order_route
from routes.buyyer.add_to_card import buyyer_route as add_to_cart_route
from routes.seller_route.add_product_route import product_route as add_product
from routes.seller_route.create_sale import product_route as create_sale_route
from routes.seller_route.delete_product_route import product_route as delete_route
from routes.seller_route.get_product import product_route as get_product_route
from routes.seller_route.update_product import product_route as update_route
from routes.goest.get_products import guest_route as goest_prod
from routes.goest.get_product_by_t import guest_route as goest_prod_b_t
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")), name="static")
app.mount("/static", StaticFiles(directory="static"), name="static")

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Разрешаем все методы (GET, POST, и т.д.)
    allow_headers=["*"],  # Разрешаем все заголовки
)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)



app.include_router(login_route, prefix="/auth")
app.include_router(logout_route, prefix="/auth")
app.include_router(register_route, prefix="/auth")
app.include_router(delete_user, prefix="/admin")
app.include_router(refresh_token, prefix="/auth")
app.include_router(get_user_by_id, prefix="/admin")
app.include_router(get_users, prefix="/admin")
app.include_router(update_user, prefix="/admin")
app.include_router(get_stats, prefix="/admin")
# app.include_router(delete_product, prefix="/admin")
# app.include_router(get_product_by_id, prefix="/admin")
# app.include_router(get_producs, prefix="/admin")
# app.include_router(update_product, prefix="/admin")
app.include_router(delete_order, prefix="/admin")
app.include_router(get_orders, prefix="/admin")
app.include_router(reserve_order_status, prefix="/admin")
app.include_router(get_product_buyyer_route, prefix="/buyer")
app.include_router(get_me_route, prefix="/buyer")
app.include_router(get_cart_route, prefix="/buyer")
app.include_router(delete_cart_route, prefix="/buyer")
app.include_router(create_order_route, prefix="/buyer")
app.include_router(add_to_cart_route, prefix="/buyer")
app.include_router(add_product, prefix="/seller")
app.include_router(create_sale_route, prefix="/seller")
app.include_router(delete_route, prefix="/seller")
app.include_router(get_product_route, prefix="/seller")
app.include_router(update_route, prefix="/seller")
app.include_router(goest_prod, prefix="/guest")
app.include_router(goest_prod_b_t, prefix="/guest")



