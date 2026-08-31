# ==========================================
# IMPORT REQUIRED LIBRARIES
# ==========================================

import pandas as pd
import pickle

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)


# ==========================================
# LOAD TRAINING DATA
# ==========================================

# Load the training dataset from the CSV file.

df = pd.read_csv(
    "data/expenses_training.csv"
)


# ==========================================
# CLEAN THE DATA
# ==========================================

# Remove rows where description or category is missing.

df = df.dropna(
    subset=[
        "description",
        "category"
    ]
)


# Remove unnecessary spaces from descriptions.

df["description"] = (
    df["description"]
    .astype(str)
    .str.strip()
)


# Remove empty descriptions.

df = df[
    df["description"] != ""
]


# Remove duplicate descriptions.

df = df.drop_duplicates(
    subset=["description"]
)


# ==========================================
# DISPLAY DATASET INFORMATION
# ==========================================

print()
print("==========================================")
print("SMARTSPEND MACHINE LEARNING TRAINING")
print("==========================================")
print()

print(
    "Total training records:",
    len(df)
)

print()

print("Category distribution:")

print(
    df["category"].value_counts()
)

print()


# ==========================================
# SPLIT DATASET
# ==========================================

# Separate the input descriptions from the
# category labels.

X = df["description"]

y = df["category"]


# Split the dataset into:
#
# 80% training data
# 20% testing data
#
# stratify=y keeps the category distribution
# balanced between training and testing.

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


# ==========================================
# CREATE MACHINE LEARNING PIPELINE
# ==========================================

# TF-IDF converts text into numerical features.
#
# ngram_range=(1, 2) allows the model to learn:
#
# Single words:
# "pizza"
# "coffee"
# "bus"
#
# Two-word phrases:
# "movie ticket"
# "sports shoes"
# "python course"
# "bus fare"

model = Pipeline([
    (
        "tfidf",
        TfidfVectorizer(
            ngram_range=(1, 2),
            lowercase=True,
            sublinear_tf=True,
            min_df=1
        )
    ),

    (
        "classifier",
        LogisticRegression(
            max_iter=2000,
            class_weight="balanced"
        )
    )
])


# ==========================================
# TRAIN MODEL
# ==========================================

print("Training model...")

model.fit(
    X_train,
    y_train
)

print("Training completed.")
print()


# ==========================================
# TEST MODEL
# ==========================================

# Make predictions using the test data.

predictions = model.predict(
    X_test
)


# ==========================================
# CALCULATE ACCURACY
# ==========================================

accuracy = accuracy_score(
    y_test,
    predictions
)


print("==========================================")
print("MODEL EVALUATION")
print("==========================================")
print()

print(
    "Accuracy:",
    round(accuracy * 100, 2),
    "%"
)

print()


# ==========================================
# CLASSIFICATION REPORT
# ==========================================

# This shows precision, recall and F1-score
# for every expense category.

print("Classification Report:")
print()

print(
    classification_report(
        y_test,
        predictions
    )
)


# ==========================================
# CONFUSION MATRIX
# ==========================================

print("Confusion Matrix:")
print()

print(
    confusion_matrix(
        y_test,
        predictions
    )
)

print()


# ==========================================
# RETRAIN USING THE COMPLETE DATASET
# ==========================================

# After evaluation, train the final model using
# ALL available data.
#
# This gives the final model as much training
# information as possible before deployment.

print("Training final model using complete dataset...")

model.fit(
    X,
    y
)

print("Final model trained.")
print()


# ==========================================
# SAVE TRAINED MODEL
# ==========================================

# Save the final trained model.
#
# FastAPI will load this file when the backend
# starts.

with open(
    "model.pkl",
    "wb"
) as file:

    pickle.dump(
        model,
        file
    )


# ==========================================
# FINAL INFORMATION
# ==========================================

print("==========================================")
print("MODEL SAVED")
print("==========================================")
print()

print(
    "Model saved as: model.pkl"
)

print(
    "Final training records:",
    len(df)
)

print()

print("Categories:")

for category in sorted(
    df["category"].unique()
):

    print(
        "-",
        category
    )

print()

print("Training process completed successfully.")