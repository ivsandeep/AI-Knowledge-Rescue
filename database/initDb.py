from database.database import engine
from database.models import Base

def initDb():
    Base.metadata.create_all(bind=engine)

print("Database and tables created successfully.")