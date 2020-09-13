import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv("fcc-forum-pageviews.csv", parse_dates=["date"], index_col="date")

# Clean data
mask = (df.value > df.value.quantile(0.025)) & (df.value < df.value.quantile(0.975))
df = df.loc[mask]

# General settings for fonts in plots
title_font = {"fontsize": 18}
labels_font= {"fontsize": 16}


def draw_line_plot():
    # Draw line plot
    fig,axs = plt.subplots(figsize=(20, 10))

    df.plot(ax=axs, fontsize=12, c="r", legend=False)
    axs.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019", fontdict=title_font)
    axs.set_xlabel("Date", fontdict=labels_font)
    axs.set_ylabel("Page Views", fontdict=labels_font)

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig


def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.resample("M", kind="period").mean().reset_index().copy()
    df_bar["year"] = df_bar.date.apply(lambda it: it.strftime("%Y"))
    df_bar["month"] = df_bar.date.apply(lambda it: it.strftime("%B"))
    
    # Draw bar plot
    months_order = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

    fig, axs = plt.subplots(figsize=(10, 10))

    sns.barplot(data=df_bar, x="year", y="value", hue="month", hue_order=months_order, palette="bright", ax=axs)
    axs.set_xlabel("Years", fontdict=labels_font)
    axs.set_ylabel("Average Page Views", fontdict=labels_font)
    axs.legend(loc="upper left", title="Months")
    plt.xticks(rotation=90)

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig


def draw_box_plot():
    # Prepare data for box plots
    df_box = df.reset_index().copy()
    df_box["month"] = df_box.date.apply(lambda it: it.strftime("%b"))
    df_box["year"] = df_box.date.apply(lambda it: it.strftime("%Y"))

    # Draw box plots (using Seaborn)
    months_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))

    sns.boxplot(ax=ax1, data=df_box, x="year", y="value")
    ax1.set_title("Year-wise Box Plot (Trend)", fontdict=title_font)
    ax1.set_xlabel("Year", fontdict=labels_font)
    ax1.set_ylabel("Page Views", fontdict=labels_font)

    sns.boxplot(ax=ax2, data=df_box, x="month", y="value", order=months_order)
    ax2.set_title("Month-wise Box Plot (Seasonality)", fontdict=title_font)
    ax2.set_xlabel("Month", fontdict=labels_font)
    ax2.set_ylabel("Page Views", fontdict=labels_font)

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
