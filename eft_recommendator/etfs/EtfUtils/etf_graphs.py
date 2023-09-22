import numpy as np
import pandas as pd
import sqlite3
import plotly.express as px
from plotly.offline import plot
from plotly.io import to_html
from django.conf import settings
from pathlib import Path

db_path = Path.joinpath(settings.BASE_DIR, "db.sqlite3")
db_summary_table = "etfs_etf"
db_price_table = "etf_prices"
base_color="#0671B7"
bg_color="#E6F1F8"
dark_gray="#4d4d4d"

def get_etf_summary_graph():
    """ Return a graph of all the Etfs supported on the site, in div format to be included in a template """
    
    with sqlite3.connect(db_path) as con:
        summary_df = pd.read_sql(f"SELECT * FROM {db_summary_table}", con)
    summary_df["avg_return"] = summary_df["avg_return"] * 100
    summary_df["volatility"] = summary_df["volatility"] * 100
    fig = px.scatter(summary_df, y="avg_return", x="volatility",
                     labels={
                        "avg_return": "Average Return (Last 10 years)",
                        "volatility": "Return Volatility (Last 10 years)"
                     },
                      hover_data={
                        "ticker": True,
                        "avg_return": ':.2f',
                        "volatility": ':.2f'})
    fig.update_traces(hovertemplate='Ticker: %{customdata[0]} <br>Average Return: %{y:.2f}% <br>Volatility: %{x:.2f}%')
    fig.update_yaxes(ticksuffix="%")
    fig.update_xaxes(ticksuffix="%")
    fig.update_layout(
        margin_r=10,
        plot_bgcolor=bg_color,
        font_color=dark_gray,
        hoverlabel_bgcolor=base_color,
        xaxis={'linecolor':dark_gray, 'ticks':'outside'},
        yaxis={'linecolor':dark_gray, 'ticks':'outside'})
    return to_html(fig, include_plotlyjs="cdn", full_html=False, div_id="price_graph")

def get_etf_history_graph(ticker):
    """ Return a graph of the historical price of a particular Etf, in div format to be included in a template """

    with sqlite3.connect(db_path) as con:
        price_df = pd.read_sql(f"SELECT date, price FROM {db_price_table} WHERE ticker='{ticker}'", con)
    fig = px.line(price_df, x="date", y="price", render_mode='webg1',
                  labels={
                        "date": "Date",
                        "price": "Price (Adjusted for Dividends)"
                     })
    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
            dict(count=1, label="1M", step="month", stepmode="backward"),
            dict(count=6, label="6M", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1Y", step="year", stepmode="backward"),
            dict(count=5, label="5Y", step="year", stepmode="backward"),
            dict(label="10Y", step="all")
            ])
            )
        )
    fig.update_layout(
        margin_r=10,
        plot_bgcolor=bg_color,
        font_color=dark_gray,
        hoverlabel_bgcolor=base_color,
        xaxis={'linecolor':dark_gray, 'ticks':'outside', 'showgrid':False},
        yaxis={'linecolor':dark_gray, 'ticks':'outside'})
    fig.update_traces(hovertemplate='Date: %{x:|%x} <br>Price: %{y:.2f}', line_color=base_color)
    return to_html(fig, include_plotlyjs="cdn", full_html=False, div_id="price_graph")