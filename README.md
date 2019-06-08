# instagram-post-scrape
Currently scrapes posts from public accounts

Scraping:
- Timestamp
- Like count
- Comment count

(if available)

- Video views
- Video duration

Inspired by [this post](https://medium.com/@srujana.rao2/scraping-instagram-with-python-using-selenium-and-beautiful-soup-8b72c186a058)

### Requirements

```elm
pip install bs4
pip install pandas
pip install selenium
```

Download and extract [chromedriver](http://chromedriver.chromium.org/) and change the location in 'scrape.py':

```python
browser = webdriver.Chrome('/PATH_TO_CHROMEDRIVER/chromedriver.exe')
```
```elm
python scrape.py
```
