# dependencies/lib files
from splinter import Browser
from bs4 import BeautifulSoup
import requests, time
import pandas as pd

def init_browser():
# set up browser for scrapping
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()

    # define website and start scraping
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    # Retrieve page with the requests module
    html = browser.html

    # Create BeautifulSoup object; parse with 'html'
    soup = BeautifulSoup(html)

    # # Scraping the Mars News

    # scrape news headline
    titles = soup.find_all(class_='content_title')

    news_title = titles[1].text
    #print(news_title)

    # scrape news teaser text
    teasers = soup.find(class_="article_teaser_body")
    news_teaser = teasers.text
    #print(news_teaser)


    # # Scraping the Mars Space Images

    # define website and start scraping
    url = "https://www.jpl.nasa.gov/spaceimages/"
    browser.visit(url)

    # Retrieve page with the requests module
    # response = requests.get(url)
    html = browser.html

    # Create BeautifulSoup object; parse with 'html'
    soup = BeautifulSoup(html)

    # the page image
    links_found = browser.find_by_id('full_image')
    #print(links_found)
    
    # click to get the full image
    links_found.click()
    time.sleep(1)

    # Create BeautifulSoup object; parse with 'html'
    html = browser.html
    soup = BeautifulSoup(html)

    image_file = soup.select(".fancybox-image")

    #print(image_file)
    image_url = image_file[0]['src']
    #print (image_file[0]['src'])
    #print (image_url)

    # create real url for the image
    root_url = "https://www.jpl.nasa.gov"
    featured_image_url = root_url + image_url
    #print(featured_image_url)


    # # Scraping the Mars Facts

    # define website and start scraping
    url = "https://space-facts.com/mars/"
    browser.visit(url)

    html = browser.html

    # Create BeautifulSoup object; parse with 'html'
    soup = BeautifulSoup(html)

    # see what tables were pulled into pandas
    tables = pd.read_html(html)
    #tables

    mars_df = tables[0]
    #mars_df

    mars_df = mars_df.rename(columns={0:"Metrics", 1:"Mars"})
    #mars_df

    # convert Mars DF to html string
    result = mars_df.to_html(index=False, classes=["table", "table-borderless", "table-striped", "mytable"])
    #print(result)


    # # Scraping the Mars Facts

    # create dictionary, list storage for Mars images and titles
    titles=[]
    images=[]

    # define website and start scraping
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    html = browser.html

    # Create BeautifulSoup object; parse with 'html'
    soup = BeautifulSoup(html)

    # find links to hemisphere pages
    links_found = browser.links.find_by_partial_text("Enhanced")
    #print(*links_found)
    #print(len(links_found))

    # create loop for each link found to scrape image title and img_url

    for i in range(len(links_found)):
        # activate click to get detail page
        links_found[i].click()
        time.sleep(1)
        #update browser with new html
        html = browser.html
        #load the soup
        soup = BeautifulSoup(html)
        #find tags with original and get image url
        image_file = soup.find("a", text="Original")
        img_url = image_file.get('href')
        #find titles for images
        title_obj = soup.find("h2", class_="title")
        title = title_obj.text
        #append data to lists for storage
        titles.append(title)
        images.append(img_url + "/full.jpg")
        
        #reset the url, browser, html, links found to starting point, soup for next loop
        url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
        browser.visit(url)
        html = browser.html
        links_found = browser.links.find_by_partial_text("Enhanced")
        soup = BeautifulSoup(html)

    browser.quit()
    # print(titles, images)

    # create dictionary for image titles and urls
    hemisphere_images = {titles[i]: images[i] for i in range(len(titles))} 
    
    # hemisphere_image_urls = []

    # for i in range(len(titles)):
    #     hemisphere_image_urls.append(
    #     {titles[i]: images[i]})

    #print(hemisphere_image_urls)

    # make dictionary return from function

    mars_dict = {

        "Mars_headline": news_title,
        "Mars_teaser": news_teaser,
        "JPL_Image": featured_image_url,
        "Mars_facts": result,
        # "Mars_hem": hemisphere_image_urls
        "Mars_hem": hemisphere_images
    }

    return mars_dict

# data = scrape()
# print(data)
 