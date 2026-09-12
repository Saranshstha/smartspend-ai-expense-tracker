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
    page_icon="favicon.png",
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
        max-width: none;
        margin: 0;
        padding: 2.5rem 3.5rem 4rem;

        transition:
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

        background-color: var(--card-bg) !important;

        border: 1px solid var(--border) !important;

        border-radius: 10px;

        min-height: 46px;

        transition:
            background-color 0.18s ease,
            border-color 0.18s ease,
            box-shadow 0.18s ease;
    }

    div[data-baseweb="input"]:hover {

        background-color: var(--hover-bg) !important;

        border-color: var(--border-hover) !important;
    }

    div[data-baseweb="input"]:focus-within {

        background-color: var(--card-bg) !important;

        border-color: var(--border-hover) !important;

        box-shadow:
            0 0 0 3px
            rgba(255, 255, 255, 0.06);
    }

    div[data-baseweb="input"] input {

        background-color: transparent !important;

        color: var(--text-primary) !important;
    }

    div[data-baseweb="select"] > div {

        background-color: var(--card-bg) !important;

        border: 1px solid var(--border) !important;

        border-radius: 10px;

        transition:
            background-color 0.18s ease,
            border-color 0.18s ease;
    }

    div[data-baseweb="select"] > div:hover {

        background-color: var(--hover-bg) !important;

        border-color: var(--border-hover) !important;
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

        background-color: transparent !important;

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

        border: 1px solid var(--border) !important;

        border-radius: 14px;

        overflow: hidden;

        margin-top: 10px;

        background-color: var(--card-bg) !important;
    }

    [data-testid="stDataFrame"] [role="grid"] {

        font-size: 0.9rem;

        background-color: var(--card-bg) !important;
    }

    [data-testid="stDataFrame"] canvas {

        background-color: var(--card-bg) !important;
    }


    /* ========================================================
       DATA EDITOR
       ======================================================== */

    div[data-testid="stDataEditor"] {

        border: 1px solid var(--border) !important;

        border-radius: 14px;

        overflow: hidden;

        background-color: var(--card-bg) !important;
    }

    [data-testid="stDataEditor"] canvas {

        background-color: var(--card-bg) !important;
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
    amount,
    is_essential=False
):

    try:

        response = requests.post(
            API_URL + "/predict",
            json={
                "description": description,
                "amount": amount,
                "is_essential": is_essential
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


def get_budget():

    try:
        response = requests.get(
            API_URL + "/budget",
            timeout=5
        )

        response.raise_for_status()

        return response.json()

    except requests.RequestException:
        return None


def save_budget(monthly_budget):

    try:
        response = requests.put(
            API_URL + "/budget",
            json={
                "monthly_budget": monthly_budget
            },
            timeout=5
        )

        response.raise_for_status()

        return True, response.json()

    except requests.HTTPError:
        try:
            detail = response.json().get(
                "detail",
                "Unable to update budget."
            )
        except Exception:
            detail = "Unable to update budget."

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
    'Manage expenses and analyze spending.'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="hero-subtitle">'
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
        ("Analytics", "◫"),
        ("Budget", "◈")
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
        "Recently Deleted",
        use_container_width=True,
        type=button_type,
        key="sidebar_recently_deleted"
    ):

        st.session_state.selected_page = page_name

        st.session_state.confirm_delete = False

        st.rerun()


    # --------------------------------------------------------
    # LEGAL
    # --------------------------------------------------------

    st.markdown(
        '<div class="sidebar-section">Legal</div>',
        unsafe_allow_html=True
    )


    legal_items = [
        "Privacy Policy",
        "Terms & Conditions"
    ]


    for legal_page in legal_items:

        is_selected = (
            st.session_state.selected_page
            == legal_page
        )

        button_type = (
            "primary"
            if is_selected
            else "secondary"
        )

        if st.button(
            legal_page,
            use_container_width=True,
            type=button_type,
            key=(
                "sidebar_"
                + legal_page.lower()
                .replace(" ", "_")
                .replace("&", "and")
            )
        ):

            st.session_state.selected_page = legal_page

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


        metric1, metric2, metric3, metric4 = st.columns(
            4,
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

        with metric4:

            st.metric(
                "Essential Spending",
                "Rs. {:,.2f}".format(
                    summary.get(
                        "essential_spending",
                        0
                    )
                )
            )


        budget = get_budget()

        if budget is not None and budget.get("monthly_budget", 0) > 0:

            st.markdown(
                '<div class="section-label">'
                'Budget Status'
                '</div>',
                unsafe_allow_html=True
            )

            budget_col1, budget_col2, budget_col3, budget_col4 = st.columns(
                4,
                gap="medium"
            )

            with budget_col1:
                st.metric(
                    "Monthly Budget",
                    "Rs. {:,.2f}".format(
                        budget["monthly_budget"]
                    )
                )

            with budget_col2:
                st.metric(
                    "Remaining",
                    "Rs. {:,.2f}".format(
                        budget["remaining"]
                    )
                )

            with budget_col3:
                st.metric(
                    "Budget Used",
                    "{:.1f}%".format(
                        budget["usage_percent"]
                    )
                )

            st.caption(
                "Regular spending is what counts toward the monthly budget. "
                "Essential / unexpected spending is tracked separately."
            )

            if budget["status"] == "Over budget":
                st.error(budget["alert"])
            elif budget["status"] in (
                "Near limit",
                "Watch spending"
            ):
                st.warning(budget["alert"])
            else:
                st.success(budget["alert"])


        essential_total = float(
            summary.get(
                "essential_spending",
                0
            )
        )

        essential_count = int(
            summary.get(
                "essential_expenses",
                0
            )
        )

        st.divider()

        st.markdown(
            '<div class="section-label">'
            'Essential & Unexpected'
            '</div>',
            unsafe_allow_html=True
        )

        st.caption(
            "Important expenses are shown separately from regular spending."
        )

        if essential_total > 0:
            st.metric(
                "Essential Spending",
                "Rs. {:,.2f}".format(
                    essential_total
                ),
                str(essential_count) + " expense"
                + ("" if essential_count == 1 else "s")
            )

            essential_rows = expenses[
                expenses.get(
                    "is_essential",
                    False
                ).fillna(False).astype(bool)
            ].copy() if "is_essential" in expenses.columns else pd.DataFrame()

            if not essential_rows.empty:
                essential_display = essential_rows[
                    [
                        "description",
                        "amount",
                        "category"
                    ]
                ].rename(
                    columns={
                        "description": "Expense",
                        "amount": "Amount (Rs.)",
                        "category": "Category"
                    }
                )

                essential_display[
                    "Amount (Rs.)"
                ] = essential_display[
                    "Amount (Rs.)"
                ].round(2)

                st.dataframe(
                    essential_display.head(5),
                    use_container_width=True,
                    hide_index=True
                )
        else:
            st.info(
                "No essential or unexpected spending recorded."
            )


        st.divider()


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

        spending_type = st.radio(
            "Spending Type",
            [
                "Regular Spending",
                "Essential / Unexpected"
            ],
            index=0,
            horizontal=True,
            key="spending_type_input"
        )

        is_essential = (
            spending_type == "Essential / Unexpected"
        )

        predict_clicked = st.button(
            "Predict Expense",
            type="primary",
            use_container_width=True,
            key="predict_expense_button"
        )


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

            st.caption(
                "Type: "
                + (
                    "Essential / Unexpected"
                    if prediction.get("is_essential")
                    else "Regular Spending"
                )
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
                amount,
                is_essential
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

        # ====================================================
        # PREPARE DATA
        # ====================================================

        expenses = expenses.copy()


        expenses["amount"] = pd.to_numeric(
            expenses["amount"],
            errors="coerce"
        )


        expenses["confidence"] = pd.to_numeric(
            expenses["confidence"],
            errors="coerce"
        )


        expenses["created_at"] = pd.to_datetime(
            expenses["created_at"],
            errors="coerce",
            utc = True
        ).dt.tz_convert("Asia/Kathmandu")


        # ====================================================
        # FILTER & SORT
        # ====================================================

        st.markdown(
            '<div class="section-label">'
            'Filter & Sort'
            '</div>',
            unsafe_allow_html=True
        )


        filter_col1, filter_col2, filter_col3, filter_col4 = st.columns(
            [1.7, 1, 1, 1],
            gap="medium"
        )


        # ----------------------------------------------------
        # SEARCH
        # ----------------------------------------------------

        with filter_col1:

            search = st.text_input(
                "Search",
                placeholder="Description or category...",
                key="expense_search_input"
            )


        # ----------------------------------------------------
        # CATEGORY
        # ----------------------------------------------------

        with filter_col2:

            categories = [
                "All"
            ] + sorted(
                expenses[
                    "category"
                ]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )


            selected_category = st.selectbox(
                "Category",
                categories,
                key="expense_category_filter"
            )


        # ----------------------------------------------------
        # SORT
        # ----------------------------------------------------

        with filter_col3:

            sort_option = st.selectbox(
                "Sort by",
                [
                    "Newest",
                    "Oldest",
                    "Highest amount",
                    "Lowest amount",
                    "Highest confidence",
                    "Lowest confidence"
                ],
                key="expense_sort_option"
            )

        with filter_col4:

            type_options = [
                "All",
                "Regular Spending",
                "Essential / Unexpected"
            ]

            selected_type = st.selectbox(
                "Spending Type",
                type_options,
                key="expense_type_filter"
            )


        # ====================================================
        # SECOND FILTER ROW
        # ====================================================

        filter_col4, filter_col5, filter_col6 = st.columns(
            [1, 1, 1],
            gap="medium"
        )


        # ----------------------------------------------------
        # DATE
        # ----------------------------------------------------

        with filter_col4:

            date_options = [
                "All time",
                "Today",
                "Last 7 days",
                "Last 30 days",
                "This month"
            ]


            selected_date = st.selectbox(
                "Date",
                date_options,
                key="expense_date_filter"
            )


        # ----------------------------------------------------
        # MINIMUM AMOUNT
        # ----------------------------------------------------

        with filter_col5:

            minimum_amount = st.number_input(
                "Minimum amount",
                min_value=0.0,
                value=0.0,
                step=50.0,
                format="%.2f",
                key="expense_min_amount"
            )


        # ----------------------------------------------------
        # MAXIMUM AMOUNT
        # ----------------------------------------------------

        with filter_col6:

            maximum_amount = st.number_input(
                "Maximum amount",
                min_value=0.0,
                value=0.0,
                step=50.0,
                format="%.2f",
                key="expense_max_amount"
            )


        # ====================================================
        # APPLY SEARCH
        # ====================================================

        filtered = expenses.copy()


        if search.strip():

            search_lower = (
                search
                .strip()
                .lower()
            )


            description_match = (
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
            )


            category_match = (
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
            )


            filtered = filtered[
                description_match
                | category_match
            ]


        # ====================================================
        # APPLY CATEGORY
        # ====================================================

        if selected_category != "All":

            filtered = filtered[
                filtered[
                    "category"
                ]
                == selected_category
            ]


        # ====================================================
        # APPLY SPENDING TYPE
        # ====================================================

        if selected_type != "All":

            type_value = (
                selected_type
                == "Essential / Unexpected"
            )

            filtered = filtered[
                filtered["is_essential"].fillna(False).astype(bool)
                == type_value
            ]


        # ====================================================
        # APPLY DATE
        # ====================================================

        current_time = pd.Timestamp.now(
            tz="Asia/Kathmandu"
        )


        if selected_date == "Today":

            today = current_time.normalize()

            filtered = filtered[
                filtered[
                    "created_at"
                ] >= today
            ]


        elif selected_date == "Last 7 days":

            seven_days_ago = (
                current_time
                - pd.Timedelta(days=7)
            )

            filtered = filtered[
                filtered[
                    "created_at"
                ] >= seven_days_ago
            ]


        elif selected_date == "Last 30 days":

            thirty_days_ago = (
                current_time
                - pd.Timedelta(days=30)
            )

            filtered = filtered[
                filtered[
                    "created_at"
                ] >= thirty_days_ago
            ]


        elif selected_date == "This month":

            month_start = pd.Timestamp(
                current_time.year,
                current_time.month,
                1,
                tz="Asia/Kathmandu"
            )

            filtered = filtered[
                filtered[
                    "created_at"
                ] >= month_start
            ]


        # ====================================================
        # APPLY AMOUNT RANGE
        # ====================================================

        if minimum_amount > 0:

            filtered = filtered[
                filtered[
                    "amount"
                ] >= minimum_amount
            ]


        if maximum_amount > 0:

            if maximum_amount < minimum_amount:

                st.warning(
                    "Maximum amount cannot be lower "
                    "than minimum amount."
                )

            else:

                filtered = filtered[
                    filtered[
                        "amount"
                    ] <= maximum_amount
                ]


        # ====================================================
        # SORT
        # ====================================================

        if sort_option == "Newest":

            filtered = filtered.sort_values(
                "created_at",
                ascending=False
            )


        elif sort_option == "Oldest":

            filtered = filtered.sort_values(
                "created_at",
                ascending=True
            )


        elif sort_option == "Highest amount":

            filtered = filtered.sort_values(
                "amount",
                ascending=False
            )


        elif sort_option == "Lowest amount":

            filtered = filtered.sort_values(
                "amount",
                ascending=True
            )


        elif sort_option == "Highest confidence":

            filtered = filtered.sort_values(
                "confidence",
                ascending=False
            )


        elif sort_option == "Lowest confidence":

            filtered = filtered.sort_values(
                "confidence",
                ascending=True
            )


        # ====================================================
        # RESULT SUMMARY
        # ====================================================

        total_records = len(
            expenses
        )


        filtered_records = len(
            filtered
        )


        filtered_total = filtered[
            "amount"
        ].sum()


        if filtered_records > 0:

            filtered_average = (
                filtered_total
                / filtered_records
            )

        else:

            filtered_average = 0


        summary_col1, summary_col2, summary_col3 = (
            st.columns(
                3,
                gap="medium"
            )
        )


        with summary_col1:

            st.metric(
                "Showing",
                str(
                    filtered_records
                )
                + " / "
                + str(
                    total_records
                )
            )


        with summary_col2:

            st.metric(
                "Filtered Spending",
                "Rs. {:,.2f}".format(
                    filtered_total
                )
            )


        with summary_col3:

            st.metric(
                "Average",
                "Rs. {:,.2f}".format(
                    filtered_average
                )
            )


        # ====================================================
        # EXPENSE TABLE
        # ====================================================

        if len(filtered) == 0:

            st.info(
                "No expenses match your current "
                "search and filter settings."
            )


        else:

            st.divider()


            st.markdown(
                '<div class="section-label">'
                'Expense Records'
                '</div>',
                unsafe_allow_html=True
            )


            st.caption(
                "Edit Description or Amount directly "
                "in the table. Category and Confidence "
                "are generated by the AI model. "
                "Changing a description will recalculate "
                "its category when you save the changes."
            )


            editable_table = filtered[
                [
                    "id",
                    "description",
                    "amount",
                    "category",
                    "confidence",
                    "is_essential",
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
                        "is_essential": "Type",
                        "created_at": "Date"
                    }
                )
            )


            editable_table[
                "Amount (Rs.)"
            ] = (
                editable_table[
                    "Amount (Rs.)"
                ]
                .round(2)
            )


            editable_table[
                "Confidence (%)"
            ] = (
                editable_table[
                    "Confidence (%)"
                ]
                .round(2)
            )


            editable_table[
                "Type"
            ] = editable_table[
                "Type"
            ].apply(
                lambda value:
                "Essential / Unexpected"
                if bool(value)
                else "Regular Spending"
            )

            editable_table[
                "Date"
            ] = (
                editable_table[
                    "Date"
                ]
                .dt.strftime(
                    "%Y-%m-%d %H:%M"
                )
            )


            # =================================================
            # EDITABLE TABLE
            # =================================================

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

                    "Type": st.column_config.SelectboxColumn(
                        "Type",
                        options=[
                            "Regular Spending",
                            "Essential / Unexpected"
                        ],
                        required=True
                    ),

                    "Date": st.column_config.TextColumn(
                        "Date",
                        disabled=True
                    )
                },

                key="expense_editor"
            )


            st.markdown("")


            # =================================================
            # SAVE CHANGES
            # =================================================

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
                        row[
                            "Description"
                        ]
                    ).strip()


                    try:

                        amount_value = float(
                            row[
                                "Amount (Rs.)"
                            ]
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
                                row[
                                    "ID"
                                ]
                            ),

                            "description": (
                                description_value
                            ),

                            "amount": (
                                amount_value
                            ),

                            "is_essential": (
                                str(
                                    row["Type"]
                                ).strip()
                                == "Essential / Unexpected"
                            )
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
                            "Changed descriptions were "
                            "automatically re-categorized "
                            "by the AI model."
                        )

                        st.rerun()


                    else:

                        st.error(
                            result
                        )


        # ====================================================
        # DELETE EXPENSE
        # ====================================================

        st.divider()


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


        # ====================================================
        # DELETE CONFIRMATION
        # ====================================================

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
# BUDGET
# ============================================================

elif page == "Budget":

    st.markdown(
        '<div class="section-label">'
        'Budget & Spending Alerts'
        '</div>',
        unsafe_allow_html=True
    )

    st.caption(
        "Set a monthly limit and get a simple warning before spending gets out of control."
    )

    budget = get_budget()

    if budget is None:

        st.error(
            "Unable to retrieve budget information."
        )

    else:

        current_budget = float(
            budget.get(
                "monthly_budget",
                0
            )
        )

        budget_input = st.number_input(
            "Monthly budget (Rs.)",
            min_value=1.0,
            value=max(
                1.0,
                current_budget
            ),
            step=1000.0,
            format="%.2f",
            key="monthly_budget_input"
        )

        if st.button(
            "Save Monthly Budget",
            type="primary",
            use_container_width=True,
            key="save_monthly_budget_button"
        ):

            success, result = save_budget(
                budget_input
            )

            if success:
                st.success(
                    "Monthly budget saved successfully."
                )
                st.rerun()
            else:
                st.error(result)

        st.divider()

        if current_budget <= 0:

            st.info(
                "Set a monthly budget to start tracking your spending."
            )

        else:

            budget_col1, budget_col2, budget_col3, budget_col4 = st.columns(
                4,
                gap="medium"
            )

            with budget_col1:
                st.metric(
                    "Spent This Month",
                    "Rs. {:,.2f}".format(
                        budget["spent"]
                    )
                )

            with budget_col2:
                st.metric(
                    "Remaining",
                    "Rs. {:,.2f}".format(
                        budget["remaining"]
                    )
                )

            with budget_col3:
                st.metric(
                    "Budget Used",
                    "{:.1f}%".format(
                        budget["usage_percent"]
                    )
                )

            with budget_col4:
                st.metric(
                    "Essential Spending",
                    "Rs. {:,.2f}".format(
                        budget.get("essential_spending", 0)
                    )
                )

            st.progress(
                min(
                    budget["usage_percent"] / 100,
                    1.0
                )
            )

            if budget["status"] == "Over budget":
                st.error(budget["alert"])
            elif budget["status"] in (
                "Near limit",
                "Watch spending"
            ):
                st.warning(budget["alert"])
            else:
                st.success(budget["alert"])

            st.divider()

            st.markdown(
                '<div class="section-label">'
                'Spending Forecast'
                '</div>',
                unsafe_allow_html=True
            )

            forecast_col1, forecast_col2 = st.columns(
                2,
                gap="medium"
            )

            with forecast_col1:
                st.metric(
                    "Projected Month-End",
                    "Rs. {:,.2f}".format(
                        budget["projected_spending"]
                    )
                )

            with forecast_col2:
                if budget["projected_over_budget"] > 0:
                    st.metric(
                        "Projected Over Budget",
                        "Rs. {:,.2f}".format(
                            budget["projected_over_budget"]
                        )
                    )
                else:
                    st.metric(
                        "Projected Over Budget",
                        "Rs. 0.00"
                    )

            st.caption(
                "Forecast uses your average daily spending so far this month."
            )


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
        ] = (
            display_deleted[
                "Amount (Rs.)"
            ]
            .round(2)
        )


        st.dataframe(
            display_deleted,
            use_container_width=True,
            hide_index=True
        )


        st.divider()


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
                + " - Rs. "
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
# PRIVACY POLICY
# ============================================================

elif page == "Privacy Policy":

    st.markdown(
        '<div class="section-label">'
        'Privacy Policy'
        '</div>',
        unsafe_allow_html=True
    )

    st.subheader(
        "SmartSpend Privacy Policy"
    )

    st.caption(
        "Last updated: September 2026"
    )

    st.write(
        "This page explains how SmartSpend handles information entered "
        "into the application. The policy is written for this project "
        "demonstration and should be replaced with the organisation's "
        "final legal policy before public commercial use."
    )

    with st.expander(
        "1. Information stored"
    ):

        st.write(
            "SmartSpend stores expense information needed to provide "
            "its features. This can include expense descriptions, "
            "amounts, categories, confidence scores, creation "
            "timestamps, and deletion timestamps."
        )


    with st.expander(
        "2. How information is used"
    ):

        st.write(
            "Stored expense information is used to categorize expenses, "
            "display expense history, calculate spending summaries, "
            "generate analytics, and support restoration of deleted "
            "expenses."
        )


    with st.expander(
        "3. Machine learning"
    ):

        st.write(
            "Expense descriptions may be processed by the local "
            "machine learning model used by SmartSpend to predict "
            "an expense category and calculate a confidence score."
        )


    with st.expander(
        "4. Deleted expenses"
    ):

        st.write(
            "Deleted expenses are kept in Recently Deleted for up "
            "to 15 days so they can be restored. After the retention "
            "period, the backend permanently removes them."
        )


    with st.expander(
        "5. Data sharing"
    ):

        st.write(
            "This project does not intentionally sell or share "
            "expense records with third parties. Any public "
            "deployment should document the actual hosting "
            "providers, services, and integrations used."
        )


    with st.expander(
        "6. Security"
    ):

        st.write(
            "SmartSpend uses application and database controls "
            "appropriate for the current project. A production "
            "deployment should use HTTPS, authentication, access "
            "controls, secure secrets, backups, and a managed "
            "database where appropriate."
        )


    with st.expander(
        "7. Contact"
    ):

        st.write(
            "For questions about this project, use the contact "
            "details supplied by the project owner or organisation."
        )


# ============================================================
# TERMS & CONDITIONS
# ============================================================

elif page == "Terms & Conditions":

    st.markdown(
        '<div class="section-label">'
        'Terms & Conditions'
        '</div>',
        unsafe_allow_html=True
    )

    st.subheader(
        "SmartSpend Terms & Conditions"
    )

    st.caption(
        "Last updated: September 2026"
    )

    st.write(
        "These terms describe the intended use of the SmartSpend "
        "project. They are suitable as project documentation, "
        "not as a substitute for a reviewed legal agreement."
    )


    with st.expander(
        "1. Intended use"
    ):

        st.write(
            "SmartSpend is intended to help users record expenses, "
            "categorize them, review spending, and understand "
            "historical spending patterns."
        )


    with st.expander(
        "2. AI predictions"
    ):

        st.write(
            "Expense categories and confidence scores are generated "
            "by a machine learning model. Predictions can be incorrect "
            "and should be reviewed by the user before being relied upon."
        )


    with st.expander(
        "3. Analytics"
    ):

        st.write(
            "Analytics and projections are informational tools based "
            "on the data available to the application. They are not "
            "financial advice."
        )


    with st.expander(
        "4. User responsibility"
    ):

        st.write(
            "Users are responsible for the accuracy of information "
            "they enter and for reviewing expense records before "
            "making financial decisions."
        )


    with st.expander(
        "5. Deleted expenses"
    ):

        st.write(
            "Deleted expenses may be restored during the 15-day "
            "Recently Deleted retention period. Once permanently "
            "removed, they cannot be restored through the application."
        )


    with st.expander(
        "6. Availability"
    ):

        st.write(
            "The project may be unavailable during maintenance, "
            "development, deployment changes, or technical failures. "
            "No uninterrupted availability is guaranteed by this "
            "project version."
        )


    with st.expander(
        "7. Changes"
    ):

        st.write(
            "These terms may be updated as SmartSpend changes. "
            "The displayed update date should be revised whenever "
            "the policy changes."
        )


# ============================================================
# ANALYTICS
# ============================================================

elif page == "Analytics":

    # ========================================================
    # HEADER
    # ========================================================

    st.markdown(
        '<div class="section-label">'
        'Spending Analytics {Present to whole year}'
        '</div>',
        unsafe_allow_html=True
    )



    # ========================================================
    # LOAD DATA ONCE
    # ========================================================

    expenses = get_expenses()

    if expenses is None:

        st.error(
            "Unable to retrieve expense data."
        )

    else:

        expenses = expenses.copy()


        # ====================================================
        # PREPARE DATA
        # ====================================================

        if not expenses.empty:

            expenses["amount"] = pd.to_numeric(
                expenses["amount"],
                errors="coerce"
            ).fillna(0)


            expenses["created_at"] = pd.to_datetime(
                expenses["created_at"],
                errors="coerce",
                utc=True
            ).dt.tz_convert(
                "Asia/Kathmandu"
            )

            expenses["is_essential"] = (
                expenses["is_essential"]
                .fillna(False)
                .astype(bool)
                if "is_essential" in expenses.columns
                else False
            )

        else:

            expenses["amount"] = pd.Series(
                dtype="float64"
            )

            expenses["created_at"] = pd.Series(
                dtype="datetime64[ns, Asia/Kathmandu]"
            )


        # ====================================================
        # CURRENT TIME
        # ====================================================

        now = pd.Timestamp.now(
            tz="Asia/Kathmandu"
        )

        today = now.normalize()


        week_start = (
            today
            - pd.Timedelta(
                days=today.weekday()
            )
        )


        month_start = pd.Timestamp(
            year=today.year,
            month=today.month,
            day=1,
            tz="Asia/Kathmandu"
        )


        year_start = pd.Timestamp(
            year=today.year,
            month=1,
            day=1,
            tz="Asia/Kathmandu"
        )


        # ====================================================
        # HELPER
        # ====================================================

        def money(value):

            return (
                "Rs. "
                + "{:,.2f}".format(
                    float(value)
                )
            )


        # ====================================================
        # TODAY
        # ====================================================

        st.markdown(
            '<div class="section-label">'
            'Today'
            '</div>',
            unsafe_allow_html=True
        )

        st.caption(
            "Spending and transactions."
        )


        if expenses.empty:

            today_data = expenses.copy()

        else:

            today_data = expenses[
                expenses["created_at"] >= today
            ].copy()


        today_total = float(
            today_data["amount"].sum()
        )

        today_count = len(
            today_data
        )


        today_col1, today_col2 = st.columns(
            2,
            gap="medium"
        )


        with today_col1:

            st.metric(
                "Spent Today",
                money(
                    today_total
                )
            )


        with today_col2:

            st.metric(
                "Transactions",
                str(
                    today_count
                )
            )


        if today_count > 0:

            today_categories = (
                today_data
                .groupby("category")["amount"]
                .sum()
                .sort_values(
                    ascending=False
                )
            )


            top_today_category = (
                today_categories.index[0]
            )


            top_today_amount = float(
                today_categories.iloc[0]
            )


            st.caption(
                "Most spent on "
                + str(
                    top_today_category
                )
                + " · "
                + money(
                    top_today_amount
                )
            )


            today_highest = today_data.loc[
                today_data["amount"].idxmax()
            ]


            st.caption(
                "Biggest transaction: "
                + str(
                    today_highest["description"]
                )
                + " · "
                + money(
                    today_highest["amount"]
                )
            )


            today_display = today_data[
                [
                    "description",
                    "amount",
                    "category",
                    "is_essential"
                ]
            ].copy()


            today_display = today_display.rename(
                columns={
                    "description": "Transaction",
                    "amount": "Amount (Rs.)",
                    "category": "Category",
                    "is_essential": "Type"
                }
            )


            today_display["Type"] = today_display[
                "Type"
            ].apply(
                lambda value:
                "Essential"
                if bool(value)
                else "Regular"
            )

            today_display[
                "Amount (Rs.)"
            ] = today_display[
                "Amount (Rs.)"
            ].round(2)


            st.dataframe(
                today_display,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "No expenses recorded today."
            )


        st.divider()

        # ====================================================
        # ESSENTIAL / UNEXPECTED SPENDING
        # ====================================================

        st.markdown(
            '<div class="section-label">'
            'Essential & Unexpected'
            '</div>',
            unsafe_allow_html=True
        )

        st.caption(
            "Important spending is separated from regular spending."
        )

        month_data = expenses[
            expenses["created_at"] >= month_start
        ].copy()

        month_essential = month_data[
            month_data["is_essential"]
        ].copy()

        month_regular = month_data[
            ~month_data["is_essential"]
        ].copy()

        essential_col1, essential_col2, essential_col3 = st.columns(
            3,
            gap="medium"
        )

        with essential_col1:
            st.metric(
                "Regular Spending",
                money(
                    month_regular["amount"].sum()
                )
            )

        with essential_col2:
            st.metric(
                "Essential / Unexpected",
                money(
                    month_essential["amount"].sum()
                )
            )

        with essential_col3:
            total_month = float(
                month_data["amount"].sum()
            )
            essential_share = (
                float(month_essential["amount"].sum())
                / total_month
                * 100
                if total_month > 0
                else 0
            )
            st.metric(
                "Essential Share",
                "{:.1f}%".format(
                    essential_share
                )
            )

        if not month_essential.empty:
            essential_display = month_essential[
                [
                    "description",
                    "amount",
                    "category"
                ]
            ].rename(
                columns={
                    "description": "Expense",
                    "amount": "Amount (Rs.)",
                    "category": "Category"
                }
            )

            essential_display[
                "Amount (Rs.)"
            ] = essential_display[
                "Amount (Rs.)"
            ].round(2)

            st.dataframe(
                essential_display.head(8),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info(
                "No essential or unexpected spending recorded this month."
            )

        st.divider()


        # ====================================================
        # THIS WEEK
        # ====================================================

        st.markdown(
            '<div class="section-label">'
            'This Week'
            '</div>',
            unsafe_allow_html=True
        )

        st.caption(
            "See how your spending is moving from Sunday to Saturday."
        )


        weekly = get_weekly_analytics()


        if weekly is None:

            st.warning(
                "Weekly analytics are currently unavailable."
            )

        else:

            weekly_total = float(
                weekly.get(
                    "total_spending",
                    0
                )
            )


            weekly_count = int(
                weekly.get(
                    "total_expenses",
                    0
                )
            )


            weekly_average = float(
                weekly.get(
                    "average_expense",
                    0
                )
            )


            week_col1, week_col2, week_col3 = st.columns(
                3,
                gap="medium"
            )


            with week_col1:

                st.metric(
                    "Spent This Week",
                    money(
                        weekly_total
                    )
                )


            with week_col2:

                st.metric(
                    "Transactions",
                    str(
                        weekly_count
                    )
                )


            with week_col3:

                st.metric(
                    "Average",
                    money(
                        weekly_average
                    )
                )


            weekly_daily = pd.DataFrame(
                weekly.get(
                    "daily_spending",
                    []
                )
            )


            if not weekly_daily.empty:

                weekly_daily["date"] = pd.to_datetime(
                    weekly_daily["date"],
                    errors="coerce"
                )


                weekly_daily["amount"] = pd.to_numeric(
                    weekly_daily["amount"],
                    errors="coerce"
                ).fillna(0)


                weekly_daily["Day"] = (
                    weekly_daily["date"]
                    .dt.strftime("%a")
                )

                day_order = [
                    "Sun",
                    "Mon",
                    "Tue",
                    "Wed",
                    "Thu",
                    "Fri",
                    "Sat"
                ]

                weekly_daily["Day"] = pd.Categorical(
                    weekly_daily["Day"],
                    categories=day_order,
                    ordered=True
                )

                weekly_daily = weekly_daily.sort_values(
                    "Day"
                )




                daily_chart = (
                    weekly_daily[
                        [
                            "Day",
                            "amount"
                        ]
                    ]
                    .set_index("Day")
                )


                st.bar_chart(
                    daily_chart,
                    use_container_width=True,
                    height=280
                )


                st.caption(
                    "Each bar shows how much you spent on that day."
                )


            weekly_categories = weekly.get(
                "categories",
                {}
            )


            if weekly_categories:

                weekly_category_series = (
                    pd.Series(
                        weekly_categories,
                        dtype="float64"
                    )
                    .sort_values(
                        ascending=True
                    )
                )


                st.markdown(
                    '<div class="section-label">'
                    'This Week by Category'
                    '</div>',
                    unsafe_allow_html=True
                )


                st.bar_chart(
                    weekly_category_series,
                    horizontal=True,
                    use_container_width=True,
                    height=240
                )


                top_week_category = (
                    weekly_category_series.idxmax()
                )


                st.caption(
                    "Most spent on "
                    + str(
                        top_week_category
                    )
                    + " this week."
                )


        st.divider()


        # ====================================================
        # THIS MONTH
        # ====================================================

        st.markdown(
            '<div class="section-label">'
            'This Month'
            '</div>',
            unsafe_allow_html=True
        )

        st.caption(
            "Understand where this month's money is going."
        )


        monthly = get_monthly_analytics(
            int(now.year),
            int(now.month)
        )


        comparison = get_monthly_comparison(
            int(now.year),
            int(now.month)
        )


        if monthly is None:

            st.warning(
                "Monthly analytics are currently unavailable."
            )

        else:

            month_total = float(
                monthly.get(
                    "total_spending",
                    0
                )
            )


            month_count = int(
                monthly.get(
                    "total_expenses",
                    0
                )
            )


            month_average = float(
                monthly.get(
                    "average_expense",
                    0
                )
            )


            month_col1, month_col2, month_col3 = st.columns(
                3,
                gap="medium"
            )


            with month_col1:

                st.metric(
                    "Spent This Month",
                    money(
                        month_total
                    )
                )


            with month_col2:

                st.metric(
                    "Transactions",
                    str(
                        month_count
                    )
                )


            with month_col3:

                st.metric(
                    "Average",
                    money(
                        month_average
                    )
                )


            month_categories = monthly.get(
                "categories",
                {}
            )


            if month_categories:

                st.markdown(
                    '<div class="section-label">'
                    'Where Your Money Goes'
                    '</div>',
                    unsafe_allow_html=True
                )


                st.caption(
                    "A simple breakdown of this month's spending."
                )


                month_category_series = (
                    pd.Series(
                        month_categories,
                        dtype="float64"
                    )
                    .sort_values(
                        ascending=True
                    )
                )


                st.bar_chart(
                    month_category_series,
                    horizontal=True,
                    use_container_width=True,
                    height=270
                )


                top_month_category = (
                    month_category_series.idxmax()
                )


                top_month_amount = float(
                    month_category_series.max()
                )


                top_month_share = (
                    top_month_amount
                    / month_total
                    * 100
                    if month_total > 0
                    else 0
                )


                st.caption(
                    str(
                        top_month_category
                    )
                    + " is your biggest category at "
                    + money(
                        top_month_amount
                    )
                    + " ("
                    + "{:.1f}%".format(
                        top_month_share
                    )
                    + " of this month's spending)."
                )


            if comparison is not None:

                previous_total = float(
                    comparison.get(
                        "previous_month",
                        {}
                    ).get(
                        "total_spending",
                        0
                    )
                )


                if previous_total > 0:

                    difference = (
                        month_total
                        - previous_total
                    )


                    change = (
                        difference
                        / previous_total
                        * 100
                    )


                    if difference > 0:

                        st.info(
                            "You spent "
                            + money(
                                abs(
                                    difference
                                )
                            )
                            + " more than last month "
                            + "({:+.1f}%).".format(
                                change
                            )
                        )

                    elif difference < 0:

                        st.success(
                            "You spent "
                            + money(
                                abs(
                                    difference
                                )
                            )
                            + " less than last month "
                            + "({:+.1f}%).".format(
                                change
                            )
                        )

                    else:

                        st.info(
                            "Your spending is the same as last month."
                        )


            month_highest = monthly.get(
                "highest_expense"
            )


            if month_highest:

                st.markdown(
                    '<div class="section-label">'
                    'Biggest Expense'
                    '</div>',
                    unsafe_allow_html=True
                )


                highest_col1, highest_col2 = st.columns(
                    [2, 1],
                    gap="medium"
                )


                with highest_col1:

                    st.metric(
                        "Expense",
                        str(
                            month_highest.get(
                                "description",
                                "-"
                            )
                        )
                    )


                    st.caption(
                        "Your largest single expense this month."
                    )


                with highest_col2:

                    st.metric(
                        "Amount",
                        money(
                            month_highest.get(
                                "amount",
                                0
                            )
                        )
                    )


                    st.caption(
                        "Category: "
                        + str(
                            month_highest.get(
                                "category",
                                "-"
                            )
                        )
                    )


        st.divider()


        # ====================================================
        # LAST 6 MONTHS
        # ====================================================

        st.markdown(
            '<div class="section-label">'
            'Last 6 Months'
            '</div>',
            unsafe_allow_html=True
        )

        st.caption(
            "See whether your overall spending is rising or falling."
        )


        trend = get_monthly_trend(
            6
        )


        if trend is None:

            st.warning(
                "Six-month trend is currently unavailable."
            )

        else:

            trend_data = pd.DataFrame(
                trend.get(
                    "months",
                    []
                )
            )


            if trend_data.empty:

                st.info(
                    "Not enough data for a six-month trend."
                )

            else:

                trend_data["total_spending"] = pd.to_numeric(
                    trend_data["total_spending"],
                    errors="coerce"
                ).fillna(0)


                trend_data["label"] = (
                    trend_data["label"]
                    .astype(str)
                )


                trend_values = (
                    trend_data
                    .set_index("label")[
                        "total_spending"
                    ]
                )


                st.line_chart(
                    trend_values,
                    use_container_width=True,
                    height=300
                )


                highest_month = trend_data.loc[
                    trend_data["total_spending"].idxmax()
                ]


                lowest_month = trend_data.loc[
                    trend_data["total_spending"].idxmin()
                ]


                trend_total = float(
                    trend_data["total_spending"].sum()
                )


                trend_average = (
                    trend_total
                    / len(trend_data)
                )


                six_col1, six_col2, six_col3 = st.columns(
                    3,
                    gap="medium"
                )


                with six_col1:

                    st.metric(
                        "Average Monthly",
                        money(
                            trend_average
                        )
                    )


                with six_col2:

                    st.metric(
                        "Highest Month",
                        str(
                            highest_month["label"]
                        )
                    )


                    st.caption(
                        money(
                            highest_month[
                                "total_spending"
                            ]
                        )
                    )


                with six_col3:

                    st.metric(
                        "Lowest Month",
                        str(
                            lowest_month["label"]
                        )
                    )


                    st.caption(
                        money(
                            lowest_month[
                                "total_spending"
                            ]
                        )
                    )


        st.divider()


        # ====================================================
        # THIS YEAR
        # ====================================================

        st.markdown(
            '<div class="section-label">'
            'This Year'
            '</div>',
            unsafe_allow_html=True
        )

        st.caption(
            "Your complete spending picture for "
            + str(
                now.year
            )
            + "."
        )


        year_data = expenses[
            expenses["created_at"] >= year_start
        ].copy()


        year_total = float(
            year_data["amount"].sum()
        )


        year_count = len(
            year_data
        )


        year_average = (
            year_total
            / year_count
            if year_count > 0
            else 0
        )


        year_col1, year_col2, year_col3 = st.columns(
            3,
            gap="medium"
        )


        with year_col1:

            st.metric(
                "Yearly Spending",
                money(
                    year_total
                )
            )


        with year_col2:

            st.metric(
                "Transactions",
                str(
                    year_count
                )
            )


        with year_col3:

            st.metric(
                "Average Transaction",
                money(
                    year_average
                )
            )


        if year_data.empty:

            st.info(
                "No expenses recorded this year."
            )

        else:

            # ------------------------------------------------
            # MONTHLY YEAR VIEW
            # ------------------------------------------------

            yearly_monthly = (
                year_data
                .assign(
                    Month=year_data[
                        "created_at"
                    ].dt.strftime(
                        "%b"
                    )
                )
                .groupby("Month")["amount"]
                .sum()
            )


            month_order = [
                "Jan",
                "Feb",
                "Mar",
                "Apr",
                "May",
                "Jun",
                "Jul",
                "Aug",
                "Sep",
                "Oct",
                "Nov",
                "Dec"
            ]


            yearly_monthly = (
                yearly_monthly
                .reindex(
                    month_order,
                    fill_value=0
                )
            )


            st.markdown(
                '<div class="section-label">'
                'Monthly Spending'
                '</div>',
                unsafe_allow_html=True
            )


            st.caption(
                "See how much you spent each month this year."
            )


            st.bar_chart(
                yearly_monthly,
                use_container_width=True,
                height=300
            )


            # ------------------------------------------------
            # YEARLY CATEGORIES
            # ------------------------------------------------

            yearly_categories = (
                year_data
                .groupby("category")["amount"]
                .sum()
                .sort_values(
                    ascending=True
                )
            )


            if not yearly_categories.empty:

                st.markdown(
                    '<div class="section-label">'
                    'Yearly Spending by Category'
                    '</div>',
                    unsafe_allow_html=True
                )


                st.bar_chart(
                    yearly_categories,
                    horizontal=True,
                    use_container_width=True,
                    height=260
                )


            # ------------------------------------------------
            # HIGHEST SPENDING MONTH
            # ------------------------------------------------

            highest_year_month = (
                yearly_monthly.idxmax()
            )


            highest_year_month_amount = float(
                yearly_monthly.max()
            )


            st.caption(
                "Highest spending month: "
                + highest_year_month
                + " · "
                + money(
                    highest_year_month_amount
                )
            )


        st.divider()


        # ====================================================
        # SPENDING PATTERNS
        # ====================================================

        st.markdown(
            '<div class="section-label">'
            'Spending Patterns'
            '</div>',
            unsafe_allow_html=True
        )

        st.caption(
            "Simple patterns found in your expense history."
        )


        if expenses.empty:

            st.info(
                "Add more expenses to see your spending patterns."
            )

        else:

            valid_expenses = expenses.dropna(
                subset=[
                    "created_at",
                    "amount"
                ]
            ).copy()


            if valid_expenses.empty:

                st.info(
                    "Not enough valid expense data yet."
                )

            else:

                # --------------------------------------------
                # MOST ACTIVE CATEGORY
                # --------------------------------------------

                category_frequency = (
                    valid_expenses[
                        "category"
                    ]
                    .value_counts()
                )


                most_frequent_category = (
                    category_frequency.index[0]
                )


                most_frequent_count = int(
                    category_frequency.iloc[0]
                )


                # --------------------------------------------
                # HIGHEST SPENDING DAY
                # --------------------------------------------

                daily_totals = (
                    valid_expenses
                    .assign(
                        date_only=valid_expenses[
                            "created_at"
                        ].dt.date
                    )
                    .groupby(
                        "date_only"
                    )["amount"]
                    .sum()
                )


                highest_day = (
                    daily_totals.idxmax()
                )


                highest_day_amount = float(
                    daily_totals.max()
                )


                # --------------------------------------------
                # AVERAGE TRANSACTION
                # --------------------------------------------

                overall_average = float(
                    valid_expenses["amount"].mean()
                )


                # --------------------------------------------
                # SPENDING DAYS
                # --------------------------------------------

                spending_days = int(
                    daily_totals.shape[0]
                )


                pattern_col1, pattern_col2 = st.columns(
                    2,
                    gap="medium"
                )


                with pattern_col1:

                    st.metric(
                        "Most Frequent Category",
                        str(
                            most_frequent_category
                        )
                    )


                    st.caption(
                        str(
                            most_frequent_count
                        )
                        + " transaction"
                        + (
                            "s"
                            if most_frequent_count != 1
                            else ""
                        )
                    )


                with pattern_col2:

                    st.metric(
                        "Highest Spending Day",
                        highest_day.strftime(
                            "%d %b %Y"
                        )
                    )


                    st.caption(
                        money(
                            highest_day_amount
                        )
                        + " spent that day."
                    )


                pattern_col3, pattern_col4 = st.columns(
                    2,
                    gap="medium"
                )


                with pattern_col3:

                    st.metric(
                        "Average Transaction",
                        money(
                            overall_average
                        )
                    )


                with pattern_col4:

                    st.metric(
                        "Spending Days",
                        str(
                            spending_days
                        )
                    )


        st.divider()


        # ====================================================
        # WHAT STANDS OUT
        # ====================================================

        st.markdown(
            '<div class="section-label">'
            'What Stands Out'
            '</div>',
            unsafe_allow_html=True
        )


        observations = []


        # ----------------------------------------------------
        # TODAY
        # ----------------------------------------------------

        if today_count > 0:

            observations.append(
                "You made "
                + str(
                    today_count
                )
                + " transaction"
                + (
                    "s"
                    if today_count != 1
                    else ""
                )
                + " today, totaling "
                + money(
                    today_total
                )
                + "."
            )


        # ----------------------------------------------------
        # MONTH CATEGORY
        # ----------------------------------------------------

        if (
            monthly is not None
            and month_categories
        ):

            observations.append(
                str(
                    top_month_category
                )
                + " is your biggest category this month."
            )


        # ----------------------------------------------------
        # MONTH COMPARISON
        # ----------------------------------------------------

        if comparison is not None:

            current_month_total = float(
                comparison.get(
                    "current_month",
                    {}
                ).get(
                    "total_spending",
                    0
                )
            )


            previous_month_total = float(
                comparison.get(
                    "previous_month",
                    {}
                ).get(
                    "total_spending",
                    0
                )
            )


            if previous_month_total > 0:

                if current_month_total > previous_month_total:

                    observations.append(
                        "You are spending more this month than last month."
                    )

                elif current_month_total < previous_month_total:

                    observations.append(
                        "You are spending less this month than last month."
                    )

                else:

                    observations.append(
                        "Your spending is similar to last month."
                    )


        # ----------------------------------------------------
        # YEAR
        # ----------------------------------------------------

        if year_count > 0:

            observations.append(
                "You have spent "
                + money(
                    year_total
                )
                + " so far this year."
            )


        if observations:

            for observation in observations[:3]:

                st.info(
                    observation
                )

        else:

            st.info(
                "Keep adding expenses to see useful spending patterns."
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