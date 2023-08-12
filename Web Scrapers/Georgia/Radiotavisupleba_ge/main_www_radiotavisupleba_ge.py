import os
from bs4 import BeautifulSoup
import time
from selenium import webdriver
import json
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import requests
from selenium.webdriver.common.keys import Keys
import trafilatura
from writeToFiles import write_file
from config import start_page_number, end_page_number, local_drive_path, chrome_extension
from  DTO_css4impact_save import db_save
from api_helper_db import api_helper_db
import urllib.parse   

def www_radiotavisupleba_ge(webpage, start_page_number,end_page_number, category_name, keyword, search_keyword, data_found=False):
   try:
      next_page = webpage+search_keyword+"&tab=all&pi="+ str(start_page_number) + "&r=any&pp=10"
      
      print(next_page)
      try:
         
         response= requests.get(str(next_page))
         #Get the page response code
         response_code = str(response.status_code)
         #return if page response not 200
         if(str(response_code) != str(200)):
            return #urls
         soup = BeautifulSoup(response.text, features="lxml")
         next_button=soup.find('li',class_='pagination__item ta-c pagination__item--next')
         articles = soup.findAll('div', class_="media-block")
         if len(articles) == 0:
               if not data_found:
                  print("No data found")
               return
         # Extracting urls
         for link in articles:
            try:
               url = f"https://www.radiotavisupleba.ge{link.find('a')['href']}"
               date = ""
               language ="Georgian"
               db_save(url, date, language, category_name, keyword, search_keyword)
            
            except Exception as e:
               if date is None and url:
                  # This block will be executed if an exception occurs
                  print("An exception occurred: ", e)
         if next_button:   
            if start_page_number < end_page_number:
               start_page_number = start_page_number + 1
               www_radiotavisupleba_ge(webpage, start_page_number,end_page_number, category_name, keyword, search_keyword,True)
            #return urls
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
            key = f"{idp}{keyword}"
            webpage = f"https://www.radiotavisupleba.ge/s?k=" 
            search_keyword = urllib.parse.quote(key)          
            www_radiotavisupleba_ge(webpage, start_page_number,end_page_number, category_name, keyword, search_keyword)
print("search is Complete")


   
