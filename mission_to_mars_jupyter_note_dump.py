#!/usr/bin/env python
# coding: utf-8

# In[1]:


# dependencies/lib files
from splinter import Browser
from bs4 import BeautifulSoup
import requests, time
import pandas as pd


# In[2]:


# set up browser for scrapping

executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser("chrome", **executable_path, headless=False)


# In[3]:


# define website and start scraping
url = "https://mars.nasa.gov/news/"
browser.visit(url)

# Retrieve page with the requests module
# response = requests.get(url)
html = browser.html

# Create BeautifulSoup object; parse with 'html'
soup = BeautifulSoup(html)


#print(soup.prettify())
    


# # Scraping the Mars News

# In[4]:


# scrape news headline
titles = soup.find_all(class_='content_title')

news_title = titles[1].text
print(news_title)


# In[5]:


# scrape news teaser text
teasers = soup.find(class_="article_teaser_body")
news_teaser = teasers.text
print(news_teaser)


# # Scraping the Mars Space Images

# In[6]:


# define website and start scraping
url = "https://www.jpl.nasa.gov/spaceimages/"
browser.visit(url)

# Retrieve page with the requests module
# response = requests.get(url)
html = browser.html

# Create BeautifulSoup object; parse with 'html'
soup = BeautifulSoup(html)


#print(soup.prettify())


# In[7]:


# the page image
links_found = browser.find_by_id('full_image')
print(links_found)
   
#links_found.click()
   
#image = soup.find("img", class_='content_title')

#print(image)


# In[8]:


links_found.click()
time.sleep(1)


# In[9]:


# Create BeautifulSoup object; parse with 'html'
html = browser.html
soup = BeautifulSoup(html)


# In[10]:


image_file = soup.select(".fancybox-image")
#image_file = soup.select("#fancybox-lock")

#print(image_file)
image_url = image_file[0]['src']
print (image_file[0]['src'])
print (image_url)


# In[11]:


# create real url for the image
root_url = "https://www.jpl.nasa.gov"
featured_image_url = root_url + image_url
print(featured_image_url)


# # Scraping the Mars Facts

# In[122]:


# define website and start scraping
url = "https://space-facts.com/mars/"
browser.visit(url)

html = browser.html

# Create BeautifulSoup object; parse with 'html'
soup = BeautifulSoup(html)

#print(soup.prettify())


# In[123]:


# see what tables were pulled into pandas
tables = pd.read_html(html)
tables


# In[124]:


mars_df = tables[0]
mars_df


# In[125]:


mars_df = mars_df.rename(columns={0:"Metrics", 1:"Mars"})
mars_df


# In[126]:


# convert Mars DF to html string
result = mars_df.to_html()
#print(result)


# # Scraping the Mars Facts

# In[128]:


# create dictionary, list storage for Mars images and titles
titles=[]
images=[]


# In[129]:


# define website and start scraping
url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
browser.visit(url)

html = browser.html

# Create BeautifulSoup object; parse with 'html'
soup = BeautifulSoup(html)

# print(soup.prettify())


# In[130]:


# find links to hemisphere pages
links_found = browser.links.find_by_partial_text("Enhanced")
print(*links_found)
print(len(links_found))


# In[131]:


# create loop for each link found to scrape image title and img_url


# In[132]:


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
    images.append(img_url)
    
    #reset the url, browser, html, links found to starting point, soup for next loop
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    html = browser.html
    links_found = browser.links.find_by_partial_text("Enhanced")
    soup = BeautifulSoup(html)


# In[133]:


print(titles, images)


# In[134]:


# create dictionary for image titles and urls
hemisphere_image_urls = []

for i in range(len(titles)):
    hemisphere_image_urls.append(
    {'title':titles[i], 'image_url':images[i]})


# In[135]:


print(hemisphere_image_urls)


# In[ ]:


# below was proofing the individual scrape prior to setting up a loop


# In[82]:


# click links to large pictures

# links_found[0].click()
# time.sleep(1)

    


# In[83]:


# Create BeautifulSoup object; parse with 'html'
# html = browser.html
# soup = BeautifulSoup(html)


# In[84]:


# image_file = soup.find("a", text="Original")
# #print(image_file)

# # print (image_file.get('href'))
# img_url = image_file.get('href')
# print(img_url)


# In[91]:


# title_obj = soup.find("h2", class_="title")
# print(title_obj.text)

# title = title_obj.text

# print(title)


# In[95]:


# load lists with values

# titles.append(title)
# images.append(img_url)

# print(titles, images)


# In[ ]:




