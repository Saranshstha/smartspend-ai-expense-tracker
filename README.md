# SmartSpend

AI-powered expense categorization and spending analytics system built with **FastAPI, Streamlit, SQLite, and Machine Learning**.

SmartSpend helps users record expenses, automatically categorize them using an NLP model, monitor spending, manage a monthly budget, and understand their spending patterns through simple analytics.


## Features

### AI Expense Categorization

SmartSpend automatically predicts the category of an expense from its description using a supervised machine learning model.

Supported categories include:

- Food
- Transport
- Education
- Shopping
- Entertainment

The system also provides a prediction confidence score for each expense.

---

### Expense Management

Users can:

- Add new expenses
- View all expenses
- Search and filter expenses
- Edit descriptions and amounts
- Automatically re-categorize expenses when descriptions are changed
- Delete expenses
- Restore recently deleted expenses
- Track deleted expenses for a limited retention period

---

### Regular and Essential Spending

SmartSpend distinguishes between normal spending and essential or unexpected spending.

When adding an expense:

- **Regular Spending** is selected by default
- **Essential / Unexpected** can be selected for expenses such as prescription glasses, emergency medical costs, urgent repairs, or other unavoidable expenses

This distinction is reflected across the application.

Essential spending:

- Appears separately in the dashboard
- Is identified in the Expenses table
- Can be filtered in the Expenses page
- Appears separately in Analytics
- Does not count toward normal monthly budget usage

This provides a more realistic view of a user's financial situation.

---

### Budget Tracking

Users can set a monthly spending budget and SmartSpend tracks regular spending against it.

The system provides:

- Monthly budget
- Regular spending
- Remaining budget
- Budget usage percentage
- Essential / unexpected spending
- Spending alerts
- Estimated month-end spending
- Projected budget overage

Budget status can indicate:

- On Track
- Watch Spending
- Near Limit
- Over Budget

Essential or unexpected expenses are shown separately so unavoidable expenses do not incorrectly represent normal budget overspending.

---

### Spending Analytics

SmartSpend provides simple analytics designed to be understandable at a glance.

Analytics include:

- Today's spending
- Current week's spending
- Current month's spending
- Last 6 months
- Current year's spending
- Weekly spending patterns
- Spending trends
- Category spending
- Month-to-month comparisons
- Essential versus regular spending
- Spending insights

Weekly analytics follow a **Sunday to Saturday** structure.

---

### Dashboard

The dashboard provides an overview of financial activity, including:

- Total spending
- Number of expenses
- Average expense
- Budget status
- Regular spending
- Essential / unexpected spending
- Spending by category
- Recent expenses

---

## Machine Learning

SmartSpend uses a supervised Natural Language Processing approach for expense categorization.

### Model Pipeline

Expense Description
        ↓
Text Preprocessing
        ↓
TF-IDF Feature Extraction
        ↓
Logistic Regression
        ↓
Predicted Category
        ↓
Confidence Score
