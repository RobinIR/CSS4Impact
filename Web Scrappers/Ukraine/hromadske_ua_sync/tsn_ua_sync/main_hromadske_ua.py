from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
from selenium import webdriver
import json
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import requests
from selenium.webdriver.common.keys import Keys
import trafilatura
from writeToFiles import write_file
from config import start_page_number,end_page_number, local_drive_path, chrome_extension
# Use the imported variables
# print(page_number)
from  DTO_css4impact_save import db_save
from api_helper_db import api_helper_db
from datetime import datetime
capabilities = DesiredCapabilities.CHROME.copy()

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

capabilities['goog:loggingPrefs'] = {'performance': 'ALL'}

options = webdriver.ChromeOptions()


headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    "Cache-Control": "max-age=0",
    "Cookie": "_ga=GA1.1.1500022979.1686654299; __utmc=114553374; __utmz=114553374.1686654299.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _icl_current_language=uk; __gsas=ID=04d113fe5624e9aa:T=1686654313:RT=1686654313:S=ALNI_MbY7z8rARdaXvMZPPB2NE-D-FpysA; _ga_K1PS8PVHFG=GS1.1.1686734277.2.0.1686734277.60.0.0; __utma=114553374.1500022979.1686654299.1686654299.1686734277.2",
    "Referer": "https://www.helsinki.org.ua/",
    "Sec-Ch-Ua": "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}
options.add_argument("--headless")  # Optional: Run Chrome in headless mode
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument(f"--user-agent={headers['User-Agent']}")
options.add_argument(f"--referer={headers['Referer']}")


def get_status(logs):
    for log in logs:
        if log['message']:
            d = json.loads(log['message'])
            try:
                content_type = 'text/html' in d['message']['params']['response']['headers']['content-type']
                response_received = d['message']['method'] == 'Network.responseReceived'
                if content_type and response_received:
                    return d['message']['params']['response']['status']
            except:
                pass


def hromadske_ua_sync(webpage, start_page_number,end_page_number, category, keyword, search_keyword):
   
  search_url = webpage + search_keyword
  try:
    driver = webdriver.Chrome(executable_path=r"C:\Users\mt_ah\.cache\selenium\chromedriver\win32\108.0.5359.71\chromedriver.exe")
    time.sleep(5)
    driver.get(search_url)
    print("Webpage: ",search_url)
    time.sleep(3)
    resoponse_log =driver.get_log('performance')
    response_code = get_status(resoponse_log)
      # Send GET request to the URL
  except:
      pass
  try:
    response = requests.get(search_url)
  except:
    return
  language = "Ukranian"
  # Check if the request was successful (status code 200)
  if response.status_code == 200:
      # Check the content type of the response
      content_type = response.headers.get("content-type", "").lower()

      if "application/json" in content_type:
          # Parse the JSON response
          data = response.json()

          # Extract the required data from the JSON response
          if data['data']['data'] is not None:
              try:
                
                for item in data['data']['data']:
                    #date = item['created_at'].strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%fZ')
                    article_url = item['slug']
                    date = item["published_at"]["datetime"].split(" ")[0]
                    language = "Ukranian"
                    db_save(article_url, date,language, category, keyword, search_keyword)
              except Exception as e:
                if date is None and url:
                    print("An exception occurred: ", e)

          if "next" in data:
              next_page_url = data["next"]
              if start_page_number <= end_page_number:
                  start_page_number = start_page_number+1
                  hromadske_ua_sync(next_page_url, start_page_number,end_page_number, category, keyword, search_keyword)
      else:
        soup = BeautifulSoup(response.text, features="lxml")
        for link in soup.findAll('div', class_="lineNewsCard"): 
          url = ""
          date = ""
          try:  
            article_url = link.find('a')['href']
            #article_url = article_url['href']
            date = ""#link.find('time').text.strip()
            language = "Ukranian"
            db_save(article_url, date,language, category, keyword, search_keyword)
          except Exception as e:
              if date is None and url:
                  print("An exception occurred: ", e)
        if start_page_number <= end_page_number:
          start_page_number = start_page_number + 1
          find_next_page = soup.find('div', class_='col-md-8 col-lg-6')

          try:
            search_url = find_next_page.find('button')['data-url']
            #search_url = find_next_page.get('data-url')
            hromadske_ua_sync(search_url, start_page_number,end_page_number, category, keyword, search_keyword)
          except Exception as e:
            print("something wrong")
  else:
      print("Request failed with status code:", response.status_code)

category_url = "http://localhost:8000/category/path/Ukranian"
all_category_data = api_helper_db.getCategoryApi(category_url)
for item in all_category_data:
    categoryId = item['id']
    category_name = item['category']
    idps = item['idp']
    keywords = item['keywords']
    # To check it on only for one category. Delete the if condition on final implementation.
   
        
    for idp in idps:
        for keyword in keywords:
            search_keyword = f"{idp} {keyword}"
            webpage = f"https://hromadske.ua/search?q=" 
            start_page_number = start_page_number
            end_page_number = end_page_number             
            
            hromadske_ua_sync(webpage, start_page_number,end_page_number, category_name, keyword, search_keyword)