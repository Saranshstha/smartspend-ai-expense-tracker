# streamlit run app.py

import os
from datetime import datetime

import pandas as pd
import requests
import streamlit as st


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="SmartSpend",
    page_icon="S",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM DESIGN
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       SMARTSPEND COLOR SYSTEM
       ======================================================== */

    :root {
        --sidebar-bg: #101010;
        --page-bg: #151515;

        --card-bg: #1B1B1B;
        --input-bg: #181818;

        --hover-bg: #222222;
        --active-bg: #2D2D2D;

        --border: #303030;
        --border-hover: #444444;

        --text-primary: #FFFFFF;
        --text-secondary: #B8B8B8;
        --text-muted: #777777;
    }


    /* ========================================================
       GLOBAL PAGE
       ======================================================== */

    .stApp {
        background-color: var(--page-bg);
        color: var(--text-primary);
    }

    .main {
        background-color: var(--page-bg);
    }

    .block-container {
        width: 100%;
        max-width: 1400px;
        margin: 0 auto;
        padding: 2.5rem 3.5rem 4rem;

        transition:
            max-width 0.2s ease,
            padding 0.2s ease;
    }

    header[data-testid="stHeader"] {
        background: transparent;
    }


    /* ========================================================
       SIDEBAR
       ======================================================== */

    section[data-testid="stSidebar"] {

        width: 260px !important;
        min-width: 260px !important;

        background-color: var(--sidebar-bg);

        border-right: 1px solid #292929;
    }

    section[data-testid="stSidebar"] > div {

        padding-top: 0.8rem;
        padding-bottom: 1rem;
    }

    section[data-testid="stSidebar"] .block-container {

        padding: 0.8rem 0.85rem 1rem;
    }


    /* ========================================================
       SIDEBAR BRAND
       ======================================================== */

    .sidebar-brand {

        font-size: 12px;

        font-weight: 750;

        letter-spacing: 0.17em;

        color: var(--text-primary);

        margin:
            0.8rem
            0
            1.65rem
            0.35rem;
    }


    /* ========================================================
       SIDEBAR SECTION LABEL
       ======================================================== */

    .sidebar-section {

        font-size: 10px;

        font-weight: 700;

        letter-spacing: 0.14em;

        color: var(--text-muted);

        text-transform: uppercase;

        margin:
            1.25rem
            0
            0.55rem
            0.35rem;
    }


    /* ========================================================
       SIDEBAR NAVIGATION BUTTONS
       ======================================================== */

    section[data-testid="stSidebar"] div.stButton {

        width: 100%;

        margin-bottom: 0.25rem;
    }

    section[data-testid="stSidebar"] div.stButton > button {

        width: 100%;

        min-height: 40px;

        padding:
            0.45rem
            0.75rem;

        border-radius: 9px;

        border: 1px solid transparent;

        background: transparent;

        color: var(--text-secondary);

        font-size: 0.9rem;

        font-weight: 500;

        display: flex;

        align-items: center;

        justify-content: flex-start;

        text-align: left;

        transition:
            background-color 0.18s ease,
            border-color 0.18s ease,
            color 0.18s ease,
            transform 0.18s ease,
            box-shadow 0.18s ease;
    }


    /* ========================================================
       FORCE SIDEBAR BUTTON CONTENT LEFT
       ======================================================== */

    section[data-testid="stSidebar"]
    div.stButton > button > div {

        width: 100%;

        display: flex;

        align-items: center;

        justify-content: flex-start;

        text-align: left;
    }

    section[data-testid="stSidebar"]
    div.stButton > button p {

        width: 100%;

        margin: 0;

        text-align: left;
    }


    /* ========================================================
       SIDEBAR HOVER
       ======================================================== */

    section[data-testid="stSidebar"]
    div.stButton > button:hover {

        background-color: var(--hover-bg);

        border-color: var(--active-bg);

        color: var(--text-primary);

        transform: translateX(3px);

        box-shadow:
            0 4px 16px rgba(0, 0, 0, 0.22);
    }

    section[data-testid="stSidebar"]
    div.stButton > button:active {

        transform:
            translateX(2px)
            scale(0.99);
    }


    /* ========================================================
       ACTIVE SIDEBAR BUTTON
       ======================================================== */

    section[data-testid="stSidebar"]
    div.stButton > button[kind="primary"] {

        background-color: var(--active-bg);

        border-color: #3A3A3A;

        color: var(--text-primary);

        font-weight: 600;

        box-shadow:
            inset 0 0 0 1px
            rgba(255, 255, 255, 0.02),

            0 3px 12px
            rgba(0, 0, 0, 0.25);
    }

    section[data-testid="stSidebar"]
    div.stButton > button[kind="primary"]:hover {

        background-color: #363636;

        border-color: #454545;

        color: var(--text-primary);

        transform: translateX(3px);
    }


    /* ========================================================
       SIDEBAR INFORMATION
       ======================================================== */

    .sidebar-info {

        color: #6F6F6F;

        font-size: 11px;

        line-height: 1.55;

        margin:
            2.2rem
            0.35rem
            0;

        padding-top: 1rem;

        border-top:
            1px solid #242424;
    }


    /* ========================================================
       SIDEBAR COLLAPSE BUTTON
       ======================================================== */

    section[data-testid="stSidebar"]
    button[data-testid="stSidebarCollapseButton"] {

        width: 36px;

        height: 36px;

        border-radius: 8px;

        transition:
            background-color 0.18s ease,
            transform 0.18s ease;
    }

    section[data-testid="stSidebar"]
    button[data-testid="stSidebarCollapseButton"]:hover {

        background-color: var(--hover-bg);

        transform: scale(1.05);
    }


    /* ========================================================
       MAIN BRAND
       ======================================================== */

    .brand {

        font-size: 11px;

        font-weight: 700;

        letter-spacing: 0.16em;

        color: var(--text-primary);

        margin-bottom: 12px;
    }


    /* ========================================================
       HERO TITLE
       ======================================================== */

    .hero-title {

        font-size:
            clamp(
                2.25rem,
                4vw,
                3.25rem
            );

        font-weight: 700;

        line-height: 1.08;

        color: var(--text-primary);

        margin-bottom: 12px;
    }


    /* ========================================================
       HERO SUBTITLE
       ======================================================== */

    .hero-subtitle {

        max-width: 680px;

        font-size: 1rem;

        line-height: 1.7;

        color: var(--text-secondary);

        margin-bottom: 20px;
    }


    /* ========================================================
       SECTION LABELS
       ======================================================== */

    .section-label {

        font-size: 11px;

        font-weight: 700;

        letter-spacing: 0.14em;

        color: var(--text-secondary);

        text-transform: uppercase;

        margin-top: 10px;

        margin-bottom: 18px;
    }


    /* ========================================================
       COLUMNS
       ======================================================== */

    [data-testid="column"] {

        padding-left: 0.5rem;

        padding-right: 0.5rem;
    }

    [data-testid="column"]:first-child {

        padding-left: 0;
    }

    [data-testid="column"]:last-child {

        padding-right: 0;
    }


    /* ========================================================
       METRIC CARDS
       ======================================================== */

    div[data-testid="stMetric"] {

        background: var(--card-bg);

        border:
            1px solid var(--border);

        border-radius: 14px;

        padding:
            20px
            22px;

        min-height: 112px;

        box-sizing: border-box;

        transition:
            border-color 0.2s ease,
            transform 0.2s ease,
            box-shadow 0.2s ease;
    }

    div[data-testid="stMetric"]:hover {

        border-color: var(--border-hover);

        transform: translateY(-2px);

        box-shadow:
            0 8px 24px
            rgba(0, 0, 0, 0.22);
    }

    div[data-testid="stMetricLabel"] {

        color: #A8A8A8 !important;

        font-size: 11px !important;

        font-weight: 600 !important;

        text-transform: uppercase;

        letter-spacing: 0.09em;
    }

    div[data-testid="stMetricValue"] {

        color: var(--text-primary) !important;

        font-size: 1.7rem !important;

        font-weight: 700 !important;
    }


    /* ========================================================
       INPUT FIELDS
       ======================================================== */

    div[data-baseweb="input"] {

        background-color: var(--input-bg);

        border:
            1px solid #383838;

        border-radius: 10px;

        min-height: 46px;

        transition:
            border-color 0.18s ease,
            box-shadow 0.18s ease;
    }

    div[data-baseweb="input"]:focus-within {

        border-color: #E5E5E5;

        box-shadow:
            0 0 0 3px
            rgba(255, 255, 255, 0.10);
    }

    div[data-baseweb="select"] > div {

        background-color: var(--input-bg);

        border-color: #383838;

        border-radius: 10px;
    }

    input {

        color: var(--text-primary) !important;
    }

    textarea {

        color: var(--text-primary) !important;
    }

    label[data-testid="stWidgetLabel"] p {

        color: #D4D4D4 !important;

        font-size: 0.9rem;

        font-weight: 600;
    }


    /* ========================================================
       NUMBER INPUT / SELECT TEXT
       ======================================================== */

    div[data-baseweb="input"] input {

        background-color: transparent;

        color: var(--text-primary) !important;
    }

    div[data-baseweb="select"] {

        color: var(--text-primary);
    }


    /* ========================================================
       MAIN BUTTONS
       ======================================================== */

    .stButton > button {

        min-height: 44px;

        border-radius: 10px;

        border:
            1px solid #3C3C3C;

        background-color: #1A1A1A;

        color: #F5F5F5;

        font-weight: 600;

        padding:
            0.4rem
            1rem;

        transition:
            background-color 0.18s ease,
            border-color 0.18s ease,
            color 0.18s ease,
            transform 0.18s ease,
            box-shadow 0.18s ease;
    }

    .stButton > button:hover {

        border-color: #707070;

        background-color: #252525;

        color: #FFFFFF;

        transform: translateY(-1px);

        box-shadow:
            0 5px 16px
            rgba(0, 0, 0, 0.18);
    }

    .stButton > button:active {

        transform:
            translateY(0)
            scale(0.99);
    }


    /* ========================================================
       PRIMARY BUTTON
       ======================================================== */

    div.stButton > button[kind="primary"] {

        background-color: #FFFFFF;

        color: #0A0A0A;

        border-color: #FFFFFF;
    }

    div.stButton > button[kind="primary"]:hover {

        background-color: #E5E5E5;

        border-color: #E5E5E5;

        color: #0A0A0A;
    }


    /* ========================================================
       SECONDARY BUTTON
       ======================================================== */

    div.stButton > button[kind="secondary"] {

        background-color: #1A1A1A;

        color: #F5F5F5;

        border-color: #3C3C3C;
    }


    /* ========================================================
       DIVIDERS
       ======================================================== */

    hr {

        border-color: #2B2B2B;

        margin-top: 32px;

        margin-bottom: 32px;
    }


    /* ========================================================
       DATAFRAME
       ======================================================== */

    div[data-testid="stDataFrame"] {

        border:
            1px solid var(--border);

        border-radius: 14px;

        overflow: hidden;

        margin-top: 10px;

        background-color: #171717;
    }

    [data-testid="stDataFrame"] [role="grid"] {

        font-size: 0.9rem;
    }


    /* ========================================================
       DATA EDITOR
       ======================================================== */

    div[data-testid="stDataEditor"] {

        border:
            1px solid var(--border);

        border-radius: 14px;

        overflow: hidden;

        background-color: #171717;
    }


    /* ========================================================
       CHARTS
       ======================================================== */

    [data-testid="stArrowVegaLiteChart"],
    [data-testid="stVegaLiteChart"] {

        background-color: #171717;

        border:
            1px solid var(--border);

        border-radius: 14px;

        padding: 0.7rem;
    }


    /* ========================================================
       STATUS
       ======================================================== */

    .status-dot {

        display: inline-block;

        width: 7px;

        height: 7px;

        background-color: #FFFFFF;

        border-radius: 50%;

        margin-right: 7px;

        vertical-align: middle;
    }

    .status-text {

        color: var(--text-secondary);

        font-size: 12px;
    }


    /* ========================================================
       ALERTS
       ======================================================== */

    div[data-testid="stAlert"] {

        background-color: var(--card-bg);

        border-radius: 12px;

        border:
            1px solid #383838;

        color: var(--text-primary);
    }


    /* ========================================================
       EXPANDERS
       ======================================================== */

    div[data-testid="stExpander"] {

        background-color: var(--card-bg);

        border:
            1px solid var(--border);

        border-radius: 12px;
    }


    /* ========================================================
       SELECTBOX / DROPDOWN
       ======================================================== */

    div[data-baseweb="popover"] {

        background-color: #181818;
    }

    div[data-baseweb="menu"] {

        background-color: #181818;

        border:
            1px solid #303030;
    }

    div[data-baseweb="menu"] li {

        color: #FFFFFF;
    }

    div[data-baseweb="menu"] li:hover {

        background-color: #2D2D2D;
    }


    /* ========================================================
       SLIDER
       ======================================================== */

    div[data-testid="stSlider"] {

        color: var(--text-primary);
    }


    /* ========================================================
       CAPTION
       ======================================================== */

    .stCaption {

        color: #888888 !important;
    }


    /* ========================================================
       FOOTER
       ======================================================== */

    .footer {

        text-align: center;

        color: var(--text-muted);

        font-size: 11px;

        padding-top: 10px;
    }


    /* ========================================================
       MOBILE
       ======================================================== */

    @media (max-width: 768px) {

        .block-container {

            width: 100%;

            max-width: 100%;

            padding:
                1.75rem
                1.2rem
                2.5rem;
        }

        .hero-title {

            font-size: 2.25rem;
        }

        .hero-subtitle {

            font-size: 14px;
        }

        section[data-testid="stSidebar"] {

            width: 240px !important;

            min-width: 240px !important;
        }
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# FASTAPI CONFIGURATION
# ============================================================

API_URL = os.getenv(
    "API_URL",
    "http://127.0.0.1:8000"
)


# ============================================================
# SESSION STATE
# ============================================================

if "prediction_result" not in st.session_state:

    st.session_state.prediction_result = None


if "clear_inputs" not in st.session_state:

    st.session_state.clear_inputs = False


if "confirm_delete" not in st.session_state:

    st.session_state.confirm_delete = False


if "selected_page" not in st.session_state:

    st.session_state.selected_page = "Dashboard"


# ============================================================
# CLEAR INPUTS AFTER SUCCESSFUL PREDICTION
# ============================================================

if st.session_state.clear_inputs:

    st.session_state.description_input = ""

    st.session_state.amount_input = 0.0

    st.session_state.clear_inputs = False


# ============================================================
# API FUNCTIONS
# ============================================================

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
            data.get(
                "expenses",
                []
            )
        )

    except requests.RequestException:

        return None


def get_deleted_expenses():

    try:

        response = requests.get(
            API_URL + "/expenses/deleted",
            timeout=5
        )

        response.raise_for_status()

        return pd.DataFrame(
            response.json().get(
                "expenses",
                []
            )
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


def add_expense(
    description,
    amount
):

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
            "error":
                "FastAPI backend could not be reached."
        }


def save_table_changes(
    expenses
):

    try:

        response = requests.put(
            API_URL + "/expenses/update-table",
            json={
                "expenses": expenses
            },
            timeout=15
        )

        response.raise_for_status()

        return True, response.json()

    except requests.HTTPError:

        try:

            detail = response.json().get(
                "detail",
                "Unable to update expenses."
            )

        except Exception:

            detail = "Unable to update expenses."

        return False, detail

    except requests.RequestException:

        return (
            False,
            "FastAPI backend could not be reached."
        )


def get_monthly_analytics(
    year,
    month
):

    try:

        response = requests.get(
            API_URL + "/analytics/monthly",
            params={
                "year": year,
                "month": month
            },
            timeout=5
        )

        response.raise_for_status()

        return response.json()

    except requests.RequestException:

        return None


def get_weekly_analytics():

    try:

        response = requests.get(
            API_URL + "/analytics/weekly",
            timeout=5
        )

        response.raise_for_status()

        return response.json()

    except requests.RequestException:

        return None


def get_monthly_trend(
    months=6
):

    try:

        response = requests.get(
            API_URL + "/analytics/trend",
            params={
                "months": months
            },
            timeout=5
        )

        response.raise_for_status()

        return response.json()

    except requests.RequestException:

        return None


def get_monthly_comparison(
    year,
    month
):

    try:

        response = requests.get(
            API_URL + "/analytics/comparison",
            params={
                "year": year,
                "month": month
            },
            timeout=5
        )

        response.raise_for_status()

        return response.json()

    except requests.RequestException:

        return None


def delete_expense(
    expense_id
):

    try:

        response = requests.delete(
            API_URL
            + "/expenses/"
            + str(expense_id),
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

        return (
            False,
            "FastAPI backend could not be reached."
        )


def restore_expense(
    expense_id
):

    try:

        response = requests.post(
            API_URL
            + "/expenses/"
            + str(expense_id)
            + "/restore",
            timeout=5
        )

        response.raise_for_status()

        return True, ""

    except requests.HTTPError:

        try:

            detail = response.json().get(
                "detail",
                "Unable to restore expense."
            )

        except Exception:

            detail = "Unable to restore expense."

        return False, detail

    except requests.RequestException:

        return (
            False,
            "FastAPI backend could not be reached."
        )


# ============================================================
# HEADER
# ============================================================

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
    'AI-powered expense categorization with intelligent '
    'spending analytics.'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# API STATUS
# ============================================================

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


# ============================================================
# SIDEBAR NAVIGATION
# ============================================================

with st.sidebar:

    st.markdown(
        '<div class="sidebar-brand">'
        'SMARTSPEND'
        '</div>',
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # MAIN
    # --------------------------------------------------------

    st.markdown(
        '<div class="sidebar-section">Main</div>',
        unsafe_allow_html=True
    )


    navigation_items = [
        ("Dashboard", "⌂"),
        ("Add Expense", "＋"),
        ("Expenses", "▤"),
        ("Analytics", "◫")
    ]


    for page_name, icon in navigation_items:

        is_selected = (
            st.session_state.selected_page
            == page_name
        )

        button_type = (
            "primary"
            if is_selected
            else "secondary"
        )


        if st.button(
            icon + "  " + page_name,
            use_container_width=True,
            type=button_type,
            key=(
                "sidebar_"
                + page_name.lower()
                .replace(" ", "_")
            )
        ):

            st.session_state.selected_page = page_name

            st.session_state.confirm_delete = False

            st.rerun()


    # --------------------------------------------------------
    # MANAGE
    # --------------------------------------------------------

    st.markdown(
        '<div class="sidebar-section">Manage</div>',
        unsafe_allow_html=True
    )


    page_name = "Recently Deleted"

    is_selected = (
        st.session_state.selected_page
        == page_name
    )

    button_type = (
        "primary"
        if is_selected
        else "secondary"
    )


    if st.button(
        "↶  Recently Deleted",
        use_container_width=True,
        type=button_type,
        key="sidebar_recently_deleted"
    ):

        st.session_state.selected_page = (
            page_name
        )

        st.session_state.confirm_delete = False

        st.rerun()


    # --------------------------------------------------------
    # SIDEBAR INFORMATION
    # --------------------------------------------------------

    st.markdown(
        '<div class="sidebar-info">'
        'SmartSpend<br>'
        'AI Expense Management'
        '</div>',
        unsafe_allow_html=True
    )


# ============================================================
# CURRENT PAGE
# ============================================================

page = st.session_state.selected_page


# ============================================================
# DASHBOARD
# ============================================================

if page == "Dashboard":

    st.markdown(
        '<div class="section-label">'
        'Overview'
        '</div>',
        unsafe_allow_html=True
    )

    summary = get_summary()

    expenses = get_expenses()


    if summary is None or expenses is None:

        st.error(
            "Unable to retrieve dashboard data."
        )


    elif len(expenses) == 0:

        st.info(
            "No expenses yet. Add your first expense."
        )


    else:

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
                total_spending
                / total_expenses
            )

        else:

            average_expense = 0


        # ----------------------------------------------------
        # METRICS
        # ----------------------------------------------------

        metric1, metric2, metric3 = st.columns(
            3,
            gap="medium"
        )


        with metric1:

            st.metric(
                "Total Spending",
                "Rs. {:,.2f}".format(
                    total_spending
                )
            )


        with metric2:

            st.metric(
                "Expenses",
                str(
                    total_expenses
                )
            )


        with metric3:

            st.metric(
                "Average Expense",
                "Rs. {:,.2f}".format(
                    average_expense
                )
            )


        st.divider()


        # ----------------------------------------------------
        # SPENDING BY CATEGORY
        # ----------------------------------------------------

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
            ).sort_values(
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


        # ----------------------------------------------------
        # RECENT EXPENSES
        # ----------------------------------------------------

        st.markdown(
            '<div class="section-label">'
            'Recent Expenses'
            '</div>',
            unsafe_allow_html=True
        )


        recent = expenses.copy().head(
            8
        )


        recent = recent.rename(
            columns={
                "description": "Description",
                "amount": "Amount (Rs.)",
                "category": "Category",
                "confidence": "Confidence",
                "created_at": "Date"
            }
        )


        recent["Amount (Rs.)"] = (
            recent["Amount (Rs.)"]
            .round(2)
        )


        recent["Confidence"] = (
            recent["Confidence"]
            .round(2)
            .astype(str)
            + "%"
        )


        recent["Date"] = pd.to_datetime(
            recent["Date"],
            errors="coerce"
        ).dt.strftime(
            "%Y-%m-%d %H:%M"
        )


        st.dataframe(
            recent[
                [
                    "Description",
                    "Amount (Rs.)",
                    "Category",
                    "Confidence",
                    "Date"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# ADD EXPENSE
# ============================================================

elif page == "Add Expense":

    st.markdown(
        '<div class="section-label">'
        'Add Expense'
        '</div>',
        unsafe_allow_html=True
    )


    input_col, prediction_col = st.columns(
        [1.25, 0.85],
        gap="medium"
    )


    # --------------------------------------------------------
    # INPUT
    # --------------------------------------------------------

    with input_col:

        description = st.text_input(
            "Description",
            placeholder="e.g. Lunch at a restaurant",
            key="description_input"
        )


        amount = st.number_input(
            "Amount (Rs.)",
            min_value=0.0,
            step=50.0,
            format="%.2f",
            key="amount_input"
        )


        predict_clicked = st.button(
            "Predict Expense",
            type="primary",
            use_container_width=True,
            key="predict_expense_button"
        )


    # --------------------------------------------------------
    # AI PREDICTION
    # --------------------------------------------------------

    with prediction_col:

        st.subheader(
            "AI Prediction"
        )


        if st.session_state.prediction_result is None:

            st.write(
                "Ready"
            )


            st.caption(
                "Enter an expense to get a prediction."
            )


        else:

            prediction = (
                st.session_state.prediction_result
            )


            st.metric(
                "Category",
                prediction["category"]
            )


            st.caption(
                "Confidence: "
                + str(
                    prediction["confidence"]
                )
                + "%"
            )


            if prediction.get(
                "created_at"
            ):

                st.caption(
                    "Saved: "
                    + prediction[
                        "created_at"
                    ].replace(
                        "T",
                        " "
                    )
                )


    # --------------------------------------------------------
    # PREDICTION
    # --------------------------------------------------------

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

                st.session_state.clear_inputs = True

                st.success(
                    "Expense added successfully."
                )

                st.rerun()


# ============================================================
# EXPENSES
# ============================================================

elif page == "Expenses":

    st.markdown(
        '<div class="section-label">'
        'Expense History'
        '</div>',
        unsafe_allow_html=True
    )


    expenses = get_expenses()


    if expenses is None:

        st.error(
            "Unable to retrieve expenses."
        )


    elif len(expenses) == 0:

        st.info(
            "No expenses have been recorded yet."
        )


    else:

        # ----------------------------------------------------
        # SEARCH
        # ----------------------------------------------------

        search = st.text_input(
            "Search expenses",
            placeholder="Search by description or category",
            key="expense_search_input"
        )


        # ----------------------------------------------------
        # CATEGORY FILTER
        # ----------------------------------------------------

        categories = [
            "All"
        ] + sorted(
            expenses[
                "category"
            ]
            .dropna()
            .unique()
            .tolist()
        )


        selected_category = st.selectbox(
            "Category",
            categories,
            key="expense_category_filter"
        )


        # ----------------------------------------------------
        # FILTER DATA
        # ----------------------------------------------------

        filtered = expenses.copy()


        if search.strip():

            search_lower = (
                search.strip()
                .lower()
            )


            filtered = filtered[
                filtered[
                    "description"
                ]
                .astype(str)
                .str.lower()
                .str.contains(
                    search_lower,
                    na=False,
                    regex=False
                )
                |
                filtered[
                    "category"
                ]
                .astype(str)
                .str.lower()
                .str.contains(
                    search_lower,
                    na=False,
                    regex=False
                )
            ]


        if selected_category != "All":

            filtered = filtered[
                filtered[
                    "category"
                ]
                == selected_category
            ]


        # ----------------------------------------------------
        # EXPENSE TABLE
        # ----------------------------------------------------

        if len(filtered) == 0:

            st.info(
                "No expenses match your current search/filter."
            )


        else:

            st.caption(
                "Edit the Description or Amount directly "
                "in the table. Category and Confidence are "
                "generated by the AI model."
            )


            editable_table = filtered[
                [
                    "id",
                    "description",
                    "amount",
                    "category",
                    "confidence",
                    "created_at"
                ]
            ].copy()


            editable_table = (
                editable_table
                .rename(
                    columns={
                        "id": "ID",
                        "description": "Description",
                        "amount": "Amount (Rs.)",
                        "category": "Category",
                        "confidence": "Confidence (%)",
                        "created_at": "Date"
                    }
                )
            )


            editable_table[
                "Amount (Rs.)"
            ] = editable_table[
                "Amount (Rs.)"
            ].round(2)


            editable_table[
                "Confidence (%)"
            ] = editable_table[
                "Confidence (%)"
            ].round(2)


            editable_table[
                "Date"
            ] = pd.to_datetime(
                editable_table[
                    "Date"
                ],
                errors="coerce"
            ).dt.strftime(
                "%Y-%m-%d %H:%M"
            )


            # ------------------------------------------------
            # EDITABLE TABLE
            # ------------------------------------------------

            edited_table = st.data_editor(
                editable_table,
                use_container_width=True,
                hide_index=True,
                num_rows="fixed",
                disabled=[
                    "ID",
                    "Category",
                    "Confidence (%)",
                    "Date"
                ],
                column_config={

                    "ID": st.column_config.NumberColumn(
                        "ID",
                        disabled=True
                    ),

                    "Description": st.column_config.TextColumn(
                        "Description",
                        required=True
                    ),

                    "Amount (Rs.)": st.column_config.NumberColumn(
                        "Amount (Rs.)",
                        min_value=0.01,
                        step=50.0,
                        format="%.2f",
                        required=True
                    ),

                    "Category": st.column_config.TextColumn(
                        "Category",
                        disabled=True
                    ),

                    "Confidence (%)": st.column_config.NumberColumn(
                        "Confidence (%)",
                        format="%.2f",
                        disabled=True
                    ),

                    "Date": st.column_config.TextColumn(
                        "Date",
                        disabled=True
                    )
                },
                key="expense_editor"
            )


            st.markdown("")


            # ------------------------------------------------
            # SAVE CHANGES
            # ------------------------------------------------

            if st.button(
                "Save Changes",
                type="primary",
                use_container_width=True,
                key="save_table_changes_button"
            ):

                update_payload = []

                validation_error = None


                for _, row in edited_table.iterrows():

                    description_value = str(
                        row["Description"]
                    ).strip()


                    try:

                        amount_value = float(
                            row["Amount (Rs.)"]
                        )

                    except Exception:

                        validation_error = (
                            "Amount must be a valid number."
                        )

                        break


                    if description_value == "":

                        validation_error = (
                            "Description cannot be empty."
                        )

                        break


                    if len(description_value) < 2:

                        validation_error = (
                            "Description must contain "
                            "at least 2 characters."
                        )

                        break


                    if amount_value <= 0:

                        validation_error = (
                            "Amount must be greater than 0."
                        )

                        break


                    update_payload.append(
                        {
                            "id": int(
                                row["ID"]
                            ),
                            "description": description_value,
                            "amount": amount_value
                        }
                    )


                if validation_error:

                    st.error(
                        validation_error
                    )


                else:

                    success, result = (
                        save_table_changes(
                            update_payload
                        )
                    )


                    if success:

                        st.success(
                            "Expenses updated successfully."
                        )

                        st.info(
                            "Descriptions changed in the table "
                            "were automatically re-categorized "
                            "by the AI model."
                        )

                        st.rerun()


                    else:

                        st.error(
                            result
                        )


        st.divider()


        # ----------------------------------------------------
        # DELETE EXPENSE
        # ----------------------------------------------------

        st.markdown(
            '<div class="section-label">'
            'Delete Expense'
            '</div>',
            unsafe_allow_html=True
        )


        delete_lookup = (
            expenses
            .set_index("id")
            .to_dict("index")
        )


        selected_delete_id = st.selectbox(
            "Select expense to delete",
            expenses[
                "id"
            ].tolist(),
            format_func=lambda expense_id: (
                str(
                    delete_lookup[
                        expense_id
                    ][
                        "description"
                    ]
                )
                + " — Rs. "
                + format(
                    float(
                        delete_lookup[
                            expense_id
                        ][
                            "amount"
                        ]
                    ),
                    ".2f"
                )
            ),
            key="delete_expense_selector"
        )


        if st.button(
            "Delete Selected Expense",
            key="delete_expense_button"
        ):

            st.session_state.confirm_delete = True


        if st.session_state.confirm_delete:

            st.warning(
                "Are you sure you want to delete this expense?"
            )


            confirm_col, cancel_col = st.columns(
                2,
                gap="medium"
            )


            with confirm_col:

                if st.button(
                    "Yes, Delete",
                    type="primary",
                    use_container_width=True,
                    key="confirm_delete_button"
                ):

                    deleted, message = (
                        delete_expense(
                            selected_delete_id
                        )
                    )


                    if deleted:

                        st.session_state.confirm_delete = False

                        st.session_state.prediction_result = None

                        st.success(
                            "Expense moved to Recently Deleted."
                        )

                        st.rerun()


                    else:

                        st.error(
                            message
                        )


            with cancel_col:

                if st.button(
                    "Cancel",
                    use_container_width=True,
                    key="cancel_delete_button"
                ):

                    st.session_state.confirm_delete = False

                    st.rerun()


# ============================================================
# RECENTLY DELETED
# ============================================================

elif page == "Recently Deleted":

    st.markdown(
        '<div class="section-label">'
        'Recently Deleted'
        '</div>',
        unsafe_allow_html=True
    )


    st.caption(
        "Deleted expenses can be restored for up to 15 days."
    )


    deleted_expenses = get_deleted_expenses()


    if deleted_expenses is None:

        st.error(
            "Unable to retrieve deleted expenses."
        )


    elif deleted_expenses.empty:

        st.info(
            "No deleted expenses are available."
        )


    else:

        # ----------------------------------------------------
        # DATE PROCESSING
        # ----------------------------------------------------

        deleted_expenses[
            "deleted_at"
        ] = pd.to_datetime(
            deleted_expenses[
                "deleted_at"
            ],
            utc=True,
            errors="coerce"
        )


        now = pd.Timestamp.now(
            tz="UTC"
        )


        deleted_expenses[
            "Days remaining"
        ] = deleted_expenses[
            "deleted_at"
        ].apply(
            lambda deleted_at: max(
                0,
                int(
                    (
                        deleted_at
                        + pd.Timedelta(days=15)
                        - now
                    ).total_seconds()
                    // 86400
                )
                + 1
            )
            if pd.notna(deleted_at)
            else 0
        )


        deleted_expenses[
            "Deleted on"
        ] = (
            deleted_expenses[
                "deleted_at"
            ]
            .dt.tz_convert(
                "Asia/Kathmandu"
            )
            .dt.strftime(
                "%Y-%m-%d %H:%M"
            )
        )


        # ----------------------------------------------------
        # METRICS
        # ----------------------------------------------------

        total_deleted = len(
            deleted_expenses
        )


        total_deleted_amount = (
            deleted_expenses[
                "amount"
            ]
            .sum()
        )


        metric1, metric2 = st.columns(
            2,
            gap="medium"
        )


        with metric1:

            st.metric(
                "Deleted Expenses",
                str(
                    total_deleted
                )
            )


        with metric2:

            st.metric(
                "Deleted Amount",
                "Rs. {:,.2f}".format(
                    total_deleted_amount
                )
            )


        st.divider()


        # ----------------------------------------------------
        # DELETED TABLE
        # ----------------------------------------------------

        display_deleted = deleted_expenses[
            [
                "description",
                "amount",
                "category",
                "Deleted on",
                "Days remaining"
            ]
        ].copy()


        display_deleted = display_deleted.rename(
            columns={
                "description": "Description",
                "amount": "Amount (Rs.)",
                "category": "Category"
            }
        )


        display_deleted[
            "Amount (Rs.)"
        ] = display_deleted[
            "Amount (Rs.)"
        ].round(2)


        st.dataframe(
            display_deleted,
            use_container_width=True,
            hide_index=True
        )


        st.divider()


        # ----------------------------------------------------
        # RESTORE
        # ----------------------------------------------------

        deleted_lookup = (
            deleted_expenses
            .set_index("id")
            .to_dict("index")
        )


        restore_id = st.selectbox(
            "Select expense to restore",
            deleted_expenses[
                "id"
            ].tolist(),
            format_func=lambda expense_id: (
                str(
                    deleted_lookup[
                        expense_id
                    ][
                        "description"
                    ]
                )
                + " — Rs. "
                + format(
                    float(
                        deleted_lookup[
                            expense_id
                        ][
                            "amount"
                        ]
                    ),
                    ".2f"
                )
            ),
            key="restore_expense_selector"
        )


        if st.button(
            "Restore Selected Expense",
            type="primary",
            use_container_width=True,
            key="restore_expense_button"
        ):

            restored, message = (
                restore_expense(
                    restore_id
                )
            )


            if restored:

                st.success(
                    "Expense restored successfully."
                )

                st.rerun()


            else:

                st.error(
                    message
                )


# ============================================================
# ANALYTICS
# ============================================================

elif page == "Analytics":

    st.markdown(
        '<div class="section-label">'
        'Spending Analytics'
        '</div>',
        unsafe_allow_html=True
    )


    now = datetime.now()


    # --------------------------------------------------------
    # SELECTORS
    # --------------------------------------------------------

    selector_col1, selector_col2, selector_col3 = (
        st.columns(
            3,
            gap="medium"
        )
    )


    with selector_col1:

        selected_year = st.number_input(
            "Year",
            min_value=2000,
            max_value=2100,
            value=now.year,
            step=1,
            key="analytics_year"
        )


    with selector_col2:

        selected_month = st.selectbox(
            "Month",
            list(range(1, 13)),
            index=now.month - 1,
            format_func=lambda value: datetime(
                2000,
                value,
                1
            ).strftime(
                "%B"
            ),
            key="analytics_month"
        )


    with selector_col3:

        trend_months = st.selectbox(
            "Trend period",
            [
                3,
                6,
                12
            ],
            index=1,
            key="analytics_trend_period"
        )


    # --------------------------------------------------------
    # GET ANALYTICS
    # --------------------------------------------------------

    monthly = get_monthly_analytics(
        int(selected_year),
        int(selected_month)
    )


    weekly = get_weekly_analytics()


    trend = get_monthly_trend(
        int(trend_months)
    )


    comparison = get_monthly_comparison(
        int(selected_year),
        int(selected_month)
    )


    # ========================================================
    # WEEKLY ANALYTICS
    # ========================================================

    if weekly is None:

        st.warning(
            "Weekly analytics are currently unavailable."
        )


    else:

        st.markdown(
            '<div class="section-label">'
            'This Week'
            '</div>',
            unsafe_allow_html=True
        )


        week_start = weekly.get(
            "week_start"
        )


        week_end = weekly.get(
            "week_end"
        )


        if week_start and week_end:

            try:

                start_date = pd.to_datetime(
                    week_start
                ).strftime(
                    "%d %b %Y"
                )


                end_date = pd.to_datetime(
                    week_end
                ).strftime(
                    "%d %b %Y"
                )


                st.caption(
                    "Monday, "
                    + start_date
                    + " — Sunday, "
                    + end_date
                )


            except Exception:

                pass


        # ----------------------------------------------------
        # WEEKLY METRICS
        # ----------------------------------------------------

        weekly_metric1, weekly_metric2, weekly_metric3 = (
            st.columns(
                3,
                gap="medium"
            )
        )


        with weekly_metric1:

            st.metric(
                "Weekly Spending",
                "Rs. {:,.2f}".format(
                    weekly.get(
                        "total_spending",
                        0
                    )
                )
            )


        with weekly_metric2:

            st.metric(
                "Transactions",
                str(
                    weekly.get(
                        "total_expenses",
                        0
                    )
                )
            )


        with weekly_metric3:

            st.metric(
                "Average Expense",
                "Rs. {:,.2f}".format(
                    weekly.get(
                        "average_expense",
                        0
                    )
                )
            )


        st.divider()


        # ----------------------------------------------------
        # WEEKLY CHARTS
        # ----------------------------------------------------

        weekly_chart_col1, weekly_chart_col2 = (
            st.columns(
                2,
                gap="medium"
            )
        )


        with weekly_chart_col1:

            st.markdown(
                '<div class="section-label">'
                'Weekly Category Breakdown'
                '</div>',
                unsafe_allow_html=True
            )


            weekly_categories = weekly.get(
                "categories",
                {}
            )


            if weekly_categories:

                weekly_category_series = pd.Series(
                    weekly_categories,
                    dtype="float64"
                ).sort_values(
                    ascending=False
                )


                st.bar_chart(
                    weekly_category_series,
                    horizontal=True,
                    use_container_width=True,
                    height=max(
                        220,
                        len(
                            weekly_category_series
                        ) * 55
                    )
                )


            else:

                st.info(
                    "No spending recorded this week."
                )


        with weekly_chart_col2:

            st.markdown(
                '<div class="section-label">'
                'Daily Spending'
                '</div>',
                unsafe_allow_html=True
            )


            weekly_daily = pd.DataFrame(
                weekly.get(
                    "daily_spending",
                    []
                )
            )


            if not weekly_daily.empty:

                weekly_daily["date"] = (
                    pd.to_datetime(
                        weekly_daily[
                            "date"
                        ],
                        errors="coerce"
                    )
                )


                weekly_daily = (
                    weekly_daily
                    .set_index(
                        "date"
                    )
                )


                st.line_chart(
                    weekly_daily[
                        "amount"
                    ],
                    use_container_width=True,
                    height=320
                )


            else:

                st.info(
                    "No daily spending data available."
                )


        # ----------------------------------------------------
        # WEEKLY HIGHEST EXPENSE
        # ----------------------------------------------------

        weekly_highest = weekly.get(
            "highest_expense"
        )


        if weekly_highest:

            st.markdown(
                '<div class="section-label">'
                'Highest Expense This Week'
                '</div>',
                unsafe_allow_html=True
            )


            highest_col1, highest_col2, highest_col3 = (
                st.columns(
                    [2, 1, 1]
                )
            )


            with highest_col1:

                st.metric(
                    "Description",
                    weekly_highest[
                        "description"
                    ]
                )


            with highest_col2:

                st.metric(
                    "Amount",
                    "Rs. {:,.2f}".format(
                        weekly_highest[
                            "amount"
                        ]
                    )
                )


            with highest_col3:

                st.metric(
                    "Category",
                    weekly_highest[
                        "category"
                    ]
                )


        # ----------------------------------------------------
        # WEEKLY INSIGHTS
        # ----------------------------------------------------

        weekly_insights = weekly.get(
            "insights",
            []
        )


        if weekly_insights:

            st.markdown(
                '<div class="section-label">'
                'Weekly Insights'
                '</div>',
                unsafe_allow_html=True
            )


            for insight in weekly_insights:

                st.info(
                    insight
                )


    st.divider()


    # ========================================================
    # MONTHLY ANALYTICS
    # ========================================================

    if monthly is None:

        st.error(
            "Unable to retrieve monthly analytics."
        )


    else:

        st.subheader(
            datetime(
                int(selected_year),
                int(selected_month),
                1
            ).strftime(
                "%B %Y"
            )
        )


        # ----------------------------------------------------
        # MONTHLY METRICS
        # ----------------------------------------------------

        metric1, metric2, metric3 = st.columns(
            3,
            gap="medium"
        )


        with metric1:

            st.metric(
                "Monthly Spending",
                "Rs. {:,.2f}".format(
                    monthly[
                        "total_spending"
                    ]
                )
            )


        with metric2:

            st.metric(
                "Transactions",
                str(
                    monthly[
                        "total_expenses"
                    ]
                )
            )


        with metric3:

            st.metric(
                "Average Expense",
                "Rs. {:,.2f}".format(
                    monthly[
                        "average_expense"
                    ]
                )
            )


        st.divider()


        # ----------------------------------------------------
        # MONTHLY TREND
        # ----------------------------------------------------

        if trend is not None:

            st.markdown(
                '<div class="section-label">'
                'Monthly Spending Trend'
                '</div>',
                unsafe_allow_html=True
            )


            trend_data = pd.DataFrame(
                trend.get(
                    "months",
                    []
                )
            )


            if not trend_data.empty:

                trend_data["label"] = (
                    trend_data[
                        "label"
                    ].astype(str)
                )


                trend_data = (
                    trend_data
                    .set_index(
                        "label"
                    )
                )


                st.line_chart(
                    trend_data[
                        "total_spending"
                    ],
                    use_container_width=True,
                    height=320
                )


            else:

                st.info(
                    "No trend data available."
                )


        st.divider()


        # ----------------------------------------------------
        # MONTH-TO-MONTH COMPARISON
        # ----------------------------------------------------

        if comparison is not None:

            current = comparison[
                "current_month"
            ]


            previous = comparison[
                "previous_month"
            ]


            change = comparison[
                "change_percent"
            ]


            st.markdown(
                '<div class="section-label">'
                'Month-to-Month Comparison'
                '</div>',
                unsafe_allow_html=True
            )


            compare_col1, compare_col2, compare_col3 = (
                st.columns(
                    3
                )
            )


            with compare_col1:

                st.metric(
                    "Current Month",
                    "Rs. {:,.2f}".format(
                        current[
                            "total_spending"
                        ]
                    )
                )


            with compare_col2:

                st.metric(
                    "Previous Month",
                    "Rs. {:,.2f}".format(
                        previous[
                            "total_spending"
                        ]
                    )
                )


            with compare_col3:

                st.metric(
                    "Change",
                    "{:+.2f}%".format(
                        change
                    )
                )


            # ------------------------------------------------
            # CATEGORY COMPARISON
            # ------------------------------------------------

            category_rows = []


            for category, values in comparison[
                "category_comparison"
            ].items():

                category_rows.append(
                    {
                        "Category": category,
                        "Current (Rs.)": values[
                            "current"
                        ],
                        "Previous (Rs.)": values[
                            "previous"
                        ],
                        "Change (%)": values[
                            "change_percent"
                        ]
                    }
                )


            if category_rows:

                st.dataframe(
                    pd.DataFrame(
                        category_rows
                    ),
                    use_container_width=True,
                    hide_index=True
                )


        st.divider()


        # ----------------------------------------------------
        # HIGHEST EXPENSE
        # ----------------------------------------------------

        st.markdown(
            '<div class="section-label">'
            'Highest Expense'
            '</div>',
            unsafe_allow_html=True
        )


        highest = monthly.get(
            "highest_expense"
        )


        if highest:

            highest_col1, highest_col2, highest_col3 = (
                st.columns(
                    [2, 1, 1]
                )
            )


            with highest_col1:

                st.metric(
                    "Description",
                    highest[
                        "description"
                    ]
                )


            with highest_col2:

                st.metric(
                    "Amount",
                    "Rs. {:,.2f}".format(
                        highest[
                            "amount"
                        ]
                    )
                )


            with highest_col3:

                st.metric(
                    "Category",
                    highest[
                        "category"
                    ]
                )


        else:

            st.info(
                "No expenses recorded for this month."
            )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
    '<div class="footer">'
    'SmartSpend · FastAPI · Machine Learning · SQLite'
    '</div>',
    unsafe_allow_html=True
)
