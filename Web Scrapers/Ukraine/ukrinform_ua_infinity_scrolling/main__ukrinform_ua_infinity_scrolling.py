from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import re
from bs4 import BeautifulSoup
import time
from selenium import webdriver
import json
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import requests
from selenium.webdriver.common.keys import Keys
import trafilatura
from writeToFiles import write_file
from config import start_page_number,end_page_number, local_drive_path, chrome_extension
from  DTO_css4impact_save import db_save
from api_helper_db import api_helper_db

url = 'https://www.ukrinform.ua/redirect'

# Create a dictionary with the form data
def set_token_and_search_query_data(token, search_param):
    data = {
        'type': 'search',
        '_token': token,
        'params[date_beg]': '',
        'params[date_end]': '',
        'params[query]': search_param,
        'params[rubric_id]': '0'
    }
    return data


# Send a POST request
def ukrinform_ua_infinity_scrolling(webpage, start_page_number,end_page_number, category_name, keyword, search_keyword):   
   try: 
        print("Webpage: ",webpage)
        response = requests.get("https://www.ukrinform.ua/")
        soup = BeautifulSoup(response.text, 'html.parser')
        left_menu_div = soup.find('div', id='leftMenu', class_='siteMenu')
        token_input = left_menu_div.select_one('input[name="_token"]')
        token_value = token_input['value']
        data = set_token_and_search_query_data(token_value,search_keyword)
        
        response_with_search_api = requests.post(webpage,data)
        soup_with_search_api= BeautifulSoup(response_with_search_api.text, 'html.parser')
        url_without_page = ""
        if response_with_search_api.status_code == 200:
            
            api_url = soup_with_search_api.find('a', class_="page-link")
            if api_url:
                api_url = api_url['href']
                url_without_page = re.sub(r'\?page=\d+', '', api_url)
                service = Service(executable_path=chrome_extension)
                options = webdriver.ChromeOptions()
                driver = webdriver.Chrome(service=service, options=options)
                driver.get(url_without_page)
                time.sleep(.3)  # Allow 2 seconds for the web page to open
                scroll_pause_time = 3 #Scrolling pausing time 
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
                rest_list_section = soup.find('section', class_='restList')
            
                # Extract articles within the <section class="restList">
                articles = rest_list_section.find_all('article')
                
                for article in articles:
                    article_url = f"https://www.ukrinform.ua{article.find('a')['href']}"     
                    date = article.find('time').text
                    language = "Ukranian"
                    db_save(article_url, date,language, category_name, keyword, search_keyword)

        else:
            print('Request failed with status code:', response.status_code)
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
            webpage = f"https://www.ukrinform.ua/redirect" 
            start_page_number = start_page_number
            end_page_number = end_page_number               
            ukrinform_ua_infinity_scrolling(webpage, start_page_number,end_page_number, category_name, keyword, search_keyword)
