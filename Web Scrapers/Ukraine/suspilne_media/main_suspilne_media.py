from selenium import webdriver
from selenium.webdriver.chrome.service import Service
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
from writeToFiles import write_file
from config import start_page_number,end_page_number, local_drive_path, chrome_extension

from  DTO_css4impact_save import db_save
from api_helper_db import api_helper_db

month_mapping = {
    'січня': 1,
    'лютого': 2,
    'березня': 3,
    'квітня': 4,
    'травня': 5,
    'червня': 6,
    'липня': 7,
    'серпня': 8,
    'вересня': 9,
    'жовтня': 10,
    'листопада': 11,
    'грудня': 12
}
locale.setlocale(locale.LC_TIME, 'uk_UA')




def suspilne_media(webpage, start_page_number, end_page_number, category, keyword, search_keyword):
    # Send GET request to the URL
    search_url = f"{webpage}{search_keyword}&page={start_page_number}"
    try:
    #print(search_url)
        service = Service(executable_path=chrome_extension)
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(search_url)
        print("Webpage: ",webpage)
        time.sleep(1)

        # Get the page source and parse the JSON data
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        # Find the <pre> tag containing the JSON data
        pre_tag = soup.find('pre')

        if pre_tag:
            # Get the JSON data from the <pre> tag
            json_data = pre_tag.string

            # Parse the JSON data
            data = json.loads(json_data)

            # Extract the posts from the JSON data
            posts = data.get("posts", [])

            for post in posts:
                article_url = post.get("href")
                #print("Article URL:", article_url) 
                publish_time = post.get("publishTime")   
                date_parts = publish_time.split(' ')
                day = date_parts[0]
                month_name = date_parts[1]
                month = month_mapping.get(month_name, 1) 

                # Combine the date and time
                date  = datetime.now().replace(day=int(day), month=month, hour=0, minute=0, second=0, microsecond=0)

                #print("Publish Time:", ))
            # =datetime.strptime(publish_time, "%d %B, %H:%M").date()
                date= date.date().isoformat()
                language = "Ukrainian"

                # db_save(article_url, date, language, category, keyword, search_keyword)
                #print(article_url, date, language, category, keyword, search_keyword)
                
        if "next" in json_data:
            next_page_url = json_data["next"]

            if start_page_number <= end_page_number:
                start_page_number += 1
                suspilne_media(next_page_url, start_page_number, end_page_number, category, keyword, search_keyword)
    except:
        pass

category_url = "http://localhost:8000/category/path/Ukranian"
all_category_data = api_helper_db.getCategoryApi(category_url)
for item in all_category_data:
    categoryId = item['id']
    category_name = item['category']
    idps = item['idp']
    keywords = item['keywords']
    # To check it only for one category. Delete the if condition for final implementation.
    for idp in idps:
        for keyword in keywords:
            search_keyword = f"{idp} {keyword}"
            webpage = f"https://suspilne.media/ajax/posts/search/?query="
            start_page_number = start_page_number
            end_page_number = end_page_number

            suspilne_media(webpage, start_page_number, end_page_number, category_name, keyword, search_keyword)

