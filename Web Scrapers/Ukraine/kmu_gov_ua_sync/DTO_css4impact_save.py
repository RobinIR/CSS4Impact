import os
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
from api_helper_db import api_helper_db
import ukrain_nlp



def db_save(url,title, date, language, category, keyword, search_keyword):
    db_category = category
    driver = webdriver.Chrome(executable_path=r"C:\Users\mt_ah\.cache\selenium\chromedriver\win32\108.0.5359.71\chromedriver_win32\chromedriver.exe")
    driver.get(url)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    div = soup.find('div', class_='WordSection1')
# Find all <p> tags within the div and extract their text content
    #p_tags = div.find_all('p')
    p_tags = div.find_all('p')
    p_texts = [p.get_text(strip=True) for p in p_tags]
    #title = soup.find('h1').get_text()
    #merged_text = ' '.join(paragraph.get_text() for paragraph in paragraphs)
    #print("Testing data for save:",url," ", date," language: ", category, " Keyword: ", search_keyword, " Search keyword: ")
    # docs = trafilatura.fetch_url(url)
    # if docs is not None:
    #     show = trafilatura.extract(docs, output_format='json', include_links=True) 
    #     #print("I am here for checking: data: ", show)
    #     if show is not None:
            # dict = json.loads(show)
            # text = dict["raw_text"]
    #print("Hi I am hre for checking: ",p_texts)
           # title = dict["title"]
            
            #time.sleep(3)  
            # DB code goes here
            # Payload
            #language = "Uka"
           # print("Ahmed_buging: ",title)
            #print("Testing data for save:",url," ", date," language: ", category, " Keyword: ", search_keyword, " Search keyword: ")
        
    file_path = write_file(db_category,keyword,title,p_texts, date, url, language)
    if file_path is None:
        #print("===Ia here ====")
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
