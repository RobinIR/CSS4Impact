from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import urllib.parse
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
from config import page_number, local_drive_path, chrome_extension
from  DTO_css4impact_save import db_save
from api_helper_db import api_helper_db

from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import urllib.parse

def scrape_zn_ua(webpage, start_page_number, end_page_number, category_name, keyword, search_keyword):
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-browser-side-navigation")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36")
    options.add_argument("referer=https://zn.ua/ukr/search/query={}/p1?__cf_chl_tk=yBYnElqo2n4DIm9QqrRqavSk774xxd6V9GLTSUTMRqQ-1687353542-0-gaNycGzND2U".format(search_keyword))
    
    driver = webdriver.Chrome(executable_path=r"C:\Users\mt_ah\.cache\selenium\chromedriver\win32\94.0.4606.61\chromedriver.exe", options=options)

    for page_number in range(start_page_number, end_page_number + 1):
        search_keyword = urllib.parse.quote(search_keyword)
        search_url = f"{webpage}{search_keyword}/p{page_number}"

        print("Scraping page:", page_number)
        
        driver.get(search_url)
        time.sleep(5)  # Adjust the delay if necessary
        
        soup = BeautifulSoup(driver.page_source, "html.parser")
        search_box_items = soup.find_all(class_='search-box__item')
        
        for item in search_box_items:
            link = item.find('a', class_='search-box__link')
            if link:
                article_url = link['href']
                print("URL:", article_url)
            
            date = item.find('span', class_='search-box__date')
            if date:
                date = date.get_text(strip=True)
                print("Date:", date)
            
            # Process the data as needed
            
        print("==============================================")
    
    driver.quit()

# Example usage:
scrape_zn_ua("https://zn.ua/ukr/search/query=", 1, 3, "category_name", "keyword", "внутрішньо+переміщені+особи")
