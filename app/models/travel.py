from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.asyncio import AsyncAttrs
from app.models import Base
from app.mixins import SoftDeleteMixin, TimestampMixin


class Travel(TimestampMixin, SoftDeleteMixin, Base, AsyncAttrs):
    __tablename__ = "travels"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String, nullable=False)
