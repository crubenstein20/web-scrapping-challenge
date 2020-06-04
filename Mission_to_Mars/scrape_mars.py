#!/usr/bin/env python
# coding: utf-8

from bs4 import BeautifulSoup
from splinter import Browser
import time
import requests
import os
from selenium import webdriver
import pandas as pd

def scrape():
    final_data = {}
    output = marsNews()
    final_data["news_title"] = combo[0]
    final_data["news_p"] = combo[1]
    final_data["feature_image_url"] = marsImage()
    final_data["mars_weather"] = marsWeather()
    final_data["mars_facts"] = marsFacts()
    final_data["hemisphere_image_urls"] = marsHemispheres()

    return final_data


#Mars News
def marsNews():
    news_url = "https://mars.nasa.gov/news/"
    browser = webdriver.Chrome()
    browser.get(news_url)
    time.sleep(10)
    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')
    #print(soup.prettify())
    article = soup.find("div", class_="list_text")
    news_title = article.find("div", class_="content_title").text
    news_p = article.find("div", class_="article_teaser_body").text
    combo = [news_title, news_p]
    print(news_title)
    print(news_p)
    return output

#Mars Space Images 
def marsImage():
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser = webdriver.Chrome()
    browser.get(image_url)
    time.sleep(10)
    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')
    #print(soup.prettify())
    image = soup.find("img", class_="thumb")["src"]
    featured_image_url = "https://www.jpl.nasa.gov" + image
    print(featured_image_url)
    return feature_image_url

#Mars Weather
def marsWeather():
    url = "https://twitter.com/marswxreport?lang=en"
    browser = webdriver.Chrome()
    browser.get(url)
    time.sleep(10)
    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')
    #print(soup.prettify())
    mars_weather = soup.find_all("span", class_="css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0")
    print(mars_weather[27].text)
    return marsWeather

#Mars Facts
def marsFacts():
    funfacts_url = "https://space-facts.com/mars/"
    browser = webdriver.Chrome()
    browser.get(funfacts_url)
    time.sleep(10)
    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')
    #print(soup.prettify())
    mars_info = pd.read_html(funfacts_url)
    mars_info = pd.DataFrame(mars_info[0])
    mars_funfacts = mars_info.to_html(header = False, index = False)
    print(mars_funfacts)
    return mars_funfacts

#Mars Hemisphere
def marsHemispheres():
    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser = webdriver.Chrome()
    browser.get(hemispheres_url)
    time.sleep(10)
    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')

    items = soup.find_all('div', class_="item")

    mars_data = {}
    images = []

    main_url = "https://astrogeology.usgs.gov"

    for item in items:
        title = item.find("h3").text
        partial_img = item.find('a', class_='itemLink product-item')['href']
    
        browser.get(main_url + partial_img)
        partial_img = browser.page_source
        soup = BeautifulSoup(partial_img, 'html.parser')
    
        img_url = main_url + soup.find('img', class_="wide-image")['src']
    
        images.append({'Title': title, 'img_url': img_url})
    
    mars_data ['images'] = images

    browser.quit()
    return images




