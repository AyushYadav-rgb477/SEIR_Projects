import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
if len(sys.argv) < 2:
    print("provide url")
    sys.exit()
target = sys.argv[1]
if not target.startswith("http://") and not target.startswith("https://"):
    target = "http://" + target
def fetch_page(address):
    driver = webdriver.Chrome()
    driver.get(address)
    print(driver.title)
    print(driver.find_element(By.TAG_NAME, "body").text)
    for anchortag in driver.find_elements(By.TAG_NAME, "a"):
        link = anchortag.get_attribute("href")
        if link:
            print(link)
    driver.quit()
fetch_page(target)
