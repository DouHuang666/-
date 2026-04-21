import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
from scipy.stats import norm
from datetime import datetime
import requests
import time

st.set_page_config(page_title="宠物IP联名产品库存智能决策系统", layout="wide", page_icon="🐾")

st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">', unsafe_allow_html=True)

# ========== CSS ==========
st.markdown("""
<style>
    :root {
        --primary: #1f6e8c;
        --primary-light: #2c7da0;
        --primary-dark: #0a3b4b;
        --gray-bg: #f4f8fc;
        --card-bg: #ffffff;
        --text-dark: #1e2a3e;
        --text-light: #4a627a;
        --border-light: #e2edf2;
        --shadow-sm: 0 4px 12px rgba(0, 0, 0, 0.03);
        --shadow-md: 0 8px 24px rgba(0, 0, 0, 0.05);
        --radius-lg: 28px;
        --radius-md: 20px;
        --radius-sm: 12px;
    }

    body, .stApp {
        background: var(--gray-bg);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        color: var(--text-dark);
    }

    [data-testid="stApp"] {
        padding-top: 0 !important;
    }

    .top-brand {
        background: white;
        border-radius: var(--radius-md);
        padding: 12px 24px;
        margin-top: 0;
        margin-bottom: 20px;
        box-shadow: var(--shadow-sm);
        border: 1px solid var(--border-light);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .brand-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: var(--primary-dark);
    }
    .brand-title i {
        margin-right: 8px;
        color: var(--primary);
    }
    .brand-version {
        font-size: 0.8rem;
        color: var(--text-light);
    }
    .brand-date {
        font-size: 0.8rem;
        color: var(--text-light);
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0b2b3b 0%, #06212b 100%);
        border-right: 1px solid #1c4e62;
        overflow-x: visible !important;
    }
    
    [data-testid="stSidebar"] .stNumberInput input,
    [data-testid="stSidebar"] .stSelectbox div,
    [data-testid="stSidebar"] .stSlider [data-testid="stThumbValue"],
    [data-testid="stSidebar"] .stMarkdown,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stCheckbox span,
    [data-testid="stSidebar"] .stExpander p,
    [data-testid="stSidebar"] .stExpander summary {
        color: #e6f7ff !important;
    }
    
    .sidebar-nav-title h3 {
        color: #ffffff !important;
    }
    
    [data-testid="stSidebar"] .stNumberInput input,
    [data-testid="stSidebar"] .stSelectbox div,
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] {
        background-color: #1f4b5c !important;
        border: 1px solid #2c6e86 !important;
        border-radius: var(--radius-sm) !important;
        color: #e6f7ff !important;
    }
    div[data-baseweb="popover"] ul {
        background-color: #1f4b5c !important;
        border: 1px solid #2c6e86 !important;
        border-radius: var(--radius-sm) !important;
    }
    div[data-baseweb="popover"] li {
        color: #e6f7ff !important;
    }
    div[data-baseweb="popover"] li:hover {
        background-color: #2c6e86 !important;
    }
    
    div[data-testid="stSidebar"] div[data-testid="stButton"] button,
    div[data-testid="stSidebar"] div[data-testid="stButton"] button * {
        color: #000000 !important;
        font-weight: 600 !important;
    }
    div[data-testid="stSidebar"] div[data-testid="stButton"] button:hover,
    div[data-testid="stSidebar"] div[data-testid="stButton"] button:hover * {
        color: white !important;
    }
    div[data-testid="stSidebar"] div[data-testid="stButton"] button[kind="primary"],
    div[data-testid="stSidebar"] div[data-testid="stButton"] button[kind="primary"] * {
        color: white !important;
    }
    
    div[data-testid="stSidebar"] .stButton button {
        background: #1f4b5c;
        border-radius: 40px !important;
        padding: 8px 18px !important;
        margin-bottom: 10px;
        transition: all 0.2s ease;
        border: none;
        text-align: left;
        width: 100%;
    }
    div[data-testid="stSidebar"] .stButton button:hover {
        background: #2c6e86;
        transform: translateX(6px);
    }
    div[data-testid="stSidebar"] .stButton button[kind="primary"] {
        background: var(--primary-light) !important;
        box-shadow: 0 0 0 2px rgba(44, 125, 160, 0.3);
        border-left: 3px solid #ffcd7e;
    }

    .main-card {
        background: var(--card-bg);
        border-radius: var(--radius-lg);
        padding: 24px;
        margin-bottom: 32px;
        box-shadow: var(--shadow-md);
        border: 1px solid var(--border-light);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .main-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 16px 32px -12px rgba(0, 0, 0, 0.12);
    }

    .metric-card {
        background: white;
        border-radius: var(--radius-md);
        padding: 1.2rem;
        text-align: center;
        box-shadow: var(--shadow-sm);
        border: 1px solid var(--border-light);
        height: 100%;
    }
    .metric-value {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, var(--primary), var(--primary-light));
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
    }
    .metric-label {
        font-size: 0.85rem;
        color: var(--text-light);
        margin-top: 6px;
    }

    .param-dashboard {
        display: flex;
        justify-content: space-between;
        gap: 16px;
        margin-bottom: 24px;
    }
    .param-item {
        background: white;
        border-radius: var(--radius-md);
        padding: 12px 16px;
        flex: 1;
        text-align: center;
        box-shadow: var(--shadow-sm);
        border: 1px solid var(--border-light);
    }
    .param-label {
        font-size: 0.7rem;
        color: var(--text-light);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .param-value {
        font-size: 1.2rem;
        font-weight: 700;
        color: var(--primary);
        margin-top: 4px;
    }

    .feature-card {
        background: white;
        border-radius: var(--radius-md);
        padding: 10px 12px;
        text-align: center;
        box-shadow: var(--shadow-sm);
        border: 1px solid var(--border-light);
        transition: all 0.2s;
        height: 100%;
    }
    .feature-card:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-md);
    }
    .feature-icon {
        font-size: 1.2rem;
        color: var(--primary);
        margin-bottom: 4px;
    }
    .feature-label {
        font-size: 0.65rem;
        color: var(--text-light);
        text-transform: uppercase;
    }
    .feature-value {
        font-size: 1rem;
        font-weight: 700;
        color: var(--primary-dark);
        margin-top: 4px;
    }

    .demand-type-card {
        background: white;
        border-radius: var(--radius-md);
        padding: 16px;
        text-align: center;
        box-shadow: var(--shadow-md);
        border: 1px solid var(--border-light);
        margin-top: 20px;
    }
    .demand-type-label {
        font-size: 0.7rem;
        color: var(--text-light);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .demand-type-value {
        font-size: 1.2rem;
        font-weight: 800;
        margin-top: 8px;
    }

    .decision-card {
        background: white;
        border-radius: var(--radius-md);
        padding: 16px 12px;
        text-align: center;
        box-shadow: var(--shadow-sm);
        border: 1px solid var(--border-light);
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .decision-value {
        font-size: 1.6rem;
        font-weight: 800;
        color: var(--primary);
    }
    .decision-label {
        font-size: 0.7rem;
        color: var(--text-light);
        margin-top: 6px;
    }
    .decision-delta {
        font-size: 0.7rem;
        margin-top: 4px;
    }

    .cost-card {
        background: white;
        border-radius: var(--radius-md);
        padding: 16px;
        text-align: center;
        box-shadow: var(--shadow-sm);
        border: 1px solid var(--border-light);
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .cost-value {
        font-size: 1.5rem;
        font-weight: 800;
        color: var(--primary);
        margin: 8px 0;
    }
    .cost-label {
        font-size: 0.7rem;
        color: var(--text-light);
    }
    .cost-sub {
        font-size: 0.75rem;
        font-weight: 700;
        color: var(--primary-dark);
        margin-top: 4px;
    }

    .custom-table {
        border-radius: var(--radius-md);
        overflow-x: auto;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
        background: white;
        border: 1px solid #eef2f7;
        margin-bottom: 20px;
    }
    .custom-table table {
        width: 100%;
        border-collapse: collapse;
        font-family: 'Inter', sans-serif;
        font-size: 0.7rem !important;
    }
    .custom-table th {
        background: linear-gradient(135deg, var(--primary), var(--primary-light)) !important;
        color: white !important;
        font-weight: 700 !important;
        padding: 10px 8px !important;
        font-size: 0.7rem !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        text-align: center !important;
        border: none !important;
    }
    .custom-table td {
        background: white !important;
        padding: 8px 6px !important;
        border-bottom: 1px solid #f0f2f7 !important;
        color: var(--text-dark);
        text-align: center !important;
        font-size: 0.7rem !important;
        vertical-align: middle;
    }
    .custom-table tbody tr:nth-child(even) td {
        background: #fafcff !important;
    }
    .custom-table tbody tr:hover td {
        background: #eef4fa !important;
        transition: background 0.15s ease;
        box-shadow: inset 0 0 0 1px rgba(31, 110, 140, 0.15);
    }
    .custom-table tbody tr td:first-child {
        background: transparent !important;
    }
    .custom-table tbody tr:hover td:first-child {
        background: transparent !important;
        box-shadow: none !important;
    }

    /* 需求类型胶囊标签 - 细化配色 */
    .badge-demand-trend-up { background: #e0f2fe; color: #0369a1; }
    .badge-demand-trend-down { background: #fee2e2; color: #991b1b; }
    .badge-demand-fluctuation { background: #e5e7eb; color: #374151; }
    .badge-demand-stable { background: #d1fae5; color: #065f46; }
    .badge-demand-intermittent { background: #e0e7ff; color: #3730a3; }
    .badge-demand-default { background: #f3f4f6; color: #1f2937; }

    .priority-high { background: #fee2e2; color: #b91c1c; font-weight: 700; }
    .priority-mid { background: #fef08a; color: #854d0e; font-weight: 700; }
    .priority-low { background: #dcfce7; color: #166534; font-weight: 700; }
    
    .trend-positive { color: #16a34a; font-weight: 700; }
    .trend-negative { color: #dc2626; font-weight: 700; }
    
    .highlight-number {
        font-weight: 800;
        color: #2c7da0;
        font-size: 0.75rem;
    }
    .reorder-highlight {
        font-weight: 800;
        color: #f97316;
        font-size: 0.75rem;
    }
    .prediction-highlight {
        font-weight: 800;
        color: #2c7da0;
        font-size: 0.75rem;
    }
    
    .days-warning { color: #dc2626; font-weight: 700; }
    .days-normal { color: #16a34a; }

    .cost-badge-positive { background: #fee2e2; color: #b91c1c; font-weight: 600; padding: 2px 8px; border-radius: 20px; display: inline-block; }
    .cost-badge-zero { background: #e2e8f0; color: #475569; font-weight: 600; padding: 2px 8px; border-radius: 20px; display: inline-block; }

    .optimal-highlight {
        font-weight: 800;
        color: #16a34a;
    }

    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    ::-webkit-scrollbar-track {
        background: #e2e8f0;
        border-radius: 10px;
    }
    ::-webkit-scrollbar-thumb {
        background: var(--primary-light);
        border-radius: 10px;
    }

    .stButton button {
        border-radius: 40px !important;
        font-weight: 600 !important;
        padding: 0.4rem 1.2rem !important;
        transition: all 0.2s;
        border: none;
    }
    .stButton button[kind="primary"] {
        background: linear-gradient(95deg, var(--primary), var(--primary-light));
        color: white;
        box-shadow: 0 4px 12px rgba(31, 110, 140, 0.3);
    }
    .stButton button[kind="primary"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(31, 110, 140, 0.4);
    }
    .stButton button:active {
        transform: scale(0.98);
    }

    div[data-testid="stFileUploader"] {
        background: #f8fafc;
        border: 2px dashed var(--border-light);
        border-radius: var(--radius-md);
        padding: 1rem;
        transition: all 0.2s;
    }
    div[data-testid="stFileUploader"]:hover {
        border-color: var(--primary);
        background: #f0f9ff;
    }

    .stSlider [data-baseweb="slider"] {
        accent-color: var(--primary);
    }
    .stCheckbox {
        accent-color: var(--primary);
    }

    .help-icon {
        position: relative;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 16px;
        height: 16px;
        border-radius: 50%;
        background-color: #cbd5e1;
        color: #1e2a3e;
        font-size: 10px;
        font-weight: bold;
        cursor: help;
        transition: background 0.2s;
        margin-left: 8px;
        vertical-align: middle;
        flex-shrink: 0;
    }
    .help-icon:hover {
        background-color: var(--primary-light);
        color: white;
    }
    .help-icon .tooltip-text {
        visibility: hidden;
        width: 220px;
        background-color: #1e2a3e;
        color: #fff;
        text-align: center;
        border-radius: 6px;
        padding: 5px 8px;
        position: absolute;
        z-index: 9999;
        top: 50%;
        right: 100%;
        margin-right: 8px;
        transform: translateY(-50%);
        font-size: 12px;
        font-weight: normal;
        white-space: normal;
        word-wrap: break-word;
        opacity: 0;
        transition: opacity 0.2s;
        pointer-events: none;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    }
    .help-icon:hover .tooltip-text {
        visibility: visible;
        opacity: 1;
    }

    .hero-banner h1,
    .hero-banner p {
        color: white !important;
    }
    .hero-banner {
        background: linear-gradient(115deg, var(--primary-dark) 0%, var(--primary) 100%);
        padding: 1.8rem;
        border-radius: var(--radius-lg);
        margin-bottom: 2rem;
        box-shadow: 0 12px 24px -12px rgba(0, 0, 0, 0.2);
    }

    .stAlert {
        border-radius: var(--radius-md);
        border-left: 4px solid var(--primary);
    }

    h1:not(.hero-banner h1) {
        font-size: 24px !important;
        font-weight: 700 !important;
        color: var(--primary-dark) !important;
    }
    h2 {
        font-size: 18px !important;
        font-weight: 600 !important;
        color: var(--text-dark) !important;
        margin-top: 0 !important;
    }
    h3 {
        font-size: 16px !important;
        font-weight: 600 !important;
        color: var(--text-dark) !important;
    }
    
    /* ========== 确保 AI 助手所有文字为白色（用户和助手消息） ========== */
    .stChatMessage, .stChatMessage p, .stChatMessage div, .stChatMessage span, .stChatMessage strong, .stChatMessage em {
        color: #ffffff !important;
    }
    
    /* 侧边栏 expander 展开时的标题背景改为青蓝色（保持原有样式） */
    [data-testid="stSidebar"] .stExpander details[open] summary {
        background-color: #2c7da0 !important;
        color: #ffffff !important;
    }
    [data-testid="stSidebar"] .stExpander details summary {
        background-color: #1f4b5c !important;
        color: #e6f7ff !important;
    }
    [data-testid="stSidebar"] .streamlit-expanderHeader[aria-expanded="true"] {
        background-color: #2c7da0 !important;
        color: #ffffff !important;
    }
    [data-testid="stSidebar"] .streamlit-expanderHeader {
        background-color: #1f4b5c !important;
        color: #e6f7ff !important;
    }
</style>
""", unsafe_allow_html=True)

# ========== 辅助函数 ==========
def render_table(df, add_serial=True):
    df_copy = df.copy()
    if add_serial:
        df_copy.insert(0, '序号', range(1, len(df_copy)+1))
    
    if '需求类型' in df_copy.columns:
        def demand_type_badge(t):
            if pd.isna(t): return t
            t_str = str(t)
            if '趋势型需求（增长）' in t_str:
                return f'<span class="badge badge-demand-trend-up"><i class="fas fa-chart-line" style="margin-right: 4px;"></i> {t_str}</span>'
            elif '趋势型需求（衰退）' in t_str:
                return f'<span class="badge badge-demand-trend-down"><i class="fas fa-chart-line" style="margin-right: 4px;"></i> {t_str}</span>'
            elif '轻缓波动型需求' in t_str:
                return f'<span class="badge badge-demand-fluctuation"><i class="fas fa-water" style="margin-right: 4px;"></i> {t_str}</span>'
            elif '平稳型需求' in t_str:
                return f'<span class="badge badge-demand-stable"><i class="fas fa-balance-scale" style="margin-right: 4px;"></i> {t_str}</span>'
            elif '间歇型（块状）需求' in t_str:
                return f'<span class="badge badge-demand-intermittent"><i class="fas fa-hourglass-half" style="margin-right: 4px;"></i> {t_str}</span>'
            else:
                return f'<span class="badge badge-demand-default"><i class="fas fa-tag" style="margin-right: 4px;"></i> {t_str}</span>'
        df_copy['需求类型'] = df_copy['需求类型'].apply(demand_type_badge)
    
    if '优先级' in df_copy.columns:
        def priority_badge(p):
            if pd.isna(p): return p
            p_str = str(p)
            if '高' in p_str:
                return '<span class="badge priority-high"><i class="fas fa-circle" style="color: #b91c1c; font-size: 0.65rem; margin-right: 4px;"></i> 高</span>'
            elif '中' in p_str:
                return '<span class="badge priority-mid"><i class="fas fa-circle" style="color: #eab308; font-size: 0.65rem; margin-right: 4px;"></i> 中</span>'
            elif '低' in p_str:
                return '<span class="badge priority-low"><i class="fas fa-circle" style="color: #16a34a; font-size: 0.65rem; margin-right: 4px;"></i> 低</span>'
            else:
                return p_str
        df_copy['优先级'] = df_copy['优先级'].apply(priority_badge)
    
    if '趋势强度' in df_copy.columns:
        def trend_style(val):
            try:
                v = float(val)
                if v > 0:
                    return f'<span class="trend-positive">▲ {v:.2f}</span>'
                elif v < 0:
                    return f'<span class="trend-negative">▼ {v:.2f}</span>'
                else:
                    return f'{v:.2f}'
            except:
                return val
        df_copy['趋势强度'] = df_copy['趋势强度'].apply(trend_style)
    
    reorder_col = None
    for col in ['建议补货量', '建议补货']:
        if col in df_copy.columns:
            reorder_col = col
            break
    if reorder_col:
        def highlight_reorder(x):
            if pd.isna(x): return x
            try:
                val = float(x)
                if val == int(val): val = int(val)
                return f'<strong class="reorder-highlight">{val}</strong>'
            except:
                return x
        df_copy[reorder_col] = df_copy[reorder_col].apply(highlight_reorder)
    
    if '预测销量' in df_copy.columns:
        def highlight_pred(x):
            if pd.isna(x): return x
            try:
                val = float(x)
                if val == int(val): val = int(val)
                return f'<strong class="prediction-highlight">{val}</strong>'
            except:
                return x
        df_copy['预测销量'] = df_copy['预测销量'].apply(highlight_pred)
    
    if '库存可售天数' in df_copy.columns:
        def days_style(day):
            try:
                d = float(day)
                if d < 7:
                    return f'<span class="days-warning">{d:.1f} 天</span>'
                else:
                    return f'<span class="days-normal">{d:.1f} 天</span>'
            except:
                return day
        df_copy['库存可售天数'] = df_copy['库存可售天数'].apply(days_style)
    
    if '理论最优服务水平(%)' in df_copy.columns:
        def highlight_optimal(val):
            try:
                v = float(val)
                return f'<span class="optimal-highlight">{v:.1f}%</span>'
            except:
                return val
        df_copy['理论最优服务水平(%)'] = df_copy['理论最优服务水平(%)'].apply(highlight_optimal)
    
    if '成本增加(%)' in df_copy.columns:
        def cost_badge(val):
            try:
                v_str = str(val).replace('%', '')
                v = float(v_str)
                if v > 0:
                    return f'<span class="cost-badge-positive">▲ {v:.1f}%</span>'
                else:
                    return f'<span class="cost-badge-zero">{v:.1f}%</span>'
            except:
                return val
        df_copy['成本增加(%)'] = df_copy['成本增加(%)'].apply(cost_badge)
    
    if '行动建议' in df_copy.columns:
        def action_badge(text):
            if pd.isna(text): return text
            text_str = str(text)
            if '立即下单' in text_str:
                return f'<span class="badge priority-high"><i class="fas fa-shopping-cart" style="margin-right: 4px;"></i> {text_str}</span>'
            elif '紧急补货' in text_str:
                return f'<span class="badge priority-high"><i class="fas fa-exclamation-triangle" style="margin-right: 4px;"></i> {text_str}</span>'
            elif '建议促销' in text_str or '调拨' in text_str:
                return f'<span class="badge priority-mid"><i class="fas fa-tags" style="margin-right: 4px;"></i> {text_str}</span>'
            elif '无需操作' in text_str:
                return f'<span class="badge priority-low"><i class="fas fa-check-circle" style="margin-right: 4px;"></i> {text_str}</span>'
            else:
                return f'<span class="badge badge-demand-default">{text_str}</span>'
        df_copy['行动建议'] = df_copy['行动建议'].apply(action_badge)
    
    html = df_copy.to_html(index=False, escape=False)
    st.markdown(f'<div class="custom-table">{html}</div>', unsafe_allow_html=True)

def param_with_help(control_func, help_text):
    col1, col2 = st.columns([6, 1])
    with col1: control_func()
    with col2: st.markdown(f'<div class="help-icon">?<span class="tooltip-text">{help_text}</span></div>', unsafe_allow_html=True)

def card(content_func):
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    content_func()
    st.markdown('</div>', unsafe_allow_html=True)

# ========== 业务函数 ==========
def classify_demand_type(row):
    p = row['平均需求间隔p']; t = row['趋势强度T']; cv = row['CV']; fs = row['季节系数Fs']; f_ip = row['IP系数F_IP']; mu_nz = row.get('非零需求均值', row['需求均值μ'])
    if any(pd.isna(x) for x in [p, t, cv, fs, f_ip, mu_nz]): return '特征缺失'
    if p >= 1.32:
        if 0.4 < cv < 0.8: return '间歇型（块状）需求' if mu_nz < 10 else '平稳型需求（低频稳定）'
        else: return '轻缓波动型需求'
    if abs(t) > 0.01: return '趋势型需求（增长）' if t > 0 else '趋势型需求（衰退）'
    else:
        if cv >= 0.6 and (fs >= 1.2 or f_ip >= 1.4): return '波动型需求'
        else: return '平稳型需求'

def compute_optimal_z(b, h, L):
    if b + h * L == 0: return 1.645
    alpha = b / (b + h * L)
    if alpha >= 1: return 3.0
    if alpha <= 0: return 0.0
    return norm.ppf(alpha)

def holt_exponential_smoothing(series, alpha, beta, forecast_steps=1):
    n = len(series)
    if n == 0: return 0
    if n == 1: return series[0]
    level = series[0]; trend = series[1] - series[0] if n > 1 else 0
    for t in range(1, n):
        last_level = level
        level = alpha * series[t] + (1 - alpha) * (level + trend)
        trend = beta * (level - last_level) + (1 - beta) * trend
    return level + forecast_steps * trend

def simple_exponential_smoothing(series, alpha, forecast_steps=1):
    if len(series) == 0: return 0
    s = series[0]
    for val in series[1:]: s = alpha * val + (1 - alpha) * s
    return s

def compute_features_from_window(sales_window, season_days, off_season_days, ip_days, non_ip_days,
                                 season_pos, off_season_pos, ip_pos, non_ip_pos):
    n = len(sales_window); mu = np.mean(sales_window)
    if n >= 6:
        recent_avg = np.mean(sales_window[-3:]); early_avg = np.mean(sales_window[:3])
        T = (recent_avg - early_avg) / early_avg if early_avg != 0 else 0
    else: T = 0
    if season_pos == "末尾": season_slice = sales_window[-season_days:] if n >= season_days else sales_window
    else: season_slice = sales_window[:season_days] if n >= season_days else sales_window
    if off_season_pos == "末尾": off_season_slice = sales_window[-off_season_days:] if n >= off_season_days else sales_window
    else: off_season_slice = sales_window[:off_season_days] if n >= off_season_days else sales_window
    season_avg = np.mean(season_slice); off_season_avg = np.mean(off_season_slice)
    Fs = season_avg / off_season_avg if off_season_avg != 0 else 1.0
    if ip_pos == "末尾": ip_slice = sales_window[-ip_days:] if n >= ip_days else sales_window
    else: ip_slice = sales_window[:ip_days] if n >= ip_days else sales_window
    if non_ip_pos == "末尾": non_ip_slice = sales_window[-non_ip_days:] if n >= non_ip_days else sales_window
    else: non_ip_slice = sales_window[:non_ip_days] if n >= non_ip_days else sales_window
    ip_avg = np.mean(ip_slice); non_ip_avg = np.mean(non_ip_slice)
    F_IP = ip_avg / non_ip_avg if non_ip_avg != 0 else 1.0
    return mu, T, Fs, F_IP, non_ip_avg

def predict_sku_with_model(train_series, model_type, forecast_days, params, features):
    mu = features['mu']; T = features['T']; Fs = features['Fs']; F_IP = features['F_IP']; non_ip_mean = features['non_ip_mean']
    if params.get('future_no_ip', False) and model_type in ["霍尔特双参数+IP调整", "基础平稳+IP缓冲"]:
        base_val = non_ip_mean * params.get('persist_factor', 1.0)
    else: base_val = mu
    if model_type == "加权移动平均":
        if len(train_series) >= 3:
            recent_3 = train_series[-3:]
            pred_daily = recent_3[0]*params['w1'] + recent_3[1]*params['w2'] + recent_3[2]*params['w3']
        else: pred_daily = base_val
        return pred_daily * forecast_days
    elif model_type == "霍尔特双参数+IP调整":
        holt_pred = holt_exponential_smoothing(train_series, params['alpha'], params['beta'], forecast_steps=1)
        adjust = min(F_IP, params['ip_cap'])
        return holt_pred * adjust * forecast_days
    elif model_type == "季节调整移动平均":
        fs_used = params.get('fs_override', 0.0) if params.get('fs_override', 0.0) > 0 else Fs
        if len(train_series) >= 3: avg_3 = np.mean(train_series[-3:])
        else: avg_3 = mu
        return avg_3 * fs_used * forecast_days
    elif model_type == "基础平稳+IP缓冲":
        adjust = 1 + (F_IP - 1) / params['buffer_factor']
        return base_val * adjust * forecast_days
    elif model_type == "简单指数平滑+衰退系数":
        ses_pred = simple_exponential_smoothing(train_series, params['alpha'], forecast_steps=1)
        decay = 1 - abs(T)
        return ses_pred * decay * forecast_days
    elif model_type == "朴素预测+批量调整":
        non_zero = train_series[train_series > 0]
        last_nonzero = non_zero[-1] if len(non_zero) > 0 else mu
        batch = max(last_nonzero * params['batch_mult'], params['min_order'])
        weeks = forecast_days / 7.0
        return batch * weeks
    else: return mu * forecast_days

def compute_inventory_advice(row, period_days, params, service_level_override=None):
    dtype = row['需求类型']; mu_d = row['预测销量'] / period_days; sigma_d = row['需求标准差σ']; L = row['提前期']
    cur_stock = row['当前总库存']; P = row['采购价']; R = row['零售价']; theta = row['缺货成本']; C_w = row['仓储成本']; r = row['资金占用成本']
    B = R * theta; H = (P * r + C_w * 12) / 365
    if service_level_override is not None:
        CSL = service_level_override; z_opt = norm.ppf(CSL)
    else:
        if params['use_cost_optimization']: z_opt = compute_optimal_z(B, H, L)
        else: z_opt = params['fixed_z']
        CSL = norm.cdf(z_opt)
    if dtype in ['间歇型（块状）需求', '平稳型需求（低频稳定）', '轻缓波动型需求']:
        strategy = '(T,S)'; SS = 0; S = mu_d * params['intermittent_cycle'] * params['trend_factor']
        qty = max(0, S - cur_stock) if cur_stock < S else 0
        avg_inv = (S + cur_stock) / 2 if S else cur_stock
        daily_cost = H * max(0, avg_inv); ROP_display = '-'; S_display = round(S, 0) if S else '-'
    elif dtype in ['平稳型需求', '波动型需求']:
        strategy = '(R,Q)'; SS = 0; ROP = mu_d * L; K = params.get('K', 100.0)
        Q = np.sqrt(2 * mu_d * K / H) if H > 0 else mu_d * L
        qty = max(0, Q) if cur_stock <= ROP else 0
        avg_inv = (ROP + cur_stock) / 2 if ROP else cur_stock
        daily_cost = H * max(0, avg_inv); ROP_display = round(ROP, 0); S_display = '-'
    else:
        strategy = '(s,S)'; SS = z_opt * sigma_d * np.sqrt(L); ROP = mu_d * L + SS
        S = mu_d * (L + params['safety_cycle']) * params['trend_factor'] + SS
        qty = max(0, S - cur_stock) if cur_stock <= ROP else 0
        I_bar = mu_d * L + SS + 0.5 * mu_d * params['safety_cycle'] * params['trend_factor']
        if sigma_d > 0:
            z_ss = SS / (sigma_d * np.sqrt(L)) if sigma_d * np.sqrt(L) > 0 else 0
            U_bar = sigma_d * np.sqrt(L) * (norm.pdf(z_ss) - z_ss * (1 - norm.cdf(z_ss)))
        else: U_bar = 0
        daily_cost = H * I_bar + B * U_bar / L; ROP_display = round(ROP, 0); S_display = round(S, 0)
    if qty > 0: priority = '高' if theta >= 0.18 else '中'
    else:
        if (strategy in ['(R,Q)', '(s,S)'] and cur_stock > 1.5 * ROP) or dtype in ['趋势型需求（衰退）']: priority = '低'
        else: priority = '低'
    return pd.Series({'策略': strategy, '安全库存': round(SS, 0) if SS is not None else '-', '订货点': ROP_display, '目标库存': S_display,
                      '建议补货量': round(qty, 0), '优先级': priority, '服务水平': round(CSL*100, 1), '期望日总成本': round(daily_cost, 2)})

def short_name(name):
    name_map = {
        "Hello Kitty迷你派对系列装饰头套": "Hello Kitty头套", "史努比缤纷生活系列宠物胸背牵引绳套装": "史努比牵引绳",
        "迪士尼疯狂动物城系列宠物头套(尼克)": "尼克头套", "哈利·波特系列猫薄荷组合玩具": "哈利波特猫薄荷",
        "迪士尼史迪奇系列宠物胸背牵引绳套装": "史迪奇牵引绳", "迪士尼疯狂动物城系列宠物零食犬用棒棒糖, 朱迪, 鸡肉山羊奶味": "朱迪棒棒糖",
        "迪士尼疯狂动物城系列宠物零食猫用爪爪冻干(羊副市长)": "羊副市长冻干", "迪士尼疯狂动物城系列宠物零食猫用爪爪冻干(朱迪)": "朱迪冻干",
        "迪士尼疯狂动物城系列宠物零食猫用爪爪冻干(闪电)": "闪电冻干"
    }
    return name_map.get(name, name)

# ========== 初始化 session_state ==========
if 'daily_df' not in st.session_state:
    st.session_state.daily_df = None
    st.session_state.inv_df = None
    st.session_state.base_df = None
    st.session_state.features_computed = False
    st.session_state.forecast_df = None
    st.session_state.result_df = None
    st.session_state.page = "概览"
    st.session_state.season_pos = "末尾"
    st.session_state.season_days = 7
    st.session_state.off_season_pos = "开头"
    st.session_state.off_season_days = 7
    st.session_state.ip_pos = "末尾"
    st.session_state.ip_days = 7
    st.session_state.non_ip_pos = "开头"
    st.session_state.non_ip_days = 21
    st.session_state.manual_model_dict = {}

# ========== 主页面顶部品牌区 ==========
st.markdown(f"""
<div class="top-brand">
    <div>
        <span class="brand-title"><i class="fas fa-paw"></i> 宠物IP联名产品库存智能决策系统</span>
        <span class="brand-version"> V2.0</span>
    </div>
    <div class="brand-date">{datetime.now().strftime("%Y年%m月%d日 %A")}</div>
</div>
""", unsafe_allow_html=True)

# ========== 侧边栏导航 ==========
st.sidebar.markdown('<div class="sidebar-nav-title"><h3><i class="fas fa-compass" style="margin-right: 8px;"></i> 导航</h3></div>', unsafe_allow_html=True)

nav_options = ["概览", "数据上传", "特征分析", "需求预测", "库存优化", "决策建议"]
current_page = st.session_state.page

def set_page(page_name):
    st.session_state.page = page_name

for option in nav_options:
    if option == current_page:
        st.sidebar.button(option, key=f"nav_{option}", use_container_width=True, type="primary", on_click=set_page, args=(option,))
    else:
        st.sidebar.button(option, key=f"nav_{option}", use_container_width=True, on_click=set_page, args=(option,))

st.sidebar.markdown('<hr>', unsafe_allow_html=True)
# ========== AI 助手（侧边栏，导航下方，参数面板上方） ==========
if "xiaoku_msgs" not in st.session_state:
    st.session_state.xiaoku_msgs = [{"role": "assistant", "content": "👋 你好！我是小库。我可以解答本系统的指标含义、参数设置、预测模型、库存策略等问题。"}]

# 优先从 secrets 读取 API Key，如果没有则 session_state 中为空
if "xiaoku_api_key" not in st.session_state or not st.session_state.xiaoku_api_key:
    st.session_state.xiaoku_api_key = st.secrets.get("DEEPSEEK_API_KEY", "")

with st.sidebar:
    st.markdown("""
    <style>
        .streamlit-expanderHeader .fa-robot {
            font-size: 1.3rem;
            margin-right: 8px;
            vertical-align: middle;
        }
    </style>
    """, unsafe_allow_html=True)
    with st.expander(" AI 小库 · 智能问答", expanded=False):
        col1, col2 = st.columns([6, 1])
        with col2:
            if st.button("清空", key="clear_chat_btn", help="清空所有对话记录"):
                st.session_state.xiaoku_msgs = [{"role": "assistant", "content": "👋 对话已清空，有问题随时问我~"}]
                st.rerun()
        for msg in st.session_state.xiaoku_msgs:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
        
        user_q = st.chat_input("输入你的问题...", key="xiaoku_chat_input")
        if user_q:
            st.session_state.xiaoku_msgs.append({"role": "user", "content": user_q})
            st.rerun()
        
        if st.session_state.xiaoku_msgs and st.session_state.xiaoku_msgs[-1]["role"] == "user":
            last_q = st.session_state.xiaoku_msgs[-1]["content"]
            
            # 如果没有 API Key，则提示用户配置 secrets 或手动输入
            if not st.session_state.xiaoku_api_key:
                st.info("🔐 未检测到 DeepSeek API Key。请按以下方式配置：\n\n1. 在项目根目录创建 `.streamlit/secrets.toml` 文件，写入：\n   `DEEPSEEK_API_KEY = \"你的密钥\"`\n2. 或者在下方的输入框中临时输入（刷新页面会丢失）")
                key_input = st.text_input("临时 API Key（刷新丢失）", type="password", placeholder="sk-...", key="temp_key_input")
                if st.button("使用此 Key", key="use_temp_key"):
                    if key_input.startswith("sk-"):
                        st.session_state.xiaoku_api_key = key_input
                        st.rerun()
                    else:
                        st.error("Key 格式错误，应以 sk- 开头")
                st.stop()
            
            # 增强版系统提示词（融入论文知识）
            system_prompt = """
你是宠物IP联名产品库存智能决策系统的AI助理“小库”。你的知识库包含以下论文核心内容：

【系统背景】
本系统专为C公司宠物IP联名产品设计，集成了数据上传、需求特征分析、需求类型自动划分、6种预测模型（加权移动平均、霍尔特双参数+IP调整、季节调整移动平均、基础平稳+IP缓冲、简单指数平滑+衰退系数、朴素预测+批量调整）、滚动窗口交叉验证自动选模、报童模型最优安全库存、差异化补货策略((T,S)/(R,Q)/(s,S))、库存风险可视化等功能。

【核心指标解释】
- CV (需求变异系数) = 标准差/均值，CV≥0.6表示高波动。
- 平均需求间隔 p = 总天数/非零需求天数，p≥1.32为间歇型。
- 趋势强度 T = (最近3期平均 - 最早3期平均)/最早3期平均，|T|>0.01视为有趋势。
- 季节系数 Fs = 旺季销量/淡季销量，≥1.2有明显季节波动。
- IP营销波动系数 F_IP = IP营销月销量/非营销月销量，用于放大预测。
- 报童模型：最优服务水平 = B/(B+H*L)，B为缺货成本，H为日持有成本，L为提前期。
- 补货策略：(T,S)固定周期补货；(R,Q)连续检查订货点批量；(s,S)连续检查补至目标库存。

【参数设置建议】
- 平滑系数α、β：默认0.3、0.2，需求稳定可降低，波动大可提高。
- 趋势放大系数：增长型需求建议1.2~1.5。
- IP调整上限：默认1.8，避免过度放大。
- 自定义服务水平：提高会增加安全库存和持有成本，系统会显示与理论最优的差额。

【系统操作说明】
- 上传销售数据和库存数据后，系统自动计算特征并分类。
- 在“需求预测”页可启动滚动验证自动选择最优模型。
- 在“库存优化”页可生成补货建议，并对比自定义服务水平与理论最优的成本差异。
- 决策建议页展示待办行动清单和库存风险矩阵。

【优化结果】
- 优化后9个SKU平均预测误差从80.38%降至19.79%。
- 库存日总成本从113.12元降至45.19元，节约60.05%。
- 朱迪棒棒糖等IP热点产品节约比例达71.19%以上。

【约束】
- 只回答与需求预测、库存管理、本系统操作相关的问题。
- 拒绝回答无关话题（如天气、饮食等）。
- 回答要清晰、专业、简洁，适当使用列表或分点。

请记住你是小库，用友好热情的语气帮助用户。
"""
            messages = [{"role": "system", "content": system_prompt}]
            for m in st.session_state.xiaoku_msgs[-10:]:
                messages.append({"role": m["role"], "content": m["content"]})
            
            headers = {
                "Authorization": f"Bearer {st.session_state.xiaoku_api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "deepseek-chat",
                "messages": messages,
                "stream": False,
                "temperature": 0.7,
                "max_tokens": 800
            }
            
            max_retries = 2
            retry_delay = 2
            reply = None
            for attempt in range(max_retries + 1):
                try:
                    with st.spinner("思考中..."):
                        resp = requests.post("https://api.deepseek.com/v1/chat/completions", json=payload, headers=headers, timeout=60)
                        if resp.status_code == 200:
                            reply = resp.json()["choices"][0]["message"]["content"]
                            break
                        else:
                            reply = f"❌ API 错误 ({resp.status_code}): {resp.text}"
                            break
                except requests.exceptions.Timeout:
                    if attempt < max_retries:
                        time.sleep(retry_delay)
                        continue
                    else:
                        reply = "❌ 请求超时，请稍后重试（DeepSeek 服务可能繁忙）。"
                except Exception as e:
                    reply = f"❌ 请求失败: {str(e)}"
                    break
            
            if reply is None:
                reply = "❌ 多次重试后仍失败，请检查网络或稍后再试。"
            
            st.session_state.xiaoku_msgs.append({"role": "assistant", "content": reply})
            st.rerun()

# ========== 动态参数面板 ==========
if st.session_state.page == "数据上传":
    with st.sidebar.expander("⚙️ 特征计算参数", expanded=False):
        param_with_help(lambda: setattr(st.session_state, 'season_pos', st.selectbox("旺季位置", ["末尾", "开头"], index=1)), "选择旺季数据在时间窗口的末尾或开头")
        param_with_help(lambda: setattr(st.session_state, 'season_days', st.number_input("旺季天数", 1, 30, 7)), "用于计算旺季平均销量的天数")
        param_with_help(lambda: setattr(st.session_state, 'off_season_pos', st.selectbox("淡季位置", ["末尾", "开头"], index=0)), "选择淡季数据的位置")
        param_with_help(lambda: setattr(st.session_state, 'off_season_days', st.number_input("淡季天数", 1, 30, 7)), "用于计算淡季平均销量的天数")
        param_with_help(lambda: setattr(st.session_state, 'ip_pos', st.selectbox("IP影响期位置", ["末尾", "开头"], index=0)), "IP联名活动期间的数据位置")
        param_with_help(lambda: setattr(st.session_state, 'ip_days', st.number_input("IP影响天数", 1, 30, 7)), "IP活动持续天数")
        param_with_help(lambda: setattr(st.session_state, 'non_ip_pos', st.selectbox("非IP期位置", ["末尾", "开头"], index=1)), "非IP期间数据的位置")
        param_with_help(lambda: setattr(st.session_state, 'non_ip_days', st.number_input("非IP影响天数", 1, 30, 21)), "用于对比的非IP期天数")
elif st.session_state.page == "需求预测":
    with st.sidebar.expander("📈 预测模型参数", expanded=False):
        param_with_help(lambda: setattr(st.session_state, 'period', st.number_input("预测天数", 1, 90, 14)), "需要预测的未来天数")
        param_with_help(lambda: setattr(st.session_state, 'alpha', st.slider("霍尔特平滑 α", 0.1, 0.9, 0.3, 0.05)), "水平平滑系数，值越大越依赖近期数据")
        param_with_help(lambda: setattr(st.session_state, 'beta', st.slider("霍尔特趋势 β", 0.1, 0.9, 0.2, 0.05)), "趋势平滑系数，控制趋势变化的灵敏度")
        param_with_help(lambda: setattr(st.session_state, 'ip_cap', st.number_input("IP调整上限", 1.0, 3.0, 1.8, 0.1)), "IP系数最大影响倍数，避免预测过高")
        param_with_help(lambda: setattr(st.session_state, 'buffer_factor', st.number_input("IP缓冲分母", 1.0, 5.0, 2.0, 0.5)), "降低IP冲击的缓冲因子，值越大越平滑")
        param_with_help(lambda: setattr(st.session_state, 'batch_mult', st.number_input("批量倍数", 1.0, 2.0, 1.2, 0.1)), "朴素预测中批量订单的倍数")
        param_with_help(lambda: setattr(st.session_state, 'min_order', st.number_input("最小批量(朴素预测)", 10, 1000, 30, 10)), "朴素预测的最小订货量")
        param_with_help(lambda: setattr(st.session_state, 'fs_override', st.number_input("季节系数覆盖", 0.0, 3.0, 0.0, 0.1)), "手动指定季节系数，0表示自动计算")
        param_with_help(lambda: setattr(st.session_state, 'future_no_ip', st.checkbox("未来无IP事件")), "勾选后，未来预测将不使用IP系数放大")
        if st.session_state.future_no_ip:
            param_with_help(lambda: setattr(st.session_state, 'persist_factor', st.slider("IP热度持久因子", 1.0, 3.0, 1.5, 0.1)), "IP结束后需求的残留热度系数")
        else: st.session_state.persist_factor = 1.0
        st.markdown("**加权移动平均权重**")
        w1 = st.slider("近期权重 ω₁", 0.0, 1.0, 0.5, 0.05)
        w2 = st.slider("中期权重 ω₂", 0.0, 1.0, 0.3, 0.05)
        w3 = st.slider("远期权重 ω₃", 0.0, 1.0, 0.2, 0.05)
        total = w1 + w2 + w3
        if total > 0: st.session_state.w1, st.session_state.w2, st.session_state.w3 = w1/total, w2/total, w3/total
        else: st.session_state.w1, st.session_state.w2, st.session_state.w3 = 0.5, 0.3, 0.2
        st.markdown("**滚动窗口交叉验证**")
        param_with_help(lambda: setattr(st.session_state, 'enable_validation', st.checkbox("启用自动模型选择", value=True)), "自动选择MAD最小的预测模型")
        if st.session_state.enable_validation:
            param_with_help(lambda: setattr(st.session_state, 'train_len', st.number_input("训练窗口天数", 10, 28, 21, 1)), "用于训练模型的历史天数")
            param_with_help(lambda: setattr(st.session_state, 'val_len', st.number_input("验证窗口天数", 1, 14, 1, 1)), "用于验证预测效果的天数")
            param_with_help(lambda: setattr(st.session_state, 'step', st.number_input("滚动步长", 1, 7, 1, 1)), "滚动窗口每次移动的天数")
            param_with_help(lambda: setattr(st.session_state, 'show_old_method', st.checkbox("计算旧方法MAD", value=True)), "同时计算简单平均法的MAD作为对比")
elif st.session_state.page == "库存优化":
    with st.sidebar.expander("📦 库存策略参数", expanded=False):
        param_with_help(lambda: setattr(st.session_state, 'use_cost_opt', st.checkbox("启用报童模型优化", value=True)), "根据缺货成本与仓储成本自动优化服务水平")
        if not st.session_state.use_cost_opt:
            param_with_help(lambda: setattr(st.session_state, 'fixed_z', st.number_input("固定z值", 1.0, 3.0, 1.645, 0.05)), "手动设置安全库存系数（z分数）")
        param_with_help(lambda: setattr(st.session_state, 'trend_factor', st.slider("趋势放大系数", 0.5, 2.0, 1.2, 0.05)), "考虑需求增长时放大目标库存")
        param_with_help(lambda: setattr(st.session_state, 'intermittent_cycle', st.number_input("间歇型补货周期(天)", 7, 60, 20, 1)), "间歇型需求的补货间隔天数")
        param_with_help(lambda: setattr(st.session_state, 'ordering_cost_K', st.number_input("单次订货固定成本 K (元/次)", 0.0, 1000.0, 100.0, 10.0)), "每次下单的固定成本，影响经济订货批量")
        param_with_help(lambda: setattr(st.session_state, 'user_service_level', st.slider("自定义服务水平 (%)", 80, 99, 95, 1) / 100), "您希望达到的现货率（0-100%）")

# ========== 页面内容 ==========
if st.session_state.page == "概览":
    st.markdown("""
    <div class="hero-banner">
        <h1><i class="fas fa-paw" style="margin-right: 10px;"></i> 宠物IP联名产品库存决策系统</h1>
        <p>专为IP联名宠物产品设计的智能库存管理工具，集成需求特征分析、多模型预测、报童优化与差异补货策略</p>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.features_computed:
        sku_count = len(st.session_state.base_df) if st.session_state.base_df is not None else 0
        st.success(f"✅ 数据已就绪 | 共 {sku_count} 个SKU | 可进行需求预测与库存优化")
    else:
        st.info("📂 请先上传销售数据与库存数据，系统将自动计算特征并生成建议")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="metric-card" style="min-height: 160px; display: flex; flex-direction: column; justify-content: center;">
            <div class="metric-value"><i class="fas fa-chart-line"></i></div>
            <div class="metric-label">需求特征分析</div>
            <small style="color: #1f6e8c;">自动计算CV、趋势、季节系数、IP影响系数等</small>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="metric-card" style="min-height: 160px; display: flex; flex-direction: column; justify-content: center;">
            <div class="metric-value"><i class="fas fa-brain"></i></div>
            <div class="metric-label">6种预测模型</div>
            <small style="color: #1f6e8c;">加权移动平均、霍尔特双参数、季节调整、IP缓冲、指数平滑+衰退、朴素批量</small>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="metric-card" style="min-height: 160px; display: flex; flex-direction: column; justify-content: center;">
            <div class="metric-value"><i class="fas fa-boxes"></i></div>
            <div class="metric-label">智能库存优化</div>
            <small style="color: #1f6e8c;">报童模型自动寻优、差异化补货策略、(R,Q)/(s,S)/(T,S)策略</small>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    
    st.markdown("<h3><i class='fas fa-rocket' style='margin-right: 8px;'></i> 快速开始</h3>", unsafe_allow_html=True)
    step_cols = st.columns(4)
    steps = [
        ("<i class='fas fa-upload'></i> 上传数据", "上传近28天销售明细与产品库存成本表"),
        ("<i class='fas fa-chart-pie'></i> 特征分析", "系统自动识别需求类型、趋势、季节/IP系数"),
        ("<i class='fas fa-chart-line'></i> 需求预测", "滚动验证选择最优模型，预测未来销量"),
        ("<i class='fas fa-cubes'></i> 库存优化", "生成补货建议、服务水平对比、行动清单")
    ]
    for i, col in enumerate(step_cols):
        with col:
            st.markdown(f"""
            <div style="background: white; border-radius: 20px; padding: 16px; margin-bottom: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); text-align: center;">
                <div style="font-size: 1.3rem; font-weight: 700; margin-bottom: 6px; color: #0a3b4b;">{steps[i][0]}</div>
                <div style="font-size: 0.7rem; color: #1f6e8c;">{steps[i][1]}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("<h3><i class='fas fa-table' style='margin-right: 8px;'></i> 数据示例预览</h3>", unsafe_allow_html=True)
    if st.session_state.features_computed and st.session_state.daily_df is not None:
        st.markdown("**最新销售数据（近5天）**")
        sample_sales = st.session_state.daily_df.tail(5).reset_index().rename(columns={'index': '日期'})
        for col in sample_sales.columns:
            if col != '日期' and pd.api.types.is_numeric_dtype(sample_sales[col]):
                sample_sales[col] = sample_sales[col].apply(lambda x: int(round(x)) if pd.notnull(x) else x)
        render_table(sample_sales, add_serial=False)
    else:
        st.markdown("""
        <div style="background: #f8fafc; border-radius: 20px; padding: 16px; border: 1px dashed #cbd5e1;">
            <p style="color: #1f6e8c;"><i class="fas fa-upload"></i> 尚未上传数据，请点击左侧「数据上传」上传Excel文件。<br>
            系统会自动识别SKU、计算需求特征、选择最优预测模型并给出库存建议。</p>
            <p><strong style="color: #0a3b4b;">销售数据格式：</strong> <span style="color: #1f6e8c;">第一列为日期，后续每列为一个SKU的日销量。</span><br>
            <strong style="color: #0a3b4b;">库存数据格式：</strong> <span style="color: #1f6e8c;">包含商品名称、提前期、采购价、仓储成本、缺货成本占比等字段。</span></p>
            <p style="color: #1f6e8c;">👉 可点击「数据上传」页面下载模板。</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("<h3><i class='fas fa-star' style='margin-right: 8px;'></i> 系统亮点</h3>", unsafe_allow_html=True)
    highlight_cols = st.columns(3)
    highlights = [
        ("<i class='fas fa-target'></i> 精准分类", "基于5维特征（CV、趋势、季节、IP、间隔）自动划分需求类型"),
        ("<i class='fas fa-sliders-h'></i> 模型自选", "滚动窗口MAD对比 + 手动覆盖，灵活选择预测模型"),
        ("<i class='fas fa-chart-line'></i> 成本优化", "报童模型动态计算最优服务水平，量化自定义服务水平成本增幅")
    ]
    for i, col in enumerate(highlight_cols):
        with col:
            st.markdown(f"""
            <div style="background: white; border-radius: 20px; padding: 12px; margin-bottom: 8px; box-shadow: 0 1px 4px rgba(0,0,0,0.05);">
                <strong style="color: #0a3b4b;">{highlights[i][0]}</strong><br>
                <span style="font-size: 0.7rem; color: #1f6e8c;">{highlights[i][1]}</span>
            </div>
            """, unsafe_allow_html=True)

elif st.session_state.page == "数据上传":
    st.markdown("<h1><i class='fas fa-upload'></i> 数据上传</h1>", unsafe_allow_html=True)
    st.markdown("<h3><i class='fas fa-download'></i> 下载数据模板</h3>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        output_daily = BytesIO()
        with pd.ExcelWriter(output_daily, engine='openpyxl') as writer:
            pd.DataFrame(columns=['日期', '示例SKU1', '示例SKU2']).to_excel(writer, index=False)
        st.download_button("📥 销售数据模板", data=output_daily.getvalue(), file_name="销售数据模板.xlsx")
    with col2:
        output_inv = BytesIO()
        with pd.ExcelWriter(output_inv, engine='openpyxl') as writer:
            pd.DataFrame(columns=['商品名称', 'MOQ', '提前期', '采购价', '仓储成本', '缺货成本占比', '资金占用成本', '零售价', '仓库可用总库存', '在单量']).to_excel(writer, index=False)
        st.download_button("📥 库存数据模板", data=output_inv.getvalue(), file_name="库存数据模板.xlsx")
    st.markdown("---")
    with st.expander("上传销售数据（近28天）", expanded=True):
        daily_file = st.file_uploader("选择Excel文件", type=['xlsx'], key='daily')
        if daily_file: st.session_state.daily_file = daily_file; st.success("销售数据已暂存")
    with st.expander("上传库存数据（包含成本等）", expanded=True):
        inv_file = st.file_uploader("选择Excel文件", type=['xlsx'], key='inv')
        if inv_file: st.session_state.inv_file = inv_file; st.success("库存数据已暂存")
    if st.button("加载并计算特征", type="primary"):
        if st.session_state.get('daily_file') and st.session_state.get('inv_file'):
            with st.spinner("正在计算特征，请稍候..."):
                daily_df = pd.read_excel(st.session_state.daily_file)
                inv_df = pd.read_excel(st.session_state.inv_file)
                date_col = daily_df.columns[0]
                daily_df[date_col] = pd.to_datetime(daily_df[date_col])
                daily_df = daily_df.set_index(date_col).sort_index()
                inv_df.rename(columns={'提前期': '提前期', '缺货成本占比': '缺货成本'}, inplace=True)
                inv_df['当前总库存'] = inv_df['仓库可用总库存'] + inv_df['在单量']
                st.session_state.daily_df = daily_df; st.session_state.inv_df = inv_df
                total_days = len(daily_df); skus = inv_df['商品名称'].tolist()
                feature_list = []
                for sku in skus:
                    if sku not in daily_df.columns: continue
                    sales = daily_df[sku].values
                    if len(sales) == 0: continue
                    mu = np.mean(sales); sigma = np.std(sales, ddof=1) if len(sales) > 1 else 0
                    cv = sigma / mu if mu != 0 else 0
                    non_zero_days = np.sum(sales > 0); p = total_days / non_zero_days if non_zero_days > 0 else np.inf
                    zero_ratio = np.sum(sales == 0) / len(sales)
                    mu_nz = np.mean(sales[sales > 0]) if non_zero_days > 0 else mu
                    if len(sales) >= 6:
                        early_avg = np.mean(sales[:3]); recent_avg = np.mean(sales[-3:])
                        t = (recent_avg - early_avg) / early_avg if early_avg != 0 else 0
                    else: t = 0
                    if st.session_state.season_pos == "末尾": season_slice = sales[-st.session_state.season_days:] if len(sales) >= st.session_state.season_days else sales
                    else: season_slice = sales[:st.session_state.season_days] if len(sales) >= st.session_state.season_days else sales
                    if st.session_state.off_season_pos == "末尾": off_season_slice = sales[-st.session_state.off_season_days:] if len(sales) >= st.session_state.off_season_days else sales
                    else: off_season_slice = sales[:st.session_state.off_season_days] if len(sales) >= st.session_state.off_season_days else sales
                    season_avg = np.mean(season_slice); off_season_avg = np.mean(off_season_slice)
                    fs = season_avg / off_season_avg if off_season_avg != 0 else 1
                    if st.session_state.ip_pos == "末尾": ip_slice = sales[-st.session_state.ip_days:] if len(sales) >= st.session_state.ip_days else sales
                    else: ip_slice = sales[:st.session_state.ip_days] if len(sales) >= st.session_state.ip_days else sales
                    if st.session_state.non_ip_pos == "末尾": non_ip_slice = sales[-st.session_state.non_ip_days:] if len(sales) >= st.session_state.non_ip_days else sales
                    else: non_ip_slice = sales[:st.session_state.non_ip_days] if len(sales) >= st.session_state.non_ip_days else sales
                    ip_avg = np.mean(ip_slice); non_ip_avg = np.mean(non_ip_slice)
                    f_ip = ip_avg / non_ip_avg if non_ip_avg != 0 else 1
                    feature_list.append({'商品名称': sku, '需求均值μ': mu, '需求标准差σ': sigma, 'CV': cv, '平均需求间隔p': p,
                                         '非零需求均值': mu_nz, '非IP期均值': non_ip_avg, '趋势强度T': t, '季节系数Fs': fs, 'IP系数F_IP': f_ip, '零需求占比': zero_ratio})
                if feature_list:
                    feat_df = pd.DataFrame(feature_list)
                    base_df = inv_df.merge(feat_df, on='商品名称', how='inner')
                    base_df['需求类型'] = base_df.apply(classify_demand_type, axis=1)
                    base_df['商品简称'] = base_df['商品名称'].apply(short_name)
                    st.session_state.base_df = base_df; st.session_state.features_computed = True
                    st.success("特征计算完成！")
                else: st.error("没有匹配的SKU")
        else: st.error("请先上传两个文件")
    if st.session_state.features_computed:
        def show_data_preview():
            st.markdown("<h3>数据预览</h3>", unsafe_allow_html=True)
            st.markdown("**销售数据（近28天）**")
            daily_display = st.session_state.daily_df.head().reset_index().rename(columns={'index': '日期'})
            for col in daily_display.columns:
                if col != '日期' and pd.api.types.is_numeric_dtype(daily_display[col]):
                    daily_display[col] = daily_display[col].apply(lambda x: int(round(x)) if pd.notnull(x) else x)
            render_table(daily_display, add_serial=True)
            st.markdown("**库存数据**")
            inv_display = st.session_state.inv_df.head().copy()
            render_table(inv_display, add_serial=True)
        card(show_data_preview)

elif st.session_state.page == "特征分析":
    if not st.session_state.features_computed:
        st.warning("请先在「数据上传」页面计算特征。")
    else:
        base_df = st.session_state.base_df
        sku_list = base_df['商品名称'].tolist()
        selected_sku = st.selectbox("选择SKU", sku_list, format_func=lambda x: base_df[base_df['商品名称']==x]['商品简称'].iloc[0])
        if selected_sku:
            row = base_df[base_df['商品名称'] == selected_sku].iloc[0]
            
            categories = ['需求均值', 'CV', '趋势强度', '季节系数', 'IP系数']
            values = [row['需求均值μ'], row['CV'], row['趋势强度T'], row['季节系数Fs'], row['IP系数F_IP']]
            max_vals = [max(base_df['需求均值μ']), max(base_df['CV']), max(abs(base_df['趋势强度T'])), max(base_df['季节系数Fs']), max(base_df['IP系数F_IP'])]
            normalized = [values[i]/max_vals[i] if max_vals[i]!=0 else 0 for i in range(5)]
            
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=normalized,
                theta=categories,
                fill='toself',
                name=row['商品简称'],
                line=dict(color='#1f6e8c', width=2),
                fillcolor='rgba(31,110,140,0.3)',
                marker=dict(size=6, color='#1f6e8c')
            ))
            fig.add_trace(go.Scatterpolar(
                r=[1,1,1,1,1],
                theta=categories,
                fill=None,
                name='边界',
                line=dict(color='#cbd5e1', width=1, dash='dash'),
                showlegend=False
            ))
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, gridcolor='#e2e8f0', tickfont=dict(size=8)),
                    angularaxis=dict(gridcolor='#e2e8f0', tickfont=dict(size=10))
                ),
                font=dict(family="Inter", size=12),
                height=420,
                margin=dict(l=40, r=40, t=40, b=20),
                showlegend=False
            )
            
            col_left, col_right = st.columns([1.2, 0.8])
            with col_left:
                st.plotly_chart(fig, use_container_width=True)
            with col_right:
                st.markdown(f"""
                <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px;">
                    <div class="feature-card"><div class="feature-icon"><i class="fas fa-calculator"></i></div><div class="feature-label">需求均值</div><div class="feature-value">{row['需求均值μ']:.2f}</div></div>
                    <div class="feature-card"><div class="feature-icon"><i class="fas fa-chart-line"></i></div><div class="feature-label">CV</div><div class="feature-value">{row['CV']:.2f}</div></div>
                    <div class="feature-card"><div class="feature-icon"><i class="fas fa-arrow-trend-up"></i></div><div class="feature-label">趋势强度</div><div class="feature-value" style="color: {'#16a34a' if row['趋势强度T']>0 else '#dc2626'};">{row['趋势强度T']:.2f}</div></div>
                    <div class="feature-card"><div class="feature-icon"><i class="fas fa-calendar-alt"></i></div><div class="feature-label">季节系数</div><div class="feature-value">{row['季节系数Fs']:.2f}</div></div>
                    <div class="feature-card"><div class="feature-icon"><i class="fas fa-star"></i></div><div class="feature-label">IP系数</div><div class="feature-value">{row['IP系数F_IP']:.2f}</div></div>
                    <div class="feature-card"><div class="feature-icon"><i class="fas fa-percent"></i></div><div class="feature-label">零需求占比</div><div class="feature-value">{row['零需求占比']*100:.1f}%</div></div>
                </div>
                """, unsafe_allow_html=True)
                
                dtype = row['需求类型']
                if '趋势型需求（增长）' in dtype:
                    badge_class = "badge-demand-trend-up"
                    icon = "📈"
                elif '趋势型需求（衰退）' in dtype:
                    badge_class = "badge-demand-trend-down"
                    icon = "📉"
                elif '轻缓波动型需求' in dtype:
                    badge_class = "badge-demand-fluctuation"
                    icon = "🌊"
                elif '平稳型需求' in dtype:
                    badge_class = "badge-demand-stable"
                    icon = "⚖️"
                elif '间歇型（块状）需求' in dtype:
                    badge_class = "badge-demand-intermittent"
                    icon = "⏳"
                else:
                    badge_class = "badge-demand-default"
                    icon = "📌"
                st.markdown(f"""
                <div class="demand-type-card">
                    <div class="demand-type-label">需求类型</div>
                    <div class="demand-type-value"><span class="badge {badge_class}" style="font-size: 1rem;">{icon} {dtype}</span></div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<h3>需求特征指标</h3>", unsafe_allow_html=True)
            display_cols = {
                '商品简称': '商品简称',
                '需求均值μ': '需求均值',
                '非零需求均值': '非零需求均值',
                '平均需求间隔p': '平均需求间隔',
                'CV': 'CV',
                '趋势强度T': '趋势强度',
                '季节系数Fs': '季节系数',
                'IP系数F_IP': 'IP系数',
                '零需求占比': '零需求占比',
                '需求标准差σ': '需求标准差',
                '需求类型': '需求类型'
            }
            df_display = base_df[list(display_cols.keys())].copy().reset_index(drop=True)
            df_display.rename(columns=display_cols, inplace=True)
            for col in df_display.select_dtypes(include=['float64']).columns:
                df_display[col] = df_display[col].apply(lambda x: f"{x:.2f}" if pd.notnull(x) else x)
            render_table(df_display, add_serial=True)
        else:
            card(lambda: None)

elif st.session_state.page == "需求预测":
    if not st.session_state.features_computed:
        st.warning("请先在「数据上传」页面计算特征。")
    else:
        base_df = st.session_state.base_df.copy()
        daily_df = st.session_state.daily_df
        total_days = len(daily_df)
        period = st.session_state.get('period', 14)
        alpha = st.session_state.get('alpha', 0.3)
        beta = st.session_state.get('beta', 0.2)
        ip_cap = st.session_state.get('ip_cap', 1.8)
        buffer_factor = st.session_state.get('buffer_factor', 2.0)
        batch_mult = st.session_state.get('batch_mult', 1.2)
        min_order = st.session_state.get('min_order', 30)
        fs_override = st.session_state.get('fs_override', 0.0)
        future_no_ip = st.session_state.get('future_no_ip', False)
        persist_factor = st.session_state.get('persist_factor', 1.0)
        w1 = st.session_state.get('w1', 0.5)
        w2 = st.session_state.get('w2', 0.3)
        w3 = st.session_state.get('w3', 0.2)
        enable_validation = st.session_state.get('enable_validation', True)
        train_len = st.session_state.get('train_len', 21)
        val_len = st.session_state.get('val_len', 1)
        step = st.session_state.get('step', 1)
        show_old_method = st.session_state.get('show_old_method', True)
        params_pred = {
            'alpha': alpha, 'beta': beta, 'ip_cap': ip_cap, 'buffer_factor': buffer_factor,
            'batch_mult': batch_mult, 'min_order': min_order, 'fs_override': fs_override,
            'future_no_ip': future_no_ip, 'persist_factor': persist_factor,
            'w1': w1, 'w2': w2, 'w3': w3
        }
        model_list = ["加权移动平均", "霍尔特双参数+IP调整", "季节调整移动平均",
                      "基础平稳+IP缓冲", "简单指数平滑+衰退系数", "朴素预测+批量调整"]

        if st.button("开始预测", type="primary"):
            with st.spinner("正在执行滚动验证和预测，请稍候..."):
                best_models = {}
                if enable_validation and train_len + val_len <= total_days:
                    st.info("正在进行滚动窗口交叉验证...")
                    n_windows = (total_days - train_len - val_len) // step + 1
                    if n_windows >= 1:
                        val_results = []
                        for sku in base_df['商品名称']:
                            if sku not in daily_df.columns: continue
                            sales = daily_df[sku].values
                            if len(sales) < train_len + val_len: continue
                            model_mad_sum = {model: 0.0 for model in model_list}
                            valid_windows = 0
                            for start in range(0, n_windows):
                                train_end = start + train_len
                                val_end = train_end + val_len
                                train_sales = sales[start:train_end]
                                val_sales = sales[train_end:val_end]
                                val_actual = np.sum(val_sales)
                                mu_train, T_train, Fs_train, F_IP_train, non_ip_mean_train = compute_features_from_window(
                                    train_sales, st.session_state.season_days, st.session_state.off_season_days,
                                    st.session_state.ip_days, st.session_state.non_ip_days,
                                    st.session_state.season_pos, st.session_state.off_season_pos,
                                    st.session_state.ip_pos, st.session_state.non_ip_pos)
                                features = {'mu': mu_train, 'T': T_train, 'Fs': Fs_train, 'F_IP': F_IP_train, 'non_ip_mean': non_ip_mean_train}
                                for model in model_list:
                                    pred = predict_sku_with_model(train_sales, model, val_len, params_pred, features)
                                    if pred is not None: model_mad_sum[model] += abs(pred - val_actual)
                                valid_windows += 1
                            if valid_windows > 0:
                                avg_mad = {model: model_mad_sum[model] / valid_windows for model in model_list}
                                best_model = min(avg_mad, key=avg_mad.get)
                                best_models[sku] = best_model
                                row_dict = {'商品简称': short_name(sku)}
                                for m in model_list: row_dict[m] = avg_mad[m]
                                if show_old_method:
                                    old_pred = mu_train * val_len
                                    row_dict['旧方法'] = abs(old_pred - val_actual) / valid_windows
                                row_dict['最优模型'] = best_model
                                val_results.append(row_dict)
                        if val_results:
                            df_mad = pd.DataFrame(val_results)
                            num_cols = df_mad.select_dtypes(include=['float64', 'int64']).columns
                            df_mad[num_cols] = df_mad[num_cols].round(2)
                            st.markdown("<h3>各模型平均MAD对比</h3>", unsafe_allow_html=True)
                            render_table(df_mad, add_serial=True)
                    else:
                        st.warning("数据不足，无法进行滚动验证")
                elif enable_validation:
                    st.warning("数据总天数不足以进行滚动验证")

                final_models = {}
                for sku in base_df['商品名称']:
                    manual = st.session_state.manual_model_dict.get(sku, "自动选择（默认）")
                    if manual != "自动选择（默认）":
                        final_models[sku] = manual
                    else:
                        if enable_validation and sku in best_models:
                            final_models[sku] = best_models[sku]
                        else:
                            final_models[sku] = "加权移动平均"

                base_df['使用模型'] = base_df['商品名称'].map(final_models)

                final_preds = []
                for idx, row in base_df.iterrows():
                    sku = row['商品名称']
                    if sku not in daily_df.columns:
                        final_preds.append(None)
                        continue
                    full_sales = daily_df[sku].values
                    mu_full, T_full, Fs_full, F_IP_full, non_ip_mean_full = compute_features_from_window(
                        full_sales, st.session_state.season_days, st.session_state.off_season_days,
                        st.session_state.ip_days, st.session_state.non_ip_days,
                        st.session_state.season_pos, st.session_state.off_season_pos,
                        st.session_state.ip_pos, st.session_state.non_ip_pos)
                    features = {'mu': mu_full, 'T': T_full, 'Fs': Fs_full, 'F_IP': F_IP_full, 'non_ip_mean': non_ip_mean_full}
                    model = row['使用模型']
                    pred = predict_sku_with_model(full_sales, model, period, params_pred, features)
                    final_preds.append(pred)
                base_df['预测销量'] = final_preds
                st.session_state.forecast_df = base_df
                st.success("预测完成！")

        with st.expander("✏️ 手动覆盖模型（可选）", expanded=False):
            st.markdown("> 如果不满意自动选择的模型，可以在此手动指定。修改后请再次点击「开始预测」按钮。")
            sku_list = base_df['商品名称'].tolist()
            for sku in sku_list:
                if sku not in st.session_state.manual_model_dict:
                    st.session_state.manual_model_dict[sku] = "自动选择（默认）"
            cols = st.columns(2)
            for i, sku in enumerate(sku_list):
                with cols[i % 2]:
                    st.session_state.manual_model_dict[sku] = st.selectbox(
                        f"{short_name(sku)} 的预测模型",
                        options=["自动选择（默认）"] + model_list,
                        index=0,
                        key=f"manual_{i}_{sku}"
                    )

        if st.session_state.forecast_df is not None:
            def show_forecast():
                st.markdown("<h3>预测结果</h3>", unsafe_allow_html=True)
                show_df = st.session_state.forecast_df[['商品简称', '需求类型', '使用模型', '预测销量']].copy()
                show_df['预测销量'] = show_df['预测销量'].apply(lambda x: int(round(x)) if pd.notnull(x) else x)
                render_table(show_df, add_serial=True)
            card(show_forecast)

elif st.session_state.page == "库存优化":
    if st.session_state.forecast_df is None:
        st.warning("请先在「需求预测」页面完成预测。")
    else:
        base_df = st.session_state.forecast_df.copy()
        period = st.session_state.get('period', 14)
        use_cost_opt = st.session_state.get('use_cost_opt', True)
        fixed_z = st.session_state.get('fixed_z', 1.645)
        trend_factor = st.session_state.get('trend_factor', 1.2)
        intermittent_cycle = st.session_state.get('intermittent_cycle', 20)
        ordering_cost_K = st.session_state.get('ordering_cost_K', 100.0)
        user_service_level = st.session_state.get('user_service_level', 0.95)
        params_inv = {
            'use_cost_optimization': use_cost_opt,
            'fixed_z': fixed_z if not use_cost_opt else 0,
            'trend_factor': trend_factor,
            'intermittent_cycle': intermittent_cycle,
            'safety_cycle': 14,
            'K': ordering_cost_K
        }
        if st.button("生成订货建议", type="primary"):
            with st.spinner("正在计算最优订货建议..."):
                advice_opt = base_df.apply(lambda row: compute_inventory_advice(row, period, params_inv, service_level_override=None), axis=1)
                advice_user = base_df.apply(lambda row: compute_inventory_advice(row, period, params_inv, service_level_override=user_service_level), axis=1)
                result_df = pd.concat([
                    base_df[['商品简称', '需求类型', '预测销量', '当前总库存']],
                    advice_user[['策略', '安全库存', '订货点', '目标库存', '建议补货量', '优先级', '服务水平', '期望日总成本']]
                ], axis=1)
                result_df.rename(columns={'期望日总成本': '日总成本(用户)', '服务水平': '用户服务水平(%)'}, inplace=True)
                result_df['理论最优服务水平(%)'] = advice_opt['服务水平']
                result_df['日总成本(最优)'] = advice_opt['期望日总成本']
                result_df['成本增加额(元/天)'] = result_df['日总成本(用户)'] - result_df['日总成本(最优)']
                result_df['成本增加(%)'] = (result_df['成本增加额(元/天)'] / result_df['日总成本(最优)'] * 100).round(1)
                st.session_state.result_df = result_df
                st.success("订货建议已生成")
        if st.session_state.result_df is not None:
            def show_inventory():
                result_df = st.session_state.result_df
                st.markdown(f"""
                <div class="param-dashboard">
                    <div class="param-item"><div class="param-label"><i class="fas fa-chart-line"></i> 趋势放大系数</div><div class="param-value">{trend_factor:.2f}</div></div>
                    <div class="param-item"><div class="param-label"><i class="fas fa-clock"></i> 补货周期</div><div class="param-value">{intermittent_cycle} 天</div></div>
                    <div class="param-item"><div class="param-label"><i class="fas fa-dollar-sign"></i> 订货成本K</div><div class="param-value">¥{ordering_cost_K:.1f}</div></div>
                    <div class="param-item"><div class="param-label"><i class="fas fa-percent"></i> 服务水平</div><div class="param-value">{user_service_level*100:.0f}%</div></div>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("<h3>智能订货建议</h3>", unsafe_allow_html=True)
                display_df = result_df[['商品简称', '需求类型', '策略', '安全库存', '订货点', '目标库存', '建议补货量', '优先级',
                                        '用户服务水平(%)', '理论最优服务水平(%)', '日总成本(用户)', '成本增加额(元/天)', '成本增加(%)']].copy()
                for col in ['安全库存', '订货点', '目标库存', '建议补货量', '日总成本(用户)', '成本增加额(元/天)']:
                    if col in display_df.columns:
                        display_df[col] = display_df[col].apply(lambda x: f"{x:.2f}" if isinstance(x, (int, float)) else x)
                render_table(display_df, add_serial=True)
                
                st.markdown("<h3>💰 自定义服务水平与理论最优的成本对比</h3>", unsafe_allow_html=True)
                col1, col2 = st.columns(2)
                with col1:
                    total_extra = result_df['成本增加额(元/天)'].sum()
                    avg_increase = result_df['成本增加(%)'].mean()
                    st.markdown(f"""
                    <div class="cost-card">
                        <div class="cost-label"><i class="fas fa-chart-line"></i> 所有SKU每日总成本增加</div>
                        <div class="cost-value">¥{total_extra:.2f}</div>
                        <div class="cost-sub">平均增幅 {avg_increase:.1f}%</div>
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    best_saving = result_df['成本增加额(元/天)'].min()
                    worst_extra = result_df['成本增加额(元/天)'].max()
                    st.markdown(f"""
                    <div class="cost-card">
                        <div class="cost-label"><i class="fas fa-coins"></i> 单个SKU最小/最大额外成本</div>
                        <div class="cost-value">¥{best_saving:.2f} / ¥{worst_extra:.2f}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                cost_table = result_df[['商品简称', '用户服务水平(%)', '理论最优服务水平(%)', '日总成本(用户)', '日总成本(最优)', '成本增加额(元/天)', '成本增加(%)']].copy()
                for col in ['用户服务水平(%)', '理论最优服务水平(%)', '日总成本(用户)', '日总成本(最优)', '成本增加额(元/天)']:
                    if col in cost_table.columns:
                        cost_table[col] = cost_table[col].apply(lambda x: f"{x:.2f}" if isinstance(x, (int, float)) else x)
                render_table(cost_table, add_serial=True)
                
                output = BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    result_df.to_excel(writer, index=False, sheet_name='订货建议')
                st.download_button("📥 下载订货建议表", data=output.getvalue(), file_name="订货建议.xlsx")
            card(show_inventory)

elif st.session_state.page == "决策建议":
    if st.session_state.result_df is None:
        st.warning("请先在「库存优化」页面生成订货建议。")
    else:
        def show_decision():
            result_df = st.session_state.result_df.copy()
            base_df = st.session_state.forecast_df.copy()
            period = st.session_state.get('period', 14)
            result_df['预测日均销量'] = result_df['预测销量'] / period
            result_df['库存可售天数'] = result_df.apply(lambda x: x['当前总库存'] / x['预测日均销量'] if x['预测日均销量'] > 0 else np.inf, axis=1)
            lead_time_dict = dict(zip(base_df['商品名称'], base_df['提前期']))
            first_lead = list(lead_time_dict.values())[0] if lead_time_dict else 14
            result_df['供货周期'] = first_lead
            def risk_level(row):
                days = row['库存可售天数']
                if days < first_lead: return '缺货风险'
                elif days > 30: return '积压风险'
                else: return '正常'
            result_df['风险等级'] = result_df.apply(risk_level, axis=1)
            price_map = base_df.set_index('商品名称')['采购价'].to_dict()
            result_df['库存金额'] = result_df['当前总库存'] * result_df['商品简称'].map(lambda x: price_map.get(base_df[base_df['商品简称']==x]['商品名称'].iloc[0] if len(base_df[base_df['商品简称']==x])>0 else 0) or 0)
            
            healthy_count = len(result_df[result_df['风险等级'] == '正常'])
            shortage_count = len(result_df[result_df['风险等级'] == '缺货风险'])
            overstock_count = len(result_df[result_df['风险等级'] == '积压风险'])
            total_order_value = (result_df['建议补货量'] * result_df['商品简称'].map(lambda x: price_map.get(base_df[base_df['商品简称']==x]['商品名称'].iloc[0] if len(base_df[base_df['商品简称']==x])>0 else 0) or 0)).sum()
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown(f"""
                <div class="decision-card">
                    <div class="decision-value"><i class="fas fa-check-circle" style="color: #16a34a; margin-right: 4px;"></i> {healthy_count}/{len(result_df)}</div>
                    <div class="decision-label">库存健康率</div>
                    <div class="decision-delta">{healthy_count/len(result_df)*100:.0f}%</div>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                <div class="decision-card">
                    <div class="decision-value"><i class="fas fa-bell" style="color: #dc2626; margin-right: 4px;"></i> {shortage_count}</div>
                    <div class="decision-label">缺货风险</div>
                    <div class="decision-delta">需立即补货</div>
                </div>
                """, unsafe_allow_html=True)
            with col3:
                st.markdown(f"""
                <div class="decision-card">
                    <div class="decision-value"><i class="fas fa-box" style="color: #f97316; margin-right: 4px;"></i> {overstock_count}</div>
                    <div class="decision-label">积压风险</div>
                    <div class="decision-delta">建议促销</div>
                </div>
                """, unsafe_allow_html=True)
            with col4:
                st.markdown(f"""
                <div class="decision-card">
                    <div class="decision-value"><i class="fas fa-money-bill-wave" style="color: #eab308; margin-right: 4px;"></i> ¥{total_order_value:,.0f}</div>
                    <div class="decision-label">建议补货金额</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            st.markdown("<h3>📋 待办行动清单</h3>", unsafe_allow_html=True)
            action_df = result_df.copy()
            valid_risk = ['缺货风险', '正常', '积压风险']
            action_df = action_df[action_df['风险等级'].isin(valid_risk)].copy()
            action_df['风险等级'] = action_df['风险等级'].astype('category')
            action_df['风险等级'] = action_df['风险等级'].cat.set_categories(valid_risk, ordered=True)
            action_df = action_df.sort_values('风险等级')
            def get_action(row):
                if row['风险等级'] == '缺货风险':
                    if row['建议补货量'] > 0: return f"立即下单 {row['建议补货量']:.0f} 件"
                    else: return "紧急补货（已达订货点）"
                elif row['风险等级'] == '积压风险': return "建议促销 / 调拨"
                else: return "无需操作"
            def get_urgency(row):
                if row['风险等级'] == '缺货风险': return "🔴 紧急"
                elif row['风险等级'] == '积压风险': return "🟠 关注"
                else: return "🟢 正常"
            action_df['行动建议'] = action_df.apply(get_action, axis=1)
            action_df['紧急程度'] = action_df.apply(get_urgency, axis=1)
            action_columns = ['商品简称', '紧急程度', '当前总库存', '库存可售天数', '建议补货量', '行动建议']
            display_action = action_df[action_columns].copy()
            display_action = display_action.rename(columns={'商品简称':'商品','当前总库存':'库存','库存可售天数':'可售天数','建议补货量':'建议补货'})
            render_table(display_action, add_serial=True)
            
            st.markdown("<h3>🎯 库存风险矩阵</h3>", unsafe_allow_html=True)
            matrix_df = action_df[['商品简称', '库存可售天数', '库存金额', '风险等级']].copy()
            fig_matrix = px.scatter(matrix_df, x='库存可售天数', y='库存金额', 
                                    color='风险等级', hover_name='商品简称', size='库存金额',
                                    color_discrete_map={'缺货风险':'#d9534f','正常':'#5cb85c','积压风险':'#f0ad4e'},
                                    title='库存风险矩阵')
            fig_matrix.add_vline(x=first_lead, line_dash="dash", line_color="red", annotation_text="缺货警戒线")
            fig_matrix.add_vline(x=30, line_dash="dash", line_color="orange", annotation_text="积压警戒线")
            fig_matrix.update_layout(font=dict(family="Inter", size=12))
            st.plotly_chart(fig_matrix, use_container_width=True)
            
            st.markdown("<h3>📥 导出决策清单</h3>", unsafe_allow_html=True)
            if st.button("生成订货Excel"):
                output_excel = BytesIO()
                with pd.ExcelWriter(output_excel, engine='openpyxl') as writer:
                    action_df.to_excel(writer, index=False, sheet_name='行动清单')
                st.download_button("下载订货清单", data=output_excel.getvalue(), file_name="订货清单.xlsx")
        card(show_decision)

