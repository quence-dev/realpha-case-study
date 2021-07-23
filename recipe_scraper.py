from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver #initial import
from selenium.webdriver.common.keys import Keys #allows keystrokes
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json, requests
import pandas as pd

# webdriver location on computer
PATH = '/Users/Quence/Webdrivers/chromedriver'
# set driver to open incognito window instead
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
driver = webdriver.Chrome(PATH, chrome_options=chrome_options)

# open a webpage
driver.get('https://www.allrecipes.com/')
print("Connected to: " + driver.title)

# returns list of recipes
def searchForRecipe(user_search, *page_count):
    search = driver.find_element_by_id('search-block')
    search.clear() 
    search.send_keys(user_search)
    search.send_keys(Keys.RETURN)

    # parse total number of results and calculate approx. number of total pages
    total = int(''.join(driver.find_element_by_id('search-results-total-results').text.split(' ')[0].split(',')))
    limit = (total / 23) + (total % 23)

    # load all desired results
    pages = load_pages(user_search, limit, page_count) if len(page_count) > 0 else load_pages(user_search, limit)
    print('%d pages loaded' % pages)

    # find all recipes and scrape info
    try:
        results = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'card__recipe card__facetedSearchResult'))
        )
        for result in results:
            recipe_url = result.find_element_by_tag_name('a').get_attribute('href')
    except:
        print('failed to parse recipes')
        print('quitting...')
        driver.quit()


# separate function to load pages
def load_pages(search, limit, *page_count):
    #format search string
    f_search = search.replace(' ','%2520')
    current_page = 1
    try:
        page_limit = int(''.join(map(str, page_count[0])))
    except:
        page_limit = limit # if tuple is empty and no user input

    # if user input page limit, return that number pages
    if len(page_count) > 0 and page_limit > 0:
        while current_page < page_limit:
            current_page += 1
            try:
                response = requests.get('https://www.allrecipes.com/element-api/content-proxy/faceted-searches-load-more?search={f_search}&page={current_page}')
                data = response.json()
                print(data)
                # print(data['hasNext'])
            except:
                print('could not load page %d' % current_page)
                return current_page - 1
            # print('page %d loaded' % current_page)
        return current_page
    
    while current_page < limit:
        current_page += 1
        try:
            response = requests.get('https://www.allrecipes.com/element-api/content-proxy/faceted-searches-load-more?search={f_search}&page={current_page}')
        except:
            print('error: %d. Could not load page %d' % response.status_code, current_page)
            return current_page - 1
        print('page %d loaded' % current_page)
    return current_page

searchForRecipe('cheese pizza', 2)

time.sleep(4)
driver.quit()