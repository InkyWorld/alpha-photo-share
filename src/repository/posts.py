from typing import List
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_db