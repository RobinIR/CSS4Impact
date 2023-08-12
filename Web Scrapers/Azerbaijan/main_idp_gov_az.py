
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
from config import start_page_number, end_page_number, local_drive_path, chrome_extension
import azerbaijani_nlp

def postApiFuction(payload, url):
    # Define the headers (if necessary)
    headers = {
        'Content-Type': 'application/json'
    }

    # Convert the payload to JSON format
    json_payload = json.dumps(payload)

    # Make the POST request
    response = requests.get(url, headers=headers, data=json_payload)

    # Make the POST request
    response = requests.post(url, headers=headers, data=json_payload)

    # Check the response status code
    if response.status_code == 200:
        print("Db integrated")
    else:
        print("DB error!")


def getCategoryApi(url):
    # Define the headers (if necessary)
    headers = {
        'Content-Type': 'application/json'
    }

    # Make the GET request
    response = requests.get(url, headers=headers)

    # Check the response status code
    if response.status_code == 200:
        # Success! Print the response content
        return response.json()
    else:
        # Error! Print the response status code and reason
        print(f"Error: {response.status_code} - {response.reason}")



def get_idp_urls(webpage, start_page_number, end_page_number, category, keyword, search_keyword):
    data_found = False
    try:

        next_page = webpage + str(start_page_number)
        print("Webpage : ", next_page)
        response = requests.get(str(next_page))
        # Get the page response code
        response_code = str(response.status_code)
        # return if page response not 200
        if str(response_code) != str(200):
            return
        
        
        soup = BeautifulSoup(response.text, features="lxml")
        # Extracting urls
        for link in soup.findAll('div', class_="search_r_top"): 
            try:
                url = link.find('a')['href']
                date = link.find('span', class_='search_date').text.strip()
                db_category = category


                # Local file saving code
                docs = trafilatura.fetch_url(url)
                if docs is not None:
                    show = trafilatura.extract(docs, output_format='json', include_links=True)
                    # print(show)
                    if show is not None:
                        dict = json.loads(show)
                        text = dict["raw_text"]
                        title = dict["title"]
                        # DB code goes here
                        # Payload
                        # filePath = writeFile(keyword, title, text)
                        language = "Azerbaijani"
                        file_path = write_file(db_category, search_keyword, title, text, date, url,
                                                            language)
                        data_found = True

                        if file_path is None:
                            continue
                            
                        totalPriorityValue, persons, locations, idpKeyWordsCountedList, categoryKeyWordsCountedList, organizations = azerbaijani_nlp.azerbaijan_file_sort(file_path, language, category)
                        payload = {
                                "title": title,
                                "DatePublication": date,
                                "Language": language,
                                "Priority": totalPriorityValue,
                                "Url": url,
                                "Actors": persons,
                                "Location": locations,
                                "Organizations": organizations,
                                "IDPMatchedKeywords": idpKeyWordsCountedList,
                                "CatagoryMatchedKeywords": categoryKeyWordsCountedList,
                                "LocalPath": file_path,
                                "KeyWords": [keyword],
                                "Category": [category]
                        }
                        postApiFuction(payload, 'http://localhost:8000/collection')
                    
            except Exception as e:
                pass

    except Exception as e:
        pass

    if not data_found:
        print("No data found !")
        return
    
    if start_page_number < end_page_number:
        start_page_number += 1
        get_idp_urls(webpage, start_page_number, end_page_number, category, keyword, search_keyword)


category_url = "http://localhost:8000/category/path/Azerbaijani"
all_category_data = getCategoryApi(category_url)

for item in all_category_data:
    categoryId = item['id']
    category_name = item['category']
    idps = item['idp']
    keywords = item['keywords']
    if categoryId:
        for idp in idps:
            for keyword in keywords:
                search_keyword = f"{idp} {keyword}"
                webpage = f"http://idp.gov.az/az/search/q={search_keyword}/page/"
                # start_page_number = 1
                # end_page_number = page_number
                get_idp_urls(webpage, start_page_number, end_page_number, category_name, keyword,
                                                 search_keyword)





