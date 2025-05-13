from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_db
from src.core import log

general_check_router = APIRouter(prefix='/general', tags=['general'])

@general_check_router.get("/health_checker")
async def health_checker(db: AsyncSession = Depends(get_db)):
    print("Health checker endpoint reached")
    """
    Endpoint to check the health of the database connection.
    """
    try:
        log.debug("Executing health check query...")
        result = await db.execute(text("SELECT 1"))
        log.debug(f"Query result: {result}")
        result = result.fetchone()
        log.debug(f"Fetched result: {result}")
        if result is None:
            raise HTTPException(
                status_code=500, detail="Database is not configured correctly"
            )

        return {"message": "Database is connected and healthy", "result": result[0]}

    except Exception as e:
        log.error(f"Error in health checker: {e}")
        raise HTTPException(status_code=500, detail="Error connecting to the database")