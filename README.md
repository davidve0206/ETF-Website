# ETF Recommendations Website
Website that takes an user's investment objective and returns 4 potential ETFs. This website can be used as a landing page by Fintech's looking to acquire more retail customers, who would otherwise not be open to use investment products like stocks or bonds. View the site at http://davidve0206.pythonanywhere.com/.

There were two key problems: Allowing the person to easily express their risk level and recommending investment alternatives appropriatelly. To do this, the investment objectives are determined with only three questions, the responses of which are turned into a risk rating using a simple algorithm, while the ETFs are recommended using a clustering algorithm (k-means).

The website was built using the Django Framework, and uses the following packages:

* BeautifulSoup4 to web-scrape the 100 largest ETFs
* Yahoo-fin for retrieving historical ETF prices
* Pandas to handle the retrieved data
* Scikit-learn for k-means clustering
* Plotly to generate interactive graphs for the webpage
* Django-bootstrap to simplify some formating required for the user interface

Moreover, I created a package, Etfutils, to contain all the custom functions: the creation of the DataBase tables with stock information, the risk-rating assignation and the clustering model.

Finally, I used a Jupyter Notebook to perform the initial analysis required for the ETFs, which is kept in the Etfutils package solely for reference.
