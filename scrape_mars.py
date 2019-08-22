# Import dependencies
from bs4 import BeautifulSoup as bs
from splinter import Browser
import requests
import time
import pandas as pd

# Setting up splinter
def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless = False)

def scrape_info():
    browser = init_browser()

    ## NASA Mars News ##
    # Setting up a URL for scraping
    NASA_url = 'https://mars.nasa.gov/news/'
    browser.visit(NASA_url)
    NASA_html = browser.html
    NASA_soup = bs(NASA_html, 'html.parser')

    # Storing he title and summary of the first article found
    title = NASA_soup.find('div', class_ = 'content_title')
    news_title = title.a.text.strip()

    pp = NASA_soup.find('div', class_ = 'article_teaser_body')
    news_p = pp.text.strip()


    ## JPL Mars Space Images - Featured Image ##
    # Setting up a URL for scraping
    JPL_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(JPL_url)

    # Preparation for splinter
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(3)
    browser.click_link_by_partial_text('more info')

    JPL_html = browser.html
    JPL_soup = bs(JPL_html, 'html.parser')

    # Storing the URL for the featured image
    figure = JPL_soup.find('figure', class_ = 'lede')
    href = figure.a['href']
    base = 'https://www.jpl.nasa.gov'
    featured_image_url = f'{base}{href}'


    ## Mars Weather ##
    # Using the request method
    tweet_url = 'https://mobile.twitter.com/marswxreport?lang=en'
    response = requests.get(tweet_url)
    tweet_soup = bs(response.text, 'lxml')

    # Storing the text information of the very first tweet
    tweet = tweet_soup.find('div', class_ = 'tweet-text')
    weather = tweet.div.text.strip()


    ## Mars Facts ##
    # Setting up a URL for scraping
    facts_url = 'https://space-facts.com/mars/'
    facts = pd.read_html(facts_url)

    # Using pandas for scraping and cleaning the table for description
    df = pd.DataFrame(facts[0])
    del df['Earth']
    df.columns = ['Description', 'Value']
    df = df.set_index('Description')


    ## Mars Hemispheres ##
    # Setting up a URL for scraping
    USGS_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(USGS_url)
    USGS_html = browser.html
    USGS_soup = bs(USGS_html, 'html.parser')

    # Storing titles of images for scraping
    titles = USGS_soup.find_all('h3')
    titles_list = []

    for title in titles:
        titles_list.append(title.text)

    # Looping through articles for image and URL scraping
    hemisphere_image_urls = []
    for title in titles_list:
        browser.click_link_by_partial_text(title)
        images = {}
        images['title'] = title
        images['img_url'] = browser.find_by_text('Original')['href']
        hemisphere_image_urls.append(images)
        browser.back()
        time.sleep(1)
    
    summary = {
        'news_title': news_title,
        'news_p': news_p,
        'featured_image_url': featured_image_url,
        'weather': weather,
        'facts': df,
        'hemisphere_image_urls': hemisphere_image_urls
    }

    return summary