from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
import trafilatura
from writeToFiles import write_file
from config import start_page_number,end_page_number, local_drive_path, chrome_extension
from  DTO_css4impact_save import db_save
from api_helper_db import api_helper_db
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import urllib.parse

category_url = "http://localhost:8000/category/path/Georgian"
   

def Interpressnews_ge(webpage, start_page_number,end_page_number, category, keyword, search_keyword):
    ##### Web scrapper for infinite scrolling page #####
    next_page = webpage + search_keyword + "&page=" + str(start_page_number)
    #print(webpage)
    try:
        service = Service(executable_path=chrome_extension)
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(webpage)
        print("Webpage:",webpage)
        time.sleep(.3)  # Allow 2 seconds for the web page to open
        scroll_pause_time = 3 #Scrolling pausing time 
        screen_height = driver.execute_script("return window.screen.height;")   # get the screen height of the web
        i = 1   
        while True:
            # scroll one screen height each time
            driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
            i += 1
            time.sleep(scroll_pause_time)
            # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
            scroll_height = driver.execute_script("return document.body.scrollHeight;")  
            # Break the loop when the height we need to scroll to is larger than the total scroll height
            start_page_number = start_page_number + 1
            if(start_page_number > end_page_number):
                break
            if (screen_height) * i > scroll_height:
                break        

            
        soup = BeautifulSoup(driver.page_source, "html.parser")
        try:
            for link in soup.findAll('div', class_="categorylistitem"): 
                    title_element = link.find('div', class_='categoryitemtitle').a

                    # Extract the article title
                    article_text = title_element.text
                    article_url = link.find('a')['href']
                    article_url= f"https://www.interpressnews.ge{link.find('a')['href']}"
                    date = link.find('div', class_='categorybigdate').text.strip()
                    language = "Georgian" 
                    db_save(article_url,article_text, date,language, category_name, keyword, search_keyword)## here NLP call could be execute for nlp.
        except:
         pass   
    except:
        pass

category_url = "http://localhost:8000/category/path/Georgian"
all_category_data = api_helper_db.getCategoryApi(category_url)

for item in all_category_data:
    categoryId = item['id']
    category_name = item['category']
    idps = item['idp']
    keywords = item['keywords']
    # To check it on only for one category. Delete the if condition on final implementation.
   
    for idp in idps:
        for keyword in keywords:
            key = f"{idp} {keyword}"
            search_keyword = urllib.parse.quote(key)  
            webpage = f"https://www.interpressnews.ge/ka/search?q={search_keyword}"
            end_page_number=2
            Interpressnews_ge(webpage, start_page_number,end_page_number, category_name, keyword, search_keyword)

print("Search is complete")







