import os
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import json
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import requests
from selenium.webdriver.common.keys import Keys
import trafilatura
from writeToFiles import write_file
from config import start_page_number,end_page_number, local_drive_path, chrome_extension
import azerbaijani_nlp

category_url = "http://localhost:8000/category/path/Azerbaijani"

   
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
        # Success! Print the response content
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



def infinit_scrolling_oxu(url, start_page_number, end_page_number, category, keyword, search_keyword):
        service = Service(executable_path=chrome_extension)
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(url)
        time.sleep(3)  # Allow 2 seconds for the web page to open
        scroll_pause_time = 3 # You can set your own pause time. My laptop is a bit slow so I use 1 sec
        screen_height = driver.execute_script("return window.screen.height;")   # get the screen height of the web
        i = 1
        while True:
            # scroll one screen height each time
            driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
            i += 1
            time.sleep(scroll_pause_time)
            # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
            scroll_height = driver.execute_script("return document.body.scrollHeight;")  
            # Break the loop when the height we need to scroll to is larger than the total scroll height

            if(start_page_number > end_page_number):
                break
            if (screen_height) * i > scroll_height:
                break 
                  
        soup = BeautifulSoup(driver.page_source, "html.parser")

        data_found = False
        # find element by xpath code 
        
        for link in soup.find_all('a', class_="news-i-inner"):   
            try:          
                # looking for href inside anchor tag             
                # storing the value of href in a separate variable
                url = f"https://oxu.az{link.get('href')}"
                date_day = link.find('div', class_='date-day').text.strip()
                date_month = link.find('div', class_='date-month').text.strip()
                date_year=link.find('div', class_='date-year').text.strip()
                date= date_day+":"+date_month+":"+date_year
                print(date)
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
                        language = "Azerbaijani"
                        category = category
                        file_path = write_file(db_category,search_keyword,title,text, date, url, language)  
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
                        postApiFuction(payload,'http://localhost:8000/collection')
                            
                            
                
            except Exception as e:
                pass
        if not data_found:
            print("No data found!")
            return
    
    # Generating the next page url

        if start_page_number < end_page_number:
            start_page_number = start_page_number + 1
            infinit_scrolling_oxu(webpage, start_page_number, end_page_number, category, keyword, search_keyword)



category_url = "http://localhost:8000/category/path/Azerbaijani"
all_category_data = getCategoryApi(category_url)

for item in all_category_data:
    categoryId = item['id']
    category_name = item['category']
    idps = item['idp']
    keywords = item['keywords']
    # To check it on only for one category. Delete the if condition on final implementation
    if categoryId:
        for idp in idps:
            for keyword in keywords:
                search_keyword = f"{idp} {keyword}"
                # print(search_keyword)
                webpage = f"https://oxu.az/all?query={search_keyword}"
                infinit_scrolling_oxu(webpage, start_page_number,end_page_number, category_name, keyword, search_keyword)
























# def infinit_scrolling(url):
# ##### Web scrapper for infinite scrolling page #####
#     driver = webdriver.Chrome(executable_path=r"C:\Users\mt_ah\.cache\selenium\chromedriver\win32\108.0.5359.71\chromedriver.exe")
#     driver.get(url)
#     time.sleep(3)  # Allow 2 seconds for the web page to open
#     scroll_pause_time = 0.5 #Scrolling pausing time 
#     screen_height = driver.execute_script("return window.screen.height;")   # get the screen height of the web
#     i = 1
#     count = 0
#     while True:
#         # scroll one screen height each time
#         driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
#         i += 1
#         time.sleep(scroll_pause_time)
#         # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
#         scroll_height = driver.execute_script("return document.body.scrollHeight;")  
#         # Break the loop when the height we need to scroll to is larger than the total scroll height
#         count += 1
#         print(count)
#         if(count == 500):
#             break
#         if (screen_height) * i > scroll_height:
#             break 

#     ##### Extract  URLs #####
#     urls = []
#     soup = BeautifulSoup(driver.page_source, "html.parser")
#     c = 0
#     for link in soup.find_all('a', class_="news-i-inner"):
#         url1 = f"https://www.oxu.az{link.get('href')}"
#         urls.append(url1)
        
#     return urls
# def print_url(urls):
#   for u in urls:
#     print(u)
#   print(len(urls))
# if __name__ == '__main__':
#   urls = infinit_scrolling('https://oxu.az/all?query=+baku')
#   print_url(urls)
