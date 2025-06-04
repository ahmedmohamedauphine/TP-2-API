import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.datasets import make_classification

# Génération de données fictives
X, y = make_classification(n_samples=1000, n_features=5, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Entraînement du modèle
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Sauvegarde du modèle
with open("api/model.pkl", "wb") as f:
    pickle.dump(model, f)