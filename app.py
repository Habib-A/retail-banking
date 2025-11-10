import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
import io
from datetime import datetime
from typing import Optional
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="BankTrust Retail Banking Customer Segmentation",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Custom CSS with animations and blue theme
st.markdown("""
    <style>
    /* Main app background - light blue */
    .stApp {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 50%, #90caf9 100%);
    }
    
    /* Sidebar styling - dark blue */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d47a1 0%, #1565c0 50%, #1976d2 100%) !important;
        color: white !important;
    }
    
    [data-testid="stSidebar"] .stMarkdown,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] div {
        color: white !important;
    }
    
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] h4,
    [data-testid="stSidebar"] label {
        color: white !important;
    }
    
    /* Sidebar radio buttons */
    [data-testid="stSidebar"] [data-baseweb="radio"] {
        color: white !important;
    }
    
    [data-testid="stSidebar"] [data-baseweb="radio"] label {
        color: white !important;
    }
    
    [data-testid="stSidebar"] [data-baseweb="radio"] [data-baseweb="radio"] {
        background-color: rgba(255, 255, 255, 0.1) !important;
    }
    
    /* Sidebar divider */
    [data-testid="stSidebar"] hr {
        border-color: rgba(255, 255, 255, 0.3) !important;
    }
    
    /* Main content area - light blue background */
    .main .block-container {
        background-color: #e3f2fd;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .main-header {
        font-size: 2.8rem;
        font-weight: 700;
        background: linear-gradient(90deg, #0066cc 0%, #00a3e0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1.5rem 0;
        margin-bottom: 1rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #0066cc;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        animation: fadeInUp 0.6s ease-out;
    }
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    .kpi-card {
        background: linear-gradient(135deg, #0d47a1 0%, #1565c0 50%, #1976d2 100%);
        border-radius: 14px;
        padding: 0.85rem 1rem;
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: flex-start;
        gap: 0.75rem;
        width: 100%;
        height: 118px;
        box-shadow: 0 8px 22px rgba(13, 71, 161, 0.28);
        color: white;
        position: relative;
        overflow: hidden;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        animation: fadeInUp 0.6s ease-out;
    }
    .kpi-card::after {
        content: "";
        position: absolute;
        top: -40%;
        right: -20%;
        width: 60%;
        height: 180%;
        background: rgba(255, 255, 255, 0.12);
        transform: rotate(25deg);
    }
    .kpi-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 14px 26px rgba(13, 71, 161, 0.38);
    }
    .kpi-icon {
        font-size: 1.7rem;
        line-height: 1;
        z-index: 1;
        flex-shrink: 0;
    }
    .kpi-content {
        display: flex;
        flex-direction: column;
        justify-content: center;
        z-index: 1;
        width: 100%;
    }
    .kpi-label {
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        opacity: 0.8;
        margin-bottom: 0.2rem;
    }
    .kpi-value {
        font-size: 1.5rem;
        font-weight: 700;
        margin: 0;
    }
    .kpi-helper {
        font-size: 0.65rem;
        margin-top: 0.2rem;
        opacity: 0.75;
        display: block;
    }
    .kpi-wrapper {
        animation: fadeInUp 0.6s ease-out;
    }
    .kpi-wrapper:nth-child(1) { animation-delay: 0.1s; }
    .kpi-wrapper:nth-child(2) { animation-delay: 0.2s; }
    .kpi-wrapper:nth-child(3) { animation-delay: 0.3s; }
    .kpi-wrapper:nth-child(4) { animation-delay: 0.4s; }
    .kpi-wrapper:nth-child(5) { animation-delay: 0.5s; }
    .kpi-wrapper:nth-child(6) { animation-delay: 0.6s; }
    .kpi-wrapper:nth-child(7) { animation-delay: 0.7s; }
    .stButton>button {
        background: linear-gradient(90deg, #0066cc 0%, #00a3e0 100%);
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #0052a3 0%, #0088c7 100%);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    .cluster-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-top: 4px solid;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .cluster-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    }
    .insight-box {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #0066cc;
        margin: 0.5rem 0;
    }
    .section-header {
        font-size: 1.8rem;
        font-weight: 600;
        color: #2c3e50;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #00a3e0;
    }
    .marketing-strategy {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .marketing-strategy h4 {
        color: white;
        margin-top: 0;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def apply_light_blue_theme(fig):
    """Apply light blue background theme to Plotly charts to match main content area"""
    fig.update_layout(
        plot_bgcolor='#e3f2fd',
        paper_bgcolor='#e3f2fd',
        font=dict(color='#2c3e50')
    )
    return fig

def render_kpi_card(icon: str, label: str, value: str, helper: Optional[str] = None) -> None:
    """Render a styled KPI card with icon, label, value, and optional helper text."""
    helper_html = f'<span class="kpi-helper">{helper}</span>' if helper else ""
    card_html = f"""
    <div class="kpi-card">
        <div class="kpi-icon">{icon}</div>
        <div class="kpi-content">
            <span class="kpi-label">{label}</span>
            <span class="kpi-value">{value}</span>
            {helper_html}
        </div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)

# ============================================================================
# DATA LOADING FUNCTIONS
# ============================================================================

@st.cache_data
def load_data():
    """Load all necessary data files"""
    try:
        segments_df = pd.read_csv('Data/processed/kmeans_customer_segments.csv')
        profiles_df = pd.read_csv('Data/processed/cluster_profiles.csv')
        rfm_df = pd.read_csv('Data/processed/rfm_scores.csv')
        return segments_df, profiles_df, rfm_df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None, None

@st.cache_data
def load_raw_data():
    """Load raw transaction data from bank_data_C.csv"""
    try:
        raw_df = pd.read_csv('Data/bank_data_C.csv')
        raw_df = raw_df.copy()
        
        if 'TransactionDate' in raw_df.columns:
            raw_df['TransactionDate'] = pd.to_datetime(raw_df['TransactionDate'], format='%d/%m/%y', errors='coerce')
        
        if 'TransactionAmount (INR)' in raw_df.columns:
            raw_df = raw_df.rename(columns={'TransactionAmount (INR)': 'TransactionAmount'})
        
        if 'CustomerDOB' in raw_df.columns:
            raw_df['CustomerDOB'] = pd.to_datetime(raw_df['CustomerDOB'], format='%d/%m/%y', errors='coerce')
        
        return raw_df
    except Exception as e:
        st.warning(f"Could not load raw data: {e}")
        return None

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def calculate_revenue_stats(segments_df):
    """Calculate revenue statistics by segment"""
    revenue_stats = segments_df.groupby('Segment_Name').agg({
        'monetary': ['sum', 'mean', 'count']
    }).round(2)
    revenue_stats.columns = ['Total_Revenue', 'Avg_Spent', 'Customers']
    revenue_stats['Revenue_Percent'] = (revenue_stats['Total_Revenue'] / 
                                       revenue_stats['Total_Revenue'].sum() * 100).round(1)
    return revenue_stats.sort_values('Total_Revenue', ascending=False)

def generate_cluster_insights(segment_name, segments_df, revenue_stats):
    """Generate automated insights for a cluster"""
    segment_data = segments_df[segments_df['Segment_Name'] == segment_name]
    
    if len(segment_data) == 0:
        return ""
    
    avg_recency = segment_data['recency_days'].mean()
    avg_frequency = segment_data['frequency'].mean()
    avg_monetary = segment_data['monetary'].mean()
    customer_count = len(segment_data)
    revenue_pct = revenue_stats.loc[segment_name, 'Revenue_Percent']
    
    insights = []
    
    # Recency insights
    if avg_recency < 50:
        insights.append(f"✅ Excellent recency ({avg_recency:.1f} days) - customers are very active")
    elif avg_recency < 60:
        insights.append(f"⚠️ Moderate recency ({avg_recency:.1f} days) - monitor for engagement")
    else:
        insights.append(f"🔴 High recency ({avg_recency:.1f} days) - requires reactivation")
    
    # Frequency insights
    if avg_frequency > 1.3:
        insights.append(f"✅ High frequency ({avg_frequency:.2f}) - loyal, repeat customers")
    elif avg_frequency > 1.1:
        insights.append(f"⚡ Moderate frequency ({avg_frequency:.2f}) - potential for growth")
    else:
        insights.append(f"📉 Low frequency ({avg_frequency:.2f}) - encourage repeat purchases")
    
    # Monetary insights
    if avg_monetary > 2000:
        insights.append(f"💰 High value customers (avg £{avg_monetary:,.0f}) - premium segment")
    elif avg_monetary > 500:
        insights.append(f"💵 Mid-value customers (avg £{avg_monetary:,.0f}) - upsell potential")
    else:
        insights.append(f"💳 Low value customers (avg £{avg_monetary:,.0f}) - growth focus")
    
    # Revenue contribution
    insights.append(f"📊 Represents {customer_count:,} customers ({customer_count/len(segments_df)*100:.1f}%) generating {revenue_pct:.1f}% of total revenue")
    
    return "\n".join(insights)

def create_cluster_card(segment_name, segments_df, revenue_stats):
    """Create a styled cluster card"""
    segment_data = segments_df[segments_df['Segment_Name'] == segment_name]
    if len(segment_data) == 0:
        return None
    
    card_html = f"""
    <div class="cluster-card" style="border-top-color: {get_segment_color(segment_name)};">
        <h3 style="color: {get_segment_color(segment_name)}; margin-top: 0;">{segment_name}</h3>
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem;">
            <div>
                <strong>Customers:</strong><br>
                <span style="font-size: 1.5rem; color: #0066cc;">{len(segment_data):,}</span>
            </div>
            <div>
                <strong>Avg Recency:</strong><br>
                <span style="font-size: 1.5rem; color: #0066cc;">{segment_data['recency_days'].mean():.1f} days</span>
            </div>
            <div>
                <strong>Avg Frequency:</strong><br>
                <span style="font-size: 1.5rem; color: #0066cc;">{segment_data['frequency'].mean():.2f}</span>
            </div>
            <div>
                <strong>Avg Monetary:</strong><br>
                <span style="font-size: 1.5rem; color: #0066cc;">£{segment_data['monetary'].mean():,.0f}</span>
            </div>
            <div>
                <strong>Total Revenue:</strong><br>
                <span style="font-size: 1.5rem; color: #0066cc;">£{segment_data['monetary'].sum():,.0f}</span>
            </div>
            <div>
                <strong>Revenue %:</strong><br>
                <span style="font-size: 1.5rem; color: #0066cc;">{revenue_stats.loc[segment_data['Segment_Name'].iloc[0], 'Revenue_Percent']:.1f}%</span>
            </div>
        </div>
    </div>
    """
    return card_html

def get_segment_color(segment_name):
    """Get color for segment"""
    # Normalize segment name (handle leading spaces)
    normalized = segment_name.strip()
    colors = {
        "Big Spenders": "#FF6B6B",
        "Loyal Customers": "#4ECDC4",
        "Recent Low Value": "#FFE66D",
        "At-Risk": "#95A5A6"
    }
    return colors.get(normalized, "#3498DB")

# ============================================================================
# PAGE FUNCTIONS
# ============================================================================

def overview_page(segments_df, profiles_df):
    """Overview page with KPIs and high-level metrics"""
    st.markdown('<div class="section-header">📊 Key Performance Indicators</div>', unsafe_allow_html=True)
    
    # Key Metrics
    total_customers = len(segments_df)
    total_revenue = segments_df['monetary'].sum()
    avg_rtv = segments_df['monetary'].mean()
    num_segments = segments_df['Segment_Name'].nunique()
    avg_recency = segments_df['recency_days'].mean()
    avg_frequency = segments_df['frequency'].mean()
    
    # KPI Cards with animation
    kpi_row_one = [
        ("👥", "Total Customers", f"{total_customers:,}", "Active customers in the current dataset"),
        ("💰", "Total Revenue", f"£{total_revenue:,.0f}", "Cumulative revenue across all segments"),
        ("📈", "Avg Revenue / Customer", f"£{avg_rtv:,.0f}", "Average spend per customer"),
        ("🎯", "Customer Segments", f"{num_segments}", "Distinct behavioural segments")
    ]
    columns = st.columns(len(kpi_row_one))
    for col, (icon, label, value, helper) in zip(columns, kpi_row_one):
        with col:
            render_kpi_card(icon, label, value, helper)

    st.markdown("<div style='height:2.5rem;'></div>", unsafe_allow_html=True)

    kpi_row_two = [
        ("🕒", "Avg Recency", f"{avg_recency:.1f} days", "Mean days since last activity"),
        ("🔁", "Avg Frequency", f"{avg_frequency:.2f}", "Average transactions per customer")
    ]
    spacer_left, col1, col2, spacer_right = st.columns([0.7, 1, 1, 0.7])
    bottom_cols = [col1, col2]
    for col, (icon, label, value, helper) in zip(bottom_cols, kpi_row_two):
        with col:
            render_kpi_card(icon, label, value, helper)
    
    st.markdown("---")
    
    # Visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Segment Distribution")
        segment_counts = segments_df['Segment_Name'].value_counts()
        
        # Create color mapping for pie chart
        color_map = {
            ' Big Spenders': '#FF6B6B',
            'Loyal Customers': '#4ECDC4',
            'Recent Low Value': '#FFE66D',
            'At-Risk': '#95A5A6'
        }
        
        fig_pie = px.pie(
            values=segment_counts.values,
            names=segment_counts.index,
            title="Customer Distribution by Segment",
            color=segment_counts.index,
            color_discrete_map=color_map,
            hole=0.4
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        fig_pie = apply_light_blue_theme(fig_pie)
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        st.subheader("💰 Revenue Contribution")
        revenue_stats = calculate_revenue_stats(segments_df)
        
        fig_bar = px.bar(
            x=revenue_stats.index,
            y=revenue_stats['Revenue_Percent'],
            title="Revenue % by Segment",
            labels={'x': 'Segment', 'y': 'Revenue Percentage (%)'},
            color=revenue_stats['Revenue_Percent'],
            color_continuous_scale='Blues'
        )
        fig_bar.update_layout(showlegend=False, height=400)
        fig_bar = apply_light_blue_theme(fig_bar)
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # RFM Summary Table
    st.subheader("📋 RFM Metrics Summary")
    rfm_summary = (
        segments_df.groupby('Segment_Name')
        .agg(
            Customers=('CustomerID', 'nunique'),
            Avg_Recency=('recency_days', 'mean'),
            Avg_Frequency=('frequency', 'mean'),
            Avg_Monetary=('monetary', 'mean'),
            Total_Revenue=('monetary', 'sum')
        )
        .reset_index()
    )
    
    display_summary = rfm_summary.copy()
    display_summary['Avg_Recency'] = display_summary['Avg_Recency'].round(1)
    display_summary['Avg_Frequency'] = display_summary['Avg_Frequency'].round(2)
    display_summary['Avg_Monetary'] = display_summary['Avg_Monetary'].apply(lambda x: f"£{x:,.0f}")
    display_summary['Total_Revenue'] = display_summary['Total_Revenue'].apply(lambda x: f"£{x:,.0f}")
    display_summary.rename(
        columns={
            'Segment_Name': 'Segment',
            'Customers': 'Customers',
            'Avg_Recency': 'Avg Recency (Days)',
            'Avg_Frequency': 'Avg Frequency',
            'Avg_Monetary': 'Avg Monetary (£)',
            'Total_Revenue': 'Total Revenue (£)'
        },
        inplace=True
    )
    st.dataframe(display_summary, use_container_width=True, hide_index=True)


def segments_page(segments_df, rfm_df):
    """Segments page with interactive visualizations and K-Means summaries"""
    st.markdown('<div class="section-header">📊 Segments</div>', unsafe_allow_html=True)
    
    # Filters
    st.subheader("🔧 Filters")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        selected_segments = st.multiselect(
            "Select Segments",
            segments_df['Segment_Name'].unique(),
            default=segments_df['Segment_Name'].unique()
        )
    
    with col2:
        metric_filter = st.selectbox(
            "Filter by Metric",
            ["All", "Recency", "Frequency", "Monetary"]
        )
    
    with col3:
        cluster_filter = st.multiselect(
            "Select Clusters",
            sorted(segments_df['Cluster'].unique()),
            default=sorted(segments_df['Cluster'].unique())
        )
    
    filtered_df = segments_df[
        (segments_df['Segment_Name'].isin(selected_segments)) &
        (segments_df['Cluster'].isin(cluster_filter))
    ]
    
    st.markdown("---")
    
    # Bar chart comparison
    st.subheader("📊 Average RFM Metrics by Cluster")
    
    cluster_avg = filtered_df.groupby('Segment_Name').agg({
        'recency_days': 'mean',
        'frequency': 'mean',
        'monetary': 'mean'
    }).round(2)
    
    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        name='Recency (Days)',
        x=cluster_avg.index,
        y=cluster_avg['recency_days'],
        marker_color='#FF6B6B'
    ))
    fig_bar.add_trace(go.Bar(
        name='Frequency',
        x=cluster_avg.index,
        y=cluster_avg['frequency'],
        marker_color='#4ECDC4'
    ))
    fig_bar.add_trace(go.Bar(
        name='Monetary (£)',
        x=cluster_avg.index,
        y=cluster_avg['monetary'],
        marker_color='#FFE66D'
    ))
    
    fig_bar.update_layout(
        barmode='group',
        height=500,
        title="Average RFM Metrics Comparison",
        xaxis_title="Segment",
        yaxis_title="Value"
    )
    fig_bar = apply_light_blue_theme(fig_bar)
    st.plotly_chart(fig_bar, use_container_width=True)
    
    # 3D Scatter Plot
    st.subheader("🎯 3D RFM Space Visualization")
    
    sample_size = st.slider("Sample size for 3D plot", 1000, 10000, 5000, step=1000)
    
    fig_3d = px.scatter_3d(
        filtered_df.sample(min(sample_size, len(filtered_df)) if len(filtered_df) > 0 else 0),
        x='recency_days',
        y='frequency',
        z='monetary',
        color='Segment_Name',
        size='monetary',
        hover_data=['CustomerID'],
        title="Customer Segments in RFM Space",
        labels={
            'recency_days': 'Recency (Days)',
            'frequency': 'Frequency',
            'monetary': 'Monetary (£)'
        },
        color_discrete_map={
            ' Big Spenders': '#FF6B6B',
            'Loyal Customers': '#4ECDC4',
            'Recent Low Value': '#FFE66D',
            'At-Risk': '#95A5A6'
        }
    )
    fig_3d.update_layout(height=600)
    fig_3d = apply_light_blue_theme(fig_3d)
    st.plotly_chart(fig_3d, use_container_width=True)
    
    # Boxplots
    st.subheader("📦 Value Distributions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_box_recency = px.box(
            filtered_df,
            x='Segment_Name',
            y='recency_days',
            title="Recency Distribution by Segment",
            color='Segment_Name',
            color_discrete_map={
                'Big Spenders': '#FF6B6B',
                'Loyal Customers': '#4ECDC4',
                'Recent Low Value': '#FFE66D',
                'At-Risk': '#95A5A6'
            }
        )
        fig_box_recency.update_layout(showlegend=False, height=400)
        fig_box_recency = apply_light_blue_theme(fig_box_recency)
        st.plotly_chart(fig_box_recency, use_container_width=True)
    
    with col2:
        fig_box_frequency = px.box(
            filtered_df,
            x='Segment_Name',
            y='frequency',
            title="Frequency Distribution by Segment",
            color='Segment_Name',
            color_discrete_map={
                'Big Spenders': '#FF6B6B',
                'Loyal Customers': '#4ECDC4',
                'Recent Low Value': '#FFE66D',
                'At-Risk': '#95A5A6'
            }
        )
        fig_box_frequency.update_layout(showlegend=False, height=400)
        fig_box_frequency = apply_light_blue_theme(fig_box_frequency)
        st.plotly_chart(fig_box_frequency, use_container_width=True)
    
    # Monetary boxplot
    fig_box_monetary = px.box(
        filtered_df,
        x='Segment_Name',
        y=np.log1p(filtered_df['monetary']),
        title="Monetary Distribution by Segment (Log Scale)",
        color='Segment_Name',
        color_discrete_map={
            ' Big Spenders': '#FF6B6B',
            'Loyal Customers': '#4ECDC4',
            'Recent Low Value': '#FFE66D',
            'At-Risk': '#95A5A6'
        }
    )
    fig_box_monetary.update_layout(showlegend=False, height=400, yaxis_title="Log(Monetary Value)")
    fig_box_monetary = apply_light_blue_theme(fig_box_monetary)
    st.plotly_chart(fig_box_monetary, use_container_width=True)

def insights_recommendations_page(segments_df):
    """Insights and recommendations page"""
    st.markdown('<div class="section-header">💡 Insights & Recommendations</div>', unsafe_allow_html=True)
    
    revenue_stats = calculate_revenue_stats(segments_df)
    
    # Generate insights button
    if st.button("🔄 Regenerate Insights", help="Click to regenerate all insights"):
        st.cache_data.clear()
        st.rerun()
    
    # Segment information with marketing strategies
    segments_info = {
        " Big Spenders": {
            "description": "Customers with the highest monetary value but weaker recency and frequency",
            "recommendations": [
                "🚀 **Reactivation Campaigns**: Target with win-back offers to reduce recency",
                "🎁 **VIP Programs**: Consider exclusive perks or loyalty programs",
                "📧 **Personalized Communication**: Reach out with high-value product recommendations",
                "💰 **Upselling Opportunities**: They have high spending capacity - promote premium services"
            ],
            "marketing_strategies": [
                "**Email Campaigns**: Send personalized reactivation emails with exclusive offers",
                "**Direct Mail**: High-value physical mailers with premium product information",
                "**Phone Outreach**: Personal calls from relationship managers to re-engage",
                "**Loyalty Rewards**: Introduce tiered loyalty program with exclusive benefits",
                "**Premium Products**: Promote high-end banking products (premium accounts, investment services)",
                "**Time-Limited Offers**: Create urgency with limited-time reactivation bonuses",
                "**Referral Incentives**: Offer rewards for referring other high-value customers"
            ]
        },
        "Loyal Customers": {
            "description": "Best performing segment with excellent recency, high frequency, and substantial monetary value",
            "recommendations": [
                "⭐ **Retention Focus**: Maintain excellent service and reward loyalty",
                "🎯 **Referral Programs**: Leverage their satisfaction for new customer acquisition",
                "💎 **Premium Services**: Introduce them to higher-tier banking products",
                "🤝 **Relationship Building**: Assign dedicated relationship managers if applicable"
            ],
            "marketing_strategies": [
                "**VIP Treatment**: Exclusive access to premium services and early product launches",
                "**Referral Programs**: Reward them for bringing in new customers (e.g., £50 per referral)",
                "**Upsell Campaigns**: Promote investment products, insurance, and premium accounts",
                "**Community Building**: Invite to exclusive events, webinars, and financial workshops",
                "**Personalized Offers**: Tailored product recommendations based on their behavior",
                "**Loyalty Points**: Enhanced rewards program with points for every transaction",
                "**Cross-Sell Opportunities**: Introduce complementary products (credit cards, loans, savings)"
            ]
        },
        "Recent Low Value": {
            "description": "Recently active customers but with low transaction frequency and monetary value",
            "recommendations": [
                "📈 **Growth Campaigns**: Encourage repeat purchases and increase transaction frequency",
                "🎁 **Incentives**: Offer discounts or cashback for additional transactions",
                "📱 **Engagement**: Increase digital touchpoints and product awareness",
                "🎓 **Education**: Provide information about additional banking services"
            ],
            "marketing_strategies": [
                "**Welcome Series**: Automated email sequence introducing all banking services",
                "**Cashback Offers**: 2-5% cashback on first 3 transactions to encourage frequency",
                "**Product Education**: Webinars and guides on maximizing banking benefits",
                "**Mobile App Push**: Regular notifications about new features and offers",
                "**Transaction Incentives**: Bonus rewards for completing multiple transactions per month",
                "**Budgeting Tools**: Promote financial planning tools to increase engagement",
                "**Low-Value Upsells**: Start with small product additions (savings accounts, basic insurance)"
            ]
        },
        "At-Risk": {
            "description": "Customers showing poor performance across all RFM metrics - highest churn risk",
            "recommendations": [
                "⚠️ **Churn Prevention**: Immediate intervention with win-back offers",
                "📞 **Feedback Collection**: Understand reasons for decreased engagement",
                "💰 **Special Promotions**: Aggressive discounting or bonus offers",
                "🔄 **Product Review**: Assess if current products meet their needs",
                "📊 **Prioritization**: Focus resources on high-value At-Risk customers first"
            ],
            "marketing_strategies": [
                "**Win-Back Campaigns**: Aggressive email and SMS campaigns with special offers",
                "**Exit Surveys**: Understand why they're disengaging through feedback forms",
                "**Retention Offers**: Exclusive discounts or fee waivers for next 6 months",
                "**Product Simplification**: Offer simpler, more suitable product alternatives",
                "**Customer Success Calls**: Proactive outreach to address concerns and needs",
                "**Segmented Approach**: Prioritize high-value At-Risk customers for personal outreach",
                "**Last Chance Offers**: Final attempt with compelling value propositions before churn"
            ]
        }
    }
    
    # Display cluster cards and insights
    for segment_name, info in segments_info.items():
        # Cluster card
        card_html = create_cluster_card(segment_name, segments_df, revenue_stats)
        if card_html:
            st.markdown(card_html, unsafe_allow_html=True)
        
        # Description
        st.markdown(f"**Description:** {info['description']}")
        
        # Auto-generated insights
        insights = generate_cluster_insights(segment_name, segments_df, revenue_stats)
        st.markdown("**📊 Automated Insights:**")
        st.markdown(f'<div class="insight-box">{insights.replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
        
        # Recommendations
        st.markdown("**💡 Strategic Recommendations:**")
        for rec in info['recommendations']:
            st.markdown(f"- {rec}")
        
        # Marketing Strategies
        if 'marketing_strategies' in info:
            st.markdown("---")
            st.markdown("**📢 Marketing Strategy Recommendations:**")
            st.markdown('<div class="marketing-strategy">', unsafe_allow_html=True)
            for strategy in info['marketing_strategies']:
                st.markdown(f"- {strategy}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
    
    # Strategic summary table
    st.subheader("🎯 Overall Strategic Summary")
    strategy_table = pd.DataFrame({
        'Goal': ['Retention', 'Reactivation', 'Growth', 'Churn Management'],
        'Focus Segment': ['Loyal Customers', ' Big Spenders', 'Recent Low Value', 'At-Risk'],
        'Priority': ['High', 'Medium', 'Medium', 'High'],
        'Expected Impact': ['Maintain revenue base', 'Recapture high value', 'Increase transaction value', 'Prevent revenue loss']
    })
    st.dataframe(strategy_table, use_container_width=True, hide_index=True)

def download_center_page(segments_df, profiles_df, rfm_df):
    """Download center page"""
    st.markdown('<div class="section-header">📥 Download Center</div>', unsafe_allow_html=True)
    
    st.markdown("Download various reports and visualizations from your analysis.")
    
    st.subheader("📁 Raw Data")
    raw_df = load_raw_data()
    if raw_df is not None:
        csv_raw = raw_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Raw Data (CSV)",
            data=csv_raw,
            file_name='raw_banking_data.csv',
            mime='text/csv'
        )
    else:
        st.error("Raw data file not found. Please ensure 'Data/bank_data_C.csv' exists.")
    
    st.markdown("---")
    
    # Cluster Summary CSV
    st.subheader("📊 Cluster Summary")
    revenue_stats = calculate_revenue_stats(segments_df)
    cluster_summary = segments_df.groupby('Segment_Name').agg({
        'CustomerID': 'count',
        'recency_days': 'mean',
        'frequency': 'mean',
        'monetary': ['mean', 'sum']
    }).round(2)
    cluster_summary.columns = ['Customers', 'Avg_Recency', 'Avg_Frequency', 'Avg_Monetary', 'Total_Revenue']
    cluster_summary['Revenue_Percent'] = revenue_stats['Revenue_Percent']
    
    csv_summary = cluster_summary.to_csv()
    st.download_button(
        label="📥 Download Cluster Summary (CSV)",
        data=csv_summary,
        file_name=f'cluster_summary_{datetime.now().strftime("%Y%m%d")}.csv',
        mime='text/csv'
    )
    
    # Customer Segments CSV
    st.subheader("👥 Customer Segments")
    csv_segments = segments_df.to_csv(index=False)
    st.download_button(
        label="📥 Download Customer Segments (CSV)",
        data=csv_segments,
        file_name=f'customer_segments_{datetime.now().strftime("%Y%m%d")}.csv',
        mime='text/csv'
    )
    
    # RFM Scores CSV
    if rfm_df is not None:
        st.subheader("📈 RFM Scores")
        csv_rfm = rfm_df.to_csv(index=False)
        st.download_button(
            label="📥 Download RFM Scores (CSV)",
            data=csv_rfm,
            file_name=f'rfm_scores_{datetime.now().strftime("%Y%m%d")}.csv',
            mime='text/csv'
        )
    
    # Export summary report
    st.subheader("📄 Export Summary Report")
    st.info("💡 Summary report includes key metrics, insights, and recommendations for each segment.")
    
    report_text = f"""
BankTrust Retail Banking Customer Segmentation Report
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

EXECUTIVE SUMMARY
=================
Total Customers: {len(segments_df):,}
Total Revenue: £{segments_df['monetary'].sum():,.0f}
Average Revenue per Customer: £{segments_df['monetary'].mean():,.0f}
Number of Segments: {segments_df['Segment_Name'].nunique()}

SEGMENT ANALYSIS
================
"""
    
    for segment in segments_df['Segment_Name'].unique():
        seg_data = segments_df[segments_df['Segment_Name'] == segment]
        revenue_stats = calculate_revenue_stats(segments_df)
        
        report_text += f"""
{segment}
---------
Customers: {len(seg_data):,}
Average Recency: {seg_data['recency_days'].mean():.1f} days
Average Frequency: {seg_data['frequency'].mean():.2f}
Average Monetary: £{seg_data['monetary'].mean():,.0f}
Total Revenue: £{seg_data['monetary'].sum():,.0f}
Revenue %: {revenue_stats.loc[segment, 'Revenue_Percent']:.1f}%

"""
    
    st.download_button(
        label="📥 Download Summary Report (TXT)",
        data=report_text,
        file_name=f'segmentation_report_{datetime.now().strftime("%Y%m%d")}.txt',
        mime='text/plain'
    )
    
    # Share dashboard note
    st.markdown("---")
    st.info("💡 **Note**: You can share this dashboard by running `streamlit run app.py` on any machine with the required data files.")

def raw_data_page():
    """Raw data analysis page"""
    st.markdown('<div class="section-header">📋 Raw Data Analysis</div>', unsafe_allow_html=True)
    st.markdown("**Source:** `Data/bank_data_C.csv` - Comprehensive exploratory data analysis on the raw banking transaction dataset")
    
    raw_df = load_raw_data()
    
    if raw_df is not None:
        # Dataset Overview
        st.subheader("📊 Dataset Overview")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Records", f"{len(raw_df):,}")
        with col2:
            customer_count = raw_df['CustomerID'].nunique() if 'CustomerID' in raw_df.columns else 0
            st.metric("Total Customers", f"{customer_count:,}")
        with col3:
            total_amount = raw_df['TransactionAmount'].sum() if 'TransactionAmount' in raw_df.columns else 0
            st.metric("Total Transaction Amount", f"£{total_amount:,.0f}")
        with col4:
            avg_amount = raw_df['TransactionAmount'].mean() if 'TransactionAmount' in raw_df.columns else 0
            st.metric("Avg Transaction Amount", f"£{avg_amount:,.2f}")
        
        st.markdown("---")
        
        # Data Structure
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("📋 Data Structure")
            st.write(f"**Shape:** {raw_df.shape[0]:,} rows × {raw_df.shape[1]} columns")
            st.write("**Columns:**")
            for col in raw_df.columns:
                dtype = raw_df[col].dtype
                st.write(f"- {col} ({dtype})")
        
        with col2:
            st.subheader("🔍 Missing Values")
            missing_data = raw_df.isnull().sum()
            missing_df = pd.DataFrame({
                'Column': missing_data.index,
                'Missing Count': missing_data.values,
                'Missing %': (missing_data.values / len(raw_df) * 100).round(2)
            })
            missing_df = missing_df[missing_df['Missing Count'] > 0]
            if len(missing_df) > 0:
                st.dataframe(missing_df, use_container_width=True, hide_index=True)
            else:
                st.success("✅ No missing values found!")
        
        st.markdown("---")
        
        # Summary Statistics
        st.subheader("📈 Summary Statistics")
        numeric_cols = raw_df.select_dtypes(include=[np.number]).columns.tolist()
        if len(numeric_cols) > 0:
            st.dataframe(raw_df[numeric_cols].describe(), use_container_width=True)
        
        st.markdown("---")
        
        # Sample Data
        st.subheader("👀 Sample Data")
        num_rows = st.slider("Number of rows to display", 5, 100, 10, key="raw_sample")
        st.dataframe(raw_df.head(num_rows), use_container_width=True)
        
        st.markdown("---")
        
        # Transaction Analysis
        if 'TransactionAmount' in raw_df.columns:
            st.subheader("💰 Transaction Amount Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig_hist = px.histogram(
                    raw_df.sample(min(50000, len(raw_df))),
                    x='TransactionAmount',
                    nbins=50,
                    title="Transaction Amount Distribution",
                    labels={'TransactionAmount': 'Amount (£)', 'count': 'Frequency'}
                )
                fig_hist.update_layout(height=400)
                fig_hist = apply_light_blue_theme(fig_hist)
                st.plotly_chart(fig_hist, use_container_width=True)
            
            with col2:
                fig_box = px.box(
                    raw_df.sample(min(50000, len(raw_df))),
                    y='TransactionAmount',
                    title="Transaction Amount Box Plot",
                    labels={'TransactionAmount': 'Amount (£)'}
                )
                fig_box.update_layout(height=400)
                fig_box = apply_light_blue_theme(fig_box)
                st.plotly_chart(fig_box, use_container_width=True)
            
            # Transaction statistics by customer
            st.markdown("#### Transaction Statistics by Customer")
            customer_stats = raw_df.groupby('CustomerID').agg({
                'TransactionAmount': ['sum', 'mean', 'count'],
            }).round(2)
            customer_stats.columns = ['Total Amount', 'Avg Amount', 'Transaction Count']
            customer_stats = customer_stats.sort_values('Total Amount', ascending=False)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Top Customer Total", f"£{customer_stats['Total Amount'].max():,.0f}")
            with col2:
                st.metric("Avg Transactions per Customer", f"{customer_stats['Transaction Count'].mean():.1f}")
            with col3:
                st.metric("Median Transaction Amount", f"£{raw_df['TransactionAmount'].median():,.2f}")
        
        st.markdown("---")
        
        # Customer Demographics
        if 'CustGender' in raw_df.columns:
            st.subheader("👥 Customer Demographics")
            
            col1, col2 = st.columns(2)
            
            with col1:
                gender_counts = raw_df['CustGender'].value_counts()
                fig_gender = px.pie(
                    values=gender_counts.values,
                    names=gender_counts.index,
                    title="Gender Distribution",
                    color_discrete_sequence=px.colors.qualitative.Set2
                )
                fig_gender = apply_light_blue_theme(fig_gender)
                st.plotly_chart(fig_gender, use_container_width=True)
            
            with col2:
                if 'CustLocation' in raw_df.columns:
                    location_counts = raw_df['CustLocation'].value_counts().head(15)
                    fig_location = px.bar(
                        x=location_counts.index,
                        y=location_counts.values,
                        title="Top 15 Locations by Transaction Count",
                        labels={'x': 'Location', 'y': 'Transaction Count'},
                        color=location_counts.values,
                        color_continuous_scale='Blues'
                    )
                    fig_location.update_layout(showlegend=False, height=400, xaxis_tickangle=-45)
                    fig_location = apply_light_blue_theme(fig_location)
                    st.plotly_chart(fig_location, use_container_width=True)
        
        st.markdown("---")
        
        # Time-based Analysis
        if 'TransactionDate' in raw_df.columns:
            st.subheader("📅 Time-based Analysis")
            
            try:
                time_df = raw_df.copy()
                time_df['TransactionDate'] = pd.to_datetime(time_df['TransactionDate'], errors='coerce')
                time_df = time_df.dropna(subset=['TransactionDate'])
                time_df['YearMonth'] = time_df['TransactionDate'].dt.to_period('M').astype(str)
                time_df['Year'] = time_df['TransactionDate'].dt.year
                time_df['DayOfWeek'] = time_df['TransactionDate'].dt.day_name()
                
                col1, col2 = st.columns(2)
                
                with col1:
                    monthly_transactions = time_df.groupby('YearMonth').size().sort_index()
                    fig_time = px.line(
                        x=monthly_transactions.index,
                        y=monthly_transactions.values,
                        title="Transaction Volume Over Time",
                        labels={'x': 'Month', 'y': 'Number of Transactions'},
                        markers=True
                    )
                    fig_time.update_layout(height=400)
                    fig_time = apply_light_blue_theme(fig_time)
                    st.plotly_chart(fig_time, use_container_width=True)
                
                with col2:
                    if 'TransactionAmount' in time_df.columns:
                        monthly_revenue = time_df.groupby('YearMonth')['TransactionAmount'].sum().sort_index()
                        fig_revenue = px.line(
                            x=monthly_revenue.index,
                            y=monthly_revenue.values,
                            title="Revenue Over Time",
                            labels={'x': 'Month', 'y': 'Revenue (£)'},
                            markers=True
                        )
                        fig_revenue.update_layout(height=400)
                        fig_revenue = apply_light_blue_theme(fig_revenue)
                        st.plotly_chart(fig_revenue, use_container_width=True)
            except Exception as e:
                st.warning(f"Could not perform time-based analysis: {e}")
    else:
        st.error("Raw data file not found. Please ensure 'Data/bank_data_C.csv' exists.")

def customer_explorer_page(segments_df):
    """Customer explorer page with search functionality"""
    st.markdown('<div class="section-header">🔍 Customer Explorer</div>', unsafe_allow_html=True)
    
    # CustomerID Search Bar
    st.subheader("🔎 Search by Customer ID")
    search_customer_id = st.text_input(
        "Enter Customer ID to search",
        placeholder="e.g., C1010011",
        help="Type a Customer ID to find specific customer information"
    )
    
    # If CustomerID is provided, show that customer's details
    if search_customer_id:
        search_customer_id = search_customer_id.strip().upper()
        customer_data = segments_df[segments_df['CustomerID'].str.upper() == search_customer_id]
        
        if len(customer_data) > 0:
            st.success(f"✅ Found customer: {search_customer_id}")
            
            # Display customer details
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Customer ID", customer_data.iloc[0]['CustomerID'])
            with col2:
                st.metric("Segment", customer_data.iloc[0]['Segment_Name'])
            with col3:
                st.metric("Recency (Days)", f"{customer_data.iloc[0]['recency_days']:.0f}")
            with col4:
                st.metric("Frequency", f"{customer_data.iloc[0]['frequency']:.1f}")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Monetary Value", f"£{customer_data.iloc[0]['monetary']:,.2f}")
            with col2:
                st.metric("Cluster", customer_data.iloc[0]['Cluster'])
            with col3:
                monetary_percentile = (segments_df['monetary'] <= customer_data.iloc[0]['monetary']).sum() / len(segments_df) * 100
                st.metric("Monetary Percentile", f"{monetary_percentile:.1f}%")
            
            # Detailed customer information
            st.markdown("#### 📋 Customer Details")
            customer_display = customer_data[['CustomerID', 'Segment_Name', 'Cluster', 
                                              'recency_days', 'frequency', 'monetary']].copy()
            customer_display.columns = ['Customer ID', 'Segment', 'Cluster', 
                                       'Recency (Days)', 'Frequency', 'Monetary Value (£)']
            customer_display['Monetary Value (£)'] = customer_display['Monetary Value (£)'].apply(
                lambda x: f"£{x:,.2f}"
            )
            st.dataframe(customer_display, use_container_width=True, hide_index=True)
            
            # Comparison with segment averages
            st.markdown("#### 📊 Comparison with Segment Averages")
            segment_name = customer_data.iloc[0]['Segment_Name']
            segment_avg = segments_df[segments_df['Segment_Name'] == segment_name].agg({
                'recency_days': 'mean',
                'frequency': 'mean',
                'monetary': 'mean'
            })
            
            comparison_data = {
                'Metric': ['Recency (Days)', 'Frequency', 'Monetary Value (£)'],
                'Customer Value': [
                    f"{customer_data.iloc[0]['recency_days']:.1f}",
                    f"{customer_data.iloc[0]['frequency']:.2f}",
                    f"£{customer_data.iloc[0]['monetary']:,.2f}"
                ],
                'Segment Average': [
                    f"{segment_avg['recency_days']:.1f}",
                    f"{segment_avg['frequency']:.2f}",
                    f"£{segment_avg['monetary']:,.2f}"
                ],
                'Difference': [
                    f"{customer_data.iloc[0]['recency_days'] - segment_avg['recency_days']:.1f}",
                    f"{customer_data.iloc[0]['frequency'] - segment_avg['frequency']:.2f}",
                    f"£{customer_data.iloc[0]['monetary'] - segment_avg['monetary']:,.2f}"
                ]
            }
            comparison_df = pd.DataFrame(comparison_data)
            st.dataframe(comparison_df, use_container_width=True, hide_index=True)
            
            st.markdown("---")
            st.markdown("### 🔍 Continue with Filters Below")
        else:
            st.warning(f"⚠️ Customer ID '{search_customer_id}' not found.")
            st.info("💡 Tip: Customer IDs typically start with 'C' followed by numbers (e.g., C1010011)")
    
    st.markdown("---")
    st.subheader("🔧 Filter Customers")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        selected_segments = st.multiselect(
            "Select Segments",
            segments_df['Segment_Name'].unique(),
            default=segments_df['Segment_Name'].unique()
        )
    with col2:
        min_recency = st.slider(
            "Min Recency (Days)",
            0, int(segments_df['recency_days'].max()),
            0
        )
    with col3:
        max_recency = st.slider(
            "Max Recency (Days)",
            0, int(segments_df['recency_days'].max()),
            int(segments_df['recency_days'].max())
        )
    
    col1, col2 = st.columns(2)
    with col1:
        min_monetary = st.number_input(
            "Min Monetary (£)",
            0.0,
            float(segments_df['monetary'].max()),
            0.0
        )
    with col2:
        max_monetary = st.number_input(
            "Max Monetary (£)",
            0.0,
            float(segments_df['monetary'].max()),
            float(segments_df['monetary'].max())
        )
    
    # Apply filters
    if not search_customer_id or len(segments_df[segments_df['CustomerID'].str.upper() == search_customer_id]) == 0:
        filtered_df = segments_df[
            (segments_df['Segment_Name'].isin(selected_segments)) &
            (segments_df['recency_days'] >= min_recency) &
            (segments_df['recency_days'] <= max_recency) &
            (segments_df['monetary'] >= min_monetary) &
            (segments_df['monetary'] <= max_monetary)
        ]
        
        if len(filtered_df) > 0:
            total_revenue = filtered_df['monetary'].sum()
            avg_recency_filtered = filtered_df['recency_days'].mean()
            avg_frequency_filtered = filtered_df['frequency'].mean()
            
            col_a, col_b, col_c, col_d = st.columns(4)
            with col_a:
                st.metric("Filtered Customers", f"{len(filtered_df):,}")
            with col_b:
                st.metric("Total Revenue", f"£{total_revenue:,.0f}")
            with col_c:
                st.metric("Avg Recency", f"{avg_recency_filtered:.1f} days")
            with col_d:
                st.metric("Avg Frequency", f"{avg_frequency_filtered:.2f}")
            
            st.subheader("📋 Customer Data")
            display_df = filtered_df[['CustomerID', 'Segment_Name', 'recency_days', 
                                     'frequency', 'monetary', 'Cluster']].copy()
            display_df.columns = ['Customer ID', 'Segment', 'Recency (Days)', 
                                 'Frequency', 'Monetary Value (£)', 'Cluster']
            display_df['Monetary Value (£)'] = display_df['Monetary Value (£)'].apply(
                lambda x: f"£{x:,.2f}"
            )
            display_df['Recency (Days)'] = display_df['Recency (Days)'].apply(
                lambda x: f"{x:.0f}"
            )
            display_df['Frequency'] = display_df['Frequency'].apply(
                lambda x: f"{x:.2f}"
            )
            
            st.dataframe(display_df, use_container_width=True)
            
            # Download option
            csv = filtered_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Filtered Data",
                data=csv,
                file_name='filtered_customers.csv',
                mime='text/csv'
            )
        else:
            st.info("No customers match the selected filters.")
    else:
        st.info("💡 Clear the Customer ID search above to use the filters.")

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    # Load data
    segments_df, profiles_df, rfm_df = load_data()
    
    if segments_df is None:
        st.error("Please ensure data files are in the correct location.")
        return
    
    # Sidebar Navigation
    st.sidebar.title("🏦 BankTrust")
    
    page = st.sidebar.radio(
        "Choose a page",
        [
            "📊 Overview", 
            "📊 Segments",
            "🔍 Customer Explorer",
            "💡 Insights & Recommendations",
            "📋 Raw Data",
            "📥 Download Center"
        ]
    )
    
    # Main header
    st.markdown('<h1 class="main-header">BankTrust Retail Banking Customer Segmentation Dashboard</h1>', 
                unsafe_allow_html=True)
    
    # Page routing
    if page == "📊 Overview":
        overview_page(segments_df, profiles_df)
    elif page == "📊 Segments":
        segments_page(segments_df, rfm_df)
    elif page == "🔍 Customer Explorer":
        customer_explorer_page(segments_df)
    elif page == "💡 Insights & Recommendations":
        insights_recommendations_page(segments_df)
    elif page == "📋 Raw Data":
        raw_data_page()
    elif page == "📥 Download Center":
        download_center_page(segments_df, profiles_df, rfm_df)

if __name__ == "__main__":
    main()
