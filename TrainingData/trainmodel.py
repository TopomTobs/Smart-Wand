import os
import numpy as np
import pandas as pd
import joblib

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix


# ---------------- CONFIG ----------------
DATASET_DIR = "dataset"

LABEL_MAP = {
    "movement_0": 0,
    "movement_1": 1,
    "movement_2": 2,
    "movement_3": 3,
    "movement_4": 4,
}

MODEL_OUT = "gesture_model.joblib"
# ----------------------------------------


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


def load_dataset():
    X, y = [], []

    for folder, label in LABEL_MAP.items():
        folder_path = os.path.join(DATASET_DIR, folder)

        for file in os.listdir(folder_path):
            if not file.endswith(".csv"):
                continue

            df = pd.read_csv(
                os.path.join(folder_path, file),
                sep=";",
                header=None
            )

            df = df.iloc[:, 1:]  # drop index column
            df.columns = ["ax", "ay", "az", "gx", "gy", "gz"]

            features = extract_features_from_file(df)
            X.append(features)
            y.append(label)

    return np.array(X), np.array(y)


def main():
    print("Loading dataset...")
    X, y = load_dataset()

    print("Dataset shape:", X.shape)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("clf", RandomForestClassifier(
            n_estimators=100,
            random_state=42
        ))
    ])

    print("Training model...")
    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)

    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("Confusion matrix:")
    print(confusion_matrix(y_test, y_pred))

    print("Saving model to:", MODEL_OUT)
    joblib.dump(pipeline, MODEL_OUT)

    print("Training complete.")


if __name__ == "__main__":
    main()
