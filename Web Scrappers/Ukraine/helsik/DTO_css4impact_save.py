import trafilatura
import json
from writeToFiles import write_file
from api_helper_db import api_helper_db
import time
from datetime import datetime
import ukrain_nlp



def db_save(url, date, language, category, keyword, search_keyword):
    db_category = category
    #print("Testing data for save:",url," ", date," language: ", category, " Keyword: ", search_keyword, " Search keyword: ")
    docs = trafilatura.fetch_url(url)
    if docs is not None:
        show = trafilatura.extract(docs, output_format='json', include_links=True) 
        # print(show)
        if show is not None:
            dict = json.loads(show)
            text = dict["raw_text"]
            title = dict["title"]
            

# Get the current timestamp
            timestamp = datetime.timestamp(datetime.now())
            title = title+str(timestamp)
            # print("Date: ",date, title)
            t_date = dict["date"]
            #time.sleep(3)  
            # DB code goes here
            # Payload
            #language = "Uka"
           # print("Ahmed_buging: ",title)
            #print("Testing data for save:",url," ", date," language: ", category, " Keyword: ", search_keyword, " Search keyword: ")
        
            file_path = write_file(db_category,keyword,date,text, t_date, url, language)
            if file_path is None:
                return ## error line

            #NLP
            totalPriorityValue, persons, locations, idpKeywordSimilarityList, categoryKeywordSimilarityList, organizations = ukrain_nlp.ukarian_file_sort(file_path, language, category)
            payload = {
                "title": title,
                "DatePublication": date,
                "Language": language,
                "Priority": totalPriorityValue,
                "Url": url,
                "Actors": persons,
                "Location": locations,
                "Organizations": organizations,
                "IDPMatchedKeywords": idpKeywordSimilarityList,
                "CatagoryMatchedKeywords": categoryKeywordSimilarityList,
                "LocalPath": file_path,
                "KeyWords": [keyword],
                "Category": [category]
            }
            api_helper_db.postApiFuction(payload, 'http://localhost:8000/collection') ##error line
