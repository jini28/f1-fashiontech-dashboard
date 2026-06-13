
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="F1 FashionTech Dashboard",
    page_icon="🏎️",
    layout="wide"
)

# -----------------------------
# Load Data
# -----------------------------
analysis_df = pd.read_csv("data/f1_fashion_analysis.csv")
trends_long = pd.read_csv("data/f1_fashion_trends.csv")
team_performance = pd.read_csv("data/f1_team_performance.csv")

trends_long["date"] = pd.to_datetime(trends_long["date"])

# -----------------------------
# CSS Styling
# -----------------------------
st.markdown("""
<style>
.stApp {
    background-color: #171717;
    color: #F2F2F2;
}

.main-title {
    font-size: 46px;
    font-weight: 800;
    color: #FFFFFF;
    margin-bottom: 0px;
}

.subtitle {
    font-size: 17px;
    color: #A8A8A8;
    margin-bottom: 30px;
}

.metric-card {
    background-color: #242423;
    padding: 25px;
    border-radius: 16px;
    border: 1px solid #343434;
    box-shadow: 0px 4px 25px rgba(0,0,0,0.25);
}

.metric-value {
    font-size: 34px;
    font-weight: 800;
    color: #FFFFFF;
}

.metric-label {
    font-size: 15px;
    color: #C9C9C9;
    margin-top: 6px;
}

.metric-change {
    font-size: 14px;
    color: #42B21E;
    margin-top: 8px;
    font-weight: 600;
}

.chart-card {
    background-color: #242423;
    padding: 25px;
    border-radius: 18px;
    border: 1px solid #3A3A3A;
    margin-top: 24px;
}

.section-title {
    font-size: 16px;
    letter-spacing: 2px;
    color: #AAA7A0;
    font-weight: 700;
    text-transform: uppercase;
    margin-bottom: 18px;
}

hr {
    border: 1px solid #333333;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Header
# -----------------------------
st.markdown('<div class="main-title">From Grid to Wardrobe</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">An interactive FashionTech dashboard analyzing the relationship between Formula 1 team performance and fashion/merch search demand.</div>',
    unsafe_allow_html=True
)

# -----------------------------
# KPIs
# -----------------------------
latest_year = int(analysis_df["year"].max())
latest_df = analysis_df[analysis_df["year"] == latest_year]

top_team = latest_df.sort_values("total_points", ascending=False).iloc[0]
top_fashion_team = latest_df.sort_values("avg_search_interest", ascending=False).iloc[0]

avg_search = analysis_df["avg_search_interest"].mean()
max_spike = analysis_df["max_search_interest"].max()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{latest_year}</div>
        <div class="metric-label">Latest season analyzed</div>
        <div class="metric-change">↑ recent F1 era</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{top_team["team_label"]}</div>
        <div class="metric-label">Top performing team</div>
        <div class="metric-change">↑ {top_team["total_points"]:.0f} points</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{top_fashion_team["team_label"]}</div>
        <div class="metric-label">Highest fashion demand</div>
        <div class="metric-change">↑ avg index {top_fashion_team["avg_search_interest"]:.1f}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{max_spike:.0f}</div>
        <div class="metric-label">Highest search spike</div>
        <div class="metric-change">Google Trends index</div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.title("Dashboard Filters")

selected_years = st.sidebar.multiselect(
    "Select year(s)",
    sorted(analysis_df["year"].unique()),
    default=sorted(analysis_df["year"].unique())
)

selected_teams = st.sidebar.multiselect(
    "Select team(s)",
    sorted(analysis_df["team_label"].unique()),
    default=sorted(analysis_df["team_label"].unique())
)

filtered_df = analysis_df[
    (analysis_df["year"].isin(selected_years)) &
    (analysis_df["team_label"].isin(selected_teams))
]

filtered_trends = trends_long[
    trends_long["team_label"].isin(selected_teams)
]

# -----------------------------
# Chart 1: Trends Over Time
# -----------------------------
st.markdown('<div class="chart-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Fashion Search Interest Over Time</div>', unsafe_allow_html=True)

fig_trends = px.line(
    filtered_trends,
    x="date",
    y="search_interest",
    color="search_term",
    title="",
    labels={
        "date": "Date",
        "search_interest": "Search Interest",
        "search_term": "Search Term"
    }
)

fig_trends.update_traces(line=dict(width=3))

fig_trends.update_layout(
    height=520,
    plot_bgcolor="#242423",
    paper_bgcolor="#242423",
    font=dict(color="#F2F2F2"),
    xaxis=dict(showgrid=True, gridcolor="#333333"),
    yaxis=dict(showgrid=True, gridcolor="#333333", range=[0, 100]),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="left",
        x=0
    ),
    margin=dict(l=40, r=40, t=50, b=40)
)

st.plotly_chart(fig_trends, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# Chart 2 and 3
# -----------------------------
left, right = st.columns(2)

with left:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Performance vs Fashion Demand</div>', unsafe_allow_html=True)

    fig_scatter = px.scatter(
        filtered_df,
        x="total_points",
        y="avg_search_interest",
        color="team_label",
        size="podiums",
        hover_data=["year", "wins", "avg_finish"],
        labels={
            "total_points": "Total Points",
            "avg_search_interest": "Avg. Search Interest",
            "team_label": "Team"
        }
    )

    fig_scatter.update_traces(
        marker=dict(
            line=dict(width=1, color="#FFFFFF"),
            opacity=0.85
        )
    )

    fig_scatter.update_layout(
        height=430,
        plot_bgcolor="#242423",
        paper_bgcolor="#242423",
        font=dict(color="#F2F2F2"),
        xaxis=dict(showgrid=True, gridcolor="#333333"),
        yaxis=dict(showgrid=True, gridcolor="#333333"),
        margin=dict(l=40, r=40, t=30, b=40)
    )

    st.plotly_chart(fig_scatter, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Team Fashion Demand Ranking</div>', unsafe_allow_html=True)

    ranking_df = filtered_df.groupby("team_label").agg(
        avg_search_interest=("avg_search_interest", "mean")
    ).reset_index().sort_values("avg_search_interest", ascending=True)

    fig_rank = px.bar(
        ranking_df,
        x="avg_search_interest",
        y="team_label",
        orientation="h",
        text="avg_search_interest",
        labels={
            "avg_search_interest": "Avg. Search Interest",
            "team_label": ""
        }
    )

    fig_rank.update_traces(
        marker_color="#2F93FF",
        texttemplate="%{text:.1f}",
        textposition="outside"
    )

    fig_rank.update_layout(
        height=430,
        plot_bgcolor="#242423",
        paper_bgcolor="#242423",
        font=dict(color="#F2F2F2"),
        xaxis=dict(showgrid=True, gridcolor="#333333"),
        yaxis=dict(showgrid=False),
        margin=dict(l=80, r=40, t=30, b=40)
    )

    st.plotly_chart(fig_rank, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# Chart 4: Performance Ranking
# -----------------------------
st.markdown('<div class="chart-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">F1 Team Performance Ranking</div>', unsafe_allow_html=True)

performance_rank = filtered_df.groupby("team_label").agg(
    total_points=("total_points", "sum"),
    podiums=("podiums", "sum"),
    wins=("wins", "sum")
).reset_index().sort_values("total_points", ascending=True)

fig_perf = px.bar(
    performance_rank,
    x="total_points",
    y="team_label",
    orientation="h",
    color="wins",
    text="total_points",
    labels={
        "total_points": "Total Points",
        "team_label": "",
        "wins": "Wins"
    },
    color_continuous_scale="Blues"
)

fig_perf.update_traces(
    texttemplate="%{text:.0f}",
    textposition="outside"
)

fig_perf.update_layout(
    height=520,
    plot_bgcolor="#242423",
    paper_bgcolor="#242423",
    font=dict(color="#F2F2F2"),
    xaxis=dict(showgrid=True, gridcolor="#333333"),
    yaxis=dict(showgrid=False),
    coloraxis_showscale=False,
    margin=dict(l=100, r=50, t=40, b=40)
)

st.plotly_chart(fig_perf, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# Insights
# -----------------------------
st.markdown('<div class="chart-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Key Insights</div>', unsafe_allow_html=True)

corr = analysis_df["total_points"].corr(analysis_df["avg_search_interest"])

st.write(f"""
- The dashboard compares **F1 performance metrics** with **fashion and merchandise search interest**.
- The correlation between total team points and average fashion search interest is **{corr:.2f}**.
- This suggests whether team success appears to move with fashion/merch demand.
- Search demand is treated as a proxy for consumer interest, not direct sales.
""")

st.markdown('</div>', unsafe_allow_html=True)
