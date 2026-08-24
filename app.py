import os

import pandas as pd
import requests
import streamlit as st


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="SmartSpend",
    page_icon="S",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ==========================================
# CUSTOM DESIGN
# ==========================================

st.markdown(
    """
    <style>

    /* =====================================
       GLOBAL PAGE
    ===================================== */

    .stApp {
        background-color: #0F1115;
        color: #F5F5F5;
    }

    .block-container {
        max-width: 1080px;
        margin: 0 auto;
        padding-top: 3rem;
        padding-right: 3rem;
        padding-bottom: 3rem;
        padding-left: 3rem;
    }


    /* =====================================
       TYPOGRAPHY
    ===================================== */

    html, body, [class*="css"] {
        font-family: Arial, Helvetica, sans-serif;
    }

    h1, h2, h3 {
        color: #F5F5F5 !important;
        font-weight: 600 !important;
        letter-spacing: -0.02em;
    }

    p {
        color: #9CA3AF;
    }


    /* =====================================
       HEADER
    ===================================== */

    .brand {
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 0.20em;
        color: #D6A85F;
        margin-bottom: 14px;
    }

    .hero-title {
        font-size: 40px;
        font-weight: 600;
        line-height: 1.12;
        color: #F5F5F5;
        margin-bottom: 10px;
    }

    .hero-subtitle {
        max-width: 680px;
        font-size: 15px;
        line-height: 1.6;
        color: #9CA3AF;
        margin-bottom: 22px;
    }


    /* =====================================
       SECTION LABELS
    ===================================== */

    .section-label {
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.14em;
        color: #8E959F;
        text-transform: uppercase;
        margin-top: 8px;
        margin-bottom: 16px;
    }


    /* =====================================
       COLUMNS
    ===================================== */

    [data-testid="column"] {
        padding-left: 0.4rem;
        padding-right: 0.4rem;
    }

    [data-testid="column"]:first-child {
        padding-left: 0;
    }

    [data-testid="column"]:last-child {
        padding-right: 0;
    }


    /* =====================================
       STREAMLIT METRICS
    ===================================== */

    div[data-testid="stMetric"] {
        background-color: #171A21;
        border: 1px solid #292E38;
        border-radius: 10px;
        padding: 18px 20px;
        min-height: 105px;
        box-sizing: border-box;
    }

    div[data-testid="stMetricLabel"] {
        color: #8E959F !important;
        font-size: 11px !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.09em;
    }

    div[data-testid="stMetricValue"] {
        color: #F5F5F5 !important;
        font-size: 25px !important;
        font-weight: 600 !important;
    }


    /* =====================================
       INPUTS
    ===================================== */

    div[data-baseweb="input"] {
        background-color: #171A21;
        border: 1px solid #292E38;
        border-radius: 8px;
        min-height: 42px;
    }

    div[data-baseweb="input"]:focus-within {
        border-color: #D6A85F;
    }

    div[data-baseweb="select"] > div {
        background-color: #171A21;
        border-color: #292E38;
        border-radius: 8px;
    }

    input {
        color: #F5F5F5 !important;
    }


    /* =====================================
       BUTTONS
    ===================================== */

    .stButton > button {
        min-height: 42px;
        border-radius: 8px;
        border: 1px solid #292E38;
        background-color: #171A21;
        color: #F5F5F5;
        font-weight: 600;
    }

    .stButton > button:hover {
        border-color: #D6A85F;
        color: #D6A85F;
    }

    div.stButton > button[kind="primary"] {
        background-color: #D6A85F;
        color: #0F1115;
        border-color: #D6A85F;
    }

    div.stButton > button[kind="primary"]:hover {
        background-color: #E0B873;
        color: #0F1115;
    }


    /* =====================================
       DIVIDERS
    ===================================== */

    hr {
        border-color: #252A32;
        margin-top: 28px;
        margin-bottom: 28px;
    }


    /* =====================================
       TABLE
    ===================================== */

    div[data-testid="stDataFrame"] {
        border: 1px solid #292E38;
        border-radius: 10px;
        overflow: hidden;
        margin-top: 8px;
    }


    /* =====================================
       STATUS
    ===================================== */

    .status-dot {
        display: inline-block;
        width: 7px;
        height: 7px;
        background-color: #7FB069;
        border-radius: 50%;
        margin-right: 7px;
        vertical-align: middle;
    }

    .status-text {
        color: #9CA3AF;
        font-size: 12px;
    }


    /* =====================================
       FOOTER
    ===================================== */

    .footer {
        text-align: center;
        color: #606773;
        font-size: 11px;
        padding-top: 6px;
    }


    /* =====================================
       MOBILE
    ===================================== */

    @media (max-width: 768px) {

        .block-container {
            max-width: 100%;
            padding-left: 1.2rem;
            padding-right: 1.2rem;
            padding-top: 2rem;
        }

        .hero-title {
            font-size: 30px;
        }

        .hero-subtitle {
            font-size: 14px;
        }

    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==========================================
# FASTAPI CONFIGURATION
# ==========================================

API_URL = os.getenv(
    "API_URL",
    "http://127.0.0.1:8000"
)


# ==========================================
# SESSION STATE
# ==========================================

if "prediction_result" not in st.session_state:
    st.session_state.prediction_result = None


# ==========================================
# API FUNCTIONS
# ==========================================

def check_api():

    try:

        response = requests.get(
            API_URL + "/health",
            timeout=5
        )

        if response.status_code == 200:
            return response.json()

        return None

    except requests.RequestException:

        return None


def get_expenses():

    try:

        response = requests.get(
            API_URL + "/expenses",
            timeout=5
        )

        response.raise_for_status()

        data = response.json()

        return pd.DataFrame(
            data.get("expenses", [])
        )

    except requests.RequestException:

        return None


def get_summary():

    try:

        response = requests.get(
            API_URL + "/summary",
            timeout=5
        )

        response.raise_for_status()

        return response.json()

    except requests.RequestException:

        return None


def add_expense(description, amount):

    try:

        response = requests.post(
            API_URL + "/predict",
            json={
                "description": description,
                "amount": amount
            },
            timeout=10
        )

        response.raise_for_status()

        return response.json()

    except requests.HTTPError:

        try:

            detail = response.json().get(
                "detail",
                "Prediction failed."
            )

        except Exception:

            detail = "Prediction failed."

        return {
            "error": detail
        }

    except requests.RequestException:

        return {
            "error": "FastAPI backend could not be reached."
        }


def delete_expense(expense_id):

    try:

        response = requests.delete(
            API_URL + "/expenses/" + str(expense_id),
            timeout=5
        )

        response.raise_for_status()

        return True, ""

    except requests.HTTPError:

        try:

            detail = response.json().get(
                "detail",
                "Unable to delete expense."
            )

        except Exception:

            detail = "Unable to delete expense."

        return False, detail

    except requests.RequestException:

        return False, "FastAPI backend could not be reached."


# ==========================================
# HEADER
# ==========================================

st.markdown(
    '<div class="brand">SMARTSPEND</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="hero-title">'
    'Understand where your money goes.'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="hero-subtitle">'
    'AI-powered expense categorization with a simple '
    'spending dashboard.'
    '</div>',
    unsafe_allow_html=True
)


# ==========================================
# API STATUS
# ==========================================

health = check_api()

if health:

    st.markdown(
        '<span class="status-dot"></span>'
        '<span class="status-text">API connected</span>',
        unsafe_allow_html=True
    )

else:

    st.error(
        "SmartSpend API is unavailable."
    )

    st.info(
        "Start FastAPI with: "
        "`uvicorn app.main:app --reload`"
    )

    st.stop()


st.divider()


# ==========================================
# ADD EXPENSE
# ==========================================

st.markdown(
    '<div class="section-label">Add Expense</div>',
    unsafe_allow_html=True
)

input_col, prediction_col = st.columns(
    [1.25, 0.85],
    gap="medium"
)


# ==========================================
# INPUT SECTION
# ==========================================

with input_col:

    description = st.text_input(
        "Description",
        placeholder="e.g. Lunch at a restaurant"
    )

    amount = st.number_input(
        "Amount (Rs.)",
        min_value=0.0,
        step=50.0,
        format="%.2f"
    )

    predict_clicked = st.button(
        "Predict Expense",
        type="primary",
        use_container_width=True
    )


# ==========================================
# AI PREDICTION SECTION
# ==========================================

with prediction_col:

    st.subheader("AI Prediction")

    if st.session_state.prediction_result is None:

        st.write("Ready")

        st.caption(
            "Enter an expense to get a prediction."
        )

    else:

        prediction = st.session_state.prediction_result

        st.metric(
            "Category",
            prediction["category"]
        )

        st.caption(
            "Confidence: "
            + str(prediction["confidence"])
            + "%"
        )


# ==========================================
# PREDICTION
# ==========================================

if predict_clicked:

    if description.strip() == "":

        st.warning(
            "Please enter an expense description."
        )

    elif amount <= 0:

        st.warning(
            "Please enter an amount greater than 0."
        )

    else:

        result = add_expense(
            description.strip(),
            amount
        )

        if "error" in result:

            st.error(
                result["error"]
            )

        else:

            st.session_state.prediction_result = result

            st.success(
                "Expense added successfully."
            )

            st.rerun()


st.divider()


# ==========================================
# DASHBOARD
# ==========================================

st.markdown(
    '<div class="section-label">Overview</div>',
    unsafe_allow_html=True
)

summary = get_summary()
expenses = get_expenses()


if summary is None or expenses is None:

    st.error(
        "Unable to retrieve dashboard data."
    )

else:

    # ==========================================
    # REFRESH
    # ==========================================

    refresh_col, empty_col = st.columns(
        [1, 6]
    )

    with refresh_col:

        if st.button("Refresh"):

            st.rerun()


    # ==========================================
    # EMPTY STATE
    # ==========================================

    if len(expenses) == 0:

        st.info(
            "No expenses yet. Add your first expense above."
        )

    else:

        # ==========================================
        # SUMMARY VALUES
        # ==========================================

        total_spending = summary.get(
            "total_spending",
            0
        )

        total_expenses = summary.get(
            "total_expenses",
            0
        )

        if total_expenses > 0:

            average_expense = (
                total_spending / total_expenses
            )

        else:

            average_expense = 0


        # ==========================================
        # OVERVIEW METRICS
        # ==========================================

        metric1, metric2, metric3 = st.columns(
            [1, 1, 1],
            gap="medium"
        )

        with metric1:

            st.metric(
                label="Total Spending",
                value="Rs. {:,.2f}".format(
                    total_spending
                )
            )

        with metric2:

            st.metric(
                label="Expenses",
                value=str(total_expenses)
            )

        with metric3:

            st.metric(
                label="Average Expense",
                value="Rs. {:,.2f}".format(
                    average_expense
                )
            )


        st.divider()


        # ==========================================
        # CATEGORY SUMMARY
        # ==========================================

        st.markdown(
            '<div class="section-label">'
            'Spending by Category'
            '</div>',
            unsafe_allow_html=True
        )

        categories = summary.get(
            "categories",
            {}
        )

        if categories:

            category_summary = pd.Series(
                categories,
                dtype="float64"
            )

            category_summary = category_summary.sort_values(
                ascending=False
            )

            st.bar_chart(
                category_summary,
                use_container_width=True
            )

        else:

            st.info(
                "No category information available."
            )


        st.divider()


        # ==========================================
        # EXPENSE HISTORY
        # ==========================================

        st.markdown(
            '<div class="section-label">'
            'Recent Expenses'
            '</div>',
            unsafe_allow_html=True
        )

        display_expenses = expenses.copy()


        # Sequential display number.
        # This is NOT the database ID.

        display_expenses.insert(
            0,
            "No.",
            range(
                1,
                len(display_expenses) + 1
            )
        )


        display_expenses = display_expenses.rename(
            columns={
                "description": "Description",
                "amount": "Amount (Rs.)",
                "category": "Category",
                "confidence": "Confidence"
            }
        )


        display_expenses["Amount (Rs.)"] = (
            display_expenses["Amount (Rs.)"]
            .round(2)
        )


        display_expenses["Confidence"] = (
            display_expenses["Confidence"]
            .round(2)
            .astype(str)
            + "%"
        )


        display_expenses = display_expenses[
            [
                "No.",
                "Description",
                "Amount (Rs.)",
                "Category",
                "Confidence"
            ]
        ]


        st.dataframe(
            display_expenses,
            use_container_width=True,
            hide_index=True
        )


        st.divider()


        # ==========================================
        # DELETE EXPENSE
        # ==========================================

        st.markdown(
            '<div class="section-label">'
            'Manage Expenses'
            '</div>',
            unsafe_allow_html=True
        )

        selected_expense = st.selectbox(
            "Select expense",
            expenses["id"].tolist(),
            format_func=lambda expense_id: (
                str(
                    expenses.loc[
                        expenses["id"] == expense_id,
                        "description"
                    ].iloc[0]
                )
                + " — Rs. "
                + str(
                    expenses.loc[
                        expenses["id"] == expense_id,
                        "amount"
                    ].iloc[0]
                )
            )
        )


        if st.button(
            "Delete Selected Expense"
        ):

            deleted, message = delete_expense(
                selected_expense
            )

            if deleted:

                st.success(
                    "Expense deleted successfully."
                )

                # Clear the displayed prediction after deletion
                st.session_state.prediction_result = None

                st.rerun()

            else:

                st.error(
                    message
                )


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.markdown(
    '<div class="footer">'
    'SmartSpend · FastAPI · Machine Learning · SQLite'
    '</div>',
    unsafe_allow_html=True
)