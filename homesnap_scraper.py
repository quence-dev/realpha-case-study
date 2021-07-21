from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver #initial import
from selenium.webdriver.common.keys import Keys #allows keystrokes
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

# webdriver location on computer
PATH = '/Users/Quence/Webdrivers/chromedriver'
driver = webdriver.Chrome(PATH)

# open a webpage
driver.get('https://www.homesnap.com/')
print("Connected to: " + driver.title)

main = driver.find_element_by_tag_name('main') #find the HTML element
search = main.find_element_by_tag_name('input') 
search.clear() #ensure text field is empty
search.send_keys("New York, NY") #type a string into input
search.send_keys(Keys.RETURN) #hit enter


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

try:
    # main2 = driver.find_element_by_tag_name('main')
    # scripts = main2.find_element_by_xpath('//*[contains(@id,"divList")]/script')
    time.sleep(5)
    # results = WebDriverWait(driver, 10).until(
    #     EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'span[itemprop="streetAddress"]'))
    # )
    results = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[class="pull-left ma-0 mb-5 ml-5 clearfix search-list-pa-item ps-r"]'))
    )
    # results = main.find_element_by_tag_name('script')
    for result in results:
        print(result.text)
    # print(script.get_attribute('outerHTML'))
except:
    print("JSON failed")
    driver.quit()

time.sleep(5)
driver.quit()


