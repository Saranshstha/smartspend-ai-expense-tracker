#uvicorn app.main:app --reload
from pathlib import Path
import pickle
import sqlite3

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


# PROJECT PATHS

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "model.pkl"

DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

DATABASE = DATA_DIR / "expenses.db"



# FASTAPI APPLICATION


app = FastAPI(
    title="SmartSpend API",
    description="AI-powered expense categorization API",
    version="1.0.0"
)



# LOAD AI MODEL


if not MODEL_PATH.exists():

    raise FileNotFoundError(
        "model.pkl was not found. Run train_model.py first."
    )

with open(MODEL_PATH, "rb") as file:

    model = pickle.load(file)



# DATABASE


def create_database():

    # Open the SQLite database, creating the file when it does not exist.
    connection = sqlite3.connect(DATABASE)

    # Create the expenses table for new installations.
    connection.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            confidence REAL NOT NULL DEFAULT 0
        )
    """)

    cursor = connection.cursor()

    # Inspect existing columns so older databases can be upgraded safely.
    cursor.execute(
        "PRAGMA table_info(expenses)"
    )

    columns = [
        row[1]
        for row in cursor.fetchall()
    ]

    if "confidence" not in columns:

        # Add the confidence column when migrating an older database schema.
        connection.execute(
            """
            ALTER TABLE expenses
            ADD COLUMN confidence
            REAL NOT NULL DEFAULT 0
            """
        )

    # Persist any schema changes and release the database connection.
    connection.commit()
    connection.close()


create_database()



# REQUEST MODEL


class ExpenseRequest(BaseModel):

    description: str = Field(
        min_length=2,
        max_length=500,
        description="Description of the expense"
    )

    amount: float = Field(
        gt=0,
        description="Expense amount in Nepalese Rupees"
    )



# ROOT


@app.get("/")
def root():

    return {
        "message": "Welcome to SmartSpend API",
        "status": "running",
        "docs": "/docs"
    }



# HEALTH CHECK


@app.get("/health")
def health_check():

    return {
        "status": "healthy",
        "service": "SmartSpend API",
        "model_loaded": model is not None
    }



# PREDICT EXPENSE


@app.post("/predict")
def predict_expense(expense: ExpenseRequest):

    # Keep the connection variable available for reliable cleanup in finally.
    connection = None

    try:

        # Normalize leading and trailing whitespace before prediction and storage.
        description = expense.description.strip()

        # Predict the most likely expense category from the trained model.
        prediction = model.predict(
            [description]
        )[0]

        # Calculate a percentage confidence from the strongest class probability.
        probabilities = model.predict_proba(
            [description]
        )[0]

        confidence = max(probabilities) * 100

        # Open a database connection and save the classified expense.
        connection = sqlite3.connect(
            DATABASE
        )

        connection.execute(
            """
            INSERT INTO expenses
            (
                description,
                amount,
                category,
                confidence
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                description,
                expense.amount,
                str(prediction),
                confidence
            )
        )

        # Commit the new expense before returning it to the client.
        connection.commit()

        # Return the stored expense details for the frontend prediction panel.
        return {
            "description": description,
            "amount": expense.amount,
            "category": str(prediction),
            "confidence": round(
                confidence,
                2
            )
        }

    except Exception:

        # Convert prediction or database failures into a consistent API error.
        raise HTTPException(
            status_code=500,
            detail="Unable to predict and save the expense."
        )

    finally:

        # Close the connection whether the request succeeds or fails.
        if connection is not None:

            connection.close()



# GET ALL EXPENSES


@app.get("/expenses")
def get_expenses():

    # Keep the connection variable available for reliable cleanup in finally.
    connection = None

    try:

        # Connect to the database and request newest expenses first.
        connection = sqlite3.connect(
            DATABASE
        )

        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                id,
                description,
                amount,
                category,
                confidence
            FROM expenses
            ORDER BY id DESC
        """)

        # Fetch query results before converting them into JSON-friendly objects.
        rows = cursor.fetchall()

        expenses = []

        # Convert each database row to the response format expected by Streamlit.
        for row in rows:

            expenses.append({
                "id": row[0],
                "description": row[1],
                "amount": row[2],
                "category": row[3],
                "confidence": round(
                    row[4],
                    2
                )
            })

        return {
            "count": len(expenses),
            "expenses": expenses
        }

    except sqlite3.Error:

        # Expose a safe, client-friendly error if the database query fails.
        raise HTTPException(
            status_code=500,
            detail="Unable to retrieve expenses."
        )

    finally:

        # Always release the SQLite connection after processing the request.
        if connection is not None:

            connection.close()



# SPENDING SUMMARY


@app.get("/summary")
def get_summary():

    # Keep the connection variable available for reliable cleanup in finally.
    connection = None

    try:

        # Connect to the database to calculate overall spending statistics.
        connection = sqlite3.connect(
            DATABASE
        )

        cursor = connection.cursor()

        # Calculate the number of expenses and their combined amount.
        cursor.execute("""
            SELECT
                COUNT(*),
                COALESCE(SUM(amount), 0)
            FROM expenses
        """)

        total_count, total_amount = (
            cursor.fetchone()
        )

        # Aggregate spending totals for each predicted category.
        cursor.execute("""
            SELECT
                category,
                SUM(amount)
            FROM expenses
            GROUP BY category
            ORDER BY SUM(amount) DESC
        """)

        category_rows = cursor.fetchall()

        categories = {}

        # Format grouped totals as a category-to-amount mapping for the frontend.
        for category, amount in category_rows:

            categories[category] = round(
                amount,
                2
            )

        return {
            "total_expenses": total_count,
            "total_spending": round(
                total_amount,
                2
            ),
            "categories": categories
        }

    except sqlite3.Error:

        # Expose a safe, client-friendly error if summary generation fails.
        raise HTTPException(
            status_code=500,
            detail="Unable to retrieve spending summary."
        )

    finally:

        # Always release the SQLite connection after processing the request.
        if connection is not None:

            connection.close()



# DELETE EXPENSE


@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int):

    # Keep the connection variable available for reliable cleanup in finally.
    connection = None

    try:

        # Connect to the database and delete only the selected expense ID.
        connection = sqlite3.connect(
            DATABASE
        )

        cursor = connection.cursor()

        cursor.execute(
            """
            DELETE FROM expenses
            WHERE id = ?
            """,
            (expense_id,)
        )

        # Return a not-found response when the ID did not match any record.
        if cursor.rowcount == 0:

            raise HTTPException(
                status_code=404,
                detail="Expense not found."
            )

        # Persist the deletion before confirming the result to the client.
        connection.commit()

        return {
            "message": "Expense deleted successfully.",
            "expense_id": expense_id
        }

    except HTTPException:

        # Preserve intentional HTTP responses such as the 404 above.
        raise

    except sqlite3.Error:

        # Convert database failures into a consistent API error response.
        raise HTTPException(
            status_code=500,
            detail="Database error while deleting expense."
        )

    finally:

        # Always release the SQLite connection after processing the request.
        if connection is not None:

            connection.close()
