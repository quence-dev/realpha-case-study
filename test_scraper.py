from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver #initial import
from selenium.webdriver.common.keys import Keys #allows keystrokes
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

PATH = '/Users/Quence/Webdrivers/chromedriver' #wherever the webdriver is located
driver = webdriver.Chrome(PATH)

driver.get('http://www.google.com/') #open a webpage
print(driver.title)

searchbar = driver.find_element_by_css_selector('[aria-label="Search"]') #find the HTML element
searchbar.send_keys("test") #type a string into input
searchbar.send_keys(Keys.RETURN) #hit enter

#print source code print(driver.page_source) 
try:
    results = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "search"))
    )
    # print(results.text)

    result_item = results.find_elements_by_class_name("g")
    for item in result_item:
        link = item.find_element_by_tag_name("a")
        print(link.get_attribute("href"))
except:
    print("Web driver failed")
    driver.quit()

time.sleep(5)

driver.quit()