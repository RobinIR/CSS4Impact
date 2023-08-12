import json
import os
import spacy
import config_nlp as config
import requests

idpKeyWordList = []
categoryKeyWordList = []

# Load the Ukrainian language model
nlp = spacy.load('uk_core_news_lg')


def ner(text):
    doc = nlp(text)
    entities = [(entity.text, entity.label_) for entity in doc.ents]
    return entities


def getKeyWordsList(language, category):
    if(language == "Ukranian"):
        response_API = requests.get(config.categoryApi + language)
        try:
            response_API.raise_for_status()
            data = response_API.text
            parse_json = json.loads(data)
            idpKeyWordList = []
            categoryKeyWordList = []
            # Iterate over each item in the list
            for item in parse_json:
                ukrCategory = item['category']
                idpKeyWords = item['idp']
                catKeyWords = item['keywords']

                if category == ukrCategory:
                    idpKeyWordList = idpKeyWords,
                    categoryKeyWordList = catKeyWords
            return idpKeyWordList, categoryKeyWordList
        except requests.exceptions.RequestException as e:
            print('Error occurred while making the API request:', e)
            return [], []
    else:
        print("Language not Matched")
        return [], []


def ukarian_file_sort(directory, language, category):
    idpKeyWordList, categoryKeyWordList = getKeyWordsList(language, category)

    # Extract the filename with the .txt extension from the directory path
    #filename = os.path.splitext(os.path.basename(directory))[0] + '.txt'

    if os.path.isfile(directory):
        # Read the file
        with open(directory, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Extract entities using NER
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

        # Calculate the similarity between content keywords and IDP keywords
        idpKeywordSimilarity = {keyword: max([nlp(keyword).similarity(nlp(entity)) for entity, _ in entities]) for keyword in idpKeyWordList[0]}
        idpKeywordSimilarityList = [keyword for keyword, similarity in idpKeywordSimilarity.items() if similarity > 0]

        # Calculate the similarity between content keywords and category keywords
        categoryKeywordSimilarity = {keyword: max([nlp(keyword).similarity(nlp(entity)) for entity, _ in entities]) for keyword in categoryKeyWordList}
        categoryKeywordSimilarityList = [keyword for keyword, similarity in categoryKeywordSimilarity.items() if similarity > 0]

        # Calculate the weighted keyword counts for the file based on similarity
        weighted_counts = {
            keyword: config.IDPsWeight * idpKeywordSimilarity.get(keyword, 0) + config.CatWeight * categoryKeywordSimilarity.get(keyword, 0)
            for keyword in set(idpKeyWordList[0] + categoryKeyWordList)
        }
        totalWeightedCounts = sum(weighted_counts.values())
        idpTotalValue = sum(idpKeywordSimilarity.values())
        categoryTotalValue = sum(categoryKeywordSimilarity.values())
        if idpTotalValue == 0 or categoryTotalValue == 0:
            totalPriorityValue = float(0)
        else:
            totalPriorityValue = float(f'{totalWeightedCounts:.2f}')

        # print('ID: ', id)
        # print('Directory:', directory)
        # print('Language:', language)
        # print('Category:', category)
        # print('IDP Keywords:', idpKeywordSimilarityList)
        # print('Category Keywords:', categoryKeywordSimilarityList)
        # print('Persons:', persons)
        # print('Organizations:', organizations)
        # print('Locations:', locations)
        # print('Miscellaneous:', miscellaneous)
        # print('Total Priority Value:', totalPriorityValue)
        # print('---------------------')

        return totalPriorityValue, persons, locations, idpKeywordSimilarityList, categoryKeywordSimilarityList, organizations
    else:
        print('File not found.')