
import json
import requests
# from writeToFiles import WriteToFile
from config import start_page_number, local_drive_path, chrome_extension


class api_helper_db:
    def postApiFuction(payload,url):
        # Define the URL of the API endpoint
        # Define the payload (data to be sent to the API)


        # Convert the payload to JSON format
        json_payload = json.dumps(payload)

        # Define the headers (if necessary)
        headers = {
            'Content-Type': 'application/json'
        }

        # Make the POST request
        response = requests.get(url, headers=headers, data=json_payload)

        # Make the POST request
        response = requests.post(url, headers=headers, data=json_payload)

        # Check the response status code
        if response.status_code == 200:
            # Success! Print the response content
            # print(response.content)
            print("Data found, Db integrated")
        else:
            # Error! Print the response status code and reason
            # print(f"Error: {response.status_code} - {response.reason}")
            print("DB error!")

    def getCategoryApi(url):
        # Define the headers (if necessary)
        headers = {
            'Content-Type': 'application/json'
        }

        # Make the GET request
        response = requests.get(url, headers=headers)

        # Check the response status code
        if response.status_code == 200:
            # Success! Print the response content
            return response.json()
        else:
            # Error! Print the response status code and reason
            # print(f"Error: {response.status_code} - {response.reason}")
            print("Db Insertion Error!")