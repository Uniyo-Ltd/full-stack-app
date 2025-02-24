from fastapi import APIRouter, Query, HTTPException, Depends
from sqlalchemy import func, desc
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.session import get_db
from app.models import SetMenu, Cuisine
from fastapi_cache.decorator import cache
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/set-menus")
@cache(expire=300)  # Cache for 5 minutes
async def get_set_menus(
    cuisine_slug: Optional[str] = Query(None),
    page: int = Query(1, gt=0),
    page_size: int = Query(20, gt=0, le=100),
    db: Session = Depends(get_db)
):
    try:
        logger.info(f"Starting get_set_menus request with params: cuisine_slug={cuisine_slug}, page={page}, page_size={page_size}")
        
        # Base query for live set menus
        base_query = db.query(SetMenu).filter(SetMenu.status == 1)
        logger.info("Created base query")
        
        # Apply cuisine filter if provided
        if cuisine_slug:
            base_query = base_query.join(
                SetMenu.cuisines
            ).filter(Cuisine.slug == cuisine_slug)
            logger.info(f"Applied cuisine filter: {cuisine_slug}")
        
        try:
            # Get total count for pagination
            total_count = base_query.count()
            logger.info(f"Total count: {total_count}")
            
            # Get paginated set menus sorted by popularity
            set_menus = base_query.order_by(
                desc(SetMenu.number_of_orders)
            ).offset((page - 1) * page_size).limit(page_size).all()
            logger.info(f"Retrieved {len(set_menus)} set menus")
            
            # Get cuisines with their set menu counts
            cuisines = db.query(
                Cuisine,
                func.count(SetMenu.id).label('set_menu_count'),
                func.sum(SetMenu.number_of_orders).label('total_orders')
            ).join(
                SetMenu.cuisines
            ).filter(
                SetMenu.status == 1
            ).group_by(
                Cuisine.id
            ).order_by(
                desc('total_orders')
            ).all()
            logger.info(f"Retrieved {len(cuisines)} cuisines")

            response = {
                "set_menus": [
                    {
                        "id": sm.id,
                        "name": sm.name,
                        "price_per_person": sm.price_per_person,
                        "number_of_orders": sm.number_of_orders,
                        "is_vegan": sm.is_vegan,
                        "is_vegetarian": sm.is_vegetarian,
                        "is_halal": sm.is_halal
                    } for sm in set_menus
                ],
                "cuisines": [
                    {
                        "id": c[0].id,
                        "name": c[0].name,
                        "slug": c[0].slug,
                        "set_menu_count": c[1],
                        "total_orders": c[2] or 0
                    } for c in cuisines
                ],
                "pagination": {
                    "total": total_count,
                    "page": page,
                    "page_size": page_size,
                    "total_pages": (total_count + page_size - 1) // page_size
                }
            }
            logger.info("Successfully prepared response")
            return response
            
        except Exception as e:
            logger.error(f"Database query error: {str(e)}")
            raise

    except Exception as e:
        logger.error(f"Error type: {type(e)}")
        logger.error(f"Error details: {str(e)}")
        logger.error(f"Error location: {e.__traceback__.tb_frame.f_code.co_filename}:{e.__traceback__.tb_lineno}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )