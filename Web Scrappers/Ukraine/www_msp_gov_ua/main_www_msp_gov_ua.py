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
# #


def www_msp_gov_ua(webpage, start_page_number,end_page_number, category_name, keyword, search_keyword):
  try:
      
      response= requests.get(str(webpage)+str(search_keyword)+str("&from=&till=&w="))
      #Get the page response code
      #print("Webpage: ", webpage)
      response_code = str(response.status_code)
      #return if page response not 200
      if(str(response_code) != str(200)):
         return # urls
      soup = BeautifulSoup(response.text, features="lxml")
      # Extracting urls
      temp_data_disct= {}
      for link in soup.findAll('div', class_="search_item"): 
         url = ""
         date = ""
         try:  
                  article_url = f"https://www.msp.gov.ua{link.find('a')['href']}"
                  date = link.find('small').text.strip()
                  language = "Ukranian"
                  db_save(article_url, date,language, category_name, keyword, search_keyword)
                  
         except Exception as e:
               if date is None and url:
               # This block will be executed if an exception occurs
                  print("An exception occurred: ", e)
   
  except:
         pass
def get_orginal_search_link_for_www_msp_gov_ua(webpage, start_page_number,end_page_number, category_name, keyword, search_keyword):
      try:
         
         response= requests.get(str(webpage)+keyword)
      
      #Get the page response code
         response_code = str(response.status_code)
            #return if  page response not 200

         soup = BeautifulSoup(response.text, features="lxml")
         if(soup is None):
            return
         else:
            for link in soup.findAll('div', class_="search_item"): 
               url = ""
               date = ""
               try:  
                     article_url = search_keyword = r"https://www.msp.gov.ua/"+link.find('a')['href']
                     date = link.find('small').text.strip()
                     language = "Ukranian"
                     db_save(article_url, date,language, category_name, keyword, search_keyword)
               except Exception as e:
                  if date is None and url:
                        print("An exception occurred: ", e)
         soup = soup.find('div',class_="page_split_bar")
         for link in soup.find_all('a'):
            try:
               href = link.get('href')
               if href:
                  href = f"https://www.msp.gov.ua{link.get('href')}"
                  print("Webpage :", href)       
                  www_msp_gov_ua(webpage, start_page_number,end_page_number, category_name, keyword, search_keyword)
                  if(start_page_number > end_page_number):
                     return
                  start_page_number = start_page_number + 1
            except:
               pass 
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
            webpage = f"https://www.msp.gov.ua/search/index.php?start=0&s=" 
            start_page_number = start_page_number
            end_page_number = end_page_number             
            
            get_orginal_search_link_for_www_msp_gov_ua(webpage, start_page_number,end_page_number, category_name, keyword, search_keyword)


