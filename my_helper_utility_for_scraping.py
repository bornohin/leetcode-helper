import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import streamlit as st

def scrape_links(url):
    # Send request to the URL
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
            if url and 'https://leetcode.com/problems' in url:
                # Add the data to the list
                link_data.append({'text': text, 'url': url})

        # Create a DataFrame from the list
        df = pd.DataFrame(link_data)

        # Return the DataFrame
        return df

    # If the request was not successful, return None
    else:
        return None

def check_csv(file_name):# Check if the file exists
    full_dir = 'data/' + file_name
    if os.path.isfile(full_dir):
        # st.write(f"CSV file '{file_name}' already exists.")
        print('file exists')
    else:
        # Run function to create the CSV file
        # create_csv(file_name)
        # st.write(f"CSV file '{file_name}' created successfully.")
        print('no file')

check_csv('movie_medata.csv')