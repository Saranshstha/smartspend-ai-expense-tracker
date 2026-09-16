# streamlit run frontend\app.py

import os
from datetime import datetime

import pandas as pd
import requests
import streamlit as st

from dashboard import show_dashboard
from add_expense import show_add_expense
from expenses import show_expenses
from analytics import show_analytics
from budget import show_budget
from recently_deleted import show_recently_deleted



 
# PAGE CONFIGURATION
 

st.set_page_config(
    page_title="SmartSpend",
    page_icon="favicon.png",
    layout="wide",
    initial_sidebar_state="expanded"
)


 
# CUSTOM DESIGN
 

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
            0.7rem
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
       MOBILE LAYOUT
       ======================================================== */

    [class*="st-key-mobile_bottom_nav"] {

        display: none;
    }

    @media (max-width: 768px) {

        /* Keep the main content inside the phone viewport. */
        .block-container {

            width: 100% !important;

            max-width: 100% !important;

            margin: 0 !important;

            padding: 1.25rem 0.9rem 6.75rem !important;

            box-sizing: border-box !important;

            overflow-x: hidden !important;
        }

        /* The desktop sidebar is replaced by the bottom navigation. */
        section[data-testid="stSidebar"] {

            display: none !important;

            width: 0 !important;

            min-width: 0 !important;

            max-width: 0 !important;
        }

        button[data-testid="stSidebarCollapseButton"],
        button[data-testid="stSidebarCollapsedControl"] {

            display: none !important;
        }

        .hero-title {

            font-size: clamp(1.85rem, 8vw, 2.35rem) !important;

            line-height: 1.08 !important;

            word-break: normal !important;
        }

        .hero-subtitle {

            max-width: 100% !important;

            font-size: 13px !important;

            line-height: 1.55 !important;
        }

        .brand {

            margin-bottom: 8px !important;
        }

        .section-label {

            margin-top: 6px !important;

            margin-bottom: 12px !important;
        }

        /* Streamlit column groups should become a vertical mobile stack. */
        [data-testid="stHorizontalBlock"] {

            width: 100% !important;

            flex-wrap: wrap !important;

            gap: 0.7rem !important;
        }

        [data-testid="column"] {

            width: 100% !important;

            min-width: 100% !important;

            max-width: 100% !important;

            flex: 1 1 100% !important;

            padding-left: 0 !important;

            padding-right: 0 !important;

            box-sizing: border-box !important;
        }

        /* Prevent metric values from being clipped or hidden on narrow screens. */
        div[data-testid="stMetric"] {

            width: 100% !important;

            min-height: 96px !important;

            padding: 17px 18px !important;

            overflow: visible !important;

            box-sizing: border-box !important;
        }

        div[data-testid="stMetricValue"] {

            font-size: clamp(1.35rem, 7vw, 1.8rem) !important;

            line-height: 1.15 !important;

            white-space: nowrap !important;

            overflow: visible !important;

            text-overflow: clip !important;
        }

        div[data-testid="stMetricValue"] > div {

            white-space: nowrap !important;

            overflow: visible !important;
        }

        div[data-testid="stMetricLabel"] {

            white-space: normal !important;

            line-height: 1.25 !important;
        }

        /* Touch-friendly inputs and controls. */
        div[data-baseweb="input"],
        div[data-baseweb="select"] > div {

            min-height: 48px !important;
        }

        .stButton > button {

            min-height: 46px !important;

            width: 100% !important;
        }

        div[role="radiogroup"] {

            flex-wrap: wrap !important;

            gap: 0.5rem !important;
        }

        /* Keep wide tables usable by allowing horizontal scrolling inside their card. */
        div[data-testid="stDataFrame"],
        div[data-testid="stDataEditor"] {

            width: 100% !important;

            max-width: 100% !important;

            overflow-x: auto !important;

            -webkit-overflow-scrolling: touch;
        }

        [data-testid="stDataFrame"] [role="grid"],
        [data-testid="stDataEditor"] [role="grid"] {

            min-width: 620px;
        }

        /* Charts stay inside the viewport. */
        [data-testid="stArrowVegaLiteChart"],
        [data-testid="stVegaLiteChart"],
        [data-testid="stLineChart"],
        [data-testid="stBarChart"] {

            width: 100% !important;

            max-width: 100% !important;

            overflow: hidden !important;
        }

        /* --------------------------------------------------------
           MOBILE BOTTOM NAVIGATION
           -------------------------------------------------------- */

        [class*="st-key-mobile_bottom_nav"] {

            display: block;

            position: fixed;

            left: 10px;

            right: 10px;

            bottom: calc(env(safe-area-inset-bottom, 0px) + 10px);

            z-index: 999999;

            padding: 7px;

            border: 1px solid rgba(255, 255, 255, 0.10);

            border-radius: 24px;

            background: rgba(12, 12, 12, 0.97);

            box-shadow:
                0 18px 40px rgba(0, 0, 0, 0.44),
                0 4px 12px rgba(0, 0, 0, 0.26),
                inset 0 1px 0 rgba(255, 255, 255, 0.05);

            -webkit-backdrop-filter: blur(18px) saturate(125%);

            backdrop-filter: blur(18px) saturate(125%);

            overflow: visible;

            transform: translateZ(0);

            -webkit-transform: translateZ(0);

            isolation: isolate;
        }

        [class*="st-key-mobile_bottom_nav"]::before {

            content: "";

            position: absolute;

            left: 18px;

            right: 18px;

            top: 0;

            height: 1px;

            background: linear-gradient(
                90deg,
                transparent,
                rgba(255, 255, 255, 0.12),
                transparent
            );

            pointer-events: none;
        }

        [class*="st-key-mobile_bottom_nav"] [data-testid="stHorizontalBlock"] {

            display: grid !important;

            grid-template-columns: repeat(5, minmax(0, 1fr)) !important;

            align-items: end !important;

            gap: 2px !important;

            width: 100% !important;
        }

        [class*="st-key-mobile_bottom_nav"] [data-testid="column"] {

            position: relative !important;

            width: auto !important;

            min-width: 0 !important;

            max-width: none !important;

            flex: none !important;

            padding: 0 !important;
        }

        [class*="st-key-mobile_bottom_nav"] .stButton,
        [class*="st-key-mobile_bottom_nav"] .stButton > button {

            width: 100% !important;
        }

        [class*="st-key-mobile_bottom_nav"] .stButton > button {

            position: relative !important;

            min-height: 64px !important;

            height: 64px !important;

            padding: 9px 1px 7px !important;

            margin: 0 !important;

            border: 1px solid transparent !important;

            border-radius: 17px !important;

            background: transparent !important;

            color: #858585 !important;

            box-shadow: none !important;

            font-size: 9px !important;

            line-height: 1.08 !important;

            font-weight: 600 !important;

            letter-spacing: 0.01em !important;

            white-space: pre-line !important;

            overflow: visible !important;

            -webkit-tap-highlight-color: transparent;

            transition:
                color 0.16s ease,
                background-color 0.16s ease,
                border-color 0.16s ease,
                transform 0.16s ease,
                box-shadow 0.16s ease;
        }

        [class*="st-key-mobile_bottom_nav"] .stButton > button p {

            margin: 0 !important;

            width: 100% !important;

            text-align: center !important;

            white-space: pre-line !important;

            word-break: keep-all !important;

            overflow-wrap: normal !important;
        }

        [class*="st-key-mobile_bottom_nav"] .stButton > button:hover {

            background: rgba(255, 255, 255, 0.045) !important;

            border-color: rgba(255, 255, 255, 0.06) !important;

            color: #FFFFFF !important;

            transform: translateY(-1px) !important;

            box-shadow: 0 7px 16px rgba(0, 0, 0, 0.18) !important;
        }

        [class*="st-key-mobile_bottom_nav"] .stButton > button:active {

            transform: scale(0.96) !important;
        }

        [class*="st-key-mobile_bottom_nav"] .stButton > button[kind="primary"] {

            background: rgba(255, 255, 255, 0.105) !important;

            border-color: rgba(255, 255, 255, 0.08) !important;

            color: #FFFFFF !important;

            box-shadow:
                inset 0 0 0 1px rgba(255, 255, 255, 0.025),
                0 5px 14px rgba(0, 0, 0, 0.19) !important;
        }

        [class*="st-key-mobile_bottom_nav"] .stButton > button[kind="primary"]::after {

            content: "";

            position: absolute;

            left: 50%;

            bottom: 4px;

            width: 4px;

            height: 4px;

            transform: translateX(-50%);

            border-radius: 50%;

            background: #FFFFFF;

            opacity: 0.9;
        }

        /* Raised central Add action. */
        [class*="st-key-mobile_bottom_nav"] [data-testid="column"]:nth-child(3) {

            z-index: 3 !important;
        }

        [class*="st-key-mobile_bottom_nav"] [data-testid="column"]:nth-child(3) .stButton > button {

            padding-top: 31px !important;

            color: #BEBEBE !important;

            background: transparent !important;

            border-color: transparent !important;

            box-shadow: none !important;
        }

        [class*="st-key-mobile_bottom_nav"] [data-testid="column"]:nth-child(3) .stButton > button::before {

            content: "+";

            position: absolute;

            left: 50%;

            top: -25px;

            width: 56px;

            height: 56px;

            transform: translateX(-50%);

            display: flex;

            align-items: center;

            justify-content: center;

            border-radius: 50%;

            background: #FFFFFF;

            color: #111111;

            border: 5px solid #0C0C0C;

            box-shadow:
                0 9px 24px rgba(0, 0, 0, 0.46),
                0 0 0 1px rgba(255, 255, 255, 0.10);

            font-size: 28px;

            font-weight: 400;

            line-height: 1;

            transition:
                transform 0.16s ease,
                box-shadow 0.16s ease;
        }

        [class*="st-key-mobile_bottom_nav"] [data-testid="column"]:nth-child(3) .stButton > button:hover::before {

            transform: translateX(-50%) translateY(-2px) scale(1.04);

            box-shadow:
                0 12px 28px rgba(0, 0, 0, 0.48),
                0 0 0 1px rgba(255, 255, 255, 0.12);
        }

        [class*="st-key-mobile_bottom_nav"] [data-testid="column"]:nth-child(3) .stButton > button:active::before {

            transform: translateX(-50%) scale(0.94);
        }

        [class*="st-key-mobile_bottom_nav"] [data-testid="column"]:nth-child(3) .stButton > button[kind="primary"] {

            background: rgba(255, 255, 255, 0.045) !important;

            color: #FFFFFF !important;
        }

        @media (max-width: 420px) {

            [class*="st-key-mobile_bottom_nav"] {

                left: 7px;

                right: 7px;

                bottom: calc(env(safe-area-inset-bottom, 0px) + 7px);

                padding: 6px;

                border-radius: 21px;
            }

            [class*="st-key-mobile_bottom_nav"] .stButton > button {

                min-height: 58px !important;

                height: 58px !important;

                font-size: 8.7px !important;
            }

            [class*="st-key-mobile_bottom_nav"] [data-testid="column"]:nth-child(3) .stButton > button::before {

                width: 51px;

                height: 51px;

                top: -21px;
            }
        }

    @media (prefers-reduced-motion: reduce) {

        *,
        *::before,
        *::after {

            scroll-behavior: auto !important;

            transition-duration: 0.01ms !important;

            animation-duration: 0.01ms !important;

            animation-iteration-count: 1 !important;
        }
    }

    </style>
    """,
    unsafe_allow_html=True
)


 
# FASTAPI CONFIGURATION
 

API_URL = os.getenv(
    "API_URL",
    "http://127.0.0.1:8000"
)


 
# SESSION STATE
 

if "prediction_result" not in st.session_state:

    st.session_state.prediction_result = None


if "clear_inputs" not in st.session_state:

    st.session_state.clear_inputs = False


if "confirm_delete" not in st.session_state:

    st.session_state.confirm_delete = False


if "selected_page" not in st.session_state:

    st.session_state.selected_page = "Dashboard"


 
# CLEAR INPUTS AFTER SUCCESSFUL PREDICTION
 

if st.session_state.clear_inputs:

    st.session_state.description_input = ""

    st.session_state.amount_input = 0.0

    st.session_state.clear_inputs = False


 
# API FUNCTIONS
 

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


 
# HEADER
 

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


 
# API STATUS
 

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
        "`uvicorn backend.app.main:app --reload`"
    )

    st.stop()


 
# SIDEBAR NAVIGATION
 

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

        st.query_params["page"] = page_name

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


 
# MOBILE BOTTOM NAVIGATION
 

mobile_navigation_items = [
    ("Dashboard", "⌂", "Home"),
    ("Expenses", "▤", "Expenses"),
    ("Add Expense", "", "Add"),
    ("Analytics", "◫", "Analytics"),
    ("Budget", "◈", "Budget")
]

# Use real Streamlit buttons instead of HTML links.
# This keeps navigation inside the same Streamlit session and
# prevents mobile taps from opening a new browser tab.
with st.container(key="mobile_bottom_nav"):

    nav_columns = st.columns(5, gap="small")

    for index, (page_name, icon, label) in enumerate(
        mobile_navigation_items
    ):

        with nav_columns[index]:

            button_label = icon + "\n" + label

            if st.button(
                button_label,
                use_container_width=True,
                type=(
                    "primary"
                    if st.session_state.selected_page == page_name
                    else "secondary"
                ),
                key="mobile_nav_" + page_name.lower().replace(" ", "_")
            ):

                st.session_state.selected_page = page_name
                st.session_state.confirm_delete = False
                st.rerun()


 
# CURRENT PAGE
 

page = st.session_state.selected_page


 
# PAGE CONTENT

# ============================================================
# PAGE ROUTING
# ============================================================

page = st.session_state.selected_page

with st.container(key="page_content"):

    if page == "Dashboard":
        show_dashboard(
            get_summary,
            get_expenses,
            get_budget,
        )

    elif page == "Add Expense":
        show_add_expense(add_expense)

    elif page == "Expenses":
        show_expenses(
            get_expenses,
            save_table_changes,
            delete_expense,
        )

    elif page == "Budget":
        show_budget(
            get_budget,
            save_budget,
        )

    elif page == "Recently Deleted":
        show_recently_deleted(
            get_deleted_expenses,
            restore_expense,
        )

    # PRIVACY POLICY
     

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


     
    # TERMS & CONDITIONS
     

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


     

    elif page == "Analytics":
        show_analytics(
            get_expenses,
            get_monthly_analytics,
            get_weekly_analytics,
            get_monthly_trend,
            get_monthly_comparison,
        )

# FOOTER
 

st.divider()

st.markdown(
    '<div class="footer">'
    'SmartSpend · FastAPI · Machine Learning · SQLite'
    '</div>',
    unsafe_allow_html=True
)
