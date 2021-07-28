from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver #initial import
from selenium.webdriver.common.keys import Keys #allows keystrokes
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import json
import pandas as pd

# webdriver location on computer
PATH = '/Users/Quence/Webdrivers/chromedriver'
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--disable-notifications")
driver = webdriver.Chrome(PATH, options=chrome_options)

# open a webpage
driver.get('https://www.homesnap.com/')
print("Connected to: " + driver.title)

main = driver.find_element_by_tag_name('main') #find the HTML element
search = main.find_element_by_tag_name('input') 
search.clear() #ensure text field is empty
search.send_keys("New York, NY") #type a string into input
search.send_keys(Keys.RETURN) #hit enter

# load a few pages
actions = ActionChains(driver)
try:
    load_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(@id,'divAreaStats')]"))
    )
    for i in range(4):
        actions.perform()
        time.sleep(1)
except:
    print("can't find element")
actions.move_to_element(load_element)

try:
    time.sleep(10)
    results = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[class="pull-left ma-0 mb-5 ml-5 clearfix search-list-pa-item ps-r"]'))
    )
    
    property_data = []
    for result in results:
        status = result.find_element_by_class_name('pa-item-status-bar').text
        price = result.find_element_by_class_name('pa-item-paging-price').text.split('$')[1]
        address = result.find_element_by_css_selector('span[itemprop="streetAddress"]').text
        city = result.find_element_by_css_selector('span[itemprop="addressLocality"]').text.split(',')[0]
        state = result.find_element_by_css_selector('span[itemprop="addressRegion"]').text
        zipcode = result.find_element_by_css_selector('span[itemprop="postalCode"]').text

        property_item = {
            'status': status,
            'price': price,
            'address': address,
            'city': city,
            'state': state,
            'zipcode': zipcode
        }
        property_data.append(property_item)

    print('process complete')
except:
    print("JSON failed")
    driver.quit()

# doesn't work
# market_stats = driver.find_element_by_class_name('col-xs-12 list-unstyled mb-15 ph-20')
# market_stat = market_stats.find_elements_by_class_name('pull-right')
# market_data = {
#     'new_listings': market_stat[0].text,
#     'homes': market_stat[1].text,
#     'condos': market_stat[2].text,
#     'detached': market_stat[3].text,
#     'townhouse': market_stat[4].text,
#     'median_list': market_stat[5].text,
#     'median_sale': market_stat[6].text
# }
# print(market_data)

#  make dataframe to display list
df = pd.DataFrame(property_data)
# convert price to integer (https://stackoverflow.com/questions/39684548)
df.price = df['price'].replace({'K': '*1e3', 'M': '*1e6'}, regex=True).apply(pd.eval).astype(int)
print(df)

time.sleep(5)
driver.quit()


