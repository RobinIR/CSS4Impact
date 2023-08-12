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
from config import start_page_number,end_page_number, local_drive_path, chrome_extension
from  DTO_css4impact_save import db_save
from api_helper_db import api_helper_db
import urllib.parse

def www_ombudsman_ge(webpage, start_page_number,end_page_number, category_name, keyword, search_keyword):
   try:
      next_page = webpage + search_keyword  
      
      print("Webpage:",next_page)
      try:
        
         response= requests.get(str(next_page))
         #Get the page response code
       
         response_code = str(response.status_code)
         #return if page response not 200
         if(str(response_code) != str(200)):
            return 
         soup = BeautifulSoup(response.text, features="lxml")
         #print(soup)
         # Extracting urls
         for link in soup.findAll('h3', class_="search_title"): 
            # print(link)
            url1 = f"https://www.ombudsman.ge{link.find('a')['href']}"        
            date = ""
            language ="Georgian"
            db_save(url1, date, language, category_name, keyword, search_keyword)
            
      except Exception as e:
         if date is None and next_page: 
            # This block will be executed if an exception occurs
            print("An exception occurred: ", e)
      
            www_ombudsman_ge(webpage, start_page_number,end_page_number, category_name, keyword, search_keyword)
            #return urls
         else:
            return
      except:
         pass
   except:
      pass
def get_orginal_search_link_for_www_ombudsman_ge(searchlink,start_page_number,end_page_number, category_name, keyword, search_keyword):
   searchlink = searchlink + str(search_keyword)  
   print("webpage:",searchlink)
   response= requests.get(str(searchlink))
#Get the page response code
   response_code = str(response.status_code)
   #return if page response not 200

   soup = BeautifulSoup(response.text, features="lxml")

   soup = soup.find('ul', class_="desktop_pagination")
   if(soup is None):
     print("No data found")
     return
   else:
    if start_page_number < end_page_number:
       start_page_number = start_page_number+1
       for link in soup.find_all('a'):
         href = link.get('href') 
         if href:
           href = f"https://www.ombudsman.ge{link.get('href')}" 
           www_ombudsman_ge(href, start_page_number,end_page_number, category_name, keyword, search_keyword)



category_url = "http://localhost:8000/category/path/Georgian"
all_category_data = api_helper_db.getCategoryApi(category_url)
for item in all_category_data:
    categoryId = item['id']
    category_name = item['category']
    idps = item['idp']
    keywords = item['keywords']        
    for idp in idps:
      for keyword in keywords:
            key = f"{idp} {keyword}"
            webpage = f"https://www.ombudsman.ge/geo/search/" 
            search_keyword = urllib.parse.quote(key)                     
            get_orginal_search_link_for_www_ombudsman_ge(webpage, start_page_number,end_page_number, category_name, keyword, search_keyword)

print("Search is complete")     
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   