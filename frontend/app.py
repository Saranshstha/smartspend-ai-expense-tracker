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
# CUSTOM DESIGN + POLISH PACK (items 1-12)
# ============================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    :root {
        --paper: #151515;
        --paper-raised: #1B1B1B;
        --sidebar: #101010;
        --input-bg: #181818;
        --active-nav: #2D2D2D;
        --ink: #F2F2F0;
        --ink-soft: #9F9F9C;
        --ink-faint: #696965;
        --rule: #303030;
        --rule-hover: #444444;
        --brand: #5C8DFF;
        --brand-bright: #83A8FF;
        --brand-ink: #0B0F1A;
        --cat-food: #E2914F;
        --cat-transport: #6C9DE8;
        --cat-education: #B48AF0;
        --cat-shopping: #EC80A2;
        --cat-entertainment: #4FC9B8;
        --status-good: #5DAE7A;
        --status-watch: #D9A441;
        --status-near: #CF8B3F;
        --status-over: #CF564A;
        --font-main: "Inter", -apple-system, BlinkMacSystemFont, sans-serif;
        --barw: min(480px, calc(100vw - 20px));
    }

    html, body, [class*="css"] {
        font-family: var(--font-main);
        -webkit-font-smoothing: antialiased;
    }

    /* ITEM 7 — branded text selection + slim scrollbar */
    ::selection { background: color-mix(in srgb, var(--brand) 35%, transparent); color: var(--ink); }
    * { scrollbar-width: thin; scrollbar-color: #3a3a3a transparent; }
    *::-webkit-scrollbar { width: 9px; height: 9px; }
    *::-webkit-scrollbar-track { background: transparent; }
    *::-webkit-scrollbar-thumb { background: #333; border-radius: 9px; border: 2px solid var(--paper); }
    *::-webkit-scrollbar-thumb:hover { background: #444; }

    .stApp { background-color: var(--paper); color: var(--ink); }
    .main { background-color: var(--paper); }

    .block-container {
        width: 100%; max-width: none; margin: 0;
        padding: 2.5rem 3.5rem 4rem;
        transition: padding 0.2s ease;
    }

    header[data-testid="stHeader"] { background: transparent; }

    /* ========================================================
       SIDEBAR
       ======================================================== */
    section[data-testid="stSidebar"] {
        width: 260px !important;
        background-color: var(--sidebar);
        border-right: 1px solid #292929;
    }
    section[data-testid="stSidebar"] > div { padding-top: 0.8rem; padding-bottom: 1rem; }
    section[data-testid="stSidebar"] .block-container { padding: 0.8rem 0.85rem 1rem; }

    .sidebar-brand { font-size: 12px; font-weight: 700; letter-spacing: 0.08em; color: var(--ink); margin: 0.7rem 0 1.65rem 0.35rem; }
    .sidebar-section { font-size: 10px; font-weight: 600; letter-spacing: 0.08em; color: var(--ink-faint); text-transform: uppercase; margin: 1.25rem 0 0.55rem 0.35rem; }

    section[data-testid="stSidebar"] div.stButton { width: 100%; margin-bottom: 0.25rem; }
    section[data-testid="stSidebar"] div.stButton > button {
        position: relative;
        width: 100%; min-height: 40px; padding: 0.45rem 0.75rem;
        border-radius: 3px; border: 1px solid transparent;
        background: transparent; color: var(--ink-soft);
        font-size: 12.5px; font-weight: 500;
        display: flex; align-items: center; justify-content: flex-start; text-align: left;
        transition: background-color 0.18s ease, color 0.18s ease;
    }
    /* ITEM 5 — sliding left accent bar on sidebar buttons */
    section[data-testid="stSidebar"] div.stButton > button::before {
        content: ""; position: absolute; left: 0; top: 22%; bottom: 22%; width: 2.5px;
        border-radius: 0 2px 2px 0; background: var(--brand);
        transform: scaleY(0); transform-origin: center; transition: transform 0.22s cubic-bezier(0.34, 1.56, 0.64, 1);
    }
    section[data-testid="stSidebar"] div.stButton > button > div { width: 100%; display: flex; align-items: center; justify-content: flex-start; text-align: left; }
    section[data-testid="stSidebar"] div.stButton > button p { width: 100%; margin: 0; text-align: left; }
    section[data-testid="stSidebar"] div.stButton > button:hover { background-color: var(--paper-raised); color: var(--ink); }
    section[data-testid="stSidebar"] div.stButton > button:hover::before { transform: scaleY(1);}
    section[data-testid="stSidebar"] div.stButton > button:active { transform: scale(0.99); }
    section[data-testid="stSidebar"] div.stButton > button[kind="primary"] { background-color: var(--active-nav); color: var(--ink); font-weight: 600; }
    section[data-testid="stSidebar"] div.stButton > button[kind="primary"]::before { transform: scaleY(1); }
    section[data-testid="stSidebar"] div.stButton > button[kind="primary"]:hover { background-color: var(--active-nav); color: var(--ink); }

    .sidebar-info { color: var(--ink-faint); font-size: 11px; line-height: 1.55; margin: 2.2rem 0.35rem 0; padding-top: 1rem; border-top: 1px solid var(--rule); }

    section[data-testid="stSidebar"] button[data-testid="stSidebarCollapseButton"] { width: 36px; height: 36px; border-radius: 3px; transition: background-color 0.15s ease; }
    section[data-testid="stSidebar"] button[data-testid="stSidebarCollapseButton"]:hover { background-color: var(--paper-raised); }

    /* ========================================================
       HEADER / HERO / LABELS
       ======================================================== */
    .brand { font-size: 12px; font-weight: 700; letter-spacing: 0.08em; color: var(--ink); margin-bottom: 12px; }
    .hero-title { font-size: clamp(2.25rem, 5.4vw, 3.25rem); font-weight: 600; line-height: 1.05; letter-spacing: -0.035em; color: var(--ink); margin-bottom: 12px; }
    .hero-accent {
        background: linear-gradient(100deg, var(--brand) 0%, var(--brand-bright) 100%);
        -webkit-background-clip: text; background-clip: text; color: transparent;
    }
    .hero-subtitle { max-width: 680px; font-size: 18px; line-height: 1.6; color: var(--ink-soft); margin-bottom: 20px; }
    .section-label { font-size: 12px; font-weight: 600; letter-spacing: 0.08em; color: var(--ink-faint); text-transform: uppercase; margin-top: 10px; margin-bottom: 18px; }

    /* ========================================================
       COLUMNS / METRICS
       ======================================================== */
    [data-testid="column"] { padding-left: 0.5rem; padding-right: 0.5rem; }
    [data-testid="column"]:first-child { padding-left: 0; }
    [data-testid="column"]:last-child { padding-right: 0; }

    div[data-testid="stMetric"] {
        background: var(--paper-raised); border: 1px solid var(--rule); border-radius: 0;
        padding: 20px 22px; min-height: 112px; box-sizing: border-box;
        transition: border-color 0.2s ease, transform 0.2s ease, box-shadow 0.2s ease;
    }
    div[data-testid="stMetric"]:hover { border-color: var(--rule-hover); transform: translateY(-2px); box-shadow: 0 8px 24px rgba(0, 0, 0, 0.22); }
    
    div[data-testid="stMetricLabel"] { color: var(--ink-faint) !important; font-size: 11px !important; font-weight: 600 !important; text-transform: uppercase; letter-spacing: 0.06em; }
    /* ITEM 7 — tabular figures so digits don't jitter on update */
    div[data-testid="stMetricValue"] { color: var(--ink) !important; font-size: 1.7rem !important; font-weight: 600 !important; letter-spacing: -0.025em; font-variant-numeric: tabular-nums; font-feature-settings: "tnum"; }

    /* ========================================================
       INPUTS / BUTTONS
       ======================================================== */
    div[data-baseweb="input"] { background-color: var(--input-bg) !important; border: 1px solid var(--rule) !important; border-radius: 8px; min-height: 46px; transition: border-color 0.18s ease, box-shadow 0.18s ease; }
    div[data-baseweb="input"]:hover { border-color: var(--ink-soft) !important; }
    div[data-baseweb="input"]:focus-within { border-color: var(--brand) !important; box-shadow: 0 0 0 3px color-mix(in srgb, var(--brand) 18%, transparent); }
    div[data-baseweb="input"] input { background-color: transparent !important; color: var(--ink) !important; font-variant-numeric: tabular-nums; }
    div[data-baseweb="select"] > div { background-color: var(--input-bg) !important; border: 1px solid var(--rule) !important; border-radius: 8px; transition: border-color 0.18s ease; }
    div[data-baseweb="select"] > div:hover { border-color: var(--ink-soft) !important; }
    input, textarea { color: var(--ink) !important; }
    label[data-testid="stWidgetLabel"] p { color: var(--ink-soft) !important; font-size: 0.9rem; font-weight: 500; }

    .stButton > button {
        position: relative; overflow: hidden;
        min-height: 44px; border-radius: 6px; border: 1px solid var(--rule);
        background-color: transparent; color: var(--ink); font-weight: 600; padding: 0.4rem 1rem;
        transition: transform 0.15s ease, background-color 0.18s ease, border-color 0.18s ease, box-shadow 0.18s ease;
    }
    .stButton > button:hover { transform: translateY(-1px); border-color: var(--ink-soft); }
    .stButton > button:active { transform: translateY(0) scale(0.99); }
    div.stButton > button[kind="primary"] { background-color: var(--brand); color: var(--brand-ink); border-color: var(--brand); }
    div.stButton > button[kind="primary"]:hover { background-color: var(--brand-bright); border-color: var(--brand-bright); color: var(--brand-ink); box-shadow: 0 8px 22px color-mix(in srgb, var(--brand) 35%, transparent); }
    /* ITEM 5 — light sheen sweep across primary buttons on hover */
    /* Kill the sheen sweep on navigation buttons (sidebar + mobile nav) */
    section[data-testid="stSidebar"] div.stButton > button::after,
    [class*="st-key-mnav_slot_"] .stButton > button::after {
        content: none !important;
        display: none !important;
    }
    div.stButton > button[kind="secondary"] { background-color: transparent; color: var(--ink); border-color: var(--rule); }

    /* ========================================================
       TABLES / CHARTS / MISC
       ======================================================== */
    /* ITEM 6 — gradient hairline dividers */
    hr { border: none; height: 1px; background: linear-gradient(90deg, transparent, var(--rule) 18%, var(--rule) 82%, transparent); margin-top: 34px; margin-bottom: 34px; opacity: 1; }

    div[data-testid="stDataFrame"], div[data-testid="stDataEditor"] { border: 1px solid var(--rule) !important; border-radius: 0; overflow: hidden; margin-top: 10px; background-color: var(--paper-raised) !important; }
    [data-testid="stDataFrame"] [role="grid"], [data-testid="stDataEditor"] [role="grid"] { font-size: 0.9rem; background-color: var(--paper-raised) !important; }
    [data-testid="stDataFrame"] canvas, [data-testid="stDataEditor"] canvas { background-color: var(--paper-raised) !important; }

    [data-testid="stArrowVegaLiteChart"], [data-testid="stVegaLiteChart"] { background-color: var(--paper-raised); border: 1px solid var(--rule); border-radius: 0; padding: 0.7rem; }

    /* ITEM 4 — radar-pulse status dot */
    .status-dot { position: relative; display: inline-block; width: 7px; height: 7px; background-color: var(--brand); border-radius: 50%; margin-right: 7px; vertical-align: middle; }
    .status-dot::after { content: ""; position: absolute; inset: 0; border-radius: 50%; background: var(--brand); animation: radar 2.4s cubic-bezier(0, 0, 0.2, 1) infinite; }
    @keyframes radar { 0% { transform: scale(1); opacity: 0.55; } 70%, 100% { transform: scale(3.4); opacity: 0; } }
    .status-text { color: var(--ink-soft); font-size: 12px; }

    div[data-testid="stAlert"] { background-color: var(--paper-raised); border-radius: 0; border: 1px solid var(--rule); color: var(--ink); }
    div[data-testid="stExpander"] { background-color: var(--paper-raised); border: 1px solid var(--rule); border-radius: 0; }

    div[data-baseweb="popover"] { background-color: var(--input-bg); }
    div[data-baseweb="menu"] { background-color: var(--input-bg); border: 1px solid var(--rule); }
    div[data-baseweb="menu"] li { color: var(--ink); }
    div[data-baseweb="menu"] li:hover { background-color: var(--active-nav); }

    div[data-testid="stSlider"] { color: var(--ink); }
    .stCaption { color: var(--ink-faint) !important; }
    .footer { text-align: center; color: var(--ink-faint); font-size: 11px; padding-top: 10px; }

    /* ========================================================
       DASHBOARD LEGACY CLASSES
       ======================================================== */
    .dashboard-stat-card { background: var(--paper-raised); border: 1px solid var(--rule); border-radius: 0; min-height: 91px; padding: 16px 18px; display: flex; flex-direction: column; justify-content: center; }
    .dashboard-stat-label { color: var(--ink-faint); font-size: 10px; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 9px; }
    .dashboard-stat-value { color: var(--ink); font-size: 25px; font-weight: 600; line-height: 1.05; letter-spacing: -0.025em; font-variant-numeric: tabular-nums; }
    .dashboard-card { background: var(--paper-raised); border: 1px solid var(--rule); border-radius: 0; padding: 16px 20px; height: 100%; min-height: 300px; }
    .dashboard-card-title { color: var(--ink-faint); font-size: 10px; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; }
    .dashboard-category-name { color: var(--ink-soft); font-size: 12px; font-weight: 500; }
    .dashboard-category-amount { color: var(--ink-faint); font-size: 10px; font-variant-numeric: tabular-nums; }
    .dashboard-category-track { width: 100%; height: 8px; background: var(--rule); border-radius: 4px; overflow: hidden; }
    /* ITEM 3 — category bars grow from zero */
    .dashboard-category-bar { height: 100%; min-width: 4px; border-radius: 4px; width: 0; animation: barGrow 0.85s cubic-bezier(0.22, 1, 0.36, 1) forwards; }
    @keyframes barGrow { to { width: var(--w, 0%); } }
    .recent-expense-name { color: var(--ink); font-size: 12px; font-weight: 500; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
    .recent-expense-amount { color: var(--ink); font-size: 12px; font-weight: 600; font-variant-numeric: tabular-nums; }
    .recent-essential { display: inline-block; padding: 1px 5px; margin-left: 6px; border-radius: 2px; background: rgba(207,86,74,0.24); color: var(--status-over); font-size: 8px; font-weight: 600; vertical-align: middle; }
    .dashboard-empty-state { min-height: 220px; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; background: var(--paper-raised); border: 1px solid var(--rule); }
    .dashboard-empty-title { color: var(--ink); font-size: 14px; font-weight: 600; margin-bottom: 5px; }
    .dashboard-empty-text { color: var(--ink-faint); font-size: 11px; }

    /* ========================================================
       ITEM 1 — PAGE TRANSITION FADE-RISE
       ======================================================== */
    [class*="st-key-page_content"] { animation: pageIn 0.42s cubic-bezier(0.22, 1, 0.36, 1) both; }
    @keyframes pageIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: none; } }

    /* ========================================================
       ITEM 2 — STAGGERED ENTRANCE CASCADE
       ======================================================== */
    [class*="st-key-page_content"] [data-testid="stMetric"],
    [class*="st-key-page_content"] [data-testid="stVerticalBlockBorderWrapper"],
    [class*="st-key-page_content"] [data-testid="stDataFrame"],
    [class*="st-key-page_content"] [data-testid="stDataEditor"],
    [class*="st-key-page_content"] [data-testid="stArrowVegaLiteChart"],
    [class*="st-key-page_content"] [data-testid="stVegaLiteChart"] {
        animation: cardIn 0.5s cubic-bezier(0.22, 1, 0.36, 1) both;
    }
    [class*="st-key-page_content"] [data-testid="stMetric"]:nth-of-type(1),
    [class*="st-key-page_content"] [data-testid="stVerticalBlockBorderWrapper"]:nth-of-type(1) { animation-delay: 0.04s; }
    [class*="st-key-page_content"] [data-testid="stMetric"]:nth-of-type(2),
    [class*="st-key-page_content"] [data-testid="stVerticalBlockBorderWrapper"]:nth-of-type(2) { animation-delay: 0.09s; }
    [class*="st-key-page_content"] [data-testid="stMetric"]:nth-of-type(3),
    [class*="st-key-page_content"] [data-testid="stVerticalBlockBorderWrapper"]:nth-of-type(3) { animation-delay: 0.14s; }
    [class*="st-key-page_content"] [data-testid="stMetric"]:nth-of-type(4),
    [class*="st-key-page_content"] [data-testid="stVerticalBlockBorderWrapper"]:nth-of-type(4) { animation-delay: 0.19s; }
    [class*="st-key-page_content"] [data-testid="stMetric"]:nth-of-type(n+5),
    [class*="st-key-page_content"] [data-testid="stVerticalBlockBorderWrapper"]:nth-of-type(n+5) { animation-delay: 0.24s; }
    @keyframes cardIn { from { opacity: 0; transform: translateY(14px); } to { opacity: 1; transform: none; } }

    /* ========================================================
       ITEM 9 — SCROLL-DRIVEN REVEALS (Chrome/Edge, progressive)
       ======================================================== */
    @supports (animation-timeline: view()) {
        [class*="st-key-page_content"] section,
        [class*="st-key-page_content"] [data-testid="stExpander"] {
            animation: scrollReveal linear both;
            animation-timeline: view();
            animation-range: entry 0% entry 55%;
        }
        @keyframes scrollReveal { from { opacity: 0.25; transform: translateY(22px); } to { opacity: 1; transform: none; } }
    }

    /* ========================================================
       ITEM 10 — PREDICTION REVEAL CEREMONY
       ======================================================== */
    .pred-card { border: 1px solid var(--rule); background: var(--paper-raised); padding: 22px 24px; animation: predIn 0.5s cubic-bezier(0.34, 1.56, 0.64, 1) both; }
    @keyframes predIn { from { opacity: 0; transform: scale(0.96) translateY(8px); } to { opacity: 1; transform: none; } }
    .pred-chip { display: inline-flex; align-items: center; gap: 8px; font-size: 15px; font-weight: 600; color: var(--ink); animation: chipPop 0.5s cubic-bezier(0.34, 1.56, 0.64, 1) 0.12s both; }
    .pred-swatch { width: 11px; height: 11px; border-radius: 3px; display: inline-block; animation: swatchBloom 0.5s ease 0.18s both; }
    @keyframes chipPop { from { opacity: 0; transform: scale(0.7); } to { opacity: 1; transform: scale(1); } }
    @keyframes swatchBloom { from { transform: scale(0); } to { transform: scale(1); } }
    .pred-conf-track { height: 8px; background: var(--rule); border-radius: 4px; overflow: hidden; margin: 14px 0 6px; }
    .pred-conf-fill { height: 100%; border-radius: 4px; width: 0; animation: confFill 0.9s cubic-bezier(0.34, 1.56, 0.64, 1) 0.25s forwards; }
    @keyframes confFill { to { width: var(--conf, 0%); } }
    .pred-conf-label { font-size: 12px; color: var(--ink-faint); font-variant-numeric: tabular-nums; }

    /* ========================================================
       ITEM 11 — BRANDED SKELETON SHIMMER
       ======================================================== */
    .skel-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 16px; }
    .skel-card { height: 112px; border: 1px solid var(--rule); background: var(--paper-raised); position: relative; overflow: hidden; }
    .skel-card::after { content: ""; position: absolute; inset: 0; transform: translateX(-100%); background: linear-gradient(90deg, transparent, rgba(255,255,255,0.05), transparent); animation: shimmer 1.4s infinite; }
    @keyframes shimmer { 100% { transform: translateX(100%); } }

    /* ========================================================
       ITEM 12 — SLIDE-IN TOASTS
       ======================================================== */
    [data-testid="stToast"] { animation: toastIn 0.45s cubic-bezier(0.34, 1.56, 0.64, 1) both; border: 1px solid var(--rule) !important; background: var(--paper-raised) !important; }
    @keyframes toastIn { from { opacity: 0; transform: translateX(40px); } to { opacity: 1; transform: none; } }

    /* ========================================================
       MOBILE LAYOUT (GENERAL)
       ======================================================== */
    @media (min-width: 769px) {
        div:has(> [class*="st-key-mnav_bar"]),
        div:has(> [class*="st-key-mnav_slot_"]) {
            display: none !important; margin: 0 !important; padding: 0 !important;
        }
    }

    @media (max-width: 768px) {
        body { padding-bottom: 96px !important; }
        .block-container { width: 100% !important; max-width: 100% !important; margin: 0 !important; padding: 1.25rem 0.9rem 6.75rem !important; box-sizing: border-box !important; overflow-x: hidden !important; }
        section[data-testid="stSidebar"] { display: none !important; width: 0 !important; min-width: 0 !important; max-width: 0 !important; }
        button[data-testid="stSidebarCollapseButton"], button[data-testid="stSidebarCollapsedControl"] { display: none !important; }
        .hero-title { font-size: clamp(1.85rem, 8vw, 2.35rem) !important; line-height: 1.05 !important; }
        .hero-subtitle { max-width: 100% !important; font-size: 13px !important; line-height: 1.55 !important; }
        .brand { margin-bottom: 8px !important; }
        .section-label { margin-top: 6px !important; margin-bottom: 12px !important; }
        [data-testid="stHorizontalBlock"] { width: 100% !important; flex-wrap: wrap !important; gap: 0.7rem !important; }
        [data-testid="column"] { width: 100% !important; min-width: 100% !important; max-width: 100% !important; flex: 1 1 100% !important; padding-left: 0 !important; padding-right: 0 !important; box-sizing: border-box !important; }
        div[data-testid="stMetric"] { width: 100% !important; min-height: 96px !important; padding: 17px 18px !important; overflow: visible !important; box-sizing: border-box !important; }
        div[data-testid="stMetricValue"] { font-size: clamp(1.35rem, 7vw, 1.8rem) !important; line-height: 1.15 !important; white-space: nowrap !important; overflow: visible !important; text-overflow: clip !important; }
        div[data-testid="stMetricValue"] > div { white-space: nowrap !important; overflow: visible !important; }
        div[data-testid="stMetricLabel"] { white-space: normal !important; line-height: 1.25 !important; }
        div[data-baseweb="input"], div[data-baseweb="select"] > div { min-height: 48px !important; }
        .stButton > button { min-height: 46px !important; width: 100% !important; }
        div[role="radiogroup"] { flex-wrap: wrap !important; gap: 0.5rem !important; }
        div[data-testid="stDataFrame"], div[data-testid="stDataEditor"] { width: 100% !important; max-width: 100% !important; overflow-x: auto !important; -webkit-overflow-scrolling: touch; }
        [data-testid="stDataFrame"] [role="grid"], [data-testid="stDataEditor"] [role="grid"] { min-width: 620px; }
        [data-testid="stArrowVegaLiteChart"], [data-testid="stVegaLiteChart"], [data-testid="stLineChart"], [data-testid="stBarChart"] { width: 100% !important; max-width: 100% !important; overflow: hidden !important; }
    }

    /* ========================================================
       LIQUID BOTTOM NAV — FIXED SLOT LAYOUT (MOBILE ONLY)
       ======================================================== */
    [class*="st-key-mnav_bar"],
    [class*="st-key-mnav_slot_"] { display: none; }

    @media (max-width: 768px) {

        [class*="st-key-mnav_bar"] {
            display: block; position: fixed; bottom: 14px; left: 50%; transform: translateX(-50%);
            width: var(--barw); height: 64px; background: var(--paper-raised);
            border: 1px solid var(--rule); border-radius: 18px; box-shadow: 0 14px 36px rgba(0, 0, 0, 0.42);
            z-index: 99998; overflow: visible;
        }

        [class*="st-key-mnav_bar"] .stMarkdown,
        [class*="st-key-mnav_bar"] .stMarkdown > div {
            height: 0 !important; margin: 0 !important; padding: 0 !important;
            position: static !important; overflow: visible !important;
        }

        [class*="st-key-mnav_slot_"] {
            display: block; position: fixed; bottom: 14px; height: 64px;
            width: calc(var(--barw) / 5); z-index: 99999;
        }

        [class*="st-key-mnav_slot_0"] { left: calc(50vw - var(--barw) / 2); }
        [class*="st-key-mnav_slot_1"] { left: calc(50vw - var(--barw) / 2 + var(--barw) / 5); }
        [class*="st-key-mnav_slot_2"] { left: calc(50vw - var(--barw) / 2 + 2 * var(--barw) / 5); }
        [class*="st-key-mnav_slot_3"] { left: calc(50vw - var(--barw) / 2 + 3 * var(--barw) / 5); }
        [class*="st-key-mnav_slot_4"] { left: calc(50vw - var(--barw) / 2 + 4 * var(--barw) / 5); }

        [class*="st-key-mnav_slot_"] .stButton,
        [class*="st-key-mnav_slot_"] .stButton > button { width: 100% !important; }

        [class*="st-key-mnav_slot_"] .stButton > button {
            height: 64px !important; min-height: 64px !important; padding: 0 !important; margin: 0 !important;
            border: none !important; border-radius: 0 !important; background: transparent !important; box-shadow: none !important;
            color: var(--ink-faint) !important; font-size: 17px !important; line-height: 64px !important; font-weight: 500 !important;
            transition: color 0.12s ease, transform 0.12s ease;
        }

        [class*="st-key-mnav_slot_"] .stButton > button p { margin: 0 !important; width: 100% !important; text-align: center !important; font-size: 17px !important; line-height: 64px !important; }
        [class*="st-key-mnav_slot_"] .stButton > button:hover { color: var(--ink) !important; background: transparent !important; }
        [class*="st-key-mnav_slot_"] .stButton > button:active { transform: scale(0.94) !important; }

        [class*="st-key-mnav_slot_"] .stButton > button[kind="primary"] { background: transparent !important; }
        [class*="st-key-mnav_slot_"] .stButton > button[kind="primary"] p { visibility: hidden !important; }

        .liquid-indicator {
            position: absolute;
            top: -26px;
            left: 0;
            margin-left: -28px;
            width: 56px;
            z-index: 100000;
            pointer-events: none;
            transform: translateX(calc((var(--to) + 0.5) * (var(--barw) / 5)));
            will-change: transform;
            animation: var(--slide-anim, liquid-slide-a) 0.2s cubic-bezier(0.25, -0.15, 0.25, 1.15) both;
        }

        @keyframes liquid-slide-a {
            0%   { transform: translateX(calc((var(--from) + 0.5) * (var(--barw) / 5))); }
            100% { transform: translateX(calc((var(--to) + 0.5) * (var(--barw) / 5))); }
        }

        @keyframes liquid-slide-b {
            0%   { transform: translateX(calc((var(--from) + 0.5) * (var(--barw) / 5))); }
            100% { transform: translateX(calc((var(--to) + 0.5) * (var(--barw) / 5))); }
        }

        .li-ball {
            position: absolute; top: 0; left: 0; width: 56px; height: 56px; border-radius: 50%;
            background: var(--ink); color: var(--paper);
            display: flex; align-items: center; justify-content: center; font-size: 20px; line-height: 1;
            box-shadow: 0 0 0 5px var(--paper), 0 10px 22px rgba(0, 0, 0, 0.45);
            animation: var(--drop-anim, liquid-drop-a) 0.42s cubic-bezier(0.34, 1.56, 0.64, 1) both;
        }

        @keyframes liquid-drop-a { 0% { transform: scale(1.3, 0.7); } 45% { transform: scale(0.85, 1.15); } 75% { transform: scale(1.08, 0.92); } 100% { transform: scale(1, 1); } }
        @keyframes liquid-drop-b { 0% { transform: scale(1.3, 0.7); } 45% { transform: scale(0.85, 1.15); } 75% { transform: scale(1.08, 0.92); } 100% { transform: scale(1, 1); } }

        .liquid-indicator::before, .liquid-indicator::after {
            content: ""; position: absolute; top: 14px; width: 14px; height: 14px; background: var(--paper-raised);
        }
        .liquid-indicator::before { left: -13px; border-top-left-radius: 14px; }
        .liquid-indicator::after  { right: -13px; border-top-right-radius: 14px; }

        .li-label {
            position: absolute; top: 60px; left: 50%; transform: translateX(-50%);
            font-family: var(--font-main); font-size: 10px; font-weight: 600; letter-spacing: 0.02em;
            color: var(--ink); white-space: nowrap;
        }
    }

    @media (max-width: 420px) {
        :root { --barw: calc(100vw - 16px); }
        [class*="st-key-mnav_bar"], [class*="st-key-mnav_slot_"] { bottom: 10px; }
    }

    @media (prefers-reduced-motion: reduce) {
        *, *::before, *::after {
            scroll-behavior: auto !important;
            transition-duration: 0.01ms !important;
            animation-duration: 0.01ms !important;
            animation-iteration-count: 1 !important;
        }
    }
        /* ========================================================
       REMOVE BLUE OUTLINE + GLOW FADE ON SIDEBAR HOVER
       ======================================================== */
    section[data-testid="stSidebar"] div.stButton > button:hover {
        border-color: transparent !important;
        box-shadow: none !important;
    }

    section[data-testid="stSidebar"] div.stButton > button[kind="primary"]:hover {
        background-color: var(--active-nav) !important;
        border-color: transparent !important;
        box-shadow: none !important;
        color: var(--ink) !important;
        transform: none !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# FASTAPI CONFIGURATION
# ============================================================

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")


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

if "nav_prev" not in st.session_state:
    st.session_state.nav_prev = "Dashboard"

if "nav_tick" not in st.session_state:
    st.session_state.nav_tick = 0

if "pred_tick" not in st.session_state:
    st.session_state.pred_tick = 0


if st.session_state.clear_inputs:
    st.session_state.description_input = ""
    st.session_state.amount_input = 0.0
    st.session_state.clear_inputs = False


# ============================================================
# API FUNCTIONS
# ============================================================

def check_api():
    try:
        response = requests.get(API_URL + "/health", timeout=5)
        if response.status_code == 200:
            return response.json()
        return None
    except requests.RequestException:
        return None


def get_expenses():
    try:
        response = requests.get(API_URL + "/expenses", timeout=5)
        response.raise_for_status()
        data = response.json()
        return pd.DataFrame(data.get("expenses", []))
    except requests.RequestException:
        return None


def get_deleted_expenses():
    try:
        response = requests.get(API_URL + "/expenses/deleted", timeout=5)
        response.raise_for_status()
        return pd.DataFrame(response.json().get("expenses", []))
    except requests.RequestException:
        return None


def get_summary():
    try:
        response = requests.get(API_URL + "/summary", timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return None


def add_expense(description, amount, is_essential=False):
    try:
        response = requests.post(
            API_URL + "/predict",
            json={"description": description, "amount": amount, "is_essential": is_essential},
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.HTTPError:
        try:
            detail = response.json().get("detail", "Prediction failed.")
        except Exception:
            detail = "Prediction failed."
        return {"error": detail}
    except requests.RequestException:
        return {"error": "FastAPI backend could not be reached."}


def save_table_changes(expenses):
    try:
        response = requests.put(
            API_URL + "/expenses/update-table",
            json={"expenses": expenses},
            timeout=15
        )
        response.raise_for_status()
        return True, response.json()
    except requests.HTTPError:
        try:
            detail = response.json().get("detail", "Unable to update expenses.")
        except Exception:
            detail = "Unable to update expenses."
        return False, detail
    except requests.RequestException:
        return False, "FastAPI backend could not be reached."


def get_budget():
    try:
        response = requests.get(API_URL + "/budget", timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return None


def save_budget(monthly_budget):
    try:
        response = requests.put(API_URL + "/budget", json={"monthly_budget": monthly_budget}, timeout=5)
        response.raise_for_status()
        return True, response.json()
    except requests.HTTPError:
        try:
            detail = response.json().get("detail", "Unable to update budget.")
        except Exception:
            detail = "Unable to update budget."
        return False, detail
    except requests.RequestException:
        return False, "FastAPI backend could not be reached."


def get_monthly_analytics(year, month):
    try:
        response = requests.get(API_URL + "/analytics/monthly", params={"year": year, "month": month}, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return None


def get_weekly_analytics():
    try:
        response = requests.get(API_URL + "/analytics/weekly", timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return None


def get_monthly_trend(months=6):
    try:
        response = requests.get(API_URL + "/analytics/trend", params={"months": months}, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return None


def get_monthly_comparison(year, month):
    try:
        response = requests.get(API_URL + "/analytics/comparison", params={"year": year, "month": month}, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return None


def delete_expense(expense_id):
    try:
        response = requests.delete(API_URL + "/expenses/" + str(expense_id), timeout=5)
        response.raise_for_status()
        return True, ""
    except requests.HTTPError:
        try:
            detail = response.json().get("detail", "Unable to delete expense.")
        except Exception:
            detail = "Unable to delete expense."
        return False, detail
    except requests.RequestException:
        return False, "FastAPI backend could not be reached."


def restore_expense(expense_id):
    try:
        response = requests.post(API_URL + "/expenses/" + str(expense_id) + "/restore", timeout=5)
        response.raise_for_status()
        return True, ""
    except requests.HTTPError:
        try:
            detail = response.json().get("detail", "Unable to restore expense.")
        except Exception:
            detail = "Unable to restore expense."
        return False, detail
    except requests.RequestException:
        return False, "FastAPI backend could not be reached."


# ============================================================
# ITEM 11 — SKELETON SHIMMER HELPER
# ============================================================

CATEGORY_COLORS = {
    "Food": "#E2914F",
    "Shopping": "#EC80A2",
    "Transport": "#6C9DE8",
    "Entertainment": "#4FC9B8",
    "Education": "#B48AF0",
    "Health": "#CF564A",
    "Utilities": "#D9A441",
    "Other": "#8B8A7C",
}


def show_skeleton(cards=4):
    st.markdown(
        '<div class="skel-grid">' + '<div class="skel-card"></div>' * cards + '</div>',
        unsafe_allow_html=True,
    )


# ============================================================
# HEADER
# ============================================================

st.markdown('<div class="brand">SMARTSPEND</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-title">'
    'Manage expenses and '
    '<span class="hero-accent">analyze spending.</span>'
    '</div>',
    unsafe_allow_html=True
)
st.markdown('<div class="hero-subtitle"></div>', unsafe_allow_html=True)


# ============================================================
# API STATUS
# ============================================================

health = check_api()

if health:
    st.markdown(
        '<span class="status-dot"></span><span class="status-text">API connected</span>',
        unsafe_allow_html=True
    )
else:
    st.error("SmartSpend API is unavailable.")
    st.info("Start FastAPI with: `uvicorn backend.app.main:app --reload`")
    st.stop()


# ============================================================
# SIDEBAR NAVIGATION (DESKTOP)
# ============================================================

with st.sidebar:

    st.markdown('<div class="sidebar-brand">SMARTSPEND</div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section">Main</div>', unsafe_allow_html=True)

    navigation_items = [
        ("Dashboard", "⌂"),
        ("Add Expense", "＋"),
        ("Expenses", "▤"),
        ("Analytics", "◫"),
        ("Budget", "◈")
    ]

    for page_name, icon in navigation_items:
        is_selected = st.session_state.selected_page == page_name
        button_type = "primary" if is_selected else "secondary"

        if st.button(
            icon + "  " + page_name,
            use_container_width=True,
            type=button_type,
            key="sidebar_" + page_name.lower().replace(" ", "_")
        ):
            st.session_state.selected_page = page_name
            st.session_state.confirm_delete = False
            st.rerun()

    st.markdown('<div class="sidebar-section">Manage</div>', unsafe_allow_html=True)

    page_name = "Recently Deleted"
    is_selected = st.session_state.selected_page == page_name
    button_type = "primary" if is_selected else "secondary"

    if st.button("Recently Deleted", use_container_width=True, type=button_type, key="sidebar_recently_deleted"):
        st.session_state.selected_page = page_name
        st.session_state.confirm_delete = False
        st.rerun()

    st.markdown('<div class="sidebar-section">Legal</div>', unsafe_allow_html=True)

    legal_items = ["Privacy Policy", "Terms & Conditions"]

    for legal_page in legal_items:
        is_selected = st.session_state.selected_page == legal_page
        button_type = "primary" if is_selected else "secondary"

        if st.button(
            legal_page,
            use_container_width=True,
            type=button_type,
            key="sidebar_" + legal_page.lower().replace(" ", "_").replace("&", "and")
        ):
            st.session_state.selected_page = legal_page
            st.session_state.confirm_delete = False
            st.rerun()

    st.markdown('<div class="sidebar-info">SmartSpend<br>AI Expense Management</div>', unsafe_allow_html=True)


# ============================================================
# PAGE ROUTING (ITEM 1 target: page_content)
# ============================================================

page = st.session_state.selected_page

with st.container(key="page_content"):

    if page == "Dashboard":
        _ = show_dashboard(get_summary, get_expenses, get_budget)

    elif page == "Add Expense":
        _ = show_add_expense(add_expense)

    elif page == "Expenses":
        _ = show_expenses(get_expenses, save_table_changes, delete_expense)

    elif page == "Budget":
        _ = show_budget(get_budget, save_budget)

    elif page == "Recently Deleted":
        _ = show_recently_deleted(get_deleted_expenses, restore_expense)

    elif page == "Privacy Policy":

        st.markdown('<div class="section-label">Privacy Policy</div>', unsafe_allow_html=True)
        st.subheader("SmartSpend Privacy Policy")
        st.caption("Last updated: September 2026")
        st.write("This page explains how SmartSpend handles information entered into the application.")

        with st.expander("1. Information stored"):
            st.write("SmartSpend stores expense information needed to provide its features.")
        with st.expander("2. How information is used"):
            st.write("Stored expense information is used to categorize expenses and generate analytics.")
        with st.expander("3. Machine learning"):
            st.write("Expense descriptions may be processed by the local machine learning model.")
        with st.expander("4. Deleted expenses"):
            st.write("Deleted expenses are kept in Recently Deleted for up to 15 days.")
        with st.expander("5. Data sharing"):
            st.write("This project does not intentionally sell or share expense records with third parties.")
        with st.expander("6. Security"):
            st.write("SmartSpend uses application and database controls appropriate for the current project.")
        with st.expander("7. Contact"):
            st.write("For questions about this project, use the contact details supplied by the project owner.")

    elif page == "Terms & Conditions":

        st.markdown('<div class="section-label">Terms & Conditions</div>', unsafe_allow_html=True)
        st.subheader("SmartSpend Terms & Conditions")
        st.caption("Last updated: September 2026")
        st.write("These terms describe the intended use of the SmartSpend project.")

        with st.expander("1. Intended use"):
            st.write("SmartSpend is intended to help users record and review expenses.")
        with st.expander("2. AI predictions"):
            st.write("Expense categories and confidence scores are generated by a machine learning model.")
        with st.expander("3. Analytics"):
            st.write("Analytics and projections are informational tools, not financial advice.")
        with st.expander("4. User responsibility"):
            st.write("Users are responsible for the accuracy of information they enter.")
        with st.expander("5. Deleted expenses"):
            st.write("Deleted expenses may be restored during the 15-day retention period.")
        with st.expander("6. Availability"):
            st.write("The project may be unavailable during maintenance or deployment changes.")
        with st.expander("7. Changes"):
            st.write("These terms may be updated as SmartSpend changes.")

    elif page == "Analytics":
        _ = show_analytics(
            get_expenses,
            get_monthly_analytics,
            get_weekly_analytics,
            get_monthly_trend,
            get_monthly_comparison,
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
    '<div class="footer">SmartSpend · FastAPI · Machine Learning · SQLite</div>',
    unsafe_allow_html=True
)


# ============================================================
# MOBILE BOTTOM NAVIGATION (rendered LAST)
# ============================================================

mobile_navigation_items = [
    ("Dashboard", "⌂", "Home"),
    ("Expenses", "▤", "Expenses"),
    ("Add Expense", "＋", "Add"),
    ("Analytics", "◫", "Analytics"),
    ("Budget", "◈", "Budget"),
]

page_order = [name for name, _, _ in mobile_navigation_items]

current = st.session_state.selected_page
prev = st.session_state.nav_prev

anim_suffix = "a" if st.session_state.nav_tick % 2 == 0 else "b"

with st.container(key="mnav_bar"):

    if current in page_order:

        to_idx = page_order.index(current)
        from_idx = page_order.index(prev) if prev in page_order else to_idx

        active_icon = ""
        active_label = ""
        for name, icon, label in mobile_navigation_items:
            if name == current:
                active_icon = icon
                active_label = label

        st.markdown(
            f'<div class="liquid-indicator" '
            f'style="--from:{from_idx}; --to:{to_idx}; '
            f'--slide-anim:liquid-slide-{anim_suffix}; '
            f'--drop-anim:liquid-drop-{anim_suffix};">'
            f'<span class="li-ball">{active_icon}</span>'
            f'<span class="li-label">{active_label}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )

for index, (page_name, icon, label) in enumerate(mobile_navigation_items):

    with st.container(key="mnav_slot_" + str(index)):

        if st.button(
            icon,
            use_container_width=True,
            type=(
                "primary"
                if current == page_name
                else "secondary"
            ),
            key="mobile_nav_" + page_name.lower().replace(" ", "_")
        ):
            if current in page_order:
                st.session_state.nav_prev = current
            st.session_state.nav_tick = st.session_state.nav_tick + 1
            st.session_state.selected_page = page_name
            st.session_state.confirm_delete = False
            st.rerun()

if current in page_order:
    st.session_state.nav_prev = current