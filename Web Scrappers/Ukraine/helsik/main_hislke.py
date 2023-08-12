from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
import trafilatura
from writeToFiles import write_file
from config import start_page_number,end_page_number, local_drive_path, chrome_extension,end_page_number
from  DTO_css4impact_save import db_save
from api_helper_db import api_helper_db
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()

def hislke(webpage, start_page_number, end_page_number, category, keyword, search_keyword):
# Load the initial page
    try:
        search_url= webpage+str(search_keyword)
        service = Service(executable_path=chrome_extension)
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(search_url)
        print("Webpage: ",search_url)
        time.sleep(5)
        soup = BeautifulSoup(driver.page_source,  'html.parser')

        div_elements = soup.find_all('div', class_='gsc-webResult gsc-result')
        for div_element in div_elements:
            date_element = div_element.find('div', class_='gs-snippet')
            url_element = div_element.find('a', class_='gs-title')

            date = date_element.get_text().replace('Date: ', '').strip()
            article_url = url_element['href']
            language = "Ukranian"
            db_save(article_url, date,language, category, keyword, search_keyword)
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
            #search_keyword = f"внутрішньо" #
            search_keyword = f"{idp} {keyword}"
            webpage = f"https://www.helsinki.org.ua/search_gcse/?q="
            start_page_number = start_page_number
            end_page_number = end_page_number

            hislke(webpage, start_page_number, end_page_number, category_name, keyword, search_keyword)

 


