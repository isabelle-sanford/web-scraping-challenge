from splinter import Browser
from bs4 import BeautifulSoup
import time
import pandas as pd

# function to visit a site and get its html
def visit_url(url, b):
    b.visit(url)
    time.sleep(10) # gives the browser time to load; probably unduly long but satellite internet is Bad
    soup = BeautifulSoup(b.html, 'html.parser')
    return soup


def scrape(): 
    # Set up splinter browser
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)


# -----------PART 1: Latest news article from mars.nasa.gov---
    article_url = "https://mars.nasa.gov/news/"
    article_soup = visit_url(article_url, browser)

    # get title
    titles = article_soup.find_all('div', class_="content_title")
    title = titles[1].text # titles[0] in this case is not an article

    # corresponding description
    descs = article_soup.find_all('div', class_="article_teaser_body")
    description = descs[1].text


# -----------PART 2: JPL Featured Image-----------------------
    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    jpl_soup = visit_url(jpl_url, browser)

    # get link to & visit page with image info (incl. full size image link)
    img_info_ext = jpl_soup.find("div", class_="carousel_items").a.get("data-link")
    img_info_url = "https://www.jpl.nasa.gov" + img_info_ext
    jpl_img_page = visit_url(img_info_url, browser)

    # find link to full size image
    full_img_ext = jpl_img_page.find('figure', class_="lede").a.get('href')
    full_size_img = "https://www.jpl.nasa.gov" + full_img_ext
    

# -----------PART 3: Mars Facts Table-------------------------
    facts_url = "https://space-facts.com/mars/"
    facts_tables = pd.read_html(facts_url) # read all tables into pandas

    table = facts_tables[0] # get first (and only) table
    table.to_html('facts_table.html') # make html file of table


# -----------PART 4: Mars Hemispheres-------------------------
    hemi_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    hemi_soup = visit_url(hemi_url, browser)
    
    # get list of link extensions to hemisphere pages
    links_html = hemi_soup.find_all('div', class_='description')
    links = [link.a.get('href') for link in links_html]
    
    # set up for getting stuff from each link
    base_hemi_url = 'https://astrogeology.usgs.gov'
    hemi_img_urls = []

    # for loop pulling hemisphere name & full-size-link from each link
    for l in links:
        # get html
        curr_soup = visit_url(base_hemi_url + l, browser)
        
        # full size image link
        img_link = curr_soup.ul.find_all('a')[1].get('href')
        
        # hemisphere from title
        temp_name = curr_soup.h2.text

        # remove last word ('enhanced')
        temp = temp_name.split(' ')
        temp.pop()
        name = ' '.join(temp)
        
        hemi_img_urls.append({'name': name, 'url': img_link})


    #stuff to return
    title
    description
    full_size_img
    hemi_img_urls

