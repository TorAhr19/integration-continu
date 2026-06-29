# Todo List API - CI/CD & Test Automation Project

Ce projet présente une API REST complète construite avec **FastAPI**, **SQLAlchemy** (avec base **SQLite**), et **Pytest**. 
Il met en place une suite d'automatisation de tests complète couvrant les tests unitaires (avec mock et tests paramétrés), les tests d'intégration, un audit de sécurité statique, et un scénario de test de charge (performance).

## Fonctionnalités de l'API
- Gestion de tâches : Créer, lister, filtrer par priorité/complétion, mettre à jour, terminer et supprimer.
- Détection automatique de retard (`is_overdue`) par rapport à la date d'échéance (`due_date`).
- Validation stricte des données avec **Pydantic**.
- Documentation Swagger auto-générée sur `/docs`.

---

## Installation et Lancement du Projet

### Prérequis
- Python 3.12 (ou supérieur)

### 1. Cloner le projet et se placer dans le répertoire
```bash
cd projet-ci
```

### 2. Créer et activer un environnement virtuel
Sur Windows (PowerShell) :
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```
Sur macOS/Linux :
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Lancer le serveur de développement
```bash
python -m uvicorn app.main:app --reload
```
L'API sera disponible à l'adresse suivante : [http://127.0.0.1:8000](http://127.0.0.1:8000).  
La documentation interactive de l'API est accessible sur : [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

---

## Exécution des Outils d'Automatisation de Tests

Toutes les commandes ci-dessous doivent être lancées avec l'environnement virtuel activé.

### 1. Tests Unitaires et d'Intégration + Rapport de Couverture
Cette commande exécute l'intégralité des tests (unitaires et d'intégration), vérifie que la couverture du code est supérieure ou égale à **80%**, et génère un rapport XML JUnit de test dans `reports/junit.xml`.
```bash
python -m pytest --cov=app --cov-report=term-missing --junitxml=reports/junit.xml tests/
```

### 2. Audit de Sécurité (Bandit)
Cette commande réalise une analyse de sécurité statique du code source et génère un rapport textuel dans `reports/bandit_report.txt`.
```bash
bandit -r app/ -f txt -o reports/bandit_report.txt
```

### 3. Tests de Performance (Locust)
Pour exécuter le scénario de test de charge de manière automatisée, lancez le script d'automatisation suivant :
```bash
python run_perf_tests.py
```
Ce script démarre automatiquement l'API FastAPI, exécute le test Locust en mode headless (sans interface graphique) avec 10 utilisateurs simultanés pendant 10 secondes, génère un rapport de performance HTML dans `reports/locust_report.html`, puis éteint proprement le serveur FastAPI.

Vous pouvez ouvrir le fichier `reports/locust_report.html` dans n'importe quel navigateur pour visualiser les latences (P50, P95, Max) et les courbes de requêtes.

---

## Configuration du Pipeline CI/CD (GitHub Actions)
La configuration du pipeline d'intégration continue est localisée dans le fichier `.github/workflows/ci.yml`.
Le pipeline s'exécute automatiquement à chaque commit ou pull-request poussé sur les branches `master` ou `main`.
Il réalise séquentiellement :
1. L'installation des dépendances.
2. L'audit de sécurité statique du code (`bandit`).
3. L'exécution des tests unitaires et le blocage du pipeline si la couverture est inférieure à 80% (`pytest --cov-fail-under=80`).
4. L'exécution des tests d'intégration et la génération du rapport XML.
5. L'archivage automatique des rapports de test (`reports/`).
