from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver #initial import
from selenium.webdriver.common.keys import Keys #allows keystrokes
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time, json, requests
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
    # then load all desired results
    total = int(''.join(driver.find_element_by_id('search-results-total-results').text.split(' ')[0].split(',')))
    limit = (total / 24) if  total % 24 == 0 else (total/24) + 1
    print('limit: %d' % limit)
    pages = loader(limit, page_count) if len(page_count) > 0 else loader(limit)
    print('%d pages loaded' % pages)
    # actions = ActionChains(driver)
    # load_element = driver.find_element_by_id('search-results-load-more-container')
    # for i in range(page_count):
    #     actions.move_to_element(load_element)
    #     actions.perform()

    # find all recipes and scrape info
    try:
        search_results = []

        results = WebDriverWait(driver, 60).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'card__recipe'))
        )
        for result in results:
            recipe_url = result.find_element_by_tag_name('a').get_attribute('href')
            recipe_title = result.find_element_by_tag_name('a').get_attribute('title')
            recipe_rating = float(result.find_element_by_class_name('review-star-text').text.split(' ')[1])
            recipe_rating_count = int(result.find_element_by_class_name('card__ratingCount').text.split(' ')[0])
            recipe_summary = result.find_element_by_class_name('card__summary').text
            recipe_author = result.find_element_by_class_name('card__authorName').text

            recipe_item = {
            'title': recipe_title,
            'summary': recipe_summary,
            'rating': recipe_rating,
            'rating_count': recipe_rating_count,
            'url': recipe_url,
            'author': recipe_author
            }

            details = getRecipeDetails(recipe_url)

            search_results.append(recipe_item)
        
        df = pd.DataFrame(search_results)
        print(df)

    except:
        print('failed to parse recipes')
        print('quitting...')
        driver.quit()

def getRecipeDetails(recipeURL):
    search_result = driver.find_element_by_xpath("//a[href='{recipeURL}']")
    driver.click(search_result)
    try:
        details_section = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'recipe-meta-container two-subcol-content clearfix'))
        )
        details = details_section.find_elements_by_class_name('recipe-meta-item-body')
        
        ingredients = []
        ingredient_items = driver.find_elements_by_class_name('ingredients-item-name')
        for ingredient in ingredient_items:
            ingredients.append(ingredient.text)
            print(ingredient.text)

        metadata = {
            'prep': details[0],
            'cook': details[1],
            'additional': details[2],
            'total': details[3],
            'servings': details[4],
            'yield': details[5],
            'ingredients': ingredients
        }



    except:
        print('failed')
        return



def loader(limit, *page_count):
    actions = ActionChains(driver)
    load_element = driver.find_element_by_id('search-results-load-more-container')
    actions.move_to_element(load_element)
    
    current_page = 1
    # set page_limit if there is one
    try:
        page_limit = int(''.join(map(str, page_count[0])))
    except:
        page_limit = limit # if tuple is empty and no user input

    # if user input page limit, return that number pages
    if len(page_count) > 0 and page_limit > 0:
        while current_page < page_limit:
            current_page += 1
            try:
                actions.perform()
            except:
                print('could not load page %d' % current_page)
                return current_page - 1
            print('page %d loaded' % current_page)
        return current_page
    
    while current_page < limit:
        current_page += 1
        try:
            actions.perform()
        except:
            print('could not load page %d' % current_page)
            return current_page - 1
        print('page %d loaded' % current_page)
    return current_page

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
                # data = json.loads(response.text)
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
            data = json.loads(response.text)
            print(data['hasNext'])
        except:
            print('error: %d. Could not load page %d' % response.status_code, current_page)
            return current_page - 1
        print('page %d loaded' % current_page)
    return current_page

searchForRecipe('cheese pizza', 3)

# time.sleep(4)
# driver.quit()