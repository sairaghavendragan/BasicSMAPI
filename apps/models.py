from .database import Base
from sqlalchemy import (
    Column,
    INTEGER,
    String,
    Boolean,
    PrimaryKeyConstraint,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text


class posts(Base):
    __tablename__ = "posts"

    id = Column(INTEGER, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default="True", nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False
    )
    owner_id = Column(
        INTEGER, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    owner = relationship("users")


class users(Base):
    __tablename__ = "users"

    id = Column(INTEGER, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False
    )
    admin = Column(Boolean, server_default="False", nullable=False)


class votes(Base):
    __tablename__ = "votes"

    user_id = Column(
        INTEGER,ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    post_id = Column(
        INTEGER,ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True
    )