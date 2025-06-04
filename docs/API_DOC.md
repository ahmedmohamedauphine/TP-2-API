# API Documentation – TP Data Lake

---

## Authentification

### `POST /api/token/`  
> Récupère un token JWT pour s’authentifier

- **Input**
  - `username`: string
  - `password`: string
- **Output**
  - `access`: token d’accès
  - `refresh`: token de rafraîchissement
- **Exemple**
```json
{
  "username": "romain",
  "password": "1234"
}
```

---

## Gestion des droits

### `POST /api/access/grant/`  
> Donne l’accès à un utilisateur pour une table

- **Input**
  - `user`: ID de l’utilisateur
  - `table_name`: string
  - `can_access`: booléen (true/false)
- **Output**
  - Objet de droit d’accès créé

### `POST /api/access/revoke/`  
> Supprime les droits d’accès d’un utilisateur

- **Input**
  - `username`: nom d’utilisateur
  - `table_name`: string
- **Output**
  - Message de confirmation

---

## Transactions

### `GET /api/transactions/`  
> Récupère les transactions (pagination et filtrage possibles)

- **Input (query params)**  
  - `page`: int (pagination)
  - `fields`: liste des champs à inclure (ex: `product_name,amount`)
  - `amount__gt`, `amount__lt`, `amount`: filtres sur le montant
  - `customer_rating__gt`, `customer_rating__lt`, `customer_rating`
  - `product_category`, `country`, `status`, `payment_method`
- **Output**
  - Liste paginée de transactions
- **Exemple**
```http
GET /api/transactions/?amount__gt=20&fields=product_name,amount
```

---

## Métriques

### `GET /api/metrics/last5min/`  
> Total des montants des transactions des 5 dernières minutes

- **Output**
```json
{ "total_spent_last_5_min": 249.50 }
```

### `GET /api/metrics/user-spending/`  
> Total dépensé par utilisateur et méthode de paiement

- **Output**
```json
[
  { "customer__username": "romain", "payment_method": "card", "total": 245 }
]
```

### `GET /api/metrics/top-products/<x>/`  
> Top X produits les plus achetés

- **Input**
  - `x`: entier
- **Output**
```json
[
  { "product_name": "Banane", "count": 17 }
]
```

---

## Recherche

### `GET /api/search/?q=motcle`  
> Recherche full-text dans `product_name`, `category`, `status`, `country`

- **Input**
  - `q`: chaîne recherchée
- **Output**
  - Liste des résultats correspondants

---

## Kafka

### `POST /api/repush/<transaction_id>/`  
> Re-publie une transaction dans Kafka (topic `transactions`)

- **Input**
  - `transaction_id`: entier
- **Output**
```json
{ "message": "Transaction pushed to Kafka" }
```

### `POST /api/repush/all/`  
> Re-publie toutes les transactions dans Kafka

- **Output**
```json
{ "message": "All transactions pushed to Kafka" }
```

---

## Machine Learning

### `POST /api/predict/`  
> Prédit une fraude à partir des features

- **Input**
```json
{ "features": [1.2, 0.4, 3.3, 5.1, 2.0] }
```
- **Output**
```json
{ "prediction": 1 }
```

---

## Audit et logs

### `GET /api/audit/<table_name>/`  
> Liste des utilisateurs ayant accédé à la table

- **Output**
  - Liste d'objets de log (user, méthode, path, date)

### `GET /api/resources/`  
> Affiche les ressources disponibles dans le Data Lake

```json
{ "resources": ["transactions", "users", "logs"] }
```

### `GET /api/version/<table_name>/<version_id>/`  
> (Non implémenté) retourne une erreur 501

---

## Accès sécurisé test

### `GET /api/secure/`  
> Teste si un utilisateur a accès à une table (transactions)

- **Output**
```json
{ "message": "Accès autorisé à transactions" }
```
ou
```json
{ "error": "Accès refusé" }
```