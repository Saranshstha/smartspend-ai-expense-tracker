import pickle

# Load the trained categorization pipeline from disk.
with open("model.pkl", "rb") as file:
    model = pickle.load(file)

# Define sample descriptions used to manually verify model predictions.
test_expenses = [
    "hot lemon",
    "coffee from college cafe",
    "football shoes",
    "new smartphone",
    "movie with friends",
    "python course fee",
    "pathao to college",
    "grocery delivery",
    "cricket bat",
    "spotify monthly plan",
    "college backpack",
    "taxi to cinema",
    "restaurant momo",
    "buy a calculator",
    "gaming keyboard"
]

# Generate a category and per-category confidence scores for every sample.
predictions = model.predict(test_expenses)
probabilities = model.predict_proba(test_expenses)

# Read the learned category labels from the pipeline classifier.
classes = model.named_steps["classifier"].classes_

# Print each sample alongside its predicted category and highest confidence.
for description, prediction, probability in zip(
    test_expenses,
    predictions,
    probabilities
):

    confidence = max(probability) * 100

    print(
        description,
        "->",
        prediction,
        "|",
        round(confidence, 2),
        "%"
    )
