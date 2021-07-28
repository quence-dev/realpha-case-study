from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
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
chrome_options.add_argument("--disable-notifications")
driver = webdriver.Chrome(PATH, options=chrome_options)

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
    # total = int(''.join(driver.find_element_by_id('search-results-total-results').text.split(' ')[0].split(',')))
    # limit = (total / 24) if  total % 24 == 0 else (total/24) + 1
    # pages = loader(limit, page_count) if len(page_count) > 0 else loader(limit)
    # print('%d pages loaded' % pages)

    # find all recipes and scrape info
    try:
        search_results = []

        results = WebDriverWait(driver, 60, poll_frequency=1).until(
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

            search_results.append(recipe_item)
        
        for x in range(len(search_results)):
            myurl = search_results[x]['url']
            details = getRecipeDetails(myurl)
            search_results[x]['metadata'] = details

        # save raw json file
        with open('data.json', 'w') as f:
            json.dump(search_results, f)

        df = pd.DataFrame(search_results)
        print(df)

    except:
        print('failed to parse recipes. quitting...')
        driver.quit()

# function to get recipe metadata
def getRecipeDetails(recipeURL):
    driver.get(recipeURL)

    try:
        details = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'recipe-meta-item-body'))
        )
        prep_time = details[0].text
        cook_time = "" if len(details) == 4 else details[1].text # can be unavailable
        add_time = "" if len(details) == 4 or len(details) == 5 else details[2].text # can be unavailable
        total_time = details[len(details)-3].text
        servings = details[len(details)-2].text
        total_yield = details[len(details)-1].text

        ingredients = []
        ingredient_items = driver.find_elements_by_class_name('ingredients-item-name')
        for ingredient in ingredient_items:
            ingredients.append(ingredient.text)

        directions = []
        steps = driver.find_element_by_css_selector('ul[class="instructions-section"]')
        list_of_steps = steps.find_elements_by_css_selector('li p')
        for step in list_of_steps:
            directions.append(step.text)

        metadata = {
            'prep': prep_time,
            'cook': cook_time,
            'additional': add_time,
            'total': total_time,
            'servings': servings,
            'yield': total_yield,
            'ingredients': ingredients,
            'directions': directions
        }
        return metadata
    except:
        print('failed to get instructions')
        return {
            'prep': 0,
            'cook': 0,
            'additional': 0,
            'total': 0,
            'servings': 0,
            'yield': 0,
            'ingredients': [],
            'directions': []
        }

# loads pages via page navigation
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

    # if user entered a page limit, return that number of pages (or max possible)
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

# separate function to load pages, doesn't work
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


searchForRecipe('cheese pizza', 2)
time.sleep(4)
driver.quit()