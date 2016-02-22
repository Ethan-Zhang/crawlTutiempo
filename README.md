# crawlTutiempo
A simple crawler for the history weather data in the en.tutiempo.net using scrapy framework.

# Requirements
* Python 2.7
* Works on Linux, Windows, Mac OSX, BSD

# Installation
```Python
pip install scrapy
git clone https://github.com/Ethan-Zhang/crawlTutiempo.git
```

# Quick Start
**Start crawling site with the args of city, start_year, end_year**
```
cd crawlTutiempo
scrapy crawl tutiempo -a city=Beijing -a start_year=2014 -a end_year=2015 -o item.json
```
**View the history weather data in item.json**

# More Infomation
[tutiempo China](http://en.tutiempo.net/climate/china)
[scrapy](https://github.com/scrapy/scrapy)
