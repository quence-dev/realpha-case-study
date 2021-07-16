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
print("Connected to: "+driver.title)

main = driver.find_element_by_tag_name('main') #find the HTML element
search = main.find_element_by_tag_name('input') 
search.clear() #ensure text field is empty
search.send_keys("New York, NY") #type a string into input
search.send_keys(Keys.RETURN) #hit enter

try:
    results = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, 'script'))
    )
    data = results.get_attribute('innerHTML')
    print(data)
except:
    print("JSON failed")
    driver.quit()

time.sleep(5)
driver.quit()