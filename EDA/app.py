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

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Cambodia Education Dashboard",
    page_icon="🇰🇭",
    layout="wide"
)

# ─── Load Data ────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv('cleaned_new_data.csv')
    df2 = pd.read_csv('appendix.csv')
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
        "Long-term Trends",
        "Relationship Analysis",
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
        if 'schools_without_water' in d_latest.columns:
            water_df = d_latest.groupby('province')[['schools_without_water', 'schools_without_latrine']].sum()
            water_df = water_df.sort_values('schools_without_water', ascending=True).reset_index()
            fig = go.Figure()
            fig.add_trace(go.Bar(y=water_df['province'], x=water_df['schools_without_water'],
                                 name='No Water', orientation='h', marker_color='#2196F3'))
            fig.add_trace(go.Bar(y=water_df['province'], x=water_df['schools_without_latrine'],
                                 name='No Latrine', orientation='h', marker_color='#FF5722'))
            fig.update_layout(barmode='group', title=f'Schools Without Facilities ({latest_year})',
                              template='plotly_white', height=500)
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

    def corr_heatmap(target, feature_cols, title):
        cols = [c for c in feature_cols if c in prov_agg.columns and c != target]
        corr = prov_agg[cols + [target]].corr()[[target]].drop(target)
        corr.columns = ['correlation']
        
        # Get the 5 largest positive and 5 largest negative correlations
        top_positive = corr.nlargest(5, 'correlation')
        top_negative = corr.nsmallest(5, 'correlation')
        
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

    tab1, tab2 = st.tabs(["target","Funds"])

    with tab1:
        enrollment_raw = [
        "num_schools", "num_classes", "classes_in_pagoda","repeaters_total","total_staff_total",
        "two_shift_schools_lycee", "floating_schools_lycee", "schools_in_pagoda_lycee", "attached_preschool_lycee","schools_without_water", "schools_without_latrine",
        "principal_avg_age", "principal_avg_service_years", "principal_upper_sec_plus_edu", "principal_female",
        "num_primary_schools", "num_cluster_schools", "satellite_schools",
        #"pct_overage_enrollment_primary", "pct_overage_enrollment_lower_sec", "pct_overage_enrollment_upper_sec",
        #"teaching_staff_edu_primary", "teaching_staff_edu_lower_sec", "teaching_staff_edu_upper_sec",
        #"teaching_staff_edu_graduate", "teaching_staff_edu_postgrad", "teaching_staff_edu_phd",
        #"non_teaching_staff_edu_primary", "non_teaching_staff_edu_lower_sec", "non_teaching_staff_edu_upper_sec",
        #"non_teaching_staff_edu_graduate", "non_teaching_staff_edu_postgrad", "non_teaching_staff_edu_phd",
        #"teaching_staff_no_pedagogy_primary", "teaching_staff_no_pedagogy_lower_sec", "teaching_staff_no_pedagogy_upper_sec",
        #"teaching_staff_no_pedagogy_graduate", "teaching_staff_no_pedagogy_postgrad", "teaching_staff_no_pedagogy_phd",
        "num_buildings_total", "num_rooms_total",
        "concrete_brick_buildings","wooden_buildings","bamboo_buildings",
        "buildings_repaired", "buildings_constructed",
        "buildings_poor_floor", "buildings_poor_roof", "buildings_poor_wall",
        "schools_with_office", "schools_with_library",
        "school_area_land_m2", "school_area_playground_m2", "classroom_area_per_student", "preschool_with_sport_facility",
        "sport_volleyball", "sport_football", "sport_basketball", "sport_climbing_ropes",
        "sport_shotput", "sport_high_jump", "sport_long_jump", "sport_running",
        "pb_fund_per_student_riel", "pb_fund_per_school_riel",
        "funding_school_income", "funding_community", "funding_govt_building", "funding_abroad", "funding_ios_ngos",
        "pupils_per_school", "teachers_per_school", "staff_per_school",
        "buildings_per_school", "rooms_per_school", "classrooms_per_school", "classes_per_school",
        "pupil_teacher_ratio", "pupil_staff_ratio", "pupil_class_ratio", "pupil_classroom_ratio",
        "classes_per_classroom", "classroom_area_per_pupil_m2",
        "gross_admission_rate_total","net_admission_rate_total","pct_overage_admission_total","transition_rate_lower_sec_total","transition_rate_upper_sec_total",
        "avg_repetition_rate","avg_dropout_rate","avg_repetition_rate"
        ]
        corr_heatmap('enrollment_total', enrollment_raw,
                     'Raw Features × Total Enrollment (by Province, excl. 2021)')
        corr_heatmap('teaching_staff_total', enrollment_raw,
                     'Raw Features × Total Teaching Staff (by Province, excl. 2021)')
        dropout_raw = [
        "num_schools", "num_classes", "classes_in_pagoda","repeaters_total","total_staff_total",
        "two_shift_schools_lycee", "floating_schools_lycee", "schools_in_pagoda_lycee", "attached_preschool_lycee","schools_without_water", "schools_without_latrine",
        "principal_avg_age", "principal_avg_service_years", "principal_upper_sec_plus_edu", "principal_female",
        "num_primary_schools", "num_cluster_schools", "satellite_schools",
        "pct_overage_enrollment_primary", "pct_overage_enrollment_lower_sec", "pct_overage_enrollment_upper_sec",
        "teaching_staff_edu_primary", "teaching_staff_edu_lower_sec",# "teaching_staff_edu_upper_sec",
        "teaching_staff_edu_graduate", 
        "teaching_staff_edu_postgrad", "teaching_staff_edu_phd",
        "non_teaching_staff_edu_primary", "non_teaching_staff_edu_lower_sec", "non_teaching_staff_edu_upper_sec",
        "non_teaching_staff_edu_graduate", "non_teaching_staff_edu_postgrad", "non_teaching_staff_edu_phd",
        "teaching_staff_no_pedagogy_primary", "teaching_staff_no_pedagogy_lower_sec", "teaching_staff_no_pedagogy_upper_sec",
        "teaching_staff_no_pedagogy_graduate", "teaching_staff_no_pedagogy_postgrad", "teaching_staff_no_pedagogy_phd",
        "num_buildings_total", "num_rooms_total",
        "concrete_brick_buildings","wooden_buildings","bamboo_buildings",
        "buildings_repaired", "buildings_constructed",
        "buildings_poor_floor", "buildings_poor_roof", "buildings_poor_wall",
        "schools_with_office", "schools_with_library",
        "school_area_land_m2", "school_area_playground_m2", "classroom_area_per_student", "preschool_with_sport_facility",
        "sport_volleyball", "sport_football", "sport_basketball", "sport_climbing_ropes",
        "sport_shotput", "sport_high_jump", "sport_long_jump", "sport_running",
        "pb_fund_per_student_riel", "pb_fund_per_school_riel",
        "funding_school_income", "funding_community", "funding_govt_building", "funding_abroad", "funding_ios_ngos",
        "pupils_per_school", "teachers_per_school", "staff_per_school",
        "buildings_per_school", "rooms_per_school", "classrooms_per_school", "classes_per_school",
        "pupil_teacher_ratio", "pupil_staff_ratio", "pupil_class_ratio", "pupil_classroom_ratio",
        "classes_per_classroom", "classroom_area_per_pupil_m2",
        "gross_admission_rate_total","net_admission_rate_total","pct_overage_admission_total","transition_rate_lower_sec_total","transition_rate_upper_sec_total",
        "avg_repetition_rate","avg_repetition_rate"
        
        ]
        corr_heatmap('avg_dropout_rate', dropout_raw,
                     'Raw Features × Avg drop out rate (by Province, excl. 2021)')

    with tab2:
        income_raw = [
        "num_schools", "num_classes", "classes_in_pagoda","repeaters_total","total_staff_total",
        "two_shift_schools_lycee", "floating_schools_lycee", "schools_in_pagoda_lycee", "attached_preschool_lycee","schools_without_water", "schools_without_latrine",
        "principal_avg_age", "principal_avg_service_years", "principal_upper_sec_plus_edu", "principal_female",
        "", "num_cluster_schools", "satellite_schools",
        "pct_overage_enrollment_primary", #"pct_overage_enrollment_lower_sec", "pct_overage_enrollment_upper_sec",
        "teaching_staff_edu_primary", "teaching_staff_edu_lower_sec", "teaching_staff_edu_upper_sec",
        "teaching_staff_edu_graduate", 
        "teaching_staff_edu_postgrad", "teaching_staff_edu_phd",
        "non_teaching_staff_edu_primary", "non_teaching_staff_edu_lower_sec", "non_teaching_staff_edu_upper_sec",
        "non_teaching_staff_edu_graduate", "non_teaching_staff_edu_postgrad", "non_teaching_staff_edu_phd",
        "teaching_staff_no_pedagogy_primary", "teaching_staff_no_pedagogy_lower_sec", "teaching_staff_no_pedagogy_upper_sec",
        "teaching_staff_no_pedagogy_graduate", "teaching_staff_no_pedagogy_postgrad", "teaching_staff_no_pedagogy_phd",
        "num_buildings_total", "num_rooms_total",
        "concrete_brick_buildings","wooden_buildings","bamboo_buildings",
        "buildings_repaired", "buildings_constructed",
        "buildings_poor_floor", "buildings_poor_roof", "buildings_poor_wall",
        "schools_with_office", "schools_with_library",
        "school_area_land_m2", "school_area_playground_m2", "classroom_area_per_student", "preschool_with_sport_facility",
        "sport_volleyball", "sport_football", "sport_basketball", "sport_climbing_ropes",
        "sport_shotput", "sport_high_jump", "sport_long_jump", "sport_running",
        "pupils_per_school", "teachers_per_school", "staff_per_school",
        "buildings_per_school", "rooms_per_school", "classrooms_per_school", "classes_per_school",
        "pupil_teacher_ratio", "pupil_staff_ratio", "pupil_class_ratio", "pupil_classroom_ratio",
        "classes_per_classroom", "classroom_area_per_pupil_m2",
        "gross_admission_rate_total","net_admission_rate_total","pct_overage_admission_total","transition_rate_lower_sec_total","transition_rate_upper_sec_total",
        "avg_repetition_rate","avg_repetition_rate"]
        corr_heatmap('funding_school_income', income_raw,
                     'Raw Features × school income (by Province, excl. 2021)')
        corr_heatmap('funding_community', income_raw,
                     'Raw Features × funding_community (by Province, excl. 2021)')
        corr_heatmap('funding_govt_building', income_raw,
                     'Raw Features × funding_govt_building (by Province, excl. 2021)')
        corr_heatmap('funding_abroad', income_raw,
                     'Raw Features × funding_abroad (by Province, excl. 2021)')
        corr_heatmap('funding_school_income', income_raw,
                     'Raw Features × funding_ios_ngos (by Province, excl. 2021)')


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
