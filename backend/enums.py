from enum import Enum

class Role(str, Enum):
    GUEST = "guest"
    SHOPPER = 'shopper'
    SELLER = 'seller'
    ADMIN = "admin"

class Category(str, Enum):
    APPAREL = 'apparel'
    ELECTRONICS = 'electronics'
    HOME = 'home'
    BEAUTY = 'beauty'

class OrderStatus(str, Enum):
    PENDING = "pending"
    PAID = "paid"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"