from sqlalchemy import Column, Integer, String, Float
from app.database import Base


class ProduitDB(Base):
    __tablename__ = "produits"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nom = Column(String(100), nullable=False)
    description = Column(String(255), nullable=False)
    prix = Column(Float, nullable=False)
    quantite_stock = Column(Integer, nullable=False)
