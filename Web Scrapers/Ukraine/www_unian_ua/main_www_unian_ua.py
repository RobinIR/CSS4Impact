from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from writeToFiles import write_file
from config import start_page_number,end_page_number, local_drive_path, chrome_extension
from  DTO_css4impact_save import db_save
from api_helper_db import api_helper_db

def www_unian_ua(webpage, start_page_number,end_page_number, category_name, keyword, search_keyword):
##### Web scrapper for infinite scrolling page #####
    try:
        search_keyword = webpage + str(search_keyword)
        print("Webpage: ",search_keyword)
        service = Service(executable_path=chrome_extension)
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(search_keyword)
        time.sleep(3)  # Allow 2 seconds for the web page to open
        scroll_pause_time = 5 #Scrolling pausing time 
        screen_height = driver.execute_script("return window.screen.height;")   # get the screen height of the web
        i = 1
        count = 0
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

        ##### Extract  URLs #####
        urls = []
        soup = BeautifulSoup(driver.page_source, "html.parser")
        for link in soup.find_all('a', class_="list-thumbs__title"):        
            article_url = link.get('href')
            language = "Ukranian"
            date=""        
            db_save(article_url, date,language, category_name, keyword, search_keyword)

    except:
        pass      
category_url = "http://localhost:8000/category/path/Ukranian"
all_category_data = api_helper_db.getCategoryApi(category_url)
for item in all_category_data:
    categoryId = item['id']
    category_name = item['category']
    idps = item['idp']
    keywords = item['keywords']
    # To check it on only for one category. Delete the if condition on final implementation.
  
    for idp in idps:
        for keyword in keywords:
            search_keyword = f"{idp} {keyword}"
            webpage = f"https://www.unian.ua/search?q=" 
            start_page_number = start_page_number
            end_page_number = end_page_number               
            www_unian_ua(webpage, start_page_number,end_page_number, category_name, keyword, search_keyword)
            break
        break



#urls = []
#print_url(www_unian_ua('https://www.unian.ua/search?q=внутрішньо'))

