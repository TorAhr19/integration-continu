from pydantic import BaseModel, Field, ConfigDict


class ProduitBase(BaseModel):
    nom: str = Field(..., min_length=2, max_length=100)
    description: str = Field(..., min_length=5, max_length=255)
    prix: float = Field(..., gt=0)
    quantite_stock: int = Field(..., ge=0)


class ProduitCreate(ProduitBase):
    pass


class ProduitUpdate(ProduitBase):
    pass


class Produit(ProduitBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
