#!/usr/bin/python3


import time
from lib2to3.pgen2 import driver
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

try:
    #driver = webdriver.Firefox()
    #driver = webdriver.Safari()

    s = Service('/usr/local/bin/chromedriver') 
    driver = webdriver.Chrome(service=s)

    
    driver.implicitly_wait(10)
    driver.get("https://www.bcc.com.tw/news3_search.asp")
    print("page title : " + driver.title)
    html = driver.page_source
    
    search = driver.find_element(By.ID , "q")
    search.send_keys("蘇打綠")
    search.send_keys(Keys.ENTER)

    items = driver.find_element(By.XPATH , "//div[@class='gcse-searchresults-only']")
    for item in items:
        a = item.find_element_by_tag_name("a")
        print(a.get_attribute("href"))


    '''
    form = driver.find_element(By.CLASS_NAME , "bxa2")
    print(form.tag_name)
    print(form.get_attribute("class"))
    
    p = driver.find_element(By.TAG_NAME , "div")
    print(p.text)
    
    
    soup = BeautifulSoup(html , "lxml")
    fp = open("index.html" , "w" , encoding="utf8")
    fp.write(soup.prettify())
    print("write file ...")
    fp.close()
    '''

    '''
    element = driver.find_element(By.ID , "q")
    element.send_keys("蘇打綠")
    element.submit()

    time.sleep(10)
    '''

    
    driver.quit()

except Exception as e:
    print("<<< Error >>> : " + str(e))
finally:
    pass

