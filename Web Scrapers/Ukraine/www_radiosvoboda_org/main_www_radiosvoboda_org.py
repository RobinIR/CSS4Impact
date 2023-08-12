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
from config import start_page_number,end_page_number, local_drive_path, chrome_extension
from  DTO_css4impact_save import db_save
from api_helper_db import api_helper_db

def www_radiosvoboda_org(webpage, start_page_number,end_page_number, category_name, keyword, search_keyword):   
   try: 
       
      next_page = webpage + search_keyword+'&pi='+str(start_page_number)
      print("Webpage: ",next_page)
      response= requests.get(str(next_page))
      #Get the page response code
      response_code = str(response.status_code)
      #return if page response not 200
      if(str(response_code) != str(200)):
      
       return #urls
      soup = BeautifulSoup(response.text, features="lxml")
      
      #print(soup)
      # Extracting urls
      for link in soup.findAll('div', class_="media-block"):     
         
            
            article_url = f"https://www.radiosvoboda.org{link.find('a')['href']}"
            date_element = link.find('span', class_='date--size-3')
            date = date_element.text.strip()
            language = "Ukranian"
            db_save(article_url, date,language, category_name, keyword, search_keyword)
         
         
      if start_page_number < end_page_number:
         start_page_number = start_page_number + 1
         www_radiosvoboda_org(webpage, start_page_number,end_page_number, category_name, keyword, search_keyword)
      #return urls
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
            webpage = f"https://www.radiosvoboda.org/s?k=" 
            start_page_number = start_page_number
            end_page_number = end_page_number               
            www_radiosvoboda_org(webpage, start_page_number,end_page_number, category_name, keyword, search_keyword)
