import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def plot_allocation(perf_df: pd.DataFrame) -> None:
    """Plot portfolio allocation using Plotly pie chart."""
    alloc_df = perf_df.groupby("Ticker")["Current Value ($)"].sum().reset_index()

    fig = px.pie(
        alloc_df,
        names="Ticker",
        values="Current Value ($)",
        hole=0.5,  
        title="Portfolio Allocation",
    )
    fig.update_traces(textinfo="percent+label")
    fig.update_layout(
        showlegend=True,
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color="white"),
        title_font=dict(size=18),
    )
    st.plotly_chart(fig, use_container_width=True)


def plot_profit_loss(perf_df: pd.DataFrame) -> None:
    """Plot P/L ($) by ticker using Plotly bar chart."""
    colors = ["green" if val >= 0 else "red" for val in perf_df["P/L ($)"]]

    fig = go.Figure(
        data=[
            go.Bar(
                x=perf_df["Ticker"],
                y=perf_df["P/L ($)"],
                marker_color=colors,
                text=[
                    f"${val:,.2f}<br>({pct:.2f}%)"
                    for val, pct in zip(perf_df["P/L ($)"], perf_df["P/L (%)"])
                ],
                textposition="auto",
                hovertemplate="Ticker: %{x}<br>P/L: %{y}<extra></extra>",
            )
        ]
    )

    fig.update_layout(
        title="Profit / Loss per Ticker",
        yaxis_title="P/L ($)",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color="white"),
    )

    st.plotly_chart(fig, use_container_width=True)
