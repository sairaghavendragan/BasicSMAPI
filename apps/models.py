from .database import Base
from sqlalchemy import (
    Column,
    INTEGER,
    String,
    Boolean,
    PrimaryKeyConstraint,
    ForeignKey,
)
from sqlalchemy.orm import relationship,Mapped,mapped_column
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from typing import List
from datetime import datetime


class Post(Base):
    __tablename__ = "posts"

    id:Mapped[int] = mapped_column(INTEGER, primary_key=True, nullable=False)
    title:Mapped[str] = mapped_column(String, nullable=False)
    content:Mapped[str] = mapped_column(String, nullable=False)
    published:Mapped[bool] = mapped_column(Boolean, server_default="True", nullable=False)
    created_at:Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False
    )
    owner_id:Mapped[int] = mapped_column(
        INTEGER, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    owner:Mapped["User"] = relationship( backref="posts")
    votes: Mapped[List["Vote"]] = relationship(back_populates="post")



class User(Base):
    __tablename__ = "users"

    id:Mapped[int] = mapped_column(INTEGER, primary_key=True, nullable=False)
    email:Mapped[str] = mapped_column(String, nullable=False, unique=True)
    password:Mapped[str] = mapped_column(String, nullable=False)
    created_at:Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False
    )
    admin:Mapped[bool] = mapped_column(Boolean, server_default=text("False"), nullable=False)
    votes: Mapped[List["Vote"]] = relationship(back_populates="user") 


class Vote(Base):
    __tablename__ = "votes"

    user_id:Mapped[int] = mapped_column(
        INTEGER,ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    post_id:Mapped[int] = mapped_column(
        INTEGER,ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True
    )

    dir:Mapped[int] = mapped_column(INTEGER, nullable=False)

    user:Mapped["User"] = relationship(back_populates="votes")
    post:Mapped["Post"] = relationship(back_populates="votes")