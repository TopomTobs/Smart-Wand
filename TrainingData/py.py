import pandas as pd

df = pd.read_csv("./movement_0/sample0.csv", sep=";", header=None)

# Drop index column
df = df.iloc[:, 1:]

df.columns = ["ax", "ay", "az", "gx", "gy", "gz"]
print(df.head())

import numpy as np

def extract_features_from_file(df):
    features = []
    for col in df.columns:
        data = df[col].values
        features.extend([
            data.mean(),
            data.std(),
            data.min(),
            data.max(),
            np.sum(data ** 2)  # energy
        ])
    return np.array(features)


import os

X = []
y = []

BASE_DIR = "/home/thomas/Documents/GitHub/Smart-Wand/TrainingData/"

label_map = {
    "movement_0": 0,
    "movement_1": 1
}

for folder, label in label_map.items():
    folder_path = os.path.join(BASE_DIR, folder)
    for file in os.listdir(folder_path):
        if not file.endswith(".csv"):
            continue
        df = pd.read_csv(
            os.path.join(folder_path, file),
            sep=";",
            header=None
        )
        df = df.iloc[:, 1:]  # drop index column
        X.append(extract_features_from_file(df))
        y.append(label)

X = np.array(X)
y = np.array(y)

print(X.shape, y.shape)


from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

clf = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))
print("Confusion matrix:\n", confusion_matrix(y_test, y_pred))

def predict_file(filepath, model):
    df = pd.read_csv(filepath, sep=";", header=None)
    df = df.iloc[:, 1:]
    features = extract_features_from_file(df).reshape(1, -1)
    return model.predict(features)[0]

correct = 0
total = 0

for label_name, label in label_map.items():
    folder = f"Testdata/{label_name}"
    for file in os.listdir(folder):
        pred = predict_file(os.path.join(folder, file), pipeline)
        correct += int(pred == label)
        total += 1

print("Real-world accuracy:", correct / total)
