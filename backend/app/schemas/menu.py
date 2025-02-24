from pydantic import BaseModel
from typing import List, Optional

class CuisineResponse(BaseModel):
    id: int
    name: str
    slug: str
    total_orders: int
    live_menu_count: int

class SetMenuResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price_per_person: float
    number_of_orders: int
    is_vegan: bool
    is_vegetarian: bool
    is_halal: bool
    cuisines: List[str]

class MenuListResponse(BaseModel):
    set_menus: List[SetMenuResponse]
    cuisines: List[CuisineResponse]
    total: int
    page: int
    per_page: int 