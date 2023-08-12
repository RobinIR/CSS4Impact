from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
import trafilatura
from writeToFiles import write_file
from config import start_page_number,end_page_number, local_drive_path, chrome_extension
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
import urllib.parse

def civil_ge(webpage, start_page_number, end_page_number, category_name, keyword, search_keyword):
    try:
        next_page = webpage + str(start_page_number) + '?s=' + search_keyword
        print("Webpage:", next_page)
        try:
            service = Service(executable_path=chrome_extension)
            options = webdriver.ChromeOptions()
            driver = webdriver.Chrome(service=service, options=options)
            time.sleep(3)
            driver.get(next_page)
            soup = BeautifulSoup(driver.page_source, "html.parser")
            if soup.find_all('div',class_='mag-box not-found'):
                print("no data found")
                return
            try:
                for link in soup.select('ul li div a'): 
                
                    url1 =link.get('href')
                    if("https://civil.ge/ka/archives/category/" in url1):
                        # print("Fuck you...")
                        continue
                    # print(url1)
                    date=""
                    language = "Georgian" 
                    db_save(url1, date,language, category_name, keyword, search_keyword)
                if start_page_number < end_page_number:
                    start_page_number = start_page_number + 1
                    civil_ge(webpage, start_page_number,end_page_number, category_name, keyword, search_keyword)

                    
            except:
                pass
        except Exception as e:
            print("An exception occurred:", e)

    except Exception as e:
        print("An exception occurred:", e)
      
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
            key = f"{idp} {keyword}"
            webpage = f"https://civil.ge/ka/page/" 
            search_keyword = urllib.parse.quote(key)         
            civil_ge(webpage, start_page_number,end_page_number, category_name, keyword, search_keyword)

print("Search is complete")







   # def print_url(urls):
   #   for key, value in urls.items():
   #     print('Url:',key,'\n')
   #     print('Published Date:',value,'\n')
   #   print(len(urls)) 
   #https://www.kmu.gov.ua/npasearch?&key=ВПО&from=01.02.2010&to=01.02.2023
   #urls = get_orginal_search_link_for_zakon_rada_gov_ua('',0,urls)
#    def print_url(urls):
#       for u in urls:
#       if("https://civil.ge/ka/archives/category/" in u):       
#          urls.remove(u)
#       for u in urls:
#          print(u)
#       print(len(urls))
#    except:
#    pass

# print_url(civil_ge('https://civil.ge/ka/page/',1,data_dict))
# #https://netgazeti.ge/page/2/?s=%E1%83%93%E1%83%94%E1%83%95%E1%83%9C%E1%83%98%E1%83%9A%E1%83%98%E1%83%A1