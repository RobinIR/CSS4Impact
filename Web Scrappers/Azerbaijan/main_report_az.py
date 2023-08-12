import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from bs4 import BeautifulSoup, SoupStrainer
import requests
import trafilatura
from trafilatura import feeds, extract_metadata
from trafilatura.feeds import find_feed_urls
from trafilatura.spider import focused_crawler
from writeToFiles import write_file
import json
from config import start_page_number,end_page_number, local_drive_path, chrome_extension
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
        # Success! Print the response content
        # print(response.content)
        print("Db integrated")
    else:
        # Error! Print the response status code and reason
        # print(f"Error: {response.status_code} - {response.reason}")
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
        print("Db Insertion Error!")

def infinit_scrolling_report_az(webpage, start_page_number,end_page_number, category, keyword, search_keyword):
##### Web scrapper for infinite scrolling page #####
    service = Service(executable_path=chrome_extension)
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(webpage)
    time.sleep(3)  # Allow 2 seconds for the web page to open
    scroll_pause_time = 0.5 #Scrolling pausing time 
    screen_height = driver.execute_script("return window.screen.height;")   # get the screen height of the web
    i = 1
    count = 0
    found_data = False
    while True:
        # scroll one screen height each time
        driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
        i += 1
        time.sleep(scroll_pause_time)
        # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
        scroll_height = driver.execute_script("return document.body.scrollHeight;")  
        # Break the loop when the height we need to scroll to is larger than the total scroll height
        count += 1
        if(count == 500):
            break
        if (screen_height) * i > scroll_height:
            break 

   
    
    soup = BeautifulSoup(driver.page_source, "html.parser")
    c = 0
    for link in soup.find_all('div', class_="info"):
        try:
            url = f"https://report.az{link.find('a')['href']}"
            date = link.find('div', class_='news-date').text.strip()
            print(url, date)
            db_category = category_name
        
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
                    language = "Azerbaijani"
                    file_path = write_file(db_category, search_keyword, title, text, date, url, language)
                    found_data = True
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
            pass
        
    if not found_data:
        print("No data found")
        return
   #Generating the next page url
    if start_page_number < end_page_number:
        start_page_number = start_page_number + 1
        infinit_scrolling_report_az(webpage, start_page_number,end_page_number, category_name, keyword, search_keyword)

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
                webpage = f"https://report.az/search/?query={search_keyword}/"
                infinit_scrolling_report_az(webpage, start_page_number,end_page_number, category_name, keyword, search_keyword)