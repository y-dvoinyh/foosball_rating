from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from .base import Base
from .mixins.int_id_pk import IntIdPkMixin


class Player(IntIdPkMixin, Base):
    first_name: Mapped[str] = mapped_column(unique=True)
