from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver #initial import
from selenium.webdriver.common.keys import Keys #allows keystrokes
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

PATH = '/Users/Quence/Webdrivers/chromedriver' #wherever the webdriver is located
driver = webdriver.Chrome(PATH)

driver.get('https://www.homesnap.com/') #open a webpage
print(driver.title)

main = driver.find_element_by_tag_name('main') #find the HTML element
search = main.find_element_by_tag_name('input') 
search.send_keys("Bowie, MD") #type a string into input
search.send_keys(Keys.RETURN) #hit enter

# try:
#     results = WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located(By.ID, "0_0_2_9_8_divList")
#     )
#     # print(results.text)
#     results_json = results.find_element_by_tag_name("script")
#     print(results_json.text)
# except:
#     print("Web driver failed")
#     driver.quit()

time.sleep(5)

driver.quit()