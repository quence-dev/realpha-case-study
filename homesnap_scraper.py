from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver #initial import
from selenium.webdriver.common.keys import Keys #allows keystrokes
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import pandas as pd

# webdriver location on computer
PATH = '/Users/Quence/Webdrivers/chromedriver'
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--disable-notifications")
driver = webdriver.Chrome(PATH, chrome_options=chrome_options)

# open a webpage
driver.get('https://www.homesnap.com/')
print("Connected to: " + driver.title)

main = driver.find_element_by_tag_name('main') #find the HTML element
search = main.find_element_by_tag_name('input') 
search.clear() #ensure text field is empty
search.send_keys("New York, NY") #type a string into input
search.send_keys(Keys.RETURN) #hit enter

def autoScroller():
    ######## auto scroller #########
    # pause = 0.5
    # last_height = driver.execute_script("return document.body.scrollHeight")
    # print("Last height: %d" % last_height)

    # while True:
    #     # Scroll down to bottom
    #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    #     # Wait to load page
    #     time.sleep(pause)

    #     # Calculate new scroll height and compare with last scroll height
    #     new_height = driver.execute_script("return document.body.scrollHeight")
    #     if new_height == last_height:
    #         break
    #     last_height = new_height
    ####################################
    return None

try:
    time.sleep(15)
    
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
        time.sleep(0.25)

    print('process complete')
except:
    print("JSON failed")
    driver.quit()

#  make dataframe to display list
df = pd.DataFrame(property_data)
# convert price to integer (https://stackoverflow.com/questions/39684548)
df.price = df['price'].replace({'K': '*1e3', 'M': '*1e6'}, regex=True).apply(pd.eval).astype(int)
print(df)

time.sleep(5)
driver.quit()


