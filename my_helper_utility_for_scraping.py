import requests
from bs4 import BeautifulSoup
import pandas as pd

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


