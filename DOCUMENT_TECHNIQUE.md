# Document Technique - API REST & Automatisation des Tests

**Projet :** API de Gestion de Tâches (Todo List API)  
**Cours :** Atelier Automatisation des Tests (Projet Final)  
**Date :** 29 juin 2026  

---

## 1. Présentation du Projet

Le projet consiste en une API REST robuste et performante pour la gestion de tâches (Todo List). Elle permet de créer, lire, filtrer, modifier, terminer et supprimer des tâches. Chaque tâche possède les attributs suivants :
- **ID** (Entier, unique)
- **Titre** (Chaîne de caractères, requis, non-vide, max 100 caractères)
- **Description** (Chaîne de caractères, facultatif, max 500 caractères)
- **Statut de complétion** (Booléen, défaut : faux)
- **Priorité** (Chaîne de caractères parmi : `low`, `medium`, `high`, par défaut `medium`)
- **Date de création** (Date et heure UTC automatiques)
- **Date d'échéance (due_date)** (Date et heure UTC facultative, doit être dans le futur)
- **Date de complétion** (Date et heure UTC renseignées automatiquement lors de la complétion)

### Logique Métier Implémentée
1. **Validation stricte** : Grâce à Pydantic, le titre et la priorité sont validés à la création et à la modification. La date d'échéance (`due_date`) fait l'objet d'un validateur personnalisé interdisant la planification dans le passé.
2. **Calcul de retard (is_overdue)** : Un attribut dynamique calculé compare la date d'échéance à la date et heure courantes (si la tâche n'est pas déjà complétée).
3. **Mise à jour d'état** : L'action de terminer une tâche modifie le statut `completed` à `True` et enregistre le timestamp de complétion exact dans `completed_at`.

---

## 2. Justification des Choix Technologiques

### 2.1 Langage et Framework : Python & FastAPI
- **FastAPI** a été choisi pour son excellente performance (grâce à `asyncio` et `uvicorn`) et son typage statique basé sur **Pydantic**.
- Pydantic assure une validation de type native à l'entrée de l'API (codes de retour 422 automatiques et documentés en cas de payload incorrect).
- FastAPI génère automatiquement une documentation interactive via **OpenAPI (Swagger UI)** sur le point d'accès `/docs`, ce qui simplifie grandement l'intégration pour les clients.

### 2.2 Base de Données : SQLite & SQLAlchemy
- **SQLAlchemy 2.0** (ORM) est utilisé pour découpler le modèle de données de la base physique.
- **SQLite** a été choisi comme base de données locale. Étant stockée dans un simple fichier (`todo.db`), elle est idéale pour les architectures légères et s'exécute sans aucun service externe (pas besoin de conteneur Docker ni d'installation complexe). C'est parfait pour garantir la portabilité immédiate du projet et la stabilité du pipeline CI/CD.

### 2.3 Framework de Test : Pytest
- **Pytest** est le framework standard de l'écosystème Python. Sa syntaxe à base d'assertions simples (`assert`) est très lisible.
- Il s'interface facilement avec **pytest-cov** (pour la couverture de code) et génère nativement des rapports de test normalisés au format JUnit XML, utilisables par n'importe quel serveur CI.

### 2.4 Outil CI/CD : GitHub Actions
- **GitHub Actions** a été privilégié en tant qu'outil CI/CD pour sa parfaite intégration avec le dépôt GitHub du projet.
- Il s'agit d'une solution hébergée (SaaS) ne nécessitant aucun serveur Jenkins ou GitLab autogéré. Les environnements (runners Linux) sont provisionnés à la demande de manière isolée et reproductible.

### 2.5 Outils d'Audit et de Performance : Bandit & Locust
- **Bandit** analyse l'arbre de syntaxe abstraite (AST) du code Python pour y détecter les failles de sécurité classiques (ex. injections SQL, utilisation de fonctions à risque).
- **Locust** est un outil de test de charge "code-first". Les scénarios d'utilisation sont définis en Python pur, ce qui permet de versionner les scénarios de performance au même titre que le code de l'application.

---

## 3. Analyse des Résultats des Tests et Audits

### 3.1 Couverture des Tests Unitaires (Coverage)
La suite de tests unitaires (dans `tests/test_unit.py`) cible les validateurs de schéma, la logique métier du modèle et les opérations CRUD en base de données.
Le rapport de couverture indique :
```text
---------- coverage: platform win32, python 3.12.6-final-0 -----------
Name              Stmts   Miss  Cover   Missing
-----------------------------------------------
app\config.py         4      0   100%
app\crud.py          50      2    96%   12, 42
app\database.py      11      4    64%   14-18
app\main.py          44      0   100%
app\models.py        27      1    96%   33
app\schemas.py       61     13    79%   46-51, 56-62
-----------------------------------------------
TOTAL               197     20    90%
```
- **Couverture Globale : 90%** (Largement supérieure aux 80% imposés).
- **Test Paramétré** : La logique du calcul de retard (`check_overdue`) a été testée sous différentes conditions de date d'échéance et de statut à l'aide de `@pytest.mark.parametrize` pour maximiser la couverture des branches logiques.
- **Test avec Mock** : Pour s'assurer que le calcul de dépassement fonctionne indépendamment de la date de la machine de test, la fonction `datetime.now()` a été mockée avec `unittest.mock.patch` dans `test_is_overdue_property_with_mocked_time`.

### 3.2 Tests d'Intégration
La suite d'intégration (dans `tests/test_integration.py`) vérifie le fonctionnement de tous les endpoints HTTP en conditions réelles à l'aide du `TestClient` de FastAPI.
- Tous les endpoints (`GET`, `POST`, `PUT`, `DELETE`) sont couverts.
- Les cas d'erreurs (codes HTTP 400 pour filtre invalide, 404 pour ID non existant, 422 pour payloads non conformes) sont rigoureusement testés.
- Un rapport JUnit XML est généré dans `reports/junit.xml` à l'issue de l'exécution dans le pipeline.

### 3.3 Audit Sécurité (Bandit)
L'exécution de Bandit sur l'intégralité du dossier `app/` ne révèle **aucune faille de sécurité** :
```text
Test results:
	No issues identified.
Code scanned:
	Total lines of code: 226
```
Aucun warning ni vulnérabilité (injection, secret en clair, etc.) n'a été détecté. Le rapport complet est généré dans `reports/bandit_report.txt`.

---

## 4. Analyse et Interprétation des Performances (Locust)

Un test de charge de 10 secondes a été exécuté simulant **10 utilisateurs simultanés** avec un taux d'apparition (spawn rate) de **2 utilisateurs par seconde**. Chaque utilisateur effectue des requêtes répétées (lecture, création, mise à jour, suppression) avec un délai aléatoire entre 0,5 et 1,5 seconde.

### Résultats Métriques (P95)
Le résumé des temps de réponse obtenus est le suivant :

| Endpoint / Action | Nombre de Req. | Temps Médian (P50) | Temps P95 | Temps Max | Taux d'Échec |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `GET /` (Welcome) | 12 | 3 ms | 5 ms | 5 ms | 0% |
| `GET /tasks` (List) | 23 | 5 ms | 21 ms | 24 ms | 0% |
| `GET /tasks/{id}` (Detail) | 20 | 2 ms | 5 ms | 5 ms | 0% |
| `POST /tasks` (Creation) | 20 | 12 ms | 38 ms | 38 ms | 0% |
| `PUT /tasks/{id}` (Update) | 20 | 8 ms | 15 ms | 15 ms | 0% |
| `DELETE /tasks/{id}` (Delete)| 3 | 9 ms | 10 ms | 10 ms | 0% |
| **Agrégat Total** | **98** | **7 ms** | **21 ms** | **38 ms** | **0%** |

### Analyse et Interprétation
1. **Stabilité** : Aucune requête n'a échoué (taux d'échec de 0%). L'API reste parfaitement stable sous ce niveau de charge.
2. **Latence P95** : La latence au 95ème percentile globale s'établit à **21 ms**. Cela signifie que 95% des utilisateurs reçoivent leur réponse en moins de 21 millisecondes, ce qui garantit une excellente fluidité et interactivité de l'application.
3. **Performance par endpoint** :
   - Les requêtes de lecture simple (`GET /tasks/{id}`) sont extrêmement rapides (P95 de 5 ms) car elles ne nécessitent pas de modification d'état ou d'opérations d'écriture.
   - La création de tâches (`POST /tasks`) affiche le temps P95 le plus élevé (**38 ms**). Cela s'explique par le fait qu'une insertion SQLite en base de données exige une opération d'écriture synchrone sur disque (verrouillage de fichier pour maintenir les propriétés ACID), ce qui prend naturellement plus de temps que la lecture en cache mémoire.
   - De manière générale, ces résultats valident l'architecture légère basée sur FastAPI et SQLite pour des charges légères à modérées.

---

## 5. Retour Critique et Perspectives

### Ce qui a bien fonctionné
- **Intégration FastAPI + Pytest** : La mise en place de fixtures et l'utilisation de `TestClient` a rendu l'écriture des tests d'intégration extrêmement rapide et intuitive.
- **SQLite en Test** : L'utilisation d'une base de données SQLite basée sur un fichier temporaire de test (`test.db`) a simplifié le pipeline CI/CD en s'affranchissant du besoin de configurer et nettoyer une base externe (comme PostgreSQL ou MySQL).
- **GitHub Actions** : La configuration s'est faite sans douleur et l'exécution automatique des jobs (audit -> tests unitaires -> tests d'intégration) offre un filet de sécurité immédiat.

### Ce qui aurait pu être amélioré / Évolutions futures
1. **Base de Données en Production** : SQLite montre ses limites face aux écritures concurrentes à cause du verrouillage global de sa base de données (Write-Ahead Logging atténue le problème mais ne l'élimine pas). Pour une mise en production avec des milliers d'utilisateurs concurrents, il faudrait migrer vers un serveur de base de données relationnelle comme **PostgreSQL**.
2. **Authentification & Autorisation** : L'API est actuellement ouverte. L'ajout d'une gestion des utilisateurs via OAuth2 (JWT) permettrait de restreindre l'accès et d'implémenter des tests d'intégration plus riches simulant des accès non autorisés (HTTP 401 / 403).
3. **Conteneurisation (Docker)** : Créer une image Docker de l'application permettrait d'exécuter des tests d'intégration dans un conteneur strictement identique à l'environnement de production.
