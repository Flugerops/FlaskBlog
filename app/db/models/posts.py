from .. import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

from datetime import date

class Post(Base):
    __tablename__ = "posts"
    created: Mapped[date]
    title: Mapped[str]
    content: Mapped[str]
    