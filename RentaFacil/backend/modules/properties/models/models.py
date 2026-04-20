from sqlalchemy import String, Numeric, ForeignKey, Text, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from config.database import Base, TimestampMixin
import enum

class PropertyStatus(str, enum.Enum):
    vacant = "vacant"
    occupied = "occupied"
    maintenance = "maintenance"

class PropertyType(str, enum.Enum):
    apartment = "apartment"
    house = "house"
    commercial = "commercial"
    office = "office"
    warehouse = "warehouse"

class Property(Base, TimestampMixin):
    __tablename__ = "properties"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    name: Mapped[str] = mapped_column(String(255))
    address: Mapped[str] = mapped_column(String(500))
    city: Mapped[str] = mapped_column(String(100), nullable=True)
    state: Mapped[str] = mapped_column(String(100), nullable=True)
    property_type: Mapped[str] = mapped_column(String(50), default="apartment")
    monthly_rent: Mapped[float] = mapped_column(Numeric(10, 2))
    status: Mapped[str] = mapped_column(String(20), default="vacant")
    notes: Mapped[str] = mapped_column(Text, nullable=True)
    owner = relationship("User", back_populates="properties")
    contracts = relationship("Contract", back_populates="property")
