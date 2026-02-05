from db.db_config import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import Integer, String, DateTime, ForeignKey
from datetime import datetime
import uuid
from sqlalchemy.dialects.postgresql import UUID


class UserDB(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(UUID(as_uuid=True),
                                    primary_key=True,
                                    index=True,
                                    nullable=False,
                                    default=uuid.uuid4)
    username: Mapped[str] = mapped_column(String[50],
                                          nullable=False,
                                          unique=True)
    password: Mapped[str] = mapped_column(String,
                                          nullable=False)
    
    created_users: Mapped[list["CreatedUserDB"]] = relationship(back_populates="user_author")


class CreatedUserDB(Base):
    __tablename__ = 'created_users'

    email: Mapped[str] = mapped_column(String[50],
                                       primary_key=True,
                                       nullable=False,
                                       unique=True)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True),
                                               ForeignKey("users.id", ondelete="CASCADE"),
                                               nullable=False)

    phone_no: Mapped[str] = mapped_column(String[10],
                                          unique=True,
                                          nullable=False)
    date_created: Mapped[str] = mapped_column(DateTime,
                                              nullable=False,
                                              default=datetime.now)

    user_author: Mapped["UserDB"] = relationship(back_populates="created_users")
