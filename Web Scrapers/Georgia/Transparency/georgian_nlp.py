import json
import os
import spacy
import config_nlp as config
import requests

idpKeyWordList = []
categoryKeyWordList = []

# Load the Multi language language model
nlp = spacy.load('xx_ent_wiki_sm')

def ner(text):
    doc = nlp(text)
    entities = [(entity.text, entity.label_) for entity in doc.ents]
    return entities

def getKeyWordsList(language, category):
    if(language == "Georgian"):
        response_API = requests.get(config.categoryApi + language)
        try:
            response_API.raise_for_status()
            data = response_API.text
            parse_json = json.loads(data)
            idpKeyWordList = []
            categoryKeyWordList = []
            # Iterate over each item in the list
            for item in parse_json:
                geoCategory = item['category']
                idpKeyWords = item['idp']
                catKeyWords = item['keywords']

                if category == geoCategory:
                    idpKeyWordList = idpKeyWords,
                    categoryKeyWordList = catKeyWords
            return idpKeyWordList, categoryKeyWordList
        except requests.exceptions.RequestException as e:
            print('Error occurred while making the API request:', e)
            return [], []
    else:
        print("Language not Matched")
        return [], []

def georgian_file_sort(directory, language, category):
    idpKeyWordList, categoryKeyWordList = getKeyWordsList(language, category)

    if os.path.isfile(directory):
        # Read the file
        with open(directory, 'r', encoding='utf-8') as file:
            content = file.read()
        entities = ner(content)

        persons = []
        organizations = []
        locations = []
        miscellaneous = []

        for item, entity_type in entities:
            if entity_type == 'PER':
                persons.append(item)
            elif entity_type == 'ORG':
                organizations.append(item)
            elif entity_type == 'LOC':
                locations.append(item)
            elif entity_type == 'MISC':
                miscellaneous.append(item)

        persons = list(set(persons))
        organizations = list(set(organizations))
        locations = list(set(locations))
        miscellaneous = list(set(miscellaneous))

        # Limiting the lists of 10 elements
        
        persons = persons[:config.limit] if len(persons) > config.limit else persons
        organizations = organizations[:config.limit] if len(organizations) > config.limit else organizations
        locations = locations[:config.limit] if len(locations) > config.limit else locations
        miscellaneous = miscellaneous[:config.limit] if len(miscellaneous) > config.limit else miscellaneous

        # Count the number of times each keyword appears in the file for each list
        idpKeyWordsCounts = {keyword: content.lower().count(keyword) for keyword in idpKeyWordList[0]}
        categoryKeyWordsCounts = {keyword: content.lower().count(keyword) for keyword in categoryKeyWordList}

        # Get the list of counted keywords for each list without duplicates and with counts greater than 0
        idpKeyWordsCountedList = [keyword for keyword in set(idpKeyWordsCounts.keys()) if idpKeyWordsCounts[keyword] > 0]
        categoryKeyWordsCountedList = [keyword for keyword in set(categoryKeyWordsCounts.keys()) if categoryKeyWordsCounts[keyword] > 0]

        # Calculate the weighted keyword counts for the file
        weighted_counts = {
            keyword: config.IDPsWeight * idpKeyWordsCounts.get(keyword, 0) + config.CatWeight * categoryKeyWordsCounts.get(keyword, 0)
            for keyword in set(idpKeyWordList[0] + categoryKeyWordList)
        }
        totalWeightedCounts = sum(weighted_counts.values())
        idpTotalValue = sum(idpKeyWordsCounts.values())
        categoryTotalValue = sum(categoryKeyWordsCounts.values())
        if idpTotalValue == 0 or categoryTotalValue == 0:
            totalPriorityValue = float(0)
        else:
            totalPriorityValue = float(f'{totalWeightedCounts:.2f}')
        
        # print('Directory:', directory)
        # print('Language:', language)
        # print('Category:', category)
        # print('IDP Keywords:', idpKeyWordsCountedList)
        # print('Category Keywords:', categoryKeyWordsCountedList)
        # print('Persons:', persons)
        # print('Organizations:', organizations)
        # print('Locations:', locations)
        # print('Miscellaneous:', miscellaneous)
        # print('Total Priority Value:', totalPriorityValue)
        # print('---------------------')

        return totalPriorityValue, persons, locations, idpKeyWordsCountedList, categoryKeyWordsCountedList, organizations
    
    else:
        print('File not found.')
