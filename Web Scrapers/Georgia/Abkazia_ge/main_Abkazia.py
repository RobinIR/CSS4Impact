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
from config import start_page_number,end_page_number
from  DTO_css4impact_save import db_save
from api_helper_db import api_helper_db
import urllib.parse 


# Step 1: Create a session
session = requests.Session()

# Step 2: Visit the parent site and extract the token

def abkhazia(webpage, start_page_number,end_page_number, category_name, keyword, search_keyword):
    url = "http://www.abkhazia.gov.ge"
    response = session.get(url)

    soup = BeautifulSoup(response.content, 'html.parser')
    token_input = soup.find('input', {'name': '_token'})
    token = token_input['value']

# Step 3: Send another request with the search query
    search_url = "http://www.abkhazia.gov.ge/liveSearch"
    print("searched:",search_keyword + " webpage:" + search_url)
    query = "დევნილი"
    data = {
        "_token": token,
        "keyword": query
    }
    response = session.post(search_url, data=data)


    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Extract the HTML content
        html_content = response.content

        # Parse the HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        # print(soup)
        # Find all the div elements with the specified class
        div_elements = soup.find_all('div', class_='bg-white col-md-12 col-sm-12 col-xs-12 blog-post-content xs-text-center no-padding')
        # print(soup)
        # Extract the data and URL from each div element
        counter=5
        for div in div_elements:
            if counter<0:
                return
            #print(div)
            counter = counter -1

            a_tag = div.find('a')
            if a_tag:
                url =  f"http://www.abkhazia.gov.ge{a_tag['href']}"
                print(url)
            
                date = ""
                language ="Georgian"
                db_save(url, date, language, category_name, keyword, search_keyword)
                
       
         
    else:
        print('Request failed with status code:', response.status_code)

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
            search_keyword = f"{idp} {keyword}"
            webpage = f"http://www.abkhazia.gov.ge/liveSearch" 
                        
            abkhazia(webpage, start_page_number,end_page_number, category_name, keyword, search_keyword)
      
print("Search is complete")
