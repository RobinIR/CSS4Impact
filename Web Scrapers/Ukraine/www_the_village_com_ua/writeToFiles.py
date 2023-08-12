import os
import unicodedata
import string
from config import local_drive_path

def encode_filename(filename):
   # print("Original article title:", filename)
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    #print(" valid_chars article title:", valid_chars)
    sanitized_filename = unicodedata.normalize('NFKD', filename)
    #print(" sanitized_filename article title:", sanitized_filename)
    #sanitized_filename1 = ''.join(c for c in sanitized_filename if c in valid_chars)
    #print(" sanitized_filename_1 article title:", sanitized_filename1)
    return sanitized_filename
def truncate_filename(filename):
    max_length = 106
    if len(filename) <= max_length: # Max length is 106 characters
        return filename
    else:
        truncated_filename = filename[:max_length - 3] + "..."
        return truncated_filename

def write_file(category, keyword, article_title, text, date, url, language):
    #print("Original article title:", article_title)
    directory = os.path.join(local_drive_path, 'CSS4Impact_Articles', language)
    category_subfolder = encode_filename(category)
    keyword_subfolder = encode_filename(keyword)
    article_title = encode_filename(article_title)
    #print("Article Title:", article_title)
    filename = f"{truncate_filename(article_title)}.txt"
   # print("Filename:", filename)

    subfolder_path = os.path.join(directory, category_subfolder, keyword_subfolder)
    file_path = os.path.join(subfolder_path, filename)

    os.makedirs(subfolder_path, exist_ok=True)

    if os.path.isfile(file_path):
        print("File already exists")
        return None

    try:
        with open(file_path, 'a', encoding="utf-8") as f:
            f.write(f"Title: {article_title}\n")
            f.write(f"Date: {date}\n")
            f.write(f"URL: {url}\n")
            f.write(f"\n{text}\n")

        file_size = os.path.getsize(file_path)
        if file_size < 3 * 1024:
            os.remove(file_path)
            return None

        return file_path

    except OSError as e:
        print(f"OS Error: {e}")
        return None
    