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

urls = []      

def ukc_gov_ua(flag,webpage, start_page_number,end_page_number, category_name, keyword, search_keyword):  
   
  try:
      response= requests.get(webpage)
      print("Webpage: ",webpage)
      
      response_code = str(response.status_code)
      if(str(response_code) != str(200)):
         return 
      soup = BeautifulSoup(response.text, features="lxml")
   
      for link in soup.findAll('a', class_="resource-block__link"):
         url1 = link.get('href')
         response= requests.get(url1)
         soup = BeautifulSoup(response.text, features="lxml")
         #oup = BeautifulSoup(html, 'html.parser')
         if soup.find('div', class_='section__body'):
            section_body = soup.find('div', class_='section__body')
            links = section_body.find_all('a')
            for link in links:
               url = link.get('href')
               urls.append(url)
               
         if url1 in urls:  
            continue
         else: 
            urls.append(url1)
         # print("----------------",url1)        
            ukc_gov_ua(flag,webpage, start_page_number,end_page_number, category_name, keyword, search_keyword) 
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
    #if categoryId == 69:
        
    for idp in idps:
         for keyword in keywords:
               search_keyword = f"{idp} {keyword}"
               webpage = f"https://ukc.gov.ua/?s=" 
               start_page_number = start_page_number
               end_page_number = end_page_number             
               flag = 0
               ukc_gov_ua(flag,webpage, start_page_number,end_page_number, category_name, keyword, search_keyword)
               try: 
                  date = ""  
                  language = "Ukranian"               
                  for article_url in urls:
                     db_save(article_url, date,language, category_name, keyword, search_keyword)
               except:
                  pass  
                   


