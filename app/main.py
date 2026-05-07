from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.schemas import Produit, ProduitCreate, ProduitUpdate
from app import models
from app.database import get_db, engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API CRUD Produits",
    description="API de gestion de produits pour le TP DevOps CI/CD",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def accueil():
    return {"message": "Bienvenue sur l'API CRUD Produits"}


@app.get("/produits", response_model=list[Produit])
def afficher_produits(db: Session = Depends(get_db)):
    return db.query(models.ProduitDB).all()


@app.get("/produits/{produit_id}", response_model=Produit)
def afficher_produit(produit_id: int, db: Session = Depends(get_db)):
    produit = db.query(models.ProduitDB).filter(models.ProduitDB.id == produit_id).first()
    if not produit:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    return produit


@app.post("/produits", response_model=Produit, status_code=201)
def creer_produit(produit: ProduitCreate, db: Session = Depends(get_db)):
    db_produit = models.ProduitDB(**produit.model_dump())
    db.add(db_produit)
    db.commit()
    db.refresh(db_produit)
    return db_produit


@app.put("/produits/{produit_id}", response_model=Produit)
def modifier_produit(produit_id: int, produit_modifie: ProduitUpdate, db: Session = Depends(get_db)):
    produit = db.query(models.ProduitDB).filter(models.ProduitDB.id == produit_id).first()
    if not produit:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    for key, value in produit_modifie.model_dump().items():
        setattr(produit, key, value)
    db.commit()
    db.refresh(produit)
    return produit


@app.delete("/produits/{produit_id}")
def supprimer_produit(produit_id: int, db: Session = Depends(get_db)):
    produit = db.query(models.ProduitDB).filter(models.ProduitDB.id == produit_id).first()
    if not produit:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    db.delete(produit)
    db.commit()
    return {"message": "Produit supprimé avec succès"}
