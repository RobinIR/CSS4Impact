from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
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

#Scrapping for https://zakon.rada.gov.ua/
def pagination_scrap_zakon_rada_gov_ua(webpage, start_page_number,end_page_number, category_name, keyword, search_keyword):   
   try:
      next_page = webpage + str(start_page_number)
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
      for link in soup.findAll('a', class_="valid"):
         try:
            article_url = link.get('href')
            language = "Ukranian"
            date=""
            
            db_save(article_url, date,language, category_name, keyword, search_keyword)
         except:
            pass  
      #Generating the next page url
      if start_page_number < end_page_number:
         start_page_number = start_page_number + 1
         pagination_scrap_zakon_rada_gov_ua(webpage, start_page_number,end_page_number, category_name, keyword, search_keyword)
      #print(count)
   # return urls
   except:
       pass


def get_orginal_search_link_for_zakon_rada_gov_ua(webpage, start_page_number,end_page_number, category_name, keyword, search_keyword):
  try:
      #print(str(webpage + search_keyword))
      response= requests.get(str(webpage + search_keyword))
      #print(str(webpage + search_keyword))
      #Get the page response code
      response_code = str(response.status_code)
      #return if page response not 200
      soup = BeautifulSoup(response.text, features="lxml")

   #print(soup)
   
   # Extracting urls
      for link in soup.findAll('a', class_="valid"):
         try:
            article_url = link.get('href')
            language = "Ukranian"
            date=""            
            db_save(article_url, date,language, category_name, keyword, search_keyword)
         except:
            pass  

      search_urls = soup.find('a', class_="page-link")
      orginal_url = f"https://zakon.rada.gov.ua{search_urls.get('href')}" 


      orginal_url =  orginal_url[:len(orginal_url)-1] + ''
      return pagination_scrap_zakon_rada_gov_ua(orginal_url, start_page_number,end_page_number, category_name, keyword, search_keyword)
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
            webpage = f"https://zakon.rada.gov.ua/laws/find/a?text=" 
            start_page_number = start_page_number
            end_page_number = end_page_number               
            get_orginal_search_link_for_zakon_rada_gov_ua(webpage, start_page_number,end_page_number, category_name, keyword, search_keyword)
            