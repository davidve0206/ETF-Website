import requests
from bs4 import BeautifulSoup

source_url = "https://etfdb.com/compare/market-cap/"

# The tickers are within a table row - td with data-th='Symbol'
def get_tickers(source_url = source_url):
    page = requests.get(source_url)
    soup = BeautifulSoup(page.content, "html.parser")
    tickers = set()
    for table_row in soup.find_all("td"):
        if table_row["data-th"] == "Symbol":
            tickers.add(table_row.text)
    return tickers

if __name__ == "__main__":
   print(get_tickers())