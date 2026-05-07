# API CRUD Produits

## Description

Cette application est une API REST développée avec FastAPI.
Elle permet de gérer des produits avec les opérations CRUD :

- Créer un produit
- Afficher les produits
- Modifier un produit
- Supprimer un produit

Le projet a été réalisé dans le cadre d’un TP DevOps CI/CD avec Jenkins et SonarQube.

---

## Technologies utilisées

- Python 3
- FastAPI
- Uvicorn

---

## Installation du projet

### Cloner le projet

```bash
git clone <url-du-repo>
cd api-produits
```

### Créer un environnement virtuel

```bash
python -m venv venv
```

### Activer l’environnement

#### Windows

```bash
venv\Scripts\activate
```

#### Linux / Mac

```bash
source venv/bin/activate
```

### Installer les dépendances

```bash
pip install -r requirements.txt
```

---

## Lancer le serveur

```bash
uvicorn app.main:app --reload
```

Le serveur démarre sur :

```text
http://127.0.0.1:8000
```

---

## Documentation Swagger

FastAPI génère automatiquement une documentation Swagger.

Accessible à l’adresse :

```text
http://127.0.0.1:8000/docs
```

---

## Structure du projet

```text
api-produits/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   └── schemas.py
│
├── requirements.txt
└── README.md
```

---

## Modèle Produit

```json
{
  "id": 1,
  "nom": "Clavier",
  "description": "Clavier mécanique",
  "prix": 49.99,
  "quantite_stock": 10
}
```

---

## Routes API

| Méthode | Endpoint | Description |
|---|---|---|
| GET | / | Accueil API |
| GET | /produits | Afficher tous les produits |
| GET | /produits/{id} | Afficher un produit |
| POST | /produits | Créer un produit |
| PUT | /produits/{id} | Modifier un produit |
| DELETE | /produits/{id} | Supprimer un produit |

---

## Validation des données

L’API vérifie automatiquement :

- nom minimum 2 caractères
- description minimum 5 caractères
- prix supérieur à 0
- quantité en stock positive ou nulle

---

## Auteur

Projet réalisé dans le cadre d’un TP DevOps CI/CD.