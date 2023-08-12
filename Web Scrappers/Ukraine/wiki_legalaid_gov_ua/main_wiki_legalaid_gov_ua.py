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

def wiki_legalaid_gov_ua(webpage, start_page_number,end_page_number, category_name, keyword, search_keyword):   
  
    try:
        next_page = webpage+"&search="+search_keyword
        print("Webpage: ",next_page)
        try:
            response= requests.get(str(next_page))
        except:
            pass
        #Get the page response code
        response_code = str(response.status_code)
        #return if page response not 200
        if(str(response_code) != str(200)):
            
            return #urls
        soup = BeautifulSoup(response.text, features="lxml")
        
        search_results = soup.find_all('li', class_='mw-search-result')

        for result in search_results:
            heading = result.find('div', class_='mw-search-result-heading')
            #article_url = 
            article_url = f"https://wiki.legalaid.gov.ua/{heading.find('a')['href']}"
            
            data = result.find('div', class_='mw-search-result-data').get_text()
            date = re.search(r'\d{1,2} [а-яії]+ \d{4}', data).group()
            
            print("URL:", article_url)
            print("Date:", date)

            language = "Ukranian"
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
            webpage = f"https://wiki.legalaid.gov.ua/index.php?limit=500&" 
            start_page_number = start_page_number
            end_page_number = end_page_number               
            wiki_legalaid_gov_ua(webpage, start_page_number,end_page_number, category_name, keyword, search_keyword)

