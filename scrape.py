#import dependencies

import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pymongo


def scrape():
    output = {}

    ##### NASA Mars News ######  

    # url = "https://mars.nasa.gov/news/"

    # response = requests.get(url)
    # soup_news = bs(response.text, "html.parser")

    # latest_title = soup_news.find("div", class_="content_title").a.text.strip()
    # latest_p = soup_news.find("div", class_="rollover_description_inner").text.strip()

    #alternative that doesn't currently work
    url = "https://mars.nasa.gov/news/"
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    browser.visit(url)
    html = browser.html
    soup_news = bs(html, 'html.parser')
    browser.quit()

    slide = soup_news.find("li", class_="slide")
  
    latest_title = slide.find("div", class_="content_title").a.text
    latest_p = slide.find("div", class_="article_teaser_body").text

    output['latest_title'] = latest_title
    output['latest_p'] = latest_p

    ##### JPL Mars Space Images - Featured Image ######

    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    browser.visit(url)

    results = browser.find_by_tag('button')
    link = results[1]
    link.click()

    html = browser.html
    soup = bs(html, 'html.parser')

    browser.quit()

    featured_img_url = soup.find("img", class_="headerimage fade-in")["src"]
    featured_img_url = url.replace("index.html",featured_img_url)

    output['featured_img_url'] = featured_img_url

    ##### Mars Facts ######

    url = "https://space-facts.com/mars/"
    tables = pd.read_html(url)
    output['data'] = tables[0].to_html(header = False)

    ##### USGS Astrogeology ######

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    hem_images = []

    for i in range(0,4):
        
        browser.visit(url)
        
        results = browser.find_by_tag('h3')
        link = results[i]
        link.click()
        
        html = browser.html
        soup = bs(html, 'html.parser')
        
        img_title = soup.find('h2', class_="title").text.strip()
        img_title = img_title.replace(' Enhanced','')
        img_url = soup.find("img", class_="wide-image")["src"]
        img_url = "https://astrogeology.usgs.gov"+img_url
        
        hem_images.append({
            "title" : img_title,
            "img_url":img_url
        })
        
    browser.quit()
        
    output['hem_images'] = hem_images

    return output








    

