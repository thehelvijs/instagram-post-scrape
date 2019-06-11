# instagram-post-scrape
Currently scrapes posts from public accounts

Inspired by [this post](https://medium.com/@srujana.rao2/scraping-instagram-with-python-using-selenium-and-beautiful-soup-8b72c186a058)

**Basic info:**

- Current followers, following and post amount

**Scraping from posts:**

- Timestamp
- Like count
- Comment count

**If available:**

- Video views
- Video duration

*To be added:*

*- Caption (with hashtag extraction)*
*- Location*
*- Tagged accounts*
*- Info related to account *

### Requirements

- [Python](https://www.python.org/downloads/)
- [Chromedriver](http://chromedriver.chromium.org/)
- Selenium
- Beautiful Soup

```elm
pip install bs4
pip install selenium
```

Download and extract [chromedriver](http://chromedriver.chromium.org/) and change the location in 'scrape.py':

```python
browser = webdriver.Chrome('/PATH_TO_CHROMEDRIVER/chromedriver.exe')
```
Run program
```elm
python scrape.py
```
