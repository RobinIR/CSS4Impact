# Web Scraper

This is a web scraper project that extracts information from various websites. It is built to scrape data from specific websites and perform tasks such as text and date extraction and natural language processing.
___

# Installation

- Clone this repository and open it in your preferred IDE (e.g., VS Code).

- Install Python on your system from python.org.

- Open the terminal or command prompt and navigate to the project directory.


# Installation Commands for Windows:

1. Open the terminal and Install all requirements

```
 pip install -r requirements.txt
``` 
or

```
 pip install beautifulsoup4 requests trafilatura selenium spacy
```   
2. Install spacy libraries for differnt languages
- Azerbaijani and Georgian
```
 python -m spacy download xx_ent_wiki_sm
```   
- Ukraine
```
 python -m spacy download uk_core_news_lg
```    
3. Ready to run your script
```
 python your_scripts.py
```   
___

# Installation Commands for Windows Using Virtual Environment:
1. Install Virtural Environment 
```
python -m venv ./venv
```
2. Activate Virtual Environment
```
.\venv\Scripts\activate 
```
3. Install all requirements
```
 python -m pip install -r requirements.txt 
```   
4. Install spacy library for differnt languages
- Azerbaijani and Georgian
```
 python -m spacy download xx_ent_wiki_sm
```   
- Ukraine
```
 python -m spacy download uk_core_news_lg
```  

5. Change the required directory where script exists
```
 cd required/path/
```   
6. Ready to run your script
```
 python your_scripts.py
```   
___

# Installation Commands for Mac:

1. Install Python using Brew (If python is not already installed)
```
brew install python 
```
2. Install Virtural Environment 
```
python3 -m venv ./venv
```
3. Activate Virtual Environment
```
source venv/bin/activate
```
4. Install all requirements
```
 pip install -r requirements.txt
```   
5. Install spacy library for differnt languages
- Azerbaijani and Georgian
```
 python3 -m spacy download xx_ent_wiki_sm
```   
- Ukraine
```
 python3 -m spacy download uk_core_news_lg
```  
6. Change the required directory where script exists
```
 cd required/path/
```   
7. Ready to run your script
```
 python3 your_scripts.py
```   
