import os
import requests
from bs4 import BeautifulSoup
import pandas as pd

def check_csv(file_name):# Check if the file exists
    full_path = 'data/' + file_name
    return os.path.isfile(full_path)

def gen_csv_name(file_name):
    file_name = file_name.split(" ")
    file_name = 'data/' + ''.join(x.lower() for x in file_name) + '.csv'
    return file_name

def scrape_links(page, topic_match, file_name):
    # First check if the file exists
    # File_path
    full_path = 'data/' + file_name
    if check_csv(file_name):
        df = pd.read_csv('data/' + file_name)
        return df

    # Only create a new csv file if it doesnt exist.
    # This is the main root url of interest.
    root_url = "https://www.techinterviewhandbook.org/"

    # Convert url to navigate to a certain page. Ex. "coding-interview-study-plan/"
    url = root_url + page
    response = requests.get(url)

    # If the request was successful (status code 200), parse the HTML content
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all hyperlink tags (<a> tags)
        links = soup.find_all('a')

        # Initialize an empty list to store links
        link_data = []

        # Loop through each hyperlink tag
        for link in links:
            # Extract the text of the hyperlink (displayed text)
            text = link.text.strip()

            # Extract the URL of the hyperlink (href attribute)
            url = link.get('href')

            # Check if the URL contains the string 'https://leetcode.com/problems'
            if url and topic_match in url:
                # Add the data to the list
                link_data.append({'text': text, 'url': url})

        # Create a DataFrame from the list
        df = pd.DataFrame(link_data)

        # Reset index to 1 instead of 0
        df.index = df.index + 1

        # Save the file
        df.to_csv(full_path, index=False)
        return df
    else:
        return None

def fetch_topic(csv_file):
    if check_csv(csv_file):
        df = pd.read_csv('data/' + csv_file)
    else:
        page = "coding-interview-study-plan/"
        topic_match = "algorithms/"
        full_path = 'data/' + csv_file
        df = scrape_links(page, topic_match, 'topics.csv')
        df = df.rename(columns={"text": "Topic"})
        df["url"] = "https://www.techinterviewhandbook.org" + df["url"]
        df["file_name"] = df["Topic"].apply(gen_csv_name)
        df.to_csv(full_path, index=False)
    return df
