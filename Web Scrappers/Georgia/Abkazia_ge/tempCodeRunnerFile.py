category_url = "http://localhost:8000/category/path/Georgian"
# all_category_data = api_helper_db.getCategoryApi(category_url)
# for item in all_category_data:
#     categoryId = item['id']
#     category_name = item['category']
#     idps = item['idp']
#     keywords = item['keywords']
#     # To check it on only for one category. Delete the if condition on final implementation.

#     for idp in idps:
#         for keyword in keywords:
#             key = f"{idp} {keyword}"
#             webpage = f"http://www.abkhazia.gov.ge/liveSearch" 
#             search_keyword = urllib.parse.quote(key)            
#             abkhazia(webpage, start_page_number,end_page_number, category_name, keyword, search_keyword)
# print("Search is complete")