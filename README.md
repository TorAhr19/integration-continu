# API CRUD Produits — TP DevOps CI/CD

## Description

Application backend Python (FastAPI) de gestion de produits avec une chaîne CI/CD complète intégrant Jenkins et SonarQube.

**Opérations CRUD disponibles :**
- Créer un produit
- Afficher tous les produits
- Afficher un produit par ID
- Modifier un produit
- Supprimer un produit

---

## Technologies utilisées

| Rôle | Outil |
|------|-------|
| Framework API | FastAPI |
| Serveur ASGI | Uvicorn |
| Validation données | Pydantic |
| Tests | pytest |
| Couverture | coverage.py |
| Complexité | Radon |
| Linting | Pylint |
| CI/CD | Jenkins |
| Analyse qualité | SonarQube |

---

## Structure du projet

```
integration-continu/
│
├── app/
│   ├── __init__.py
│   ├── main.py          # Routes FastAPI (CRUD)
│   └── schemas.py       # Modèles Pydantic
│
├── tests/
│   └── test_products.py # Tests unitaires et d'intégration
│
├── Jenkinsfile          # Pipeline CI/CD Jenkins
├── sonar-project.properties  # Configuration SonarQube
├── requirements.txt     # Dépendances Python
└── README.md
```

---

## Installation

### 1. Cloner le projet

```bash
git clone <url-du-repo>
cd integration-continu
```

### 2. Créer et activer l'environnement virtuel

```bash
# Créer
python3 -m venv venv

# Activer (Linux/Mac)
source venv/bin/activate

# Activer (Windows)
venv\Scripts\activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

---
## Lancer les services

```bash
docker compose up -d 
```

## Lancer Swagger

```bash
cd C:\XXX\XXX\XXX\integration-continu
venv\Scripts\activate
uvicorn app.main:app --reload
```

Serveur disponible sur : `http://127.0.0.1:8000`

Documentation Swagger : `http://127.0.0.1:8000/docs`

---

## Routes API

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/` | Message d'accueil |
| GET | `/produits` | Lister tous les produits |
| GET | `/produits/{id}` | Afficher un produit |
| POST | `/produits` | Créer un produit |
| PUT | `/produits/{id}` | Modifier un produit |
| DELETE | `/produits/{id}` | Supprimer un produit |

### Modèle Produit

```json
{
  "id": 1,
  "nom": "Clavier",
  "description": "Clavier mécanique",
  "prix": 49.99,
  "quantite_stock": 10
}
```

### Règles de validation

- `nom` : 2 à 100 caractères
- `description` : 5 à 255 caractères
- `prix` : strictement supérieur à 0
- `quantite_stock` : positif ou nul

---

## Lancer les tests

```bash
# Tests simples
pytest tests/ -v

# Tests avec rapport de couverture
pytest tests/ --cov=app --cov-report=term-missing -v

# Générer le rapport XML (pour SonarQube)
pytest tests/ --cov=app --cov-report=xml:coverage.xml -v
```

### Complexité avec Radon

```bash
# Complexité cyclomatique
radon cc app/ -s -a

# Indice de maintenabilité
radon mi app/ -s
```

---

## Pipeline CI/CD Jenkins

### Présentation

La pipeline Jenkins automatise l'ensemble du cycle de contrôle qualité à chaque push sur le dépôt. Elle est définie dans le fichier `Jenkinsfile` à la racine du projet.

### Étapes de la pipeline

```
Checkout → Installation → Linting → Tests+Coverage → Vérification 80% → Radon → SonarQube → Quality Gate
```

| Étape | Outil | Description |
|-------|-------|-------------|
| **Installation des dépendances** | pip | Crée le venv et installe tous les packages de `requirements.txt` |
| **Linting** | Pylint | Analyse statique du style et des erreurs de code dans `app/` |
| **Tests et couverture** | pytest + pytest-cov | Exécute tous les tests et génère `coverage.xml` et `test-results.xml` |
| **Vérification couverture ≥ 80%** | coverage.py | Fait échouer le build si la couverture est inférieure à 80% |
| **Complexité Radon** | Radon | Calcule la complexité cyclomatique et l'indice de maintenabilité |
| **Analyse SonarQube** | sonar-scanner | Envoie le code et les métriques vers SonarQube |
| **Quality Gate** | SonarQube | Bloque le pipeline si les critères de qualité SonarQube ne sont pas atteints |

### Prérequis Jenkins

1. **Plugins Jenkins requis :**
   - Pipeline
   - SonarQube Scanner
   - JUnit

2. **Credentials à configurer dans Jenkins :**
   - `sonar-token` : token d'authentification SonarQube (type "Secret text")

3. **Serveur SonarQube à déclarer dans Jenkins :**
   - Aller dans *Manage Jenkins → Configure System → SonarQube servers*
   - Nom : `SonarQube`
   - URL : `http://<ip-vm-sonarqube>:9000`

### Configuration SonarQube (`sonar-project.properties`)

```properties
sonar.projectKey=api-crud-produits
sonar.projectName=API CRUD Produits
sonar.sources=app
sonar.tests=tests
sonar.python.coverage.reportPaths=coverage.xml
```

---

## Répartition du travail

Le travail a été réparti en trois rôles complémentaires :

| Membre | Rôle | Mission principale |
|--------|------|--------------------|
| Personne 1 | Développeur Backend | API CRUD produits (FastAPI) |
| Personne 2 | QA / Tests | pytest, coverage.py, Radon |
| Personne 3 | DevOps | Jenkins, SonarQube, pipeline CI/CD |
