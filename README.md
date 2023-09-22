# ETF Recommendations Website
Website that takes an user's investment objective and returns 4 potential ETFs. View the site at http://davidve0206.pythonanywhere.com/.

The investment objectives are turned into a risk rating using a simple algorithm, while the ETFs are recommended using a clustering algorithm (k-means).

The website was built using the Django Framework, and uses the following packages:

* BeautifulSoup4 to web-scrape the 100 largest ETFs
* Yahoo-fin for retrieving historical ETF prices
* Pandas to handle the retrieved data
* Scikit-learn for k-means clustering
* Plotly to generate interactive graphs for the webpage
* Django-bootstrap to simplify some formating required for the user interface
* Etfutils, a self-created package to contain all the functions required for the etf functionalities

Finally, I used a Jupyter Notebook to perform the initial analysis required for the ETFs, which is kept in the Etfutils package for reference.
