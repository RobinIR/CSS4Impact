from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
import json
import trafilatura
import requests
import azerbaijani_nlp
from writeToFiles import write_file
from config import start_page_number,end_page_number, chrome_extension

def postApiFuction(payload, url):
    # Define the headers (if necessary)
    headers = {
        'Content-Type': 'application/json'
    }

    # Convert the payload to JSON format
    json_payload = json.dumps(payload)

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
        print("Db get method error!")


def azertag_az(webpage, start_page_number, end_page_number, category, keyword, search_keyword):
    next_page = webpage + str(start_page_number)
    service = Service(executable_path=chrome_extension)
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(next_page)
    time.sleep(3)
    scroll_pause_time = 3
    screen_height = driver.execute_script("return window.screen.height;")
    i = 1
    while True:
        driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
        i += 1
        time.sleep(scroll_pause_time)
        scroll_height = driver.execute_script("return document.body.scrollHeight;")
        if (start_page_number > end_page_number):
            break
        if (screen_height) * i > scroll_height:
            break

    soup = BeautifulSoup(driver.page_source, "html.parser")
    data_found = False
    c = 0
    for link in soup.findAll('div', class_="news-image"):
        a = link.find('a')
        try:
            if 'href' in a.attrs:
                urlref = a.get('href')
                url = f"https://azertag.az/{urlref}"
                date_div = soup.find("div", class_="news-item")
                date = date_div.find("div", class_="news-date").text.strip()

                db_category = category
                docs = trafilatura.fetch_url(url)
                if docs is not None:
                    show = trafilatura.extract(docs, output_format='json', include_links=True)
                    if show is not None:
                        dict = json.loads(show)
                        text = dict["raw_text"]
                        title = dict["title"]

                        language = "Azerbaijani"
                        file_path = write_file(db_category, search_keyword, title, text, date, url, language)
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
            print("Error occurred in inner loop:", e)

    if not data_found:
       print("No data found!")
       return
    
    # Generating the next page url

    if start_page_number < end_page_number:
        start_page_number = start_page_number + 1
        azertag_az(webpage, start_page_number, end_page_number, category, keyword, search_keyword)


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
                webpage = f'https://azertag.az/de/axtarish?search={search_keyword}&page='
                # start_page_number = 1
                # end_page_number = page_number
                azertag_az(webpage, start_page_number,end_page_number, category_name, keyword, search_keyword)
