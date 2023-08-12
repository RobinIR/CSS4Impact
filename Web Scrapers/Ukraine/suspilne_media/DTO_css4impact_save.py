import os
from bs4 import BeautifulSoup
import time
from selenium import webdriver
import json
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import requests
import locale
from selenium.webdriver.common.keys import Keys
import trafilatura
from datetime import datetime
import trafilatura
import json
from writeToFiles import write_file
from api_helper_db import api_helper_db
from config import start_page_number,end_page_number, local_drive_path, chrome_extension
import time
import ukrain_nlp
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


def db_save(url, date, language, category, keyword, search_keyword):
    db_category = category
    docs = trafilatura.fetch_url(url)
    
    if docs is not None:
        show = trafilatura.extract(docs, output_format='json', include_links=True) 
    
        time.sleep(10)
        if show is not None:
            dict = json.loads(show)
            text = dict["raw_text"]
            title = dict["title"]
            
        
            file_path = write_file(db_category,keyword,title,text, date, url, language)
            if file_path is None:
                return ## error line

            #NLP
            totalPriorityValue, persons, locations, idpKeywordSimilarityList, categoryKeywordSimilarityList, organizations = ukrain_nlp.ukarian_file_sort(file_path, language, category)
            payload = {
                "title": title,
                "DatePublication": date,
                "Language": language,
                "Priority": totalPriorityValue,
                "Url": url,
                "Actors": persons,
                "Location": locations,
                "Organizations": organizations,
                "IDPMatchedKeywords": idpKeywordSimilarityList,
                "CatagoryMatchedKeywords": categoryKeywordSimilarityList,
                "LocalPath": file_path,
                "KeyWords": [keyword],
                "Category": [category]
            }
            api_helper_db.postApiFuction(payload, 'http://localhost:8000/collection') ##error line

    else:
        # search_url = f"{webpage}{search_keyword}&page={start_page_number}"
    #print(search_url)
       service = Service(executable_path=chrome_extension)
       options = webdriver.ChromeOptions()
       driver = webdriver.Chrome(service=service, options=options)
       try:
            driver.get(url)
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            paragraphs = soup.find_all('p')
            title = soup.find('h1').get_text()
            merged_text = ' '.join(paragraph.get_text() for paragraph in paragraphs)
            #print(merged_text)
            #print("Title: ",title)
            text = merged_text
            title = title
            file_path = write_file(db_category,keyword,title,text, date, url, language)
            if file_path is None:
                return ## error line

            payload = {
                "title": title,
                "DatePublication": date,
                "Language": language,
                "Priority": totalPriorityValue,
                "Url": url,
                "Actors": persons,
                "Location": locations,
                "Organizations": organizations,
                "IDPMatchedKeywords": idpKeywordSimilarityList,
                "CatagoryMatchedKeywords": categoryKeywordSimilarityList,
                "LocalPath": file_path,
                "KeyWords": [keyword],
                "Category": [category]
            }
            api_helper_db.postApiFuction(payload, 'http://localhost:8000/collection')
       except:
            pass