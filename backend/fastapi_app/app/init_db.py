from .database import Base, ENGINE
from .models import Admin, Client, Comments, Furniture, Cargo, Payment, Order


def migrate():
    Base.metadata.create_all(bind=ENGINE)
