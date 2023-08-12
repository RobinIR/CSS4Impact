import os
import unicodedata
from config import local_drive_path

def encode_filename(filename):
    nfkd_form = unicodedata.normalize('NFKD', filename)
    return nfkd_form.encode('ASCII', 'ignore').decode('utf-8')

def replace_invalid_chars(filename):
    invalid_chars = r'<>:"/\|?*'
    filename = "".join([c if c.isalnum() or c.isspace() or c not in invalid_chars else "_" for c in filename])
    return filename

def truncate_filename(filename):
    max_length = 70
    if len(filename) <= max_length: # Max length is 106 characters
        return filename
    else:
        truncated_filename = filename[:max_length - 3] + "..."
        return truncated_filename

def write_file(category, keyword, article_title, text, date, url, language):
    try:
        directory = os.path.join(local_drive_path, 'CSS4Impact_Articles', language)
        category_subfolder = encode_filename(category)
        keyword_subfolder =  encode_filename(keyword)
        article_title = encode_filename(article_title)
        article_title = replace_invalid_chars(article_title)
        filename = f"{truncate_filename(article_title)}.txt"

        subfolder_path = os.path.join(directory, category_subfolder, keyword_subfolder)
        file_path = os.path.join(subfolder_path, filename)

        # Create directories if they don't exist
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

            # Check file size
            # file_size = os.path.getsize(file_path)
            # if file_size < 3 * 1024:  # Check if file size is less than or equal to 3KB (3 * 1024 bytes)
            #     os.remove(file_path)
            #     print("Removed smaller file less than 3KB")
            #     return None

            return file_path

        except OSError as e:
            print(f"OS Error: {e}")
            return None

    except Exception as e:
        print(f"Error: {e}")
        return None
