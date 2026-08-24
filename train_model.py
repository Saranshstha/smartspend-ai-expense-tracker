import pandas as pd
import pickle

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline


# Sample expense data
data = [

    # Food
    ("lunch at restaurant", "Food"),
    ("dinner at cafe", "Food"),
    ("pizza", "Food"),
    ("burger and fries", "Food"),
    ("breakfast at cafe", "Food"),
    ("grocery shopping", "Food"),
    ("milk and bread", "Food"),
    ("buy vegetables", "Food"),
    ("chicken and rice", "Food"),
    ("coffee and snacks", "Food"),
    ("restaurant meal", "Food"),
    ("lunch at college", "Food"),
    ("buy fruits", "Food"),
    ("dinner with friends", "Food"),
    ("fast food", "Food"),
    ("buy groceries", "Food"),

    # Transport
    ("bus ticket", "Transport"),
    ("taxi to college", "Transport"),
    ("uber ride", "Transport"),
    ("bus fare", "Transport"),
    ("fuel for car", "Transport"),
    ("petrol", "Transport"),
    ("taxi ride", "Transport"),
    ("ride to university", "Transport"),
    ("public bus", "Transport"),
    ("transport fare", "Transport"),
    ("motorbike fuel", "Transport"),
    ("cab to home", "Transport"),
    ("bus to college", "Transport"),
    ("travel fare", "Transport"),
    ("car fuel", "Transport"),
    ("ride sharing", "Transport"),

    # Education
    ("python programming book", "Education"),
    ("college tuition", "Education"),
    ("university fee", "Education"),
    ("buy textbook", "Education"),
    ("online programming course", "Education"),
    ("exam fee", "Education"),
    ("notebook for college", "Education"),
    ("buy stationery", "Education"),
    ("coding course", "Education"),
    ("study materials", "Education"),
    ("college books", "Education"),
    ("learning course", "Education"),
    ("school supplies", "Education"),
    ("programming tutorial", "Education"),
    ("academic book", "Education"),
    ("education fee", "Education"),

    # Entertainment
    ("movie ticket", "Entertainment"),
    ("netflix subscription", "Entertainment"),
    ("concert ticket", "Entertainment"),
    ("gaming subscription", "Entertainment"),
    ("video game", "Entertainment"),
    ("cinema", "Entertainment"),
    ("movie with friends", "Entertainment"),
    ("spotify subscription", "Entertainment"),
    ("game purchase", "Entertainment"),
    ("bowling", "Entertainment"),
    ("arcade", "Entertainment"),
    ("music subscription", "Entertainment"),
    ("movie night", "Entertainment"),
    ("entertainment ticket", "Entertainment"),
    ("game subscription", "Entertainment"),
    ("watching movie", "Entertainment"),

    # Shopping
    ("new shirt", "Shopping"),
    ("buy shoes", "Shopping"),
    ("new jeans", "Shopping"),
    ("clothes shopping", "Shopping"),
    ("buy backpack", "Shopping"),
    ("new headphones", "Shopping"),
    ("buy keyboard", "Shopping"),
    ("new mouse", "Shopping"),
    ("shopping mall", "Shopping"),
    ("buy jacket", "Shopping"),
    ("buy clothes", "Shopping"),
    ("new bag", "Shopping"),
    ("buy watch", "Shopping"),
    ("new t shirt", "Shopping"),
    ("online shopping", "Shopping"),
    ("buy accessories", "Shopping"),
]


# Convert data into a DataFrame
df = pd.DataFrame(
    data,
    columns=["description", "category"]
)


# Save the dataset as CSV
df.to_csv("expenses.csv", index=False)


# Create the machine learning pipeline
model = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("classifier", LogisticRegression(max_iter=1000))
])


# Train the model
model.fit(
    df["description"],
    df["category"]
)


# Save the trained model
with open("model.pkl", "wb") as file:
    pickle.dump(model, file)


print("Dataset created successfully.")
print("AI model trained successfully.")
print("Model saved as model.pkl")
print()
print("Number of training records:", len(df))
print()
print("Categories:")
print(df["category"].value_counts())