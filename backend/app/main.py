 
# SMARTSPEND - FASTAPI BACKEND
 

#uvicorn backend.app.main:app 

import os
import pickle
import sqlite3
from datetime import datetime, timedelta, timezone
from typing import List, Optional

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from pathlib import Path

 
# PATH CONFIGURATION
 

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
MODEL_PATH = BASE_DIR / "models" / "model.pkl"
DATA_DIR = BASE_DIR / "data"
DATABASE = DATA_DIR / "expenses.db"

 
# APPLICATION
 

app = FastAPI(
    title="SmartSpend API",
    description="AI-powered expense categorization API",
    version="1.5.0"
)


 
# TIMEZONE
# Nepal Time = UTC + 5:45
 

NEPAL_TZ = timezone(
    timedelta(hours=5, minutes=45)
)

DELETED_EXPENSE_RETENTION_DAYS = 15


 
# LOAD MACHINE LEARNING MODEL
 

try:

    with open(
        MODEL_PATH,
        "rb"
    ) as model_file:

        model = pickle.load(
            model_file
        )

except Exception as e:

    model = None

    print(
        "Warning: Could not load model:",
        e
    )


 
# DATABASE INITIALIZATION
 

def initialize_database():

    os.makedirs(
        DATA_DIR,
        exist_ok=True
    )

    connection = sqlite3.connect(
        DATABASE
    )

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            confidence REAL NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL,
            deleted_at TEXT,
            is_essential INTEGER NOT NULL DEFAULT 0
        )
        """
    )

    # --------------------------------------------------------
    # CHECK EXISTING COLUMNS
    # --------------------------------------------------------

    cursor.execute(
        "PRAGMA table_info(expenses)"
    )

    columns = [
        row[1]
        for row in cursor.fetchall()
    ]


    # --------------------------------------------------------
    # ADD CONFIDENCE COLUMN IF REQUIRED
    # --------------------------------------------------------

    if "confidence" not in columns:

        cursor.execute(
            """
            ALTER TABLE expenses
            ADD COLUMN confidence REAL NOT NULL DEFAULT 0
            """
        )


    # --------------------------------------------------------
    # ADD CREATED_AT COLUMN IF REQUIRED
    # --------------------------------------------------------

    if "created_at" not in columns:

        cursor.execute(
            """
            ALTER TABLE expenses
            ADD COLUMN created_at TEXT
            """
        )

        current_time = datetime.now(
            NEPAL_TZ
        ).isoformat()

        cursor.execute(
            """
            UPDATE expenses
            SET created_at = ?
            WHERE created_at IS NULL
            """,
            (current_time,)
        )


    # Store deletion time so expenses can be restored during retention.
    if "deleted_at" not in columns:

        cursor.execute(
            """
            ALTER TABLE expenses
            ADD COLUMN deleted_at TEXT
            """
        )

    # Mark essential or unexpected expenses separately.
    # Existing expenses remain regular by default.
    if "is_essential" not in columns:

        cursor.execute(
            """
            ALTER TABLE expenses
            ADD COLUMN is_essential INTEGER NOT NULL DEFAULT 0
            """
        )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS budget_settings (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            monthly_budget REAL NOT NULL,
            updated_at TEXT NOT NULL
        )
        """
    )

    connection.commit()

    connection.close()


initialize_database()


 
# PYDANTIC MODELS
 

class ExpenseRequest(BaseModel):

    description: str = Field(
        min_length=2,
        max_length=500
    )

    amount: float = Field(
        gt=0
    )

    is_essential: bool = False


class ExpenseTableItem(BaseModel):

    id: int

    description: str = Field(
        min_length=2,
        max_length=500
    )

    amount: float = Field(
        gt=0
    )

    is_essential: bool = False


class ExpenseTableUpdate(BaseModel):

    expenses: List[ExpenseTableItem]


class BudgetRequest(BaseModel):

    monthly_budget: float = Field(
        gt=0,
        le=100000000
    )


 
# DATABASE HELPER
 

def get_connection():

    connection = sqlite3.connect(
        DATABASE
    )

    connection.row_factory = sqlite3.Row

    return connection


def purge_expired_deleted_expenses():

    """Permanently remove expenses that have been in Trash for 15 days."""

    cutoff = datetime.now(
        NEPAL_TZ
    ) - timedelta(
        days=DELETED_EXPENSE_RETENTION_DAYS
    )

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, deleted_at
        FROM expenses
        WHERE deleted_at IS NOT NULL
        """
    )

    expired_ids = []

    for row in cursor.fetchall():

        try:

            deleted_at = datetime.fromisoformat(
                row["deleted_at"]
            )

            if deleted_at.tzinfo is None:

                deleted_at = deleted_at.replace(
                    tzinfo=NEPAL_TZ
                )

            if deleted_at.astimezone(NEPAL_TZ) <= cutoff:

                expired_ids.append(
                    row["id"]
                )

        except (TypeError, ValueError):

            # Retain unreadable legacy timestamps rather than deleting data.
            continue


    if expired_ids:

        cursor.executemany(
            "DELETE FROM expenses WHERE id = ?",
            [(expense_id,) for expense_id in expired_ids]
        )

        connection.commit()


    connection.close()


 
# ML PREDICTION HELPER
 

def predict_category(description):

    if model is None:

        raise HTTPException(
            status_code=500,
            detail="Machine learning model is not available."
        )

    try:

        prediction = model.predict(
            [description]
        )[0]

        probabilities = model.predict_proba(
            [description]
        )[0]

        confidence = float(
            max(probabilities) * 100
        )

        return (
            str(prediction),
            confidence
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail="Prediction failed: " + str(e)
        )


 
# ROOT
 

@app.get("/")
def root():

    return {
        "message": "SmartSpend API is running"
    }


 
# HEALTH
 

@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


 
# ADD / PREDICT EXPENSE
 

@app.post("/predict")
def predict_expense(
    expense: ExpenseRequest
):

    category, confidence = predict_category(
        expense.description
    )

    created_at = datetime.now(
        NEPAL_TZ
    ).isoformat()

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO expenses
        (
            description,
            amount,
            category,
            confidence,
            created_at,
            is_essential
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            expense.description,
            expense.amount,
            category,
            confidence,
            created_at,
            int(expense.is_essential)
        )
    )

    expense_id = cursor.lastrowid

    connection.commit()

    connection.close()

    return {
        "id": expense_id,
        "description": expense.description,
        "amount": expense.amount,
        "category": category,
        "confidence": round(
            confidence,
            2
        ),
        "created_at": created_at,
        "is_essential": expense.is_essential
    }


 
# GET ALL EXPENSES
 

@app.get("/expenses")
def get_expenses():

    purge_expired_deleted_expenses()

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            description,
            amount,
            category,
            confidence,
            created_at,
            is_essential
        FROM expenses
        WHERE deleted_at IS NULL
        ORDER BY id DESC
        """
    )

    rows = cursor.fetchall()

    connection.close()

    expenses = []

    for row in rows:

        expenses.append(
            {
                "id": row["id"],
                "description": row["description"],
                "amount": row["amount"],
                "category": row["category"],
                "confidence": row["confidence"],
                "created_at": row["created_at"],
                "is_essential": bool(row["is_essential"])
            }
        )

    return {
        "expenses": expenses
    }


 
# GET DELETED EXPENSES
 

@app.get("/expenses/deleted")
def get_deleted_expenses():

    purge_expired_deleted_expenses()

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            description,
            amount,
            category,
            confidence,
            created_at,
            deleted_at,
            is_essential
        FROM expenses
        WHERE deleted_at IS NOT NULL
        ORDER BY deleted_at DESC
        """
    )

    rows = cursor.fetchall()

    connection.close()

    return {
        "expenses": [dict(row) for row in rows]
    }


 
# SAVE EDITABLE TABLE
 

@app.put("/expenses/update-table")
def update_expense_table(
    request: ExpenseTableUpdate
):

    if len(request.expenses) == 0:

        return {
            "message": "No expenses to update.",
            "updated": []
        }


    connection = get_connection()

    cursor = connection.cursor()

    updated_expenses = []


    for expense in request.expenses:

        # ----------------------------------------------------
        # FIND EXISTING EXPENSE
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT *
            FROM expenses
            WHERE id = ? AND deleted_at IS NULL
            """,
            (expense.id,)
        )

        existing = cursor.fetchone()

        if existing is None:

            connection.close()

            raise HTTPException(
                status_code=404,
                detail=(
                    "Expense with ID "
                    + str(expense.id)
                    + " was not found."
                )
            )


        old_description = existing[
            "description"
        ]

        old_amount = existing[
            "amount"
        ]

        old_category = existing[
            "category"
        ]

        old_confidence = existing[
            "confidence"
        ]

        created_at = existing[
            "created_at"
        ]

        old_is_essential = bool(
            existing["is_essential"]
        )


        # ----------------------------------------------------
        # DETERMINE IF DESCRIPTION CHANGED
        # ----------------------------------------------------

        description_changed = (
            expense.description.strip()
            != old_description
        )


        # ----------------------------------------------------
        # RE-PREDICT IF DESCRIPTION CHANGED
        # ----------------------------------------------------

        if description_changed:

            new_category, new_confidence = (
                predict_category(
                    expense.description.strip()
                )
            )

        else:

            new_category = old_category

            new_confidence = old_confidence


        # ----------------------------------------------------
        # UPDATE DATABASE
        # ----------------------------------------------------

        cursor.execute(
            """
            UPDATE expenses
            SET
                description = ?,
                amount = ?,
                category = ?,
                confidence = ?,
                is_essential = ?
            WHERE id = ?
            """,
            (
                expense.description.strip(),
                expense.amount,
                new_category,
                new_confidence,
                int(expense.is_essential),
                expense.id
            )
        )


        # ----------------------------------------------------
        # RETURN UPDATED EXPENSE
        # ----------------------------------------------------

        updated_expenses.append(
            {
                "id": expense.id,
                "description": expense.description.strip(),
                "amount": expense.amount,
                "category": new_category,
                "confidence": round(
                    float(new_confidence),
                    2
                ),
                "created_at": created_at,
                "is_essential": expense.is_essential
            }
        )


    connection.commit()

    connection.close()


    return {
        "message": "Expenses updated successfully.",
        "updated": updated_expenses
    }


 
# DELETE EXPENSE
 

@app.delete("/expenses/{expense_id}")
def delete_expense(
    expense_id: int
):

    purge_expired_deleted_expenses()

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id
        FROM expenses
        WHERE id = ? AND deleted_at IS NULL
        """,
        (expense_id,)
    )

    existing = cursor.fetchone()

    if existing is None:

        connection.close()

        raise HTTPException(
            status_code=404,
            detail="Expense not found."
        )


    cursor.execute(
        """
        UPDATE expenses
        SET deleted_at = ?
        WHERE id = ?
        """,
        (
            datetime.now(NEPAL_TZ).isoformat(),
            expense_id
        )
    )

    connection.commit()

    connection.close()

    return {
        "message": (
            "Expense moved to Deleted History. "
            "It can be restored for 15 days."
        ),
        "id": expense_id
    }


 
# RESTORE DELETED EXPENSE
 

@app.post("/expenses/{expense_id}/restore")
def restore_expense(expense_id: int):

    purge_expired_deleted_expenses()

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE expenses
        SET deleted_at = NULL
        WHERE id = ? AND deleted_at IS NOT NULL
        """,
        (expense_id,)
    )

    if cursor.rowcount == 0:

        connection.close()

        raise HTTPException(
            status_code=404,
            detail=(
                "Deleted expense was not found or has already "
                "been permanently removed."
            )
        )

    connection.commit()

    connection.close()

    return {
        "message": "Expense restored successfully.",
        "id": expense_id
    }


 
# SUMMARY
 

@app.get("/summary")
def get_summary():

    purge_expired_deleted_expenses()

    connection = get_connection()

    cursor = connection.cursor()


    # --------------------------------------------------------
    # TOTALS
    # --------------------------------------------------------

    cursor.execute(
        """
        SELECT
            COUNT(*) AS total_expenses,
            COALESCE(
                SUM(amount),
                0
            ) AS total_spending,
            COALESCE(
                SUM(
                    CASE
                        WHEN is_essential = 0 THEN amount
                        ELSE 0
                    END
                ),
                0
            ) AS regular_spending,
            COALESCE(
                SUM(
                    CASE
                        WHEN is_essential = 1 THEN amount
                        ELSE 0
                    END
                ),
                0
            ) AS essential_spending,
            SUM(
                CASE
                    WHEN is_essential = 1 THEN 1
                    ELSE 0
                END
            ) AS essential_expenses
        FROM expenses
        WHERE deleted_at IS NULL
        """
    )

    totals = cursor.fetchone()


    # --------------------------------------------------------
    # CATEGORY TOTALS
    # --------------------------------------------------------

    cursor.execute(
        """
        SELECT
            category,
            COALESCE(
                SUM(amount),
                0
            ) AS total
        FROM expenses
        WHERE deleted_at IS NULL
        GROUP BY category
        ORDER BY total DESC
        """
    )

    category_rows = cursor.fetchall()

    connection.close()


    categories = {}

    for row in category_rows:

        categories[
            row["category"]
        ] = round(
            float(row["total"]),
            2
        )


    return {
        "total_expenses": totals["total_expenses"],
        "total_spending": round(
            float(totals["total_spending"]),
            2
        ),
        "regular_spending": round(
            float(totals["regular_spending"]),
            2
        ),
        "essential_spending": round(
            float(totals["essential_spending"]),
            2
        ),
        "essential_expenses": int(
            totals["essential_expenses"] or 0
        ),
        "categories": categories
    }


 
# BUDGET
 

def get_current_month_budget():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT monthly_budget
        FROM budget_settings
        WHERE id = 1
        """
    )

    row = cursor.fetchone()
    connection.close()

    if row is None:
        return 0.0

    return float(row["monthly_budget"])


@app.get("/budget")
def get_budget():

    purge_expired_deleted_expenses()

    now = datetime.now(NEPAL_TZ)
    rows = load_expense_rows()

    monthly_budget = get_current_month_budget()

    month_rows = []

    for row in rows:
        try:
            created_at = datetime.fromisoformat(
                row["created_at"]
            )

            if created_at.tzinfo is None:
                created_at = created_at.replace(
                    tzinfo=NEPAL_TZ
                )

            created_at = created_at.astimezone(
                NEPAL_TZ
            )

            if (
                created_at.year == now.year
                and created_at.month == now.month
            ):
                month_rows.append(row)

        except Exception:
            continue

    regular_spending = sum(
        float(row["amount"])
        for row in month_rows
        if not bool(row["is_essential"])
    )

    essential_spending = sum(
        float(row["amount"])
        for row in month_rows
        if bool(row["is_essential"])
    )

    total_spending = regular_spending + essential_spending

    remaining = max(
        0.0,
        monthly_budget - regular_spending
    )

    usage_percent = (
        (regular_spending / monthly_budget) * 100
        if monthly_budget > 0
        else 0
    )

    days_in_month = (
        datetime(
            now.year,
            now.month % 12 + 1 if now.month < 12 else 1,
            1,
            tzinfo=NEPAL_TZ
        )
        - datetime(
            now.year,
            now.month,
            1,
            tzinfo=NEPAL_TZ
        )
    ).days if now.month < 12 else (
        datetime(now.year + 1, 1, 1, tzinfo=NEPAL_TZ)
        - datetime(now.year, 12, 1, tzinfo=NEPAL_TZ)
    ).days

    days_elapsed = now.day
    days_remaining = max(
        0,
        days_in_month - days_elapsed
    )

    daily_average = (
        regular_spending / days_elapsed
        if days_elapsed > 0
        else 0
    )

    projected_spending = (
        daily_average * days_in_month
        if regular_spending > 0
        else 0
    )

    if monthly_budget <= 0:
        status = "Not set"
        alert = "Set a monthly budget to start tracking spending."
    elif regular_spending > monthly_budget:
        status = "Over budget"
        alert = (
            "Your regular spending has exceeded your monthly budget by Rs. "
            + format(regular_spending - monthly_budget, ",.2f")
            + "."
        )
    elif usage_percent >= 90:
        status = "Near limit"
        alert = "You are very close to your monthly budget limit."
    elif usage_percent >= 70:
        status = "Watch spending"
        alert = "You have used 70% or more of your monthly budget."
    else:
        status = "On track"
        alert = "Your spending is currently within your budget."

    projected_over_budget = max(
        0.0,
        projected_spending - monthly_budget
    ) if monthly_budget > 0 else 0.0

    return {
        "monthly_budget": round(monthly_budget, 2),
        "spent": round(regular_spending, 2),
        "regular_spending": round(regular_spending, 2),
        "essential_spending": round(essential_spending, 2),
        "total_spending": round(total_spending, 2),
        "remaining": round(remaining, 2),
        "usage_percent": round(usage_percent, 2),
        "status": status,
        "alert": alert,
        "projected_spending": round(projected_spending, 2),
        "projected_over_budget": round(projected_over_budget, 2),
        "days_elapsed": days_elapsed,
        "days_remaining": days_remaining,
        "essential_expenses": sum(
            1
            for row in month_rows
            if bool(row["is_essential"])
        )
    }


@app.put("/budget")
def update_budget(request: BudgetRequest):

    now = datetime.now(NEPAL_TZ).isoformat()

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO budget_settings (
            id, monthly_budget, updated_at
        )
        VALUES (1, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            monthly_budget = excluded.monthly_budget,
            updated_at = excluded.updated_at
        """,
        (
            request.monthly_budget,
            now
        )
    )

    connection.commit()
    connection.close()

    return {
        "message": "Monthly budget updated successfully.",
        "monthly_budget": round(
            request.monthly_budget,
            2
        )
    }


 
# ANALYTICS HELPER
 

def load_expense_rows():

    purge_expired_deleted_expenses()

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            description,
            amount,
            category,
            confidence,
            created_at,
            is_essential
        FROM expenses
        WHERE deleted_at IS NULL
        ORDER BY created_at ASC
        """
    )

    rows = cursor.fetchall()

    connection.close()

    return rows


 
# CATEGORY STATISTICS
 

def get_category_statistics(rows):

    statistics = {}

    for row in rows:

        category = row["category"]

        if category not in statistics:

            statistics[category] = {
                "spending": 0,
                "transactions": 0
            }

        statistics[category]["spending"] += float(
            row["amount"]
        )

        statistics[category]["transactions"] += 1


    for category in statistics:

        statistics[category]["spending"] = round(
            statistics[category]["spending"],
            2
        )


    return statistics


 
# HIGHEST EXPENSE
 

def get_highest_expense(rows):

    if not rows:

        return None

    highest = max(
        rows,
        key=lambda row: float(
            row["amount"]
        )
    )

    return {
        "id": highest["id"],
        "description": highest["description"],
        "amount": round(
            float(highest["amount"]),
            2
        ),
        "category": highest["category"],
        "confidence": round(
            float(highest["confidence"]),
            2
        ),
        "created_at": highest["created_at"],
        "is_essential": bool(
            highest["is_essential"]
        )
    }


 
# PERCENTAGE CHANGE
 

def percentage_change(
    current,
    previous
):

    if previous == 0:

        if current == 0:
            return 0

        return 100

    return (
        (current - previous)
        / previous
    ) * 100


 
# INSIGHTS
 

def build_insights(
    rows,
    total_spending,
    total_expenses
):

    insights = []

    if total_expenses == 0:

        return [
            "No expenses have been recorded yet."
        ]


    # --------------------------------------------------------
    # MOST SPENT CATEGORY
    # --------------------------------------------------------

    category_totals = {}

    for row in rows:

        category = row["category"]

        category_totals[category] = (
            category_totals.get(
                category,
                0
            )
            + float(row["amount"])
        )


    if category_totals:

        most_spent_category = max(
            category_totals,
            key=category_totals.get
        )

        category_amount = category_totals[
            most_spent_category
        ]

        percentage = (
            category_amount
            / total_spending
            * 100
            if total_spending > 0
            else 0
        )

        insights.append(
            most_spent_category
            + " is your highest spending category, "
            + "accounting for "
            + format(
                percentage,
                ".1f"
            )
            + "% of spending."
        )


    # --------------------------------------------------------
    # TRANSACTION FREQUENCY
    # --------------------------------------------------------

    if total_expenses >= 5:

        insights.append(
            "You have recorded "
            + str(total_expenses)
            + " expenses in this period."
        )


    # --------------------------------------------------------
    # AVERAGE EXPENSE
    # --------------------------------------------------------

    average = (
        total_spending
        / total_expenses
    )

    insights.append(
        "Your average expense is Rs. "
        + format(
            average,
            ",.2f"
        )
        + "."
    )


    return insights


 
# MONTHLY ANALYTICS
 

@app.get("/analytics/monthly")
def monthly_analytics(
    year: int = Query(...),
    month: int = Query(...)
):

    if month < 1 or month > 12:

        raise HTTPException(
            status_code=400,
            detail="Month must be between 1 and 12."
        )


    rows = load_expense_rows()

    matching_rows = []


    for row in rows:

        try:

            created_at = datetime.fromisoformat(
                row["created_at"]
            )

            if created_at.tzinfo is None:

                created_at = created_at.replace(
                    tzinfo=NEPAL_TZ
                )

            created_at_nepal = created_at.astimezone(
                NEPAL_TZ
            )

            if (
                created_at_nepal.year == year
                and created_at_nepal.month == month
            ):

                matching_rows.append(row)

        except Exception:

            continue


    total_expenses = len(
        matching_rows
    )

    total_spending = sum(
        float(row["amount"])
        for row in matching_rows
    )

    average_expense = (
        total_spending / total_expenses
        if total_expenses > 0
        else 0
    )


    # --------------------------------------------------------
    # CATEGORY TOTALS
    # --------------------------------------------------------

    categories = {}

    for row in matching_rows:

        category = row["category"]

        categories[category] = (
            categories.get(
                category,
                0
            )
            + float(row["amount"])
        )


    categories = {
        category: round(
            amount,
            2
        )
        for category, amount in categories.items()
    }


    # --------------------------------------------------------
    # DAILY SPENDING
    # --------------------------------------------------------

    daily_totals = {}

    for row in matching_rows:

        try:

            created_at = datetime.fromisoformat(
                row["created_at"]
            )

            if created_at.tzinfo is None:

                created_at = created_at.replace(
                    tzinfo=NEPAL_TZ
                )

            date_key = created_at.astimezone(
                NEPAL_TZ
            ).strftime(
                "%Y-%m-%d"
            )

            daily_totals[date_key] = (
                daily_totals.get(
                    date_key,
                    0
                )
                + float(row["amount"])
            )

        except Exception:

            continue


    daily_spending = [
        {
            "date": date,
            "amount": round(
                amount,
                2
            )
        }
        for date, amount
        in sorted(
            daily_totals.items()
        )
    ]


    # --------------------------------------------------------
    # HIGHEST EXPENSE
    # --------------------------------------------------------

    highest_expense = get_highest_expense(
        matching_rows
    )


    # --------------------------------------------------------
    # CATEGORY STATISTICS
    # --------------------------------------------------------

    category_statistics = (
        get_category_statistics(
            matching_rows
        )
    )


    most_spent_category = None

    most_frequent_category = None


    if category_statistics:

        most_spent_category = max(
            category_statistics,
            key=lambda category:
            category_statistics[category][
                "spending"
            ]
        )

        most_frequent_category = max(
            category_statistics,
            key=lambda category:
            category_statistics[category][
                "transactions"
            ]
        )


    # --------------------------------------------------------
    # INSIGHTS
    # --------------------------------------------------------

    insights = build_insights(
        matching_rows,
        total_spending,
        total_expenses
    )


    return {
        "year": year,
        "month": month,
        "total_expenses": total_expenses,
        "total_spending": round(
            total_spending,
            2
        ),
        "average_expense": round(
            average_expense,
            2
        ),
        "regular_spending": round(
            sum(
                float(row["amount"])
                for row in matching_rows
                if not bool(row["is_essential"])
            ),
            2
        ),
        "essential_spending": round(
            sum(
                float(row["amount"])
                for row in matching_rows
                if bool(row["is_essential"])
            ),
            2
        ),
        "categories": categories,
        "category_statistics": category_statistics,
        "most_spent_category": most_spent_category,
        "most_frequent_category": most_frequent_category,
        "daily_spending": daily_spending,
        "highest_expense": highest_expense,
        "insights": insights
    }


 
# WEEKLY ANALYTICS
 

@app.get("/analytics/weekly")
def weekly_analytics():

    now = datetime.now(
        NEPAL_TZ
    )

    current_date = now.date()

    days_since_sunday = (
        current_date.weekday() + 1
    ) % 7

    sunday = current_date - timedelta(
        days=days_since_sunday
    )

    saturday = sunday + timedelta(
        days=6
    )


    week_start = datetime.combine(
        sunday,
        datetime.min.time(),
        tzinfo=NEPAL_TZ
    )

    week_end = datetime.combine(
        saturday,
        datetime.max.time(),
        tzinfo=NEPAL_TZ
    )


    rows = load_expense_rows()

    matching_rows = []


    for row in rows:

        try:

            created_at = datetime.fromisoformat(
                row["created_at"]
            )

            if created_at.tzinfo is None:

                created_at = created_at.replace(
                    tzinfo=NEPAL_TZ
                )

            created_at = created_at.astimezone(
                NEPAL_TZ
            )

            if (
                week_start
                <= created_at
                <= week_end
            ):

                matching_rows.append(row)

        except Exception:

            continue


    total_expenses = len(
        matching_rows
    )

    total_spending = sum(
        float(row["amount"])
        for row in matching_rows
    )

    average_expense = (
        total_spending
        / total_expenses
        if total_expenses > 0
        else 0
    )


    # --------------------------------------------------------
    # CATEGORY TOTALS
    # --------------------------------------------------------

    categories = {}

    for row in matching_rows:

        category = row["category"]

        categories[category] = (
            categories.get(
                category,
                0
            )
            + float(row["amount"])
        )


    categories = {
        category: round(
            amount,
            2
        )
        for category, amount in categories.items()
    }


    # --------------------------------------------------------
    # DAILY SPENDING
    # --------------------------------------------------------

    daily_totals = {}

    for day_offset in range(7):

        current_day = (
            sunday
            + timedelta(
                days=day_offset
            )
        )

        daily_totals[
            current_day.strftime(
                "%Y-%m-%d"
            )
        ] = 0


    for row in matching_rows:

        try:

            created_at = datetime.fromisoformat(
                row["created_at"]
            )

            if created_at.tzinfo is None:

                created_at = created_at.replace(
                    tzinfo=NEPAL_TZ
                )

            created_at = created_at.astimezone(
                NEPAL_TZ
            )

            date_key = created_at.strftime(
                "%Y-%m-%d"
            )

            if date_key in daily_totals:

                daily_totals[date_key] += float(
                    row["amount"]
                )

        except Exception:

            continue


    daily_spending = [
        {
            "date": date,
            "amount": round(
                amount,
                2
            )
        }
        for date, amount
        in sorted(
            daily_totals.items()
        )
    ]


    # --------------------------------------------------------
    # CATEGORY STATISTICS
    # --------------------------------------------------------

    category_statistics = (
        get_category_statistics(
            matching_rows
        )
    )


    most_spent_category = None

    most_frequent_category = None


    if category_statistics:

        most_spent_category = max(
            category_statistics,
            key=lambda category:
            category_statistics[category][
                "spending"
            ]
        )

        most_frequent_category = max(
            category_statistics,
            key=lambda category:
            category_statistics[category][
                "transactions"
            ]
        )


    # --------------------------------------------------------
    # HIGHEST EXPENSE
    # --------------------------------------------------------

    highest_expense = get_highest_expense(
        matching_rows
    )


    # --------------------------------------------------------
    # INSIGHTS
    # --------------------------------------------------------

    insights = build_insights(
        matching_rows,
        total_spending,
        total_expenses
    )


    return {
        "week_start": sunday.strftime(
            "%Y-%m-%d"
        ),
        "week_end": saturday.strftime(
            "%Y-%m-%d"
        ),
        "total_expenses": total_expenses,
        "total_spending": round(
            total_spending,
            2
        ),
        "average_expense": round(
            average_expense,
            2
        ),
        "regular_spending": round(
            sum(
                float(row["amount"])
                for row in matching_rows
                if not bool(row["is_essential"])
            ),
            2
        ),
        "essential_spending": round(
            sum(
                float(row["amount"])
                for row in matching_rows
                if bool(row["is_essential"])
            ),
            2
        ),
        "categories": categories,
        "category_statistics": category_statistics,
        "most_spent_category": most_spent_category,
        "most_frequent_category": most_frequent_category,
        "daily_spending": daily_spending,
        "highest_expense": highest_expense,
        "insights": insights
    }


 
# MONTHLY TREND
 

@app.get("/analytics/trend")
def monthly_trend(
    months: int = Query(
        6,
        ge=1,
        le=24
    )
):

    now = datetime.now(
        NEPAL_TZ
    )

    rows = load_expense_rows()

    results = []


    for offset in range(
        months - 1,
        -1,
        -1
    ):

        year = now.year

        month = now.month - offset

        while month <= 0:

            month += 12
            year -= 1


        total_spending = 0
        total_expenses = 0


        for row in rows:

            try:

                created_at = datetime.fromisoformat(
                    row["created_at"]
                )

                if created_at.tzinfo is None:

                    created_at = created_at.replace(
                        tzinfo=NEPAL_TZ
                    )

                created_at = created_at.astimezone(
                    NEPAL_TZ
                )

                if (
                    created_at.year == year
                    and created_at.month == month
                ):

                    total_spending += float(
                        row["amount"]
                    )

                    total_expenses += 1

            except Exception:

                continue


        label = datetime(
            year,
            month,
            1
        ).strftime(
            "%b %Y"
        )


        results.append(
            {
                "year": year,
                "month": month,
                "label": label,
                "total_spending": round(
                    total_spending,
                    2
                ),
                "total_expenses": total_expenses
            }
        )


    return {
        "months": results
    }


 
# MONTH-TO-MONTH COMPARISON
 

@app.get("/analytics/comparison")
def monthly_comparison(
    year: int = Query(...),
    month: int = Query(...)
):

    if month < 1 or month > 12:

        raise HTTPException(
            status_code=400,
            detail="Month must be between 1 and 12."
        )


    # --------------------------------------------------------
    # PREVIOUS MONTH
    # --------------------------------------------------------

    if month == 1:

        previous_year = year - 1
        previous_month = 12

    else:

        previous_year = year
        previous_month = month - 1


    current = monthly_analytics(
        year,
        month
    )

    previous = monthly_analytics(
        previous_year,
        previous_month
    )


    change = percentage_change(
        current["total_spending"],
        previous["total_spending"]
    )


    # --------------------------------------------------------
    # CATEGORY COMPARISON
    # --------------------------------------------------------

    all_categories = set()

    all_categories.update(
        current["categories"].keys()
    )

    all_categories.update(
        previous["categories"].keys()
    )


    category_comparison = {}


    for category in sorted(
        all_categories
    ):

        current_amount = current[
            "categories"
        ].get(
            category,
            0
        )

        previous_amount = previous[
            "categories"
        ].get(
            category,
            0
        )


        category_change = percentage_change(
            current_amount,
            previous_amount
        )


        category_comparison[
            category
        ] = {
            "current": round(
                current_amount,
                2
            ),
            "previous": round(
                previous_amount,
                2
            ),
            "change_percent": round(
                category_change,
                2
            )
        }


    return {
        "current_month": current,
        "previous_month": previous,
        "change_percent": round(
            change,
            2
        ),
        "category_comparison": category_comparison
    }