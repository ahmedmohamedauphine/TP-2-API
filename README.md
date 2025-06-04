# TP API 2 – Data Lake API avec Django

Ce projet est une API sécurisée qui permet d'interagir avec un Data Lake local en exposant des données à travers différents endpoints tout en gérant l'authentification, les droits d’accès, l’audit, et des fonctionnalités avancées comme le Machine Learning et Kafka.

## Fonctionnalités

### Authentification & Autorisation
- Authentification via JWT (`/api/token/`)
- Gestion des droits d'accès à des ressources (`/api/access/grant/`, `/api/access/revoke/`)
- Journalisation des accès (middleware)

### Accès aux données
- Accès sécurisé aux données avec vérification des droits
- Projection dynamique des champs via `?fields=`
- Filtres avancés : montant, pays, catégorie, statut, note client

### Métriques
- Total dépensé sur les 5 dernières minutes
- Dépense totale par utilisateur et méthode de paiement
- Top X produits achetés

### Logs et Audit
- Journalisation automatique de chaque requête
- Endpoint pour consulter qui a accédé à quoi
- Liste des ressources disponibles

### Recherche
- Recherche full-text dans plusieurs champs avec `?q=`

### Machine Learning
- Endpoint de prédiction de fraude via un modèle `RandomForest`
- Modèle entraîné avec des données synthétiques (`fraud_model.py`)

### Kafka
- Repush d’une transaction ou de toutes les données historiques vers Kafka
- Kafka utilisé en simulation ou réel (`localhost:9092`)

## Documentation

Swagger UI est disponible à :  
📍 `http://localhost:8000/swagger/`

## Installation

```bash
git clone <repo>
cd tp_api2_project
python -m venv env
source env/bin/activate  # ou env\Scripts\activate sous Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
## Auteur

Ahmed MOHAMED et Romain LEPRETRE