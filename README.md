# Commentary Tweets of the *Elites*
Analyzing curated tweets of opinion-shapers and newsmakers provided by [nediyor.com](http://nediyor.com) and [theplazz.com](http://theplazz.com) news sites to understand the dynamics of the responses of the elites to the important events in the US and in Turkey.

## Data Collection
On the news that made to the headlines we collected about two years of curated tweets data for the United States (154,684 tweets of 1,442 commentators on 7,376 news between 01/09/2015 and 01/14/2013) and Turkey (190,180 tweets of 1306 commentators on 10,044 news between 01/09/2015 and 01/14/2013).

* Filenames starting with `scrape-` :
  * Selenium (as a Python API) is used to scrape the data from the main pages of the websites.
  * Scrolled down 1000 times to overcome the lazy loading feature of the sites.
  * To get individual comments, downloaded ~17,000 htmls from the links scraped from the main pages by `nohup sh -c "cat urls.txt | xargs -n 1 -P 10 wget " &`
  * The compressed files for [nediyor(190MB)](https://www.dropbox.com/s/3so72z136xfm9pn/nediyor_news.rar) and [theplazz(107MB)](https://www.dropbox.com/s/di6uatp7emdn5qb/theplazz_news.rar) are on dropbox.

## Data Analysis
### Daily Commentary Statistics
* `Aggregate-daily` & `container.js` :
  * Counts of comments on news are aggregated by day and visualized
  * Time series data is visualized using [Highcarts JS](http://www.highcharts.com/demo/line-time-series).

### Commentator Statistics
* `commentators-stats.py` calculates and visualizes the following statistics: 
   * Comment counts by commentator
   * Group commentators by profession
   * Monthly commentator performance
   * ...

## Initial Findings
* Daily comment count visualization is [here](http://talhaoz.com/news/)
