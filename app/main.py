from fastapi import FastAPI, HTTPException
from app.schemas import Produit, ProduitCreate, ProduitUpdate

app = FastAPI(
    title="API CRUD Produits",
    description="API de gestion de produits pour le TP DevOps CI/CD",
    version="1.0.0"
)

produits = []
prochain_id = 1


@app.get("/")
def accueil():
    return {"message": "Bienvenue sur l'API CRUD Produits"}


@app.get("/produits", response_model=list[Produit])
def afficher_produits():
    return produits


@app.get("/produits/{produit_id}", response_model=Produit)
def afficher_produit(produit_id: int):
    for produit in produits:
        if produit["id"] == produit_id:
            return produit

    raise HTTPException(status_code=404, detail="Produit non trouvé")


@app.post("/produits", response_model=Produit, status_code=201)
def creer_produit(produit: ProduitCreate):
    global prochain_id

    nouveau_produit = {
        "id": prochain_id,
        "nom": produit.nom,
        "description": produit.description,
        "prix": produit.prix,
        "quantite_stock": produit.quantite_stock
    }

    produits.append(nouveau_produit)
    prochain_id += 1

    return nouveau_produit


@app.put("/produits/{produit_id}", response_model=Produit)
def modifier_produit(produit_id: int, produit_modifie: ProduitUpdate):
    for produit in produits:
        if produit["id"] == produit_id:
            produit["nom"] = produit_modifie.nom
            produit["description"] = produit_modifie.description
            produit["prix"] = produit_modifie.prix
            produit["quantite_stock"] = produit_modifie.quantite_stock
            return produit

    raise HTTPException(status_code=404, detail="Produit non trouvé")


@app.delete("/produits/{produit_id}")
def supprimer_produit(produit_id: int):
    for produit in produits:
        if produit["id"] == produit_id:
            produits.remove(produit)
            return {"message": "Produit supprimé avec succès"}

    raise HTTPException(status_code=404, detail="Produit non trouvé")