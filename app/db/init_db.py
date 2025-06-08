from app.db.session import engine, Base
from app.models import *

def init_db():
    from app.models import Headline, Site
    Base.metadata.create_all(bind=engine)
