import pickle

with open("model.pkl", "rb") as file:
    model = pickle.load(file)

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

predictions = model.predict(test_expenses)
probabilities = model.predict_proba(test_expenses)

classes = model.named_steps["classifier"].classes_

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