 
# SMARTSPEND MACHINE LEARNING TRAINING
 


 
# IMPORT REQUIRED LIBRARIES
 

import pickle

import pandas as pd

from sklearn.feature_extraction.text import (
    TfidfVectorizer
)

from sklearn.linear_model import (
    LogisticRegression
)

from sklearn.pipeline import (
    Pipeline,
    FeatureUnion
)

from sklearn.model_selection import (
    train_test_split,
    StratifiedKFold,
    cross_val_score
)

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score
)
from pathlib import Path

 
# CONFIGURATION
 

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_PATH = (
    PROJECT_ROOT
    / "ml"
    / "data"
    / "expenses_training.csv"
)

MODEL_PATH = (
    PROJECT_ROOT
    / "backend"
    / "models"
    / "model.pkl"
)

RANDOM_STATE = 42

TEST_SIZE = 0.20

EXPECTED_CATEGORIES = {
    "Food",
    "Transport",
    "Education",
    "Entertainment",
    "Shopping"
}


 
# LOAD DATASET
 

# Load the CSV file containing expense descriptions
# and their corresponding categories.

df = pd.read_csv(
    DATA_PATH
)


 
# DATASET DIAGNOSTICS
 

print()
print("==========================================")
print("SMARTSPEND MACHINE LEARNING TRAINING")
print("==========================================")
print()

print(
    "Rows loaded from CSV:",
    len(df)
)

print()


 
# CHECK REQUIRED COLUMNS
 

# Make sure the CSV contains the columns required
# by the training pipeline.

required_columns = {
    "description",
    "category"
}

missing_columns = (
    required_columns
    - set(df.columns)
)

if missing_columns:

    raise ValueError(
        "Missing required columns: "
        + str(
            sorted(missing_columns)
        )
    )


 
# CLEAN DESCRIPTIONS
 

# Remove missing descriptions and categories.

df = df.dropna(
    subset=[
        "description",
        "category"
    ]
)


# Convert descriptions to strings and remove
# unnecessary spaces.

df["description"] = (
    df["description"]
    .astype(str)
    .str.strip()
)


# Remove empty descriptions.

df = df[
    df["description"] != ""
]


 
# CLEAN CATEGORY NAMES
 

# Remove accidental spaces from category names.
#
# For example:
#
# " Shopping"
# becomes
# "Shopping"

df["category"] = (
    df["category"]
    .astype(str)
    .str.strip()
)


 
# STANDARDIZE CATEGORY CAPITALIZATION
 

# Make the first letter uppercase and the remaining
# letters lowercase so category names remain consistent.

df["category"] = (
    df["category"]
    .str.capitalize()
)


 
# CHECK CATEGORY NAMES
 

# Make sure there are no unexpected categories.

found_categories = set(
    df["category"].unique()
)

unexpected_categories = (
    found_categories
    - EXPECTED_CATEGORIES
)

if unexpected_categories:

    raise ValueError(
        "Unexpected categories found: "
        + str(
            sorted(unexpected_categories)
        )
        + "\n\nExpected categories are: "
        + str(
            sorted(EXPECTED_CATEGORIES)
        )
    )


 
# REMOVE EXACT DUPLICATES
 

# Remove completely duplicated rows.

before_duplicates = len(df)

df = df.drop_duplicates()

duplicates_removed = (
    before_duplicates
    - len(df)
)


 
# CHECK FOR CONFLICTING LABELS
 

# A description should not belong to multiple
# different categories.
#
# Example of a problem:
#
# college backpack,Education
# college backpack,Shopping
#
# This creates contradictory training data.

description_category_counts = (
    df.groupby("description")["category"]
    .nunique()
)

conflicting_descriptions = (
    description_category_counts[
        description_category_counts > 1
    ]
    .index
    .tolist()
)


if conflicting_descriptions:

    print(
        "WARNING:"
    )

    print(
        "Conflicting descriptions found:"
    )

    for description in conflicting_descriptions:

        labels = (
            df.loc[
                df["description"] == description,
                "category"
            ]
            .unique()
            .tolist()
        )

        print(
            " -",
            description,
            "->",
            labels
        )

    print()

    # Remove conflicting descriptions rather than
    # teaching the model contradictory labels.

    df = df[
        ~df["description"].isin(
            conflicting_descriptions
        )
    ]


 
# REMOVE DUPLICATE DESCRIPTIONS
 

# After conflicting examples have been removed,
# keep one record per unique description.

before_description_duplicates = len(df)

df = df.drop_duplicates(
    subset=["description"]
)

description_duplicates_removed = (
    before_description_duplicates
    - len(df)
)


 
# FINAL DATASET CHECK
 

if len(df) == 0:

    raise ValueError(
        "No training data remains after cleaning."
    )


if df["category"].nunique() < 2:

    raise ValueError(
        "At least two categories are required for training."
    )


 
# DISPLAY CLEANING INFORMATION
 

print(
    "Exact duplicate rows removed:",
    duplicates_removed
)

print(
    "Duplicate descriptions removed:",
    description_duplicates_removed
)

print(
    "Conflicting descriptions removed:",
    len(conflicting_descriptions)
)

print()

print(
    "Final training records:",
    len(df)
)

print()

print(
    "Category distribution:"
)

print(
    df["category"].value_counts()
)

print()


 
# DEFINE INPUTS AND TARGETS
 

# X contains expense descriptions.
#
# y contains the category labels.

X = df["description"]

y = df["category"]


 
# TRAIN / TEST SPLIT
 

# Keep 20% of the cleaned dataset completely
# separate for final model evaluation.

X_train, X_test, y_train, y_test = (
    train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y
    )
)


print(
    "Training examples:",
    len(X_train)
)

print(
    "Testing examples:",
    len(X_test)
)

print()


 
# MODEL 1
# WORD-LEVEL TF-IDF
 

# The first model uses word-level TF-IDF.
#
# It learns individual words and short phrases such as:
#
# pizza
# bus
# movie
# sports
#
# and:
#
# movie ticket
# bus fare
# python course
# sports shoes

word_model = Pipeline([

    (
        "tfidf",

        TfidfVectorizer(
            lowercase=True,
            ngram_range=(1, 2),
            sublinear_tf=True,
            min_df=1
        )
    ),

    (
        "classifier",

        LogisticRegression(
            max_iter=3000,
            class_weight="balanced",
            C=2.0
        )
    )

])


 
# MODEL 2
# WORD + CHARACTER TF-IDF
 

# This model combines:
#
# Word-level features
# +
# Character-level features
#
# Character features can help recognize
# variations in wording and spelling.

combined_model = Pipeline([

    (
        "features",

        FeatureUnion([

            (
                "word_tfidf",

                TfidfVectorizer(
                    lowercase=True,
                    ngram_range=(1, 2),
                    sublinear_tf=True,
                    min_df=1
                )
            ),

            (
                "char_tfidf",

                TfidfVectorizer(
                    lowercase=True,
                    analyzer="char_wb",
                    ngram_range=(3, 5),
                    sublinear_tf=True,
                    min_df=1
                )
            )

        ])

    ),

    (
        "classifier",

        LogisticRegression(
            max_iter=3000,
            class_weight="balanced",
            C=2.0
        )
    )

])


 
# CROSS-VALIDATION SETUP
 

# Cross-validation gives us a more reliable estimate
# of how each model performs on unseen data.

cross_validation = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=RANDOM_STATE
)


 
# COMPARE MODELS
 

print("==========================================")
print("MODEL COMPARISON")
print("==========================================")
print()


print("Testing Word TF-IDF model...")

word_scores = cross_val_score(
    word_model,
    X_train,
    y_train,
    cv=cross_validation,
    scoring="f1_weighted"
)

word_mean = word_scores.mean()

word_std = word_scores.std()


print(
    "Word TF-IDF F1:",
    round(word_mean * 100, 2),
    "% +/-",
    round(word_std * 100, 2),
    "%"
)

print()


print(
    "Testing Word + Character TF-IDF model..."
)

combined_scores = cross_val_score(
    combined_model,
    X_train,
    y_train,
    cv=cross_validation,
    scoring="f1_weighted"
)

combined_mean = (
    combined_scores.mean()
)

combined_std = (
    combined_scores.std()
)


print(
    "Word + Character TF-IDF F1:",
    round(
        combined_mean * 100,
        2
    ),
    "% +/-",
    round(
        combined_std * 100,
        2
    ),
    "%"
)

print()


 
# SELECT BEST MODEL
 

# Select the model with the strongest average
# weighted F1-score during cross-validation.

if combined_mean >= word_mean:

    model = combined_model

    selected_model_name = (
        "Word + Character TF-IDF"
    )

    selected_cv_score = combined_mean

else:

    model = word_model

    selected_model_name = (
        "Word TF-IDF"
    )

    selected_cv_score = word_mean


print(
    "Selected model:",
    selected_model_name
)

print(
    "Cross-validation F1:",
    round(
        selected_cv_score * 100,
        2
    ),
    "%"
)

print()


 
# TRAIN SELECTED MODEL
 

print(
    "Training selected model..."
)

model.fit(
    X_train,
    y_train
)

print(
    "Training completed."
)

print()


 
# TEST MODEL
 

# Predict categories for the data that was kept
# completely separate from training.

predictions = model.predict(
    X_test
)


 
# CALCULATE METRICS
 

accuracy = accuracy_score(
    y_test,
    predictions
)

precision = precision_score(
    y_test,
    predictions,
    average="weighted",
    zero_division=0
)

recall = recall_score(
    y_test,
    predictions,
    average="weighted",
    zero_division=0
)

f1 = f1_score(
    y_test,
    predictions,
    average="weighted",
    zero_division=0
)


 
# DISPLAY MODEL EVALUATION
 

print("==========================================")
print("MODEL EVALUATION")
print("==========================================")
print()

print(
    "Selected model:",
    selected_model_name
)

print(
    "Accuracy:",
    round(
        accuracy * 100,
        2
    ),
    "%"
)

print(
    "Precision:",
    round(
        precision * 100,
        2
    ),
    "%"
)

print(
    "Recall:",
    round(
        recall * 100,
        2
    ),
    "%"
)

print(
    "F1-score:",
    round(
        f1 * 100,
        2
    ),
    "%"
)

print()


 
# CLASSIFICATION REPORT
 

print(
    "Classification Report:"
)

print()

print(
    classification_report(
        y_test,
        predictions,
        labels=sorted(
            EXPECTED_CATEGORIES
        ),
        zero_division=0
    )
)


 
# CONFUSION MATRIX
 

print(
    "Confusion Matrix:"
)

print()

matrix = confusion_matrix(
    y_test,
    predictions,
    labels=sorted(
        EXPECTED_CATEGORIES
    )
)

print(
    pd.DataFrame(
        matrix,
        index=sorted(
            EXPECTED_CATEGORIES
        ),
        columns=sorted(
            EXPECTED_CATEGORIES
        )
    )
)

print()


 
# TRAIN FINAL MODEL
 

# Evaluation is now complete.
#
# Train the selected model one final time using
# ALL cleaned training records so the saved model
# has access to the maximum amount of data.

print(
    "=========================================="
)

print(
    "TRAINING FINAL MODEL"
)

print(
    "=========================================="
)

print()

print(
    "Training final model using all",
    len(df),
    "records..."
)

model.fit(
    X,
    y
)

print(
    "Final model training completed."
)

print()


 
# SAVE MODEL
 

# Save the fully trained model for FastAPI.

with open(
    MODEL_PATH,
    "wb"
) as file:

    pickle.dump(
        model,
        file
    )

MODEL_PATH.parent.mkdir(
    parents=True,
    exist_ok=True
)


 
# FINAL SUMMARY
 

print(
    "=========================================="
)

print(
    "MODEL SAVED SUCCESSFULLY"
)

print(
    "=========================================="
)

print()

print(
    "Model:",
    selected_model_name
)

print(
    "Model file:",
    MODEL_PATH
)

print(
    "Training records:",
    len(df)
)

print(
    "Accuracy:",
    round(
        accuracy * 100,
        2
    ),
    "%"
)

print(
    "Precision:",
    round(
        precision * 100,
        2
    ),
    "%"
)

print(
    "Recall:",
    round(
        recall * 100,
        2
    ),
    "%"
)

print(
    "F1-score:",
    round(
        f1 * 100,
        2
    ),
    "%"
)

print()

print(
    "Categories:"
)

for category in sorted(
    df["category"].unique()
):

    print(
        "-",
        category
    )

print()

print(
    "Training process completed successfully."
)