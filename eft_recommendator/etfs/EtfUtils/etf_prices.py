import numpy as np
import pandas as pd
import sqlite3
import yahoo_fin.stock_info as si
from . import tickers
from datetime import date
from django.conf import settings
from pathlib import Path
from sklearn.cluster import KMeans

db_path = Path.joinpath(settings.BASE_DIR, "db.sqlite3")

def calculate_return(series):
    """ Function that calculates the returns based on a price in two consecutive days"""
    return (series.iloc[1] - series.iloc[0]) / series.iloc[0]

def set_clusters(summary_df):
    """ Function that applies the K-means algorithm to assign clusters of risk to each ETF"""
    # Generate clusters using K-Means
    n_clusters = 4
    
    X = summary_df[['volatility', 'max_drop']].copy()
    kmeans = KMeans(n_clusters=n_clusters).fit(X)
    cluster_labels = kmeans.predict(X)

    # Order the clusters generated using a look-up-table
    ordered_clusters = np.argsort(kmeans.cluster_centers_.sum(axis=1))
    lut = np.zeros_like(ordered_clusters)
    lut[ordered_clusters] = np.arange(n_clusters)
    lut[cluster_labels]
    summary_df["risk_cluster"] = lut[cluster_labels]

    return summary_df

def get_etf_summary(price_df, Model):
    """ Function that takes a price dataframe and converts it into a summarized
        dataframe of returns; then calls the ML function to assing clusters to these results"""
    # Apply the calculate_return function to get a df of daily returns
    returns_df = price_df.rolling(2).apply(calculate_return)
    returns_df = returns_df.iloc[1:]
    returns_df

    # Calculate the summary statistics based on the daily returns df
    return_list = []

    for column in returns_df.columns.values:
        daily_return = returns_df.loc[:,column].mean()
        yearly_return = (( 1 + daily_return ) ** 365) - 1
        daily_volatility = returns_df.loc[:,column].std()
        yearly_volatility = np.sqrt(252) * daily_volatility
        max_daily_drop = returns_df.loc[:,column].min()
        column_list = [column, yearly_return, yearly_volatility, max_daily_drop]
        return_list.append(column_list)

    returns_summary_df = pd.DataFrame(return_list, columns =['ticker', 'avg_return', 'volatility', 'max_drop'])
    returns_summary_df["sharpe_ratio"] = returns_summary_df["avg_return"] / returns_summary_df["volatility"]
    
    # Call the K-means function to get the dataframe with clusters
    output_df = set_clusters(returns_summary_df)

    # Save the results to the database
    for row in output_df.itertuples(index=False):
        Model.objects.update_or_create(ticker=row[0], defaults={
            "ticker": row[0],
            "avg_return": row[1],
            "volatility": row[2],
            "max_drop": row[3],
            "sharpe_ratio": row[4],
            "risk_cluster": row[5]
        })

def get_etf_prices(Model):
    """ Function that takes a Django Model that contains ETF Prices and fills
        its rows with the prices of the 100 largest ETFs for the last 10 years"""
    
    # Get the tickers
    ticker_set = tickers.get_tickers()

    # Set the dates to retreive
    end_date = date.today()
    start_date = date(end_date.year - 10, 1 , 1)
    date_range = pd.bdate_range(start_date, end_date)
    
    # Create a DF with the dates, where the prices will be registred
    price_df = pd.DataFrame({"date": date_range})
    price_df.head()

    # Use yahoo finance's API to retreive the price data, then merge into the DF
    for ticker in ticker_set:
        stock_data = si.get_data(ticker, start_date=start_date, end_date=end_date)
        stock_data.rename(columns={"adjclose":ticker}, inplace=True)
        price_df = price_df.merge(stock_data.loc[:,ticker], how="left", left_on="date", right_index=True)
    
    # Set the date as index and clean null values
    price_df = price_df.set_index("date")
    price_df.dropna(axis=0, how="all", inplace=True)
    price_df.dropna(axis=1, how="any", inplace=True)

    # Melt DF to get a more Django-friendly structure
    melted_df = pd.melt(price_df.reset_index(), id_vars="date", var_name="ticker", value_name="price")
    melted_df["date"] = melted_df["date"].dt.strftime('%Y-%m-%d')
    
    # Save the results to the database
    with sqlite3.connect(db_path) as connection:
        melted_df.to_sql("etf_prices", connection, if_exists="replace", index_label="id")
    
    # Call the summary function to use this information and generate the summary table in the db
    get_etf_summary(price_df, Model)