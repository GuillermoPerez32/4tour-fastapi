from fastapi import APIRouter, HTTPException
from fastapi import Depends
from app.database.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select
from typing import List
from app.models import Travel, User
from app.auth import get_current_user
from app.schemas.travel import BaseTravel, TravelCreate, TravelResponse, TravelUpdate


router = APIRouter(
    prefix="/travels",
    tags=["Travels"]
)


@router.post("/", response_model=None)
async def create_travel(
    travel: TravelCreate,
    db: AsyncSession = Depends(get_session),
    _: User = Depends(get_current_user)
):
    db_travel = Travel(
        title=travel.title,
        description=travel.description,
    )

    db.add(db_travel)
    await db.commit()
    await db.refresh(db_travel)
    return TravelResponse(
        id=db_travel.id,
        title=db_travel.title,
        description=db_travel.description,
    )


@router.get("/", response_model=List[BaseTravel])
async def read_travels(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_session)):
    travels_query = await db.execute(select(Travel).offset(skip).limit(limit))
    travels = travels_query.scalars().all()
    return travels


@router.get("/{travel_id}", response_model=BaseTravel)
async def read_travel(travel_id: int, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Travel).filter(Travel.id == travel_id))
    post = result.scalars().first()
    if post is None:
        raise HTTPException(status_code=404, detail="Travel not found")
    return post


@router.put("/{travel_id}", response_model=TravelResponse)
async def update_travel(
    travel_id: int, travel: TravelUpdate,
    db: AsyncSession = Depends(get_session),
    _: User = Depends(get_current_user)
):
    result = await db.execute(select(Travel).filter(Travel.id == travel_id))
    db_travel = result.scalars().first()
    if db_travel is None:
        raise HTTPException(status_code=404, detail="Travel not found")
    db_travel.title = travel.title or db_travel.title
    db_travel.description = travel.description or db_travel.description
    await db.commit()
    await db.refresh(db_travel)
    return TravelResponse(
        id=db_travel.id,
        title=db_travel.title,
        description=db_travel.description,
    )


@router.delete("/{travel_id}", status_code=204)
async def delete_travel(
    travel_id: int,
    db: AsyncSession = Depends(get_session),
    _: User = Depends(get_current_user)
):
    post_query = await db.execute(select(Travel).filter(Travel.id == travel_id))
    db_travel = post_query.scalars().first()
    if db_travel is None:
        raise HTTPException(status_code=404, detail="Travel not found")
    await db.delete(db_travel)
    await db.commit()
    return
