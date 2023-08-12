import os
from bs4 import BeautifulSoup
import time
from selenium import webdriver
import json
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import requests
from selenium.webdriver.common.keys import Keys
import trafilatura
# from writeToFiles import WriteToFile
from writeToFiles import write_file
from config import start_page_number,end_page_number, chrome_extension
import azerbaijani_nlp


def postApiFuction(payload,url):
    # Define the URL of the API endpoint
    # Define the payload (data to be sent to the API)
    # Convert the payload to JSON format
    json_payload = json.dumps(payload)

    # Define the headers (if necessary)
    headers = {
        'Content-Type': 'application/json'
    }

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
        # print(f"Error: {response.status_code} - {response.reason}")
        print("Db get method error!")




def azadliq_org(webpage, start_page_number, end_page_number, category, keyword, search_keyword):
    try:
        next_page = webpage + str(start_page_number)
        print("Webpage :", next_page)

        response = requests.get(str(next_page))
        # Get the page response code
        response_code = str(response.status_code)
        # Return if page response is not 200
        if str(response_code) != str(200):
            print("Page response error:", response_code)
            return
        data_found = False
        soup = BeautifulSoup(response.text, features="lxml")
        # Extracting urls
        for link in soup.findAll('div', class_="media-block"):
            try:
                url = f"https://www.azadliq.org{link.find('a')['href']}"
                date = soup.find('span', class_="date").text.strip()
                db_category = category
                docs = trafilatura.fetch_url(url)
                if docs is not None:
                    show = trafilatura.extract(docs, output_format='json', include_links=True)
                    if show is not None:
                        dict = json.loads(show)
                        text = dict["raw_text"]
                        title = dict["title"]
                        # DB code goes here
                        # Payload
                        language = "Azerbaijani"
                        file_path = write_file(db_category, search_keyword, title, text, date, url, language)
                        data_found = True
                        if file_path is not None:
                            # NLP call here
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
                print("Error occurred in inner loop:", e)

    except Exception as e:
        print("Error occurred in outer loop:", e)

    if not data_found:
       print("No data found!")
       return
    # Generating the next page url
    if start_page_number < end_page_number:
        start_page_number = start_page_number + 1
        azadliq_org(webpage, start_page_number, end_page_number, category, keyword, search_keyword)

category_url = "http://localhost:8000/category/path/Azerbaijani"
all_category_data = getCategoryApi(category_url)

for item in all_category_data:
    categoryId = item['id']
    category = item['category']
    idps = item['idp']
    keywords = item['keywords']
    if categoryId:
        for idp in idps:
            for keyword in keywords:
                search_keyword = f"{idp} {keyword}"
                webpage = f'https://www.azadliq.org/s?k={search_keyword}&tab=all&pi='
                # start_page_number = 1
                # end_page_number = page_number

                try:
                    azadliq_org(webpage, start_page_number, end_page_number, category, keyword, search_keyword)
                except Exception as e:
                    print("Error occurred in main loop:", e)