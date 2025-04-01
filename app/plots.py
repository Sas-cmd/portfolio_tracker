import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

def plot_allocation(perf_df: pd.DataFrame) -> None:
    """Plot portfolio allocation pie chart using the 'Current Value ($)' column."""
    alloc_df = perf_df.groupby("Ticker")["Current Value ($)"].sum()

    fig1, ax1 = plt.subplots(figsize=(4, 4), facecolor='none')
    wedges, texts, autotexts = ax1.pie(
        alloc_df,
        labels=alloc_df.index,
        autopct="%1.1f%%",
        startangle=90,
        wedgeprops=dict(width=0.4)
    )
    # Adjust text color if desired
    for text in texts + autotexts:
        text.set_color("white")
    ax1.axis("equal")
    fig1.patch.set_alpha(0)
    st.pyplot(fig1)

def plot_profit_loss(perf_df: pd.DataFrame) -> None:
    """Plot a bar chart of P/L ($) by ticker."""
    fig2, ax2 = plt.subplots(figsize=(5, 4), facecolor='none')
    colors = ['green' if val >= 0 else 'red' for val in perf_df["P/L ($)"]]
    bars = ax2.bar(perf_df["Ticker"], perf_df["P/L ($)"], color=colors)

    ax2.set_facecolor('none')
    fig2.patch.set_alpha(0)
    ax2.set_ylabel("P/L ($)", color="white")
    ax2.set_title("Profit/Loss per Stock", color="white")
    ax2.tick_params(colors="white", rotation=45)

    for spine in ["top", "right"]:
        ax2.spines[spine].set_visible(False)
    for spine in ["bottom", "left"]:
        ax2.spines[spine].set_color("white")

    # Add labels above/below bars
    for i, bar in enumerate(bars):
        value = perf_df["P/L ($)"].iloc[i]
        pct = perf_df["P/L (%)"].iloc[i]
        ax2.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + (0.01 if value >= 0 else -0.05),
            f"${value:.2f}\n({pct:.2f}%)",
            ha='center',
            va='bottom' if value >= 0 else 'top',
            color='white',
            fontsize=8
        )

    fig2.tight_layout()
    st.pyplot(fig2)
