from bs4 import BeautifulSoup
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import manager as mg


FORM_LINK = mg.FORM_LINK
ZILLOW_CLONE = "https://appbrewery.github.io/Zillow-Clone/"

response = requests.get(ZILLOW_CLONE)
web_page = response.text

soup = BeautifulSoup(web_page, "html.parser")

renting = soup.select(selector=".StyledPropertyCardDataWrapper")
# print(renting)
renting_address = []
renting_links = []
renting_price = []

for data in renting:
    address = data.find(name="address").getText().strip()
    renting_address.append(address)
    link = data.find(name='a').get("href")
    renting_links.append(link)
    price = data.find(name="span").getText().split("/")[0][0:6]
    renting_price.append(price)

print(renting_address)
print(renting_links)
print(renting_price)

# for data in renting:
#     price = data.find(name="span").getText().split("/")[0][0:6]
#     print(price)

# Part 2 - Fill in the Google Form using Selenium

# Optional - Keep the browser open (helps diagnose issues if the script crashes)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)

for n in range(len(renting_links)):
    # TODO: Add fill in the link to your own Google From
    driver.get(FORM_LINK)
    time.sleep(2)

    # Use the xpath to select the "short answer" fields in your Google Form.
    # Note, your xpath might be different if you created a different form.
    address = driver.find_element(by=By.XPATH,
                                  value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price = driver.find_element(by=By.XPATH,
                                value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link = driver.find_element(by=By.XPATH,
                               value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    submit_button = driver.find_element(by=By.XPATH,
                                        value='//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')

    address.send_keys(renting_address[n])
    price.send_keys(renting_price[n])
    link.send_keys(renting_links[n])
    submit_button.click()
