#Import Splinter and BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt

def scrape_all():
    # Initiate headless driver for deployment
    browser = Browser("chrome", executable_path="chromedriver", headless=True)

    news_title, news_paragraph = mars_news(browser)

    #Run all scraping functions and store results in a dictionary 
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres" : hemisphere_data(browser)
    }

    #Stop webdriver and return data
    browser.quit()
    return data

def mars_news(browser):
    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    #Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    #Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')
 
#Add try/except for error handling
    try:
        slide_elem = news_soup.select_one("ul.item_list li.slide")
        #Use the parent element to find the first 'a' tag and save it as "news_title"
        news_title = slide_elem.find("div", class_="content_title").get_text()
        #Use the parent element to find the paragraph text
        news_p = slide_elem.find("div", class_="article_teaser_body").get_text()

    except AttributeError:
        return None,None

    return news_title, news_p

# ### Featured Images

def featured_image(browser):
    #Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    #Find and click the full image button
    #This is a new variable to hold the scraping result, the browser finds an element by its id
    full_image_elem = browser.find_by_id('full_image')[0]
    #Splinter will "click" the image to view its full size
    full_image_elem.click()

    #Find the more info button and click that
    #search for an element that has the provided text, additional arguement allows the browser to fully load before we search
    browser.is_element_present_by_text('more info', wait_time=1)
    #create a new variable, where we employ the method, method will take our string to find the link associated
    more_info_elem = browser.links.find_by_partial_text('more info')
    #tell Splinter to click that link by chaining the function onto our variable
    more_info_elem.click()

    #Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    #Add try/except for error handling
    try:
        #Find the relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")

    except AttributeError:
        return None

    #Use the base URL to create an absolute URL
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'

    return img_url

# Fact scraping
def mars_facts():

    #Add try/except for error handling:
    try:
        # use 'read_html" to scrape the facts table into a dataframe
        df = pd.read_html('http://space-facts.com/mars/')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars']
    df.set_index('Description', inplace=True)
    

    #Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")

def hemisphere_data(browser):
    # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles
    # Hemispheres
    # 1. Use browser to visit the URL 
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    #Find the relative image url
    browser.links.find_by_partial_text('Cerberus').click()
    html = browser.html
    cer_soup = soup(html, 'html.parser')
    cer_url = cer_soup.select_one('div.downloads a').get("href")
    cer_title = cer_soup.select_one('h2', class_="title").text

    #dictionary
    cer_dict = {
        "img_url": cer_url,
        "title": cer_title
        }

    hemisphere_image_urls.append(cer_dict)

    #Find the relative image url
    browser.links.find_by_partial_text('Schiaparelli').click()
    html = browser.html
    sch_soup = soup(html, 'html.parser')
    sch_url = sch_soup.select_one('div.downloads a').get("href")
    sch_title = sch_soup.select_one('h2', class_='title').text

    #dictionary
    sch_dict = {
        "img_url": sch_url,
        "title": sch_title
        }

    hemisphere_image_urls.append(sch_dict)

    #Syrtis
    browser.links.find_by_partial_text('Syrtis').click()
    html = browser.html
    syrtis_soup = soup(html, 'html.parser')
    syrtis_url = syrtis_soup.select_one('div.downloads a').get("href")
    syrtis_title = syrtis_soup.select_one('h2', class_="title").text

    #dictionary:
    syrtis_dict = {
        "img_url": syrtis_url,
        "title": syrtis_title
    }

    hemisphere_image_urls.append(syrtis_dict)

    #Find the relative image url
    browser.links.find_by_partial_text('Valles').click()
    html = browser.html
    val_soup = soup(html, 'html.parser')
    val_url = val_soup.select_one('div.downloads a').get("href")
    val_title = val_soup.select_one('h2', class_='title').text

    #dictionary
    val_dict = {
        "img_url": val_url,
        "title": val_title
        }

    hemisphere_image_urls.append(val_dict)

# 4. Print the list that holds the dictionary of each image url and title.
    return hemisphere_image_urls

if __name__ == "__main__":

    #If running as script, print scraped data
    print(scrape_all())






