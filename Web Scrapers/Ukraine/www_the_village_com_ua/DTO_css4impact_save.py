import trafilatura
import json
from writeToFiles import write_file
from api_helper_db import api_helper_db
import time
import ukrain_nlp


def db_save(url, date, language, category, keyword, search_keyword):
    db_category = category
    docs = trafilatura.fetch_url(url)
    if docs is not None:

        show = trafilatura.extract(docs, output_format='json', include_links=True) 
        
        if show is not None:
            dict = json.loads(show)
            #print(dict)
            text = dict["raw_text"]
            title = dict["title"]
            file_path = write_file(db_category,keyword,title,text, date, url, language)
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
