import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.patheffects import withStroke
import seaborn as sns
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import Ridge, Lasso, LinearRegression
from sklearn.svm import SVR
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
import xgboost as xgb
import warnings
warnings.filterwarnings('ignore')

# ─── Helper for Feature Projection ──────────────────────────────────────────
def _fit_candidates(x, y):
    x = np.array(x, dtype=float)
    y = np.array(y, dtype=float)
    mask = ~(np.isnan(x) | np.isnan(y))
    x, y = x[mask], y[mask]
    if len(x) < 3:
        return 'linear', (lambda xf: np.array([np.nanmean(y)] * len(xf))), -999

    candidates = {}
    X_lin = x.reshape(-1, 1)
    m = LinearRegression().fit(X_lin, y)
    candidates['linear'] = (m, lambda xf: m.predict(xf.reshape(-1,1)), r2_score(y, m.predict(X_lin)))

    if np.all(x > 0):
        X_log = np.log(x).reshape(-1, 1)
        m2 = LinearRegression().fit(X_log, y)
        candidates['log'] = (m2, lambda xf: m2.predict(np.log(xf).reshape(-1,1)), r2_score(y, m2.predict(X_log)))

    if np.all(x >= 0):
        X_sqrt = np.sqrt(x).reshape(-1, 1)
        m3 = LinearRegression().fit(X_sqrt, y)
        candidates['sqrt'] = (m3, lambda xf: m3.predict(np.sqrt(xf).reshape(-1,1)), r2_score(y, m3.predict(X_sqrt)))

    if np.all(y > 0):
        X_exp = x.reshape(-1, 1)
        m4 = LinearRegression().fit(X_exp, np.log(y))
        y_pred_exp = np.exp(m4.predict(X_exp))
        candidates['exp'] = (m4, lambda xf: np.exp(m4.predict(xf.reshape(-1,1))), r2_score(y, y_pred_exp))

    best_name = max(candidates, key=lambda k: candidates[k][2])
    _, pred_fn, best_r2 = candidates[best_name]
    return best_name, pred_fn, best_r2

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Cambodia Education Dashboard",
    page_icon="🇰🇭",
    layout="wide"
)

import os

# ─── Load Data ────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    # Robust pathing: check if we are running from root or dashboard/
    if os.path.exists('data/cleaned_new_data.csv'):
        path1 = 'data/cleaned_new_data.csv'
        path2 = 'data/appendix.csv'
    else:
        path1 = '../data/cleaned_new_data.csv'
        path2 = '../data/appendix.csv'
        
    df = pd.read_csv(path1)
    df2 = pd.read_csv(path2)
    if 'year' not in df.columns and 'Year' in df.columns:
        df = df.rename(columns={'Year': 'year', 'Province': 'province'})
    if 'row_id' in df.columns:
        df = df.drop(columns=['row_id'])
    return df, df2

df, df2 = load_data()

GRADES = ['G1','G2','G3','G4','G5','G6','G7','G8','G9','G10','G11','G12']

# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("🇰🇭 Cambodia Education")
    st.markdown("---")

    page = st.radio("Navigate", [
        "Overview & KPIs",
        "Schools & Infrastructure",
        "Student Flow",
        "Teaching Staff & Quality",
        "Provincial Deep Dive",
        "Relationship Analysis",
        "Modelling & Forecasts",
        "Long-term Trends",
    ])

    st.markdown("---")
    all_years = sorted(df['year'].unique())
    selected_years = st.multiselect("Year", all_years, default=all_years)

    st.markdown("---")
    st.caption("Design by a psychopath")

# Guard: if no years selected, stop early
if not selected_years:
    st.warning("Please select at least one year from the sidebar.")
    st.stop()

# Filter
dff = df[df['year'].isin(selected_years)]

# Derived year helpers — used across ALL pages
latest_year = max(selected_years)
earliest_year = min(selected_years)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — Overview & KPIs
# ══════════════════════════════════════════════════════════════════════════════
if page == "Overview & KPIs":
    st.title("Overview & KPIs")
    st.markdown("---")

    d_latest = dff[dff['year'] == latest_year]
    d_prev = dff[dff['year'] == earliest_year]

    def safe_sum(d, col):
        return d[col].sum() if col in d.columns else 0

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        v = int(safe_sum(d_latest, 'num_schools'))
        delta = int(v - safe_sum(d_prev, 'num_schools'))
        st.metric("Total Schools", f"{v:,}", delta=f"{delta:+,}")
    with c2:
        v = int(safe_sum(d_latest, 'enrollment_total'))
        delta = int(v - safe_sum(d_prev, 'enrollment_total'))
        st.metric("Total Enrollment", f"{v:,}", delta=f"{delta:+,}")
    with c3:
        v = int(safe_sum(d_latest, 'teaching_staff_total'))
        delta = int(v - safe_sum(d_prev, 'teaching_staff_total'))
        st.metric("Teaching Staff", f"{v:,}", delta=f"{delta:+,}")
    with c4:
        total = safe_sum(d_latest, 'enrollment_total')
        girls = safe_sum(d_latest, 'enrollment_girl')
        pct = round(girls / total * 100, 1) if total > 0 else 0
        st.metric("Girl Enrollment %", f"{pct}%")
    with c5:
        v = int(safe_sum(d_latest, 'num_classes'))
        delta = int(v - safe_sum(d_prev, 'num_classes'))
        st.metric("Total Classes", f"{v:,}", delta=f"{delta:+,}")

    st.markdown("---")
    col_left, col_right = st.columns(2)

    with col_left:
        enroll_trend = dff.groupby('year')[['enrollment_total', 'enrollment_girl']].sum().reset_index()
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=enroll_trend['year'], y=enroll_trend['enrollment_total'],
                                 name='Total', mode='lines+markers', line=dict(color='#2196F3', width=2)))
        fig.add_trace(go.Scatter(x=enroll_trend['year'], y=enroll_trend['enrollment_girl'],
                                 name='Girls', mode='lines+markers', line=dict(color='#E91E63', width=2)))
        fig.update_layout(title='Total Enrollment Over Time', template='plotly_white',
                          hovermode='x unified', height=350)
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        school_trend = dff.groupby('year')['num_schools'].sum().reset_index()
        fig = go.Figure()
        fig.add_trace(go.Bar(x=school_trend['year'], y=school_trend['num_schools'],
                             marker_color='#FF9800', name='Schools'))
        fig.update_layout(title='Total Schools Over Time', template='plotly_white', height=350)
        st.plotly_chart(fig, use_container_width=True)

    level_cols = {
        'Primary': 'primary_enrollment_total',
        'Lower Sec': 'lower_sec_enrollment_total',
        'Upper Sec': 'upper_sec_enrollment_total',
    }
    existing = {k: v for k, v in level_cols.items() if v in dff.columns}
    if existing:
        level_df = dff.groupby('year')[[*existing.values()]].sum().reset_index()
        fig = go.Figure()
        colors = ['#4CAF50', '#2196F3', '#9C27B0']
        for i, (label, col) in enumerate(existing.items()):
            fig.add_trace(go.Scatter(x=level_df['year'], y=level_df[col],
                                     name=label, stackgroup='one',
                                     line=dict(color=colors[i % len(colors)])))
        fig.update_layout(title='Enrollment by School Level Over Time',
                          template='plotly_white', hovermode='x unified', height=350)
        st.plotly_chart(fig, use_container_width=True)

        enroll_trend = dff.groupby('year')[['teaching_staff_total', 'teaching_staff_female']].sum().reset_index()
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=enroll_trend['year'], y=enroll_trend['teaching_staff_total'],
                                 name='Total', mode='lines+markers', line=dict(color='#2196F3', width=2)))
        fig.add_trace(go.Scatter(x=enroll_trend['year'], y=enroll_trend['teaching_staff_female'],
                                 name='Female', mode='lines+markers', line=dict(color='#E91E63', width=2)))
        fig.update_layout(title='Total Teacher Over Time', template='plotly_white',
                          hovermode='x unified', height=350)
        st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — Schools & Infrastructure
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Schools & Infrastructure":
    st.title("Schools & Infrastructure")
    st.markdown("---")
    level_school_cols = {
        'Preschool': 'num_schools_preschool',
        'Primary': 'num_schools_primary',
        'College': 'num_schools_college',
        'Lycee': 'num_schools_lycee',
    }
    existing = {k: v for k, v in level_school_cols.items() if v in dff.columns}
    if existing:
        s_df = dff.groupby('year')[[*existing.values()]].sum().reset_index()
        fig = go.Figure()
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
        for i, (label, col) in enumerate(existing.items()):
            fig.add_trace(go.Bar(x=s_df['year'], y=s_df[col], name=label,
                                 marker_color=colors[i % len(colors)]))
        fig.update_layout(barmode='group', title='Number of Schools by Level',
                          template='plotly_white', hovermode='x unified', height=400)
        st.plotly_chart(fig, use_container_width=True)
    build_cols = {
            'Concrete/Brick': 'concrete_brick_buildings',
            'Wooden': 'wooden_buildings',
            'Bamboo': 'bamboo_buildings',
        }
    existing = {k: v for k, v in build_cols.items() if v in dff.columns}
    if existing:
        b_df = dff.groupby('year')[[*existing.values()]].sum().reset_index()
        fig = go.Figure()
        colors = ['#607D8B', '#795548', '#8BC34A']
        for i, (label, col) in enumerate(existing.items()):
            fig.add_trace(go.Bar(x=b_df['year'], y=b_df[col], name=label,
                                 marker_color=colors[i]))
        fig.update_layout(barmode='stack', title='Building Types Over Time',
                          template='plotly_white', height=400)
        st.plotly_chart(fig, use_container_width=True)
        
    col_left, col_right = st.columns(2)
    with col_left:
        d_latest = dff[dff['year'] == latest_year]
        # Prefer using existing percentage columns if present
        if 'pct_schools_without_water' in d_latest.columns and 'pct_schools_without_toilet' in d_latest.columns:
            water_df = d_latest.groupby('province')[['pct_schools_without_water', 'pct_schools_without_toilet']].mean().reset_index()
            water_df = water_df.sort_values('pct_schools_without_toilet', ascending=True)
            fig = go.Figure()
            fig.add_trace(go.Bar(y=water_df['province'], x=water_df['pct_schools_without_water'],
                                 name='No Water (%)', orientation='h', marker_color='#2196F3', hovertemplate='%{x:.1f}%'))
            fig.add_trace(go.Bar(y=water_df['province'], x=water_df['pct_schools_without_toilet'],
                                 name='No Toilet/Latrine (%)', orientation='h', marker_color='#FF5722', hovertemplate='%{x:.1f}%'))
            fig.update_layout(barmode='group', title=f'Schools Without Water / Toilet Rate ({latest_year})',
                              template='plotly_white', height=500)
            st.plotly_chart(fig, use_container_width=True)
        else:
            # Fallbacks: try using counts or previously computed rates
            # If pct exists individually, use it
            if 'pct_schools_without_toilet' in d_latest.columns:
                lat_df = d_latest.groupby('province')[['pct_schools_without_toilet']].mean().reset_index()
                lat_df = lat_df.sort_values('pct_schools_without_toilet', ascending=True)
                fig = go.Figure()
                fig.add_trace(go.Bar(y=lat_df['province'], x=lat_df['pct_schools_without_toilet'],
                                     name='No Toilet/Latrine (%)', orientation='h', marker_color='#FF5722', hovertemplate='%{x:.1f}%'))
                fig.update_layout(title=f'Schools Without Toilet/Latrine Rate ({latest_year})', template='plotly_white', height=500)
                st.plotly_chart(fig, use_container_width=True)
            elif 'schools_without_latrine' in d_latest.columns and 'num_schools' in d_latest.columns:
                lat_df = d_latest.groupby('province')[['schools_without_latrine','num_schools']].sum()
                lat_df['pct_schools_without_latrine'] = (lat_df['schools_without_latrine'] / lat_df['num_schools']).replace([np.inf, -np.inf], np.nan) * 100
                lat_df = lat_df.sort_values('pct_schools_without_latrine', ascending=True).reset_index()
                fig = go.Figure()
                fig.add_trace(go.Bar(y=lat_df['province'], x=lat_df['pct_schools_without_latrine'],
                                     name='No Latrine Rate (%)', orientation='h', marker_color='#FF5722', hovertemplate='%{x:.1f}%'))
                fig.update_layout(title=f'Schools Without Latrine Rate ({latest_year})', template='plotly_white', height=500)
                st.plotly_chart(fig, use_container_width=True)
            elif 'schools_without_latrine' in d_latest.columns:
                lat_df = d_latest.groupby('province')[['schools_without_latrine']].sum().reset_index()
                lat_df = lat_df.sort_values('schools_without_latrine', ascending=True)
                fig = go.Figure()
                fig.add_trace(go.Bar(y=lat_df['province'], x=lat_df['schools_without_latrine'],
                                     name='No Latrine (count)', orientation='h', marker_color='#FF5722'))
                fig.update_layout(title=f'Schools Without Latrine ({latest_year})', template='plotly_white', height=500)
                st.plotly_chart(fig, use_container_width=True)

    with col_right:
        if 'schools_with_library' in dff.columns:
            lib_df = dff.groupby('year')[['schools_with_office', 'schools_with_library']].sum().reset_index()
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=lib_df['year'], y=lib_df['schools_with_office'],
                                     name='With Office', mode='lines+markers'))
            fig.add_trace(go.Scatter(x=lib_df['year'], y=lib_df['schools_with_library'],
                                     name='With Library', mode='lines+markers'))
            fig.update_layout(title='Schools with Office / Library', template='plotly_white',
                              hovermode='x unified', height=350)
            st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — Student Flow
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Student Flow":
    st.title("Student Flow")
    st.caption("Dropout, repetition, and promotion across grades")
    st.markdown("---")

    flow_data = []
    for i in range(1, 13):
        p_col, r_col, d_col = f'g{i}_promotion', f'g{i}_repetition', f'g{i}_dropout'
        if all(c in dff.columns for c in [p_col, r_col, d_col]):
            row = dff[dff['year'] == latest_year][[p_col, r_col, d_col]].mean()
            flow_data.append({'Grade': f'G{i}',
                              'Promotion': row[p_col],
                              'Repetition': row[r_col],
                              'Dropout': row[d_col]})
    if flow_data:
        flow_df = pd.DataFrame(flow_data)
        fig = go.Figure()
        fig.add_trace(go.Bar(x=flow_df['Grade'], y=flow_df['Promotion'],
                             name='Promotion', marker_color='#4CAF50'))
        fig.add_trace(go.Bar(x=flow_df['Grade'], y=flow_df['Repetition'],
                             name='Repetition', marker_color='#FF9800'))
        fig.add_trace(go.Bar(x=flow_df['Grade'], y=flow_df['Dropout'],
                             name='Dropout', marker_color='#F44336'))
        fig.update_layout(barmode='group',
                          title=f'Promotion / Repetition / Dropout by Grade ({latest_year})',
                          template='plotly_white', hovermode='x unified', height=400)
        st.plotly_chart(fig, use_container_width=True)
    dropout_trend = []
    for i in range(1, 13):
        col = f'g{i}_dropout'
        if col in dff.columns:
            t = dff.groupby('year')[col].mean().reset_index()
            t['grade'] = f'G{i}'
            t = t.rename(columns={col: 'dropout'})
            dropout_trend.append(t)
    if dropout_trend:
        dt_df = pd.concat(dropout_trend)
        fig = px.line(dt_df, x='year', y='dropout', color='grade',
                     title='Dropout Rate by Grade Over Time',
                     labels={'dropout': 'Dropout Rate'}, template='plotly_white')
        fig.update_layout(hovermode='x unified', height=400)
        st.plotly_chart(fig, use_container_width=True)

    dropout_cols = [f'g{i}_dropout' for i in range(1, 13) if f'g{i}_dropout' in dff.columns]
    if dropout_cols:
        dff_copy = dff.copy()
        dff_copy['avg_dropout'] = dff_copy[dropout_cols].mean(axis=1)
        pivot = dff_copy.pivot_table(index='province', columns='year',
                                     values='avg_dropout', aggfunc='mean')
        fig = px.imshow(pivot, aspect='auto', color_continuous_scale='Reds',
                       title='Average Dropout Rate — Province × Year',
                       labels=dict(color='Dropout Rate'))
        fig.update_layout(height=600)
        st.plotly_chart(fig, use_container_width=True)
        d_latest = dff[dff['year'] == latest_year]
        prov_grade = d_latest.groupby('province')[dropout_cols].mean()
        prov_grade.columns = [f'G{i+1}' for i in range(len(dropout_cols))]
        fig = px.imshow(prov_grade, aspect='auto', color_continuous_scale='YlOrRd',
                       title=f'Dropout Rate by Province & Grade ({latest_year})',
                       labels=dict(color='Dropout Rate'))
        fig.update_layout(height=600)
        st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4 — Teaching Staff & Quality
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Teaching Staff & Quality":
    st.title("Teaching Staff & Quality")
    st.markdown("---")

    edu_cols = {
        'Primary': 'teaching_staff_edu_primary',
        'Lower Sec': 'teaching_staff_edu_lower_sec',
        'Upper Sec': 'teaching_staff_edu_upper_sec',
        'Graduate': 'teaching_staff_edu_graduate',
        'Post Grad': 'teaching_staff_edu_postgrad',
        'PhD': 'teaching_staff_edu_phd',
    }
    existing_edu = {k: v for k, v in edu_cols.items() if v in dff.columns}
    if existing_edu:
        edu_trend = dff.groupby('year')[[*existing_edu.values()]].sum().reset_index()
        fig = go.Figure()
        colors = ['#F44336', '#FF9800', '#FFEB3B', '#4CAF50', '#2196F3', '#9C27B0']
        for i, (label, col) in enumerate(existing_edu.items()):
            fig.add_trace(go.Scatter(x=edu_trend['year'], y=edu_trend[col],
                                     name=label, stackgroup='one',
                                     line=dict(color=colors[i % len(colors)])))
        fig.update_layout(title='Teacher Education Level Mix Over Time',
                          template='plotly_white', hovermode='x unified', height=400)
        st.plotly_chart(fig, use_container_width=True)
    if 'teaching_staff_edu_primary' in dff.columns and 'teaching_staff_edu_graduate' in dff.columns:
        qual = dff.groupby('year').agg(
            low=('teaching_staff_edu_primary', 'sum'),
            high=('teaching_staff_edu_graduate', 'sum')
        ).reset_index()
        if 'teaching_staff_edu_lower_sec' in dff.columns:
            qual['low'] += dff.groupby('year')['teaching_staff_edu_lower_sec'].sum().values
        if 'teaching_staff_edu_postgrad' in dff.columns:
            qual['high'] += dff.groupby('year')['teaching_staff_edu_postgrad'].sum().values
        if 'teaching_staff_edu_phd' in dff.columns:
            qual['high'] += dff.groupby('year')['teaching_staff_edu_phd'].sum().values
        qual['low_pct'] = qual['low'] / (qual['low'] + qual['high']) * 100
        qual['high_pct'] = 100 - qual['low_pct']
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=qual['year'], y=qual['low_pct'],
                                 name='Low Quality (Primary/LSec)', stackgroup='one',
                                 line=dict(color='#F44336'), fillcolor='rgba(244,67,54,0.5)'))
        fig.add_trace(go.Scatter(x=qual['year'], y=qual['high_pct'],
                                 name='High Quality (Grad+)', stackgroup='one',
                                 line=dict(color='#4CAF50'), fillcolor='rgba(76,175,80,0.5)'))
        fig.update_layout(title='Teacher Quality Split Over Time',
                          template='plotly_white', hovermode='x unified',
                          yaxis_ticksuffix='%', height=350)
        st.plotly_chart(fig, use_container_width=True)

    if 'pupil_teacher_ratio' in dff.columns:
        ptr = dff.groupby('year')['pupil_teacher_ratio'].mean().reset_index()
        fig = px.line(ptr, x='year', y='pupil_teacher_ratio', markers=True,
                     title='Average Pupil-Teacher Ratio Over Time',
                     labels={'pupil_teacher_ratio': 'Pupils per Teacher'},
                     template='plotly_white')
        fig.update_layout(height=330)
        st.plotly_chart(fig, use_container_width=True)
    dropout_cols = [f'g{i}_dropout' for i in range(1, 13) if f'g{i}_dropout' in dff.columns]

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 6 — Provincial Deep Dive
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Provincial Deep Dive":
    st.title("Provincial Deep Dive")
    st.markdown("---")

    # FIX: use dff (filtered) not df for province list
    selected_province = st.selectbox("Select Province", sorted(dff['province'].unique()))
    df_prov = dff[dff['province'] == selected_province]

    st.subheader(f"📍 {selected_province}")
    st.markdown("---")

    d_l = df_prov[df_prov['year'] == latest_year]

    def sv(d, col):
        return int(d[col].sum()) if col in d.columns else 0

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Schools", f"{sv(d_l, 'num_schools'):,}")
    with c2:
        st.metric("Enrollment", f"{sv(d_l, 'enrollment_total'):,}")
    with c3:
        st.metric("Teaching Staff", f"{sv(d_l, 'teaching_staff_total'):,}")
    with c4:
        total = sv(d_l, 'enrollment_total')
        girls = sv(d_l, 'enrollment_girl')
        st.metric("Girl %", f"{round(girls/total*100, 1) if total > 0 else 0}%")

    st.markdown("---")
    col_left, col_right = st.columns(2)

    with col_left:
        enroll_trend = df_prov.groupby('year')[['enrollment_total', 'enrollment_girl']].sum().reset_index()
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=enroll_trend['year'], y=enroll_trend['enrollment_total'],
                                 name='Total', mode='lines+markers', line=dict(color='#2196F3')))
        fig.add_trace(go.Scatter(x=enroll_trend['year'], y=enroll_trend['enrollment_girl'],
                                 name='Girls', mode='lines+markers', line=dict(color='#E91E63')))
        fig.update_layout(title='Enrollment Trend', template='plotly_white',
                          hovermode='x unified', height=300)
        st.plotly_chart(fig, use_container_width=True)

        dropout_cols = [f'g{i}_dropout' for i in range(1, 13) if f'g{i}_dropout' in df_prov.columns]
        if dropout_cols:
            drop_trend = df_prov.groupby('year')[dropout_cols].mean().reset_index()
            drop_trend['avg_dropout'] = drop_trend[dropout_cols].mean(axis=1)
            fig = px.line(drop_trend, x='year', y='avg_dropout', markers=True,
                         title='Average Dropout Rate Trend',
                         labels={'avg_dropout': 'Avg Dropout Rate'},
                         template='plotly_white')
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)

    with col_right:
        edu_cols = {
            'Primary': 'teaching_staff_edu_primary',
            'Lower Sec': 'teaching_staff_edu_lower_sec',
            'Upper Sec': 'teaching_staff_edu_upper_sec',
            'Graduate': 'teaching_staff_edu_graduate',
            'Post Grad': 'teaching_staff_edu_postgrad',
            'PhD': 'teaching_staff_edu_phd',
        }
        existing_edu = {k: v for k, v in edu_cols.items() if v in df_prov.columns}
        if existing_edu:
            edu_prov = df_prov.groupby('year')[[*existing_edu.values()]].sum().reset_index()
            fig = go.Figure()
            colors = ['#F44336', '#FF9800', '#FFEB3B', '#4CAF50', '#2196F3', '#9C27B0']
            for i, (label, col) in enumerate(existing_edu.items()):
                fig.add_trace(go.Bar(x=edu_prov['year'], y=edu_prov[col],
                                     name=label, marker_color=colors[i % len(colors)]))
            fig.update_layout(barmode='stack', title='Teacher Education Mix',
                              template='plotly_white', height=300)
            st.plotly_chart(fig, use_container_width=True)

        infra_cols = {
            'Concrete': 'concrete_brick_buildings',
            'Wooden': 'wooden_buildings',
            'Bamboo': 'bamboo_buildings',
        }
        existing_infra = {k: v for k, v in infra_cols.items() if v in df_prov.columns}
        if existing_infra:
            infra_prov = df_prov.groupby('year')[[*existing_infra.values()]].sum().reset_index()
            fig = go.Figure()
            colors = ['#607D8B', '#795548', '#8BC34A']
            for i, (label, col) in enumerate(existing_infra.items()):
                fig.add_trace(go.Bar(x=infra_prov['year'], y=infra_prov[col],
                                     name=label, marker_color=colors[i]))
            fig.update_layout(barmode='stack', title='Building Types',
                              template='plotly_white', height=300)
            st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.subheader(f"Grade Flow ({latest_year})")
    flow_data = []
    for i in range(1, 13):
        p_col, r_col, d_col = f'g{i}_promotion', f'g{i}_repetition', f'g{i}_dropout'
        if all(c in d_l.columns for c in [p_col, r_col, d_col]):
            row = d_l[[p_col, r_col, d_col]].mean()
            flow_data.append({'Grade': f'G{i}',
                              'Promotion': row[p_col],
                              'Repetition': row[r_col],
                              'Dropout': row[d_col]})
    if flow_data:
        flow_df = pd.DataFrame(flow_data)
        fig = go.Figure()
        fig.add_trace(go.Bar(x=flow_df['Grade'], y=flow_df['Promotion'],
                             name='Promotion', marker_color='#4CAF50'))
        fig.add_trace(go.Bar(x=flow_df['Grade'], y=flow_df['Repetition'],
                             name='Repetition', marker_color='#FF9800'))
        fig.add_trace(go.Bar(x=flow_df['Grade'], y=flow_df['Dropout'],
                             name='Dropout', marker_color='#F44336'))
        fig.update_layout(barmode='group', template='plotly_white',
                          hovermode='x unified', height=350)
        st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 7 — Relationship Analysis
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Relationship Analysis":
    st.title("Relationship Analysis")
    st.caption("2021 excluded — government policy anomaly.")
    st.markdown("---")

    dff_clean = dff[dff['year'] != 2021].copy()
    prov_agg = dff_clean.groupby('province').mean(numeric_only=True)
    repetition_cols = [f'g{i}_repetition' for i in range(1, 13)]
    prov_agg['avg_repetition_rate'] = prov_agg[repetition_cols].mean(axis=1)
    dropout_cols = [f'g{i}_dropout' for i in range(1, 13)]
    prov_agg['avg_dropout_rate'] = prov_agg[dropout_cols].mean(axis=1)
    promotion_cols = [f'g{i}_promotion' for i in range(1, 13)]
    prov_agg['avg_promotion_rate'] = prov_agg[promotion_cols].mean(axis=1)
    prov_agg['bad_qual_teacher']= prov_agg[["teaching_staff_edu_primary","teaching_staff_edu_lower_sec","teaching_staff_edu_upper_sec"]].sum(axis=1)
    prov_agg['good_qual_teacher']= prov_agg[["teaching_staff_edu_graduate","teaching_staff_edu_postgrad","teaching_staff_edu_phd"]].sum(axis=1)
        
    edu_levels = ["primary", "lower_sec", "upper_sec", "graduate", "postgrad", "phd"]
    weights = {"primary": 1, "lower_sec": 2, "upper_sec": 3, "graduate": 4, "postgrad": 5, "phd": 6}

    # No-pedagogy ratio
    prov_agg["no_pedagogy_ratio"] = (
        prov_agg[[f"teaching_staff_no_pedagogy_{l}" for l in edu_levels]].sum(axis=1)
        / prov_agg["teaching_staff_total"].replace(0, pd.NA)
    )

    # High/low qual ratio (teaching staff)
    prov_agg["teaching_high_qual_ratio"] = (
        prov_agg[[f"teaching_staff_edu_{l}" for l in ["graduate", "postgrad", "phd"]]].sum(axis=1)
        / prov_agg["teaching_staff_total"].replace(0, pd.NA)
    )
    prov_agg["teaching_low_qual_ratio"] = (
        prov_agg[[f"teaching_staff_edu_{l}" for l in ["primary", "lower_sec", "upper_sec"]]].sum(axis=1)
        / prov_agg["teaching_staff_total"].replace(0, pd.NA)
    )
    prov_agg['kids_population']=prov_agg[["pop_aged6_total","pop_aged6_11_total","pop_aged12_14_total","pop_aged15_17_total"]].sum(axis=1)

    # Qualification index per staff group
    for prefix in ["teaching_staff_edu", "non_teaching_staff_edu", "teaching_staff_no_pedagogy"]:
        weighted_sum = sum(prov_agg[f"{prefix}_{level}"] * w for level, w in weights.items())
        total = prov_agg[[f"{prefix}_{level}" for level in edu_levels]].sum(axis=1).replace(0, pd.NA)
        prov_agg[f"{prefix}_qual_index"] = weighted_sum / total

    def corr_heatmap(target, feature_cols, title):
        cols = [c for c in feature_cols if c in prov_agg.columns and c != target]
        corr = prov_agg[cols + [target]].corr()[[target]].drop(target)
        corr.columns = ['correlation']
        
        # Get the 5 largest positive and 5 largest negative correlations
        top_positive = corr.nlargest(5, 'correlation')
        top_negative = corr.nsmallest(10, 'correlation')
        
        # Combine and sort them
        corr = pd.concat([top_negative, top_positive]).drop_duplicates().sort_values('correlation')
        
        fig = px.imshow(
            corr,
            color_continuous_scale='RdBu_r',
            zmin=-1, zmax=1,
            aspect='auto',
            text_auto='.2f',
            title=title,
        )
        fig.update_layout(
            height=max(300, len(corr) * 44),
            coloraxis_colorbar=dict(title='r'),
        )
        st.plotly_chart(fig, use_container_width=True)

    def plot_features_grid(df, features, target):
        # Ensure column names match lowercase
        df = df.copy()
        df.columns = [c.lower() for c in df.columns]
        features = [f.lower() for f in features]
        target = target.lower()

        # --- Apply Dark Theme Styling ---
        plt.style.use("dark_background")
        # Match Streamlit's dark background roughly (#0e1117)
        rc_params = {
            "figure.facecolor": "#11141a",
            "axes.facecolor": "#11141a",
            "axes.edgecolor": "#31333f",
            "grid.color": "#31333f",
            "text.color": "#ffffff",
            "axes.labelcolor": "#a3a8b4",
            "xtick.color": "#a3a8b4",
            "ytick.color": "#a3a8b4",
        }
        plt.rcParams.update(rc_params)

        # Setup the 5x3 grid
        fig, axes = plt.subplots(5, 3, figsize=(20, 25))
        fig.suptitle(
            f"Features vs {target.replace('_', ' ').title()}",
            fontsize=22,
            color="#ffffff",
            weight="bold",
        )

        # Vibrant neon/pastel palette that pops beautifully on dark backgrounds
        colors = sns.color_palette("coolwarm", len(features))

        # Loop through features and populate the subplots dynamically
        for i, feature in enumerate(features):
            row = i // 3
            col = i % 3
            ax = axes[row, col]

            if feature in df.columns:
                sns.regplot(
                    data=df,
                    x=feature,
                    y=target,
                    ax=ax,
                    scatter_kws={"alpha": 0.6, "color": colors[i], "s": 40},
                    # Semi-transparent confidence interval area
                    line_kws={"color": "#ff4b4b", "linewidth": 2},
                )
                ax.set_title(feature, fontsize=12, color="#ffffff", pad=10)
                ax.set_xlabel(feature, fontsize=10)
                ax.set_ylabel(target, fontsize=10)
                ax.grid(True, linestyle="--", alpha=0.1)  # Subtle grid lines
            else:
                ax.text(
                    0.5,
                    0.5,
                    f"Feature '{feature}'\nnot found",
                    ha="center",
                    va="center",
                    fontsize=12,
                    color="#ff4b4b",
                )
                ax.axis("off")

        # Adjust layout for neat spacing
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])

        # Render natively in streamlit with matching background
        st.pyplot(fig, clear_figure=True)


# --- Example Call ---
# plot_features_grid(df_cleaned, features_list, target='enrollment_total')
    tab1, tab2, tab3 = st.tabs(["heatmap","scatter","pairplot"])

    with tab1:
        enrollment_raw = [
        "num_classrooms","wooden_rooms", "bamboo_buildings", "bamboo_rooms","schools_with_office", "schools_with_library",#Infrastructure & Buildings
        "schools_without_water", "schools_without_latrine","classroom_area_per_student","preschool_with_sport_facility",#Amenities & Environment
        "total_staff_total","principal_avg_service_years","bad_qual_teacher","good_qual_teacher",# Human Resources & Professional Qualifications
        "pb_fund_per_school_riel","funding_school_income", "funding_community", "funding_govt_building", "funding_abroad", "funding_ios_ngos",#funding
        "pupil_teacher_ratio","pupil_classroom_ratio","pct_schools_two_shift","pct_schools_in_pagoda",# Supply/Demand Matching Ratios
        "kids_population",# Target Population Demographics
        ]
        corr_heatmap('enrollment_total', enrollment_raw,
                     'Raw Features × Total Enrollment (by Province, excl. 2021)')
        dropout_raw = [
        "num_classrooms","wooden_rooms", "bamboo_buildings", "bamboo_rooms","schools_with_office", "schools_with_library",#Infrastructure & Buildings
        "schools_without_water", "schools_without_latrine","classroom_area_per_student","preschool_with_sport_facility",#Amenities & Environment
        "total_staff_total","principal_avg_service_years","bad_qual_teacher","good_qual_teacher",# Human Resources & Professional Qualifications
        "pb_fund_per_school_riel","funding_school_income", "funding_community", "funding_govt_building", "funding_abroad", "funding_ios_ngos",#funding
        "pupil_teacher_ratio","pupil_classroom_ratio","pct_schools_two_shift","pct_schools_in_pagoda",# Supply/Demand Matching Ratios
        "pct_overage_enrollment_primary", "pct_overage_enrollment_lower_sec", "pct_overage_enrollment_upper_sec","kids_population"# Target Population Demographics
        ]
        corr_heatmap('avg_dropout_rate', dropout_raw,
                     'Raw Features × Avg drop out rate (by Province, excl. 2021)')
        teacher_qual_raw = [
        "num_classrooms","wooden_rooms", "bamboo_buildings", "bamboo_rooms","schools_with_office", "schools_with_library",#Infrastructure & Buildings
        "schools_without_water", "schools_without_latrine","classroom_area_per_student","preschool_with_sport_facility",#Amenities & Environment
        "pb_fund_per_school_riel","funding_school_income", "funding_community", "funding_govt_building", "funding_abroad", "funding_ios_ngos",#funding
        "pupil_teacher_ratio","pupil_classroom_ratio","pct_schools_two_shift","pct_schools_in_pagoda",# Supply/Demand Matching Ratios
        "kids_population"# Target Population Demographics
        ]
        corr_heatmap('teaching_staff_edu_qual_index', teacher_qual_raw,
                     'Raw Features × teacher quality (by Province, excl. 2021)')

    with tab2:
        features_list_enrollment = [
            "classroom_area_per_student",
            "wooden_rooms",
            "pb_fund_per_school_riel",
            "bamboo_buildings",
            "pct_schools_two_shift",
            "bamboo_rooms",
            "pct_schools_in_pagoda",
            "pupil_teacher_ratio",
            "funding_community",
            "pupil_classroom_ratio",
            "schools_with_library",
            "bad_qual_teacher",
            "total_staff_total",
            "kids_population",
            "num_classrooms",
        ]
        plot_features_grid(prov_agg, features_list_enrollment, target='enrollment_total')
        drop_out_features = [
            "pct_schools_in_pagoda",
            "principal_avg_service_years",
            "good_qual_teacher",
            "pb_fund_per_school_riel",
            "total_staff_total",
            "bad_qual_teacher",
            "kids_population",
            "num_classrooms",
            "schools_with_library",
            "schools_with_office",
            "pct_schools_two_shift",
            "pct_overage_enrollment_lower_sec",
            "pupil_teacher_ratio",
            "pct_overage_enrollment_primary",
            "wooden_rooms",
        ]
        plot_features_grid(prov_agg, drop_out_features, target='avg_dropout_rate')
        teacher_quality_features = [
            "classroom_area_per_student",
            "wooden_rooms",
            "pct_schools_two_shift",
            "pupil_teacher_ratio",
            "bamboo_buildings",
            "bamboo_rooms",
            "funding_abroad",
            "schools_without_water",
            "pb_fund_per_school_riel",
            "funding_ios_ngos",
            "num_classrooms",
            "schools_with_office",
            "schools_with_library",
            "pct_schools_in_pagoda",
            "preschool_with_sport_facility",
        ]
        plot_features_grid(prov_agg, teacher_quality_features, target='teaching_staff_edu_qual_index')

    with tab3:
        st.markdown("### Pairplot / Scatter Matrix")
        # numeric candidate features
        numeric_cols = [c for c in prov_agg.columns if pd.api.types.is_numeric_dtype(prov_agg[c])]
        default_feats = [f for f in features_list_enrollment if f in numeric_cols][:6]
        selected_pair_feats = st.multiselect("Select features for pairplot (3-8 recommended)", options=numeric_cols, default=default_feats)
        pair_sample = st.number_input("Max sample rows (0 = all)", min_value=0, value=0, step=1)
        pair_corr_method = st.selectbox("Correlation method (for annotations)",["pearson","spearman"], index=0)

        if len(selected_pair_feats) < 2:
            st.info("Select at least 2 numeric features to build a pairplot.")
        else:
            df_pair = prov_agg[selected_pair_feats].dropna()
            if pair_sample and pair_sample > 0 and pair_sample < len(df_pair):
                df_pair = df_pair.sample(pair_sample, random_state=42)

            # Pairplot using seaborn (corner to reduce plots)
            try:
                pp = sns.pairplot(df_pair, corner=True, diag_kind='kde', plot_kws={'alpha':0.6, 's':40})
                st.pyplot(pp.fig)
                plt.close(pp.fig)
            except Exception as e:
                st.error(f"Pairplot failed: {e}")

            # show correlation table for selected features
            corr_sel = df_pair.corr(method=pair_corr_method)
            st.markdown("**Correlation matrix (selected features)**")
            st.dataframe(corr_sel.style.background_gradient(cmap='RdBu_r').format("{:.2f}"))


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 7.5 — Modelling & Forecasts
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Modelling & Forecasts":
    st.title("🚀 Advanced Modelling & Education Forecasts")
    st.markdown("---")
    
    st.write("""
    This section uses a comprehensive ML pipeline to forecast key education indicators for Cambodia.
    We evaluate multiple models (Random Forest, XGBoost, WOA-SVR, ARIMAX, etc.) to identify the most accurate predictor for each target.
    """)

    # 1. Targets & Features Configuration
    TARGETS = {
        'Total Enrollment': 'enrollment_total',
        'Average Dropout Rate': 'avg_dropout_rate',
        'Teacher Quality Index': 'teaching_staff_edu_qual_index'
    }
    
    # Pre-calculated features from notebook analysis
    FEATURE_MAP = {
        'enrollment_total': ['total_staff_total', 'kids_population', 'num_classrooms'],
        'avg_dropout_rate': ['buildings_repaired', 'over_age_enrollment_total', 'staff_per_school', 
                             'buildings_per_school', 'gross_admission_rate_total', 'avg_transition_rate', 
                             'teaching_staff_edu_qual_index'],
        'teaching_staff_edu_qual_index': ['schools_without_water', 'schools_without_latrine', 
                                          'principal_avg_service_years', 'principal_upper_sec_plus_edu', 
                                          'buildings_poor_roof', 'pb_fund_per_school_riel', 
                                          'classrooms_per_school', 'gross_admission_rate_total', 
                                          'transition_rate_lower_sec_total']
    }

    # 2. Data Engineering (Alignment with Notebook)
    def engineer_targets(df):
        d = df.copy()
        # Drop 2021 as it's an outlier year
        d = d[d['year'] != 2021].reset_index(drop=True)
        
        # Repetition/Dropout/Overage/Transition
        if 'g1_repetition' in d.columns:
            d['avg_repetition_rate'] = d[[f'g{i}_repetition' for i in range(1, 13)]].mean(axis=1)
        if 'g1_dropout' in d.columns:
            d['avg_dropout_rate'] = d[[f'g{i}_dropout' for i in range(1, 13)]].mean(axis=1)
        
        overage_cols = ['pct_overage_enrollment_primary','pct_overage_enrollment_lower_sec','pct_overage_enrollment_upper_sec']
        if all(c in d.columns for c in overage_cols):
            d['over_age_enrollment_total'] = d[overage_cols].sum(axis=1)
            
        if 'transition_rate_lower_sec_total' in d.columns:
            d['avg_transition_rate'] = d[['transition_rate_lower_sec_total', 'transition_rate_upper_sec_total']].mean(axis=1)

        d['kids_population'] = d[['pop_aged6_total','pop_aged6_11_total','pop_aged12_14_total','pop_aged15_17_total']].sum(axis=1)
        
        # Qual Index
        edu_levels = ['primary','lower_sec','upper_sec','graduate','postgrad','phd']
        weights = {'primary':1,'lower_sec':2,'upper_sec':3,'graduate':4,'postgrad':5,'phd':6}
        if 'teaching_staff_edu_primary' in d.columns:
            weighted_sum = sum(d[f'teaching_staff_edu_{l}'] * w for l, w in weights.items())
            total = d[[f'teaching_staff_edu_{l}' for l in edu_levels]].sum(axis=1).replace(0, pd.NA)
            d['teaching_staff_edu_qual_index'] = weighted_sum / total
        
        # Handle some transformations (log/sqrt) if required by feature list
        if 'buildings_repaired' in d.columns:
            d['log_buildings_repaired'] = np.log1p(d['buildings_repaired'])
        if 'buildings_per_school' in d.columns:
            d['sqrt_buildings_per_school'] = np.sqrt(d['buildings_per_school'])
        if 'schools_without_water' in d.columns:
            d['log_schools_without_water'] = np.log1p(d['schools_without_water'])
        if 'schools_without_latrine' in d.columns:
            d['log_schools_without_latrine'] = np.log1p(d['schools_without_latrine'])
        if 'principal_upper_sec_plus_edu' in d.columns:
            d['log_principal_upper_sec_plus_edu'] = np.log1p(d['principal_upper_sec_plus_edu'])
        if 'buildings_poor_roof' in d.columns:
            d['log_buildings_poor_roof'] = np.log1p(d['buildings_poor_roof'])
        if 'pb_fund_per_school_riel' in d.columns:
            d['log_pb_fund_per_school_riel'] = np.log1p(d['pb_fund_per_school_riel'])
        if 'classrooms_per_school' in d.columns:
            d['sqrt_classrooms_per_school'] = np.sqrt(d['classrooms_per_school'])

        return d

    # 3. User Selection
    col1, col2 = st.columns([1, 1])
    with col1:
        target_label = st.selectbox("Select Forecast Target", list(TARGETS.keys()))
        target_col = TARGETS[target_label]
    with col2:
        forecast_years = st.multiselect("Forecast Horizon", [2027, 2028, 2029, 2030], default=[2027, 2028, 2029, 2030])

    if st.button("Run ML Pipeline"):
        with st.spinner(f"Training models for {target_label}..."):
            processed_df = engineer_targets(df)
            
            # Simple feature mapping update for transformed cols
            raw_feats = FEATURE_MAP[target_col]
            final_feats = []
            for f in raw_feats:
                if f == 'buildings_repaired': final_feats.append('log_buildings_repaired')
                elif f == 'buildings_per_school': final_feats.append('sqrt_buildings_per_school')
                elif f == 'schools_without_water': final_feats.append('log_schools_without_water')
                elif f == 'schools_without_latrine': final_feats.append('log_schools_without_latrine')
                elif f == 'principal_upper_sec_plus_edu': final_feats.append('log_principal_upper_sec_plus_edu')
                elif f == 'buildings_poor_roof': final_feats.append('log_buildings_poor_roof')
                elif f == 'pb_fund_per_school_riel': final_feats.append('log_pb_fund_per_school_riel')
                elif f == 'classrooms_per_school': final_feats.append('sqrt_classrooms_per_school')
                else: final_feats.append(f)
            
            # 4. Pipeline Logic
            # Prep Data
            feats = [c for c in final_feats if c in processed_df.columns]
            train_mask = processed_df['year'] <= 2023
            val_mask = (processed_df['year'] > 2023) & (processed_df['year'] <= 2026)
            
            X_train_raw = processed_df.loc[train_mask, feats]
            X_val_raw = processed_df.loc[val_mask, feats]
            y_train = processed_df.loc[train_mask, target_col]
            y_val = processed_df.loc[val_mask, target_col]

            imputer = SimpleImputer(strategy='median')
            X_train_imp = pd.DataFrame(imputer.fit_transform(X_train_raw), columns=feats)
            X_val_imp = pd.DataFrame(imputer.transform(X_val_raw), columns=feats)

            scaler = StandardScaler()
            X_train_sc = scaler.fit_transform(X_train_imp)
            X_val_sc = scaler.transform(X_val_imp)

            log_transform = (target_col == 'avg_dropout_rate')
            y_fit = np.log1p(y_train.values) if log_transform else y_train.values

            models = {
                'Random Forest':     (RandomForestRegressor(n_estimators=150, max_depth=8, min_samples_leaf=4, random_state=42, n_jobs=-1), X_train_imp, X_val_imp),
                'Gradient Boosting': (GradientBoostingRegressor(n_estimators=150, max_depth=4, learning_rate=0.05, random_state=42),         X_train_imp, X_val_imp),
                'XGBoost':           (xgb.XGBRegressor(n_estimators=150, max_depth=4, learning_rate=0.05, random_state=42, verbosity=0),     X_train_imp, X_val_imp),
                'SVR (RBF)':         (SVR(kernel='rbf',    C=10, epsilon=0.1),                                                               X_train_sc,  X_val_sc),
                'SVR (Linear)':      (SVR(kernel='linear', C=1),                                                                             X_train_sc,  X_val_sc),
                'Ridge':             (Ridge(alpha=1.0),                                                                                      X_train_imp, X_val_imp),
                'Lasso':             (Lasso(alpha=0.01, max_iter=5000),                                                                      X_train_imp, X_val_imp),
            }

            records, val_preds_dict = [], {}
            for name, (model, X_tr, X_v) in models.items():
                try:
                    model.fit(X_tr, y_fit)
                    raw_pred = model.predict(X_v)
                    y_pred = np.expm1(raw_pred) if log_transform else raw_pred
                    records.append({
                        'Model': name,
                        'R²': r2_score(y_val, y_pred),
                        'RMSE': np.sqrt(mean_squared_error(y_val, y_pred)),
                        'MAE': mean_absolute_error(y_val, y_pred)
                    })
                    val_preds_dict[name] = y_pred
                except Exception as e:
                    st.error(f"Model {name} failed: {e}")

            results_df = pd.DataFrame(records).sort_values('R²', ascending=False).reset_index(drop=True)
            
            # Display Metrics
            st.subheader("📊 Model Comparison Dashboard")
            st.dataframe(results_df.style.highlight_max(subset=['R²'], color='#4CAF50').format({"R²": "{:.4f}", "RMSE": "{:.2f}", "MAE": "{:.2f}"}))
            
            best_name = results_df.iloc[0]['Model']
            st.success(f"✅ Recommended Model: **{best_name}**")

            # 5. Final Forecast (Robust Feature Projection)
            st.markdown("---")
            st.subheader(f"📈 Input Feature Projections for {target_label}")
            st.write("Before forecasting the target, we project the necessary input features using best-fit trends (Linear, Log, Exp, or Sqrt).")
            
            future_years = np.array(forecast_years)
            
            # Group historical data by year for projection fitting
            national_means = processed_df.groupby('year')[raw_feats].mean().reset_index()
            
            # Setup columns for projection plots
            proj_cols = st.columns(3)
            
            # Logic to store projected values
            proj_data = {'year': future_years}
            
            for idx, feat in enumerate(raw_feats):
                # 1. Fit best curve for this feature
                fit_name, pred_fn, r2 = _fit_candidates(national_means['year'].values, national_means[feat].values)
                
                # 2. Project future values
                y_proj = pred_fn(future_years)
                proj_data[feat] = y_proj
                
                # 3. Plot for UI
                with proj_cols[idx % 3]:
                    fig_p = go.Figure()
                    fig_p.add_trace(go.Scatter(x=national_means['year'], y=national_means[feat], name='Hist Mean', mode='markers', marker=dict(color='#2196F3')))
                    fig_p.add_trace(go.Scatter(x=future_years, y=y_proj, name='Projected', line=dict(color='#D85A30', dash='dash')))
                    fig_p.update_layout(title=f"{feat}<br><span style='font-size:10px'>{fit_name.upper()} (R²={r2:.2f})</span>", height=250, margin=dict(l=20, r=20, t=40, b=20), showlegend=False, template='plotly_dark')
                    st.plotly_chart(fig_p, use_container_width=True)

            # Create projected feature dataframe and apply transforms
            X_fut_df = pd.DataFrame(proj_data)
            # Re-apply transforms if needed
            if 'buildings_repaired' in X_fut_df.columns: X_fut_df['log_buildings_repaired'] = np.log1p(X_fut_df['buildings_repaired'])
            if 'buildings_per_school' in X_fut_df.columns: X_fut_df['sqrt_buildings_per_school'] = np.sqrt(X_fut_df['buildings_per_school'])
            if 'schools_without_water' in X_fut_df.columns: X_fut_df['log_schools_without_water'] = np.log1p(X_fut_df['schools_without_water'])
            if 'schools_without_latrine' in X_fut_df.columns: X_fut_df['log_schools_without_latrine'] = np.log1p(X_fut_df['schools_without_latrine'])
            if 'principal_upper_sec_plus_edu' in X_fut_df.columns: X_fut_df['log_principal_upper_sec_plus_edu'] = np.log1p(X_fut_df['principal_upper_sec_plus_edu'])
            if 'buildings_poor_roof' in X_fut_df.columns: X_fut_df['log_buildings_poor_roof'] = np.log1p(X_fut_df['buildings_poor_roof'])
            if 'pb_fund_per_school_riel' in X_fut_df.columns: X_fut_df['log_pb_fund_per_school_riel'] = np.log1p(X_fut_df['pb_fund_per_school_riel'])
            if 'classrooms_per_school' in X_fut_df.columns: X_fut_df['sqrt_classrooms_per_school'] = np.sqrt(X_fut_df['classrooms_per_school'])

            X_fut_imp = pd.DataFrame(imputer.transform(X_fut_df[feats]), columns=feats)
            X_fut_sc = scaler.transform(X_fut_imp)

            # Re-train best model on full data
            full_X_imp = pd.concat([X_train_imp, X_val_imp])
            full_y = np.log1p(pd.concat([y_train, y_val])) if log_transform else pd.concat([y_train, y_val])
            full_X_sc = np.vstack([X_train_sc, X_val_sc])
            
            # Best model instance
            best_model_def = {
                'Random Forest':     RandomForestRegressor(n_estimators=150, max_depth=8, min_samples_leaf=4, random_state=42, n_jobs=-1),
                'Gradient Boosting': GradientBoostingRegressor(n_estimators=150, max_depth=4, learning_rate=0.05, random_state=42),
                'XGBoost':           xgb.XGBRegressor(n_estimators=150, max_depth=4, learning_rate=0.05, random_state=42, verbosity=0),
                'SVR (RBF)':         SVR(kernel='rbf',    C=10, epsilon=0.1),
                'SVR (Linear)':      SVR(kernel='linear', C=1),
                'Ridge':             Ridge(alpha=1.0),
                'Lasso':             Lasso(alpha=0.01, max_iter=5000),
            }
            final_model = best_model_def[best_name]
            use_sc = ('SVR' in best_name)
            final_model.fit(full_X_sc if use_sc else full_X_imp, full_y)
            
            raw_fut = final_model.predict(X_fut_sc if use_sc else X_fut_imp)
            y_future = np.expm1(raw_fut) if log_transform else raw_fut

            # 6. Comprehensive Plotting (Remake)
            st.markdown("---")
            st.subheader(f"🎯 Model Performance & Forecast: {target_label}")
            
            # Create a 3-column dashboard using subplots
            fig = make_subplots(
                rows=1, cols=3,
                subplot_titles=("R² Comparison", "Error Metrics (RMSE/MAE)", f"Forecast: {best_name}"),
                column_widths=[0.25, 0.25, 0.5],
                specs=[[{"type": "bar"}, {"type": "bar"}, {"type": "scatter"}]]
            )

            # Trace 1: R2 Bar
            sorted_res = results_df.sort_values('R²')
            fig.add_trace(go.Bar(
                x=sorted_res['R²'], y=sorted_res['Model'], orientation='h',
                marker=dict(color=['#D85A30' if m == best_name else '#378ADD' for m in sorted_res['Model']]),
                name='R²'
            ), row=1, col=1)

            # Trace 2: Error Metrics
            fig.add_trace(go.Bar(y=results_df['Model'], x=results_df['RMSE'], name='RMSE', orientation='h', marker_color='#1D9E75'), row=1, col=2)
            fig.add_trace(go.Bar(y=results_df['Model'], x=results_df['MAE'], name='MAE', orientation='h', marker_color='#EF9F27'), row=1, col=2)

            # Trace 3: The Forecast (with Predicted Values)
            # Historical Actuals
            hist_data = processed_df.groupby('year')[target_col].mean().reset_index()
            fig.add_trace(go.Scatter(x=hist_data['year'], y=hist_data[target_col], name='Historical actual', line=dict(color='#2196F3', width=3), mode='lines+markers'), row=1, col=3)
            
            # Validation Predictions (The "Predicted Value" part)
            best_val_preds = val_preds_dict[best_name]
            val_df = pd.DataFrame({'year': processed_df.loc[val_mask, 'year'], 'pred': best_val_preds})
            val_means = val_df.groupby('year')['pred'].mean().reset_index()
            fig.add_trace(go.Scatter(x=val_means['year'], y=val_means['pred'], name='Val prediction', mode='markers', marker=dict(color='#4CAF50', size=10, symbol='diamond', line=dict(width=2, color='white'))), row=1, col=3)

            # Future Forecast
            fig.add_trace(go.Scatter(x=future_years, y=y_future, name='ML Forecast', line=dict(color='#F44336', width=3, dash='dash'), mode='lines+markers', marker=dict(size=8)), row=1, col=3)

            fig.update_layout(height=500, template='plotly_dark', showlegend=True, barmode='group')
            st.plotly_chart(fig, use_container_width=True)

            st.markdown("---")
            st.subheader(f"📅 {target_label} Forecast Values")
            forecast_df = pd.DataFrame({'Year': future_years, 'Forecast': y_future})
            st.table(forecast_df.style.format({"Forecast": "{:.2f}"}))

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 8 — Long-term Trends (appendix)
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Long-term Trends":
    st.title("Long-term Trends")
    st.caption("Historical data — longer time horizon")
    st.markdown("---")

    df2_clean = df2.copy()
    df2_clean.rename(columns={'Academic Year': 'Year'}, inplace=True)
    df2_clean['Year'] = df2_clean['Year'].astype(str).str.split('-').str[0].astype(int)
    df2_clean.fillna(0, inplace=True)

    tab1, tab2 = st.tabs(["Raw Counts", "Indexed Growth"])

    with tab1:
        metric = st.selectbox("Select metric", ['Schools', 'Classes', 'Students', 'Staff'])
        prefix_map = {'Schools': 'school', 'Classes': 'class', 'Students': 'student', 'Staff': 'staff'}
        prefix = prefix_map[metric]
        type_cols = {
            'Preschool': f'{prefix}_pre',
            'Primary': f'{prefix}_pri',
            'Lower Sec': f'{prefix}_l.sec',
            'Upper Sec': f'{prefix}_u.sec',
        }
        existing_t = {k: v for k, v in type_cols.items() if v in df2_clean.columns}
        if existing_t:
            fig = go.Figure()
            colors = {'Preschool': '#FF6B6B', 'Primary': '#4ECDC4',
                      'Lower Sec': '#45B7D1', 'Upper Sec': '#96CEB4'}
            for label, col in existing_t.items():
                fig.add_trace(go.Scatter(x=df2_clean['Year'], y=df2_clean[col],
                                         name=label, mode='lines',
                                         fill='tozeroy', line=dict(color=colors.get(label, '#999'))))
            fig.update_layout(title=f'{metric} Growth by Type Over Time',
                              template='plotly_white', hovermode='x unified', height=450)
            st.plotly_chart(fig, use_container_width=True)

    with tab2:
        base_year_options = sorted(df2_clean['Year'].unique())
        base_year = st.selectbox("Base year (= 100)", base_year_options, index=0)
        metric2 = st.selectbox("Select metric ", ['Schools', 'Classes', 'Students', 'Staff'])
        prefix2 = prefix_map[metric2]
        type_cols2 = {
            'Preschool': f'{prefix2}_pre',
            'Primary': f'{prefix2}_pri',
            'Lower Sec': f'{prefix2}_l.sec',
            'Upper Sec': f'{prefix2}_u.sec',
        }
        existing_t2 = {k: v for k, v in type_cols2.items() if v in df2_clean.columns}
        if existing_t2:
            base_row = df2_clean[df2_clean['Year'] == base_year].iloc[0]
            fig = go.Figure()
            for label, col in existing_t2.items():
                base_val = base_row[col] if base_row[col] != 0 else 1
                indexed = df2_clean[col] / base_val * 100
                fig.add_trace(go.Scatter(x=df2_clean['Year'], y=indexed,
                                         name=label, mode='lines+markers'))
            fig.add_hline(y=100, line_dash='dash', line_color='gray',
                         annotation_text=f'Base ({base_year})')
            fig.update_layout(title=f'Indexed Growth — {metric2} (Base {base_year} = 100)',
                              template='plotly_white', hovermode='x unified',
                              yaxis_title='Index (Base = 100)', height=450)
            st.plotly_chart(fig, use_container_width=True)
