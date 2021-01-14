from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import os

title = "Title"
price = "100"
description = "Description\nDescription\nDescription"

options = Options()
options.add_argument("--disable-notifications")
path = 'C:/Program Files (x86)/chromedriver.exe'
with open("login.txt", "r") as file:
    login, password = file.read().split('\n')

driver = webdriver.Chrome(path, chrome_options=options)
driver.get('https://www.facebook.com/')
driver.find_element_by_id("email").send_keys(login)
driver.find_element_by_id("pass").send_keys(password)
driver.find_element_by_id("u_0_b").submit()
driver.implicitly_wait(.1)
driver.maximize_window()
driver.implicitly_wait(.1)
driver.get("https://www.facebook.com/marketplace/create/item/")
driver.implicitly_wait(.1)
pictures_ = driver.find_element_by_xpath(
    "/html/body/div[1]/div/div[1]/div[1]/div[3]/div/div/div[1]/div[1]/div[1]/div/div[3]/div[1]/div[2]/div/div/div[2]/div[1]/div/div/div")
image_path = "C:/Users/sulta/PycharmProjects/furniture_shop/image.jpg"
pictures_.send_keys(image_path)
driver.implicitly_wait(.1)
title_ = driver.find_element_by_xpath(
    '/html/body/div[1]/div/div[1]/div[1]/div[3]/div/div/div[1]/div[1]/div[1]/div/div[2]/div[1]/div[2]/div/div/div[3]/div/div/label/div/div/input')
title_.send_keys(title)
driver.implicitly_wait(.1)
price_ = driver.find_element_by_xpath(
    '/html/body/div[1]/div/div[1]/div[1]/div[3]/div/div/div[1]/div[1]/div[1]/div/div[2]/div[1]/div[2]/div/div/div[4]/div[1]/div/label/div/div/input')
price_.send_keys(price)
driver.implicitly_wait(.1)
description_ = driver.find_element_by_xpath(
    '/html/body/div[1]/div/div[1]/div[1]/div[3]/div/div/div[1]/div[1]/div[1]/div/div[3]/div[1]/div[2]/div/div/div[7]/div/div/label/div/div/textarea')
description_.send_keys(description)
driver.implicitly_wait(.1)