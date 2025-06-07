# app/db/init_db.py

from app.db.session import engine, Base
from app.models.tweet import Tweet
from app.models.gdelt import GDELTEntry

def init_db():
    print("🔧 Tworzenie tabel w bazie danych...")
    Base.metadata.create_all(bind=engine)
    print("✅ Gotowe!")

if __name__ == "__main__":
    init_db()
