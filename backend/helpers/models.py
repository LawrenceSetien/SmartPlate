from sqlalchemy import Column, Integer, String, LargeBinary
from helpers.database import Base

class Image(Base):
    __TABLENAME__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    content_type = Column(String, nullable=False)
    data = Column(LargeBinary, nullable=False)