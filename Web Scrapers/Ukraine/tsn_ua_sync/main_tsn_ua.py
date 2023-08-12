from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
from selenium import webdriver
import json
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import requests
from selenium.webdriver.common.keys import Keys
import trafilatura
from writeToFiles import write_file
from config import end_page_number,start_page_number, local_drive_path, chrome_extension
from  DTO_css4impact_save import db_save
from api_helper_db import api_helper_db

flag = False
def tsn_ua(webpage, start_page_number,end_page_number, category, keyword, search_keyword):
    # Send GET request to the URL
    global flag
    if not flag:
     search_url = webpage + search_keyword
     flag = 1
    else:
       search_url = webpage
    print("Webpage: ",search_url)
    try:
        response = requests.get(search_url)
        language = "Ukranian"
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Check the content type of the response
            content_type = response.headers.get("content-type", "").lower()

            if "application/json" in content_type:
                # Parse the JSON response
                data = response.json()

                # Extract the required data from the JSON response
                if "items" in data:
                    try:
                      for item in data["items"]:
                          article_url = item["url"]
                          date = item["published_at"]["datetime"].split(" ")[0]
                          language = "Ukranian"
                          db_save(article_url, date,language, category, keyword, search_keyword)
                    except Exception as e:
                      if date is None and url:
                          print("An exception occurred: ", e)

                if "next" in data:
                    next_page_url = data["next"]
                    if start_page_number <= end_page_number:
                        start_page_number = start_page_number+1
                        tsn_ua(next_page_url, start_page_number,end_page_number, category, keyword, search_keyword)
            else:
              soup = BeautifulSoup(response.text, features="lxml")
              for link in soup.findAll('div', class_="c-card__body"): 
                url = ""
                date = ""
                try:  
                  article_url = link.find('a', class_='c-card__link')
                  article_url = article_url['href']
                  date = link.find('time').text.strip()
                  language = "Ukranian"
                  db_save(article_url, date,language, category, keyword, search_keyword)
                except Exception as e:
                    if date is None and url:
                        print("An exception occurred: ", e)
              if start_page_number < end_page_number:
                start_page_number = start_page_number + 1
                find_next_page = soup.find('main',class_ = 'c-section')
                try:
                  find_next_page = find_next_page.find('div',class_='l-row')
                  search_url = find_next_page.get('data-url')
                  tsn_ua(search_url, start_page_number,end_page_number, category, keyword, search_keyword)
                except Exception as e:
                  print("something wrong")
        else:
            print("Request failed with status code:", response.status_code)
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
    if categoryId:
        
        for idp in idps:
            for keyword in keywords:
                #
                search_keyword = f"{idp} {keyword}"
                #earch_keyword = f"внутрішньо+переміщені+особи"
                webpage = f"https://tsn.ua/search?query=" 
                start_page_number = start_page_number
                end_page_number = end_page_number             
                flag = 0
                tsn_ua(webpage, start_page_number,end_page_number, category_name, keyword, search_keyword)