from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime

from database.database import Base


class Document(Base):

    __tablename__ = "Documents"

    id = Column(Integer, primary_key=True, index=True)

    fileName = Column(String)

    fileType = Column(String)

    filePath = Column(String)

    extractedText = Column(Text)

    summary = Column(Text)

    uploadedAt = Column(DateTime, default=datetime.utcnow)