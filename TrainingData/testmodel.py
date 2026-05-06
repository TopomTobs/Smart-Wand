import os
import numpy as np
import pandas as pd
import joblib


# ---------------- CONFIG ----------------
TEST_DIR = "test_data"
MODEL_PATH = "gesture_model.joblib"

LABEL_MAP = {
    "movement_0": 0,
    "movement_1": 1,
    "movement_2": 2,
    "movement_3": 3,
    "movement_4": 4,
}
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
            np.sum(data ** 2)
        ])
    return np.array(features)


def predict_file(filepath, model):
    df = pd.read_csv(filepath, sep=";", header=None)
    df = df.iloc[:, 1:]
    df.columns = ["ax", "ay", "az", "gx", "gy", "gz"]

    features = extract_features_from_file(df).reshape(1, -1)
    prediction = model.predict(features)[0]
    confidence = model.predict_proba(features)[0]

    return prediction, confidence


def main():
    print("Loading model...")
    model = joblib.load(MODEL_PATH)

    correct = 0
    total = 0

    for label_name, true_label in LABEL_MAP.items():
        folder = os.path.join(TEST_DIR, label_name)

        for file in os.listdir(folder):
            if not file.endswith(".csv"):
                continue

            path = os.path.join(folder, file)
            pred, conf = predict_file(path, model)

            print(f"{file} → predicted: {pred}, confidence: {conf}")

            if pred == true_label:
                correct += 1
            total += 1

    print("\nFinal accuracy:", correct / total)


if __name__ == "__main__":
    main()
