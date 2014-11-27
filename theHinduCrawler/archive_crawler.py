import datetime as dt
import db
import logging
from lxml import html
from selenium import webdriver
from selenium.webdriver.common.by import By
import selenium.webdriver.support.ui as ui
from selenium.webdriver.support import expected_conditions as EC
import time


logging.basicConfig(filename='crawllog.log', level=logging.INFO)

# sections to look for
sections = [
    'News',
    'National',
    'International',
    'Economy',
    'Internet',
    'Editorial',
    'World',
    'Business',
]

def get_xpath():
    """returns relevant xpath
    expression according to
    predefined sections"""

    l= []
    for section in sections:
        xp = "//li[@data-section=\"{}\"]/a/@href".format(section)
        l.append(xp)
    return ' | '.join(l)

# date constants
oneday = dt.timedelta(days=1)
start_date = dt.date(2009, 8, 15)
end_date = dt.date.today()
fmt = "%Y/%m/%d"

# url and xpath
root_url = "http://www.thehindu.com/archive/web/"
xpath_expr = get_xpath()

# intialize webdriver and handle ajax load
br = webdriver.PhantomJS()
wait = ui.WebDriverWait(br, 10)
wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, '.archive_loading_bar')))

def archive_links(start, end, step):
    while start < end:
        yield root_url + start.strftime(fmt), start.strftime(fmt)
        start += step

def get_link_from_day_arhive(url):
    try:
        br.get(url)
        tree = html.fromstring(br.page_source)
        for link in tree.xpath(xpath_expr):
            yield link
    except Exception as e:
        logging.error("{0}: {1}".format(url, e))

def crawl_archive():
    for day_link in archive_links(start_date, end_date, oneday):
        starttimer = time.time()
        for link in get_link_from_day_arhive(day_link[0]):
            db.add_story({'date': day_link[1], 'url': link})
        timediff = time.time() - starttimer
        logging.info("{0}: {1}".format(day_link[1], timediff))

if __name__ == '__main__':
    crawl_archive()
