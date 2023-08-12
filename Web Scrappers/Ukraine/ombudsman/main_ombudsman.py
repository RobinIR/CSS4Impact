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

def ombudsman(webpage, start_page_number,end_page_number, category, keyword, search_keyword):
    
    try:
       # Send GET request
        webpage = webpage + str(search_keyword)
        response = requests.get(webpage)
        print("Webpage: ",webpage)
        # Parse the HTML content
        soup = BeautifulSoup(response.content, "html.parser")

        # Find all <a> tags within the specified <div> class
        news_items = soup.find_all("div", class_="news-list-wrapper")[0].find_all("a")

        # Extract the URLs from the <a> tags
        urls = [item["href"] for item in news_items]

        # Print the extracted URLs
        date = ""
        language = "Ukranian"
        for article_url in urls:
            db_save(article_url, date,language, category, keyword, search_keyword) 
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
    if categoryId == categoryId:

        for idp in idps:
            for keyword in keywords:
                search_keyword = f"{idp} {keyword}"
                #earch_keyword = f"внутрішньо+переміщені+особи"
                webpage = f"https://www.ombudsman.gov.ua/news/search?query=" 
                start_page_number = start_page_number
                end_page_number = end_page_number             
                flag = 0
                ombudsman(webpage, start_page_number,end_page_number, category_name, keyword, search_keyword)