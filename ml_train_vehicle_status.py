import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Cargar dataset
df = pd.read_csv("dataset.csv")

X = df[[
    "rpm",
    "velocidad",
    "acelerador",
    "carga_motor",
    "delta_velocidad"
]]

y = df["estado"]

# 2. Train / Test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# 3. Modelo Random Forest
model = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    random_state=42
)

model.fit(X_train, y_train)

import joblib
joblib.dump(model, "vehicle_status_model.pkl")


# 4. Evaluacion
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print("\nAccuracy:", round(accuracy * 100, 2), "%\n")

print("Classification report:\n")
print(classification_report(y_test, y_pred))


# 5. Matriz de confusion
cm = confusion_matrix(y_test, y_pred, labels=model.classes_)

plt.figure(figsize=(7, 5))
sns.heatmap(
    cm,
    annot=True,
    fmt="d",
    cmap="Blues",
    xticklabels=model.classes_,
    yticklabels=model.classes_
)

plt.xlabel("Predicted")
plt.ylabel("Real")
plt.title("Confusion Matrix - Vehicle State Classification")
plt.tight_layout()
plt.show()
