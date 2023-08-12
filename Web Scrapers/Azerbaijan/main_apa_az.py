import os
from bs4 import BeautifulSoup
import time
from selenium import webdriver
import json
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import requests
from selenium.webdriver.common.keys import Keys
import trafilatura
from config import start_page_number,end_page_number, local_drive_path, chrome_extension
from writeToFiles import write_file

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




def apa_az(webpage, start_page_number, end_page_number, category, keyword, search_keyword):  
   try: 
        next_page = webpage + str(start_page_number)
        
        print("Webpage :",next_page)
        
        response= requests.get(str(next_page))
        #Get the page response code
        response_code = str(response.status_code)
        #return if page response not 200
        if(str(response_code) != str(200)):
            #  print(response_code)
            return
        
        soup = BeautifulSoup(response.text, features="html.parser")
        data_found = False
        div_block = soup.find("div", class_="four_columns_block mt-site")
        if not div_block:
            print("No data found!")
            return
        links = div_block.find_all("a", class_="item")
            # Extracting the date
        count = 0 
        for link in links:
                try:
                    url = link.get("href")
                    response = requests.get(url)
                    content = response.text
                    soup = BeautifulSoup(content, "html.parser")
                    date_div = soup.find("div", class_="date_news").find("div", class_="date")
                    date = date_div.find("span", class_="date").text.strip()
                    db_category = category
                    
                    
                    docs = trafilatura.fetch_url(url)
                    if docs is not None:
                        show = trafilatura.extract(docs, output_format='json', include_links=True) 
                        # print(show)
                        if show is not None:
                            dict = json.loads(show)
                            text = dict["raw_text"]
                            title = dict["title"]
                            language = "Azerbaijani"
                            file_path = write_file(db_category,search_keyword,title,text, date, url, language)
                            data_found = True
                            if file_path is None:
                                continue 

                            ### NLP code here ####
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
   
   #Generating the next page url
   if start_page_number < end_page_number:
      start_page_number = start_page_number + 1
      apa_az(webpage, start_page_number,end_page_number, category, keyword, search_keyword)
   
   
category_url = "http://localhost:8000/category/path/Azerbaijani"
all_category_data = getCategoryApi(category_url)

for item in all_category_data:
    categoryId = item['id']
    category = item['category']
    idps = item['idp']
    keywords = item['keywords']
    # To check it on only for one category. Delete the if condition on final implementation
    if categoryId:
        # Limited the keywords for checking
        for idp in idps:
            for keyword in keywords:
                search_keyword = f"{idp} {keyword}"
                webpage = f"https://apa.az/az/search-result?search={search_keyword}&page="
                apa_az(webpage, start_page_number,end_page_number, category, keyword, search_keyword)