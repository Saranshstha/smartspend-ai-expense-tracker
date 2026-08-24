# ==========================================
# IMPORT REQUIRED LIBRARIES
# ==========================================

import pandas as pd
import pickle

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline


# ==========================================
# LOAD TRAINING DATA
# ==========================================

# Read the expense descriptions and their categories
# from the CSV file used to train the machine learning model.

df = pd.read_csv("data/expenses_training.csv")


# ==========================================
# CREATE MACHINE LEARNING PIPELINE
# ==========================================

# TF-IDF converts expense descriptions into numerical
# features that the machine learning algorithm can understand.
#
# ngram_range=(1, 2) allows the model to learn both
# individual words and two-word phrases such as:
# "movie ticket", "bus fare", and "sports shoes".

# Logistic Regression is used to classify each expense
# description into one of the predefined expense categories.

model = Pipeline([
    (
        "tfidf",
        TfidfVectorizer(
            ngram_range=(1, 2),
            lowercase=True,
            sublinear_tf=True
        )
    ),
    (
        "classifier",
        LogisticRegression(
            max_iter=1000
        )
    )
])


# ==========================================
# TRAIN THE MODEL
# ==========================================

# Train the machine learning pipeline using:
# - description as the input feature
# - category as the target label

model.fit(
    df["description"],
    df["category"]
)


# ==========================================
# SAVE THE TRAINED MODEL
# ==========================================

# Save the trained model as a pickle file.
# FastAPI will load this file later when the API starts.

with open("model.pkl", "wb") as file:

    pickle.dump(
        model,
        file
    )


# ==========================================
# DISPLAY TRAINING INFORMATION
# ==========================================

# Print basic information so we can confirm that
# the training process completed successfully.

print("Model trained successfully.")
print("Training records:", len(df))
print()
print("Category distribution:")
print(df["category"].value_counts())