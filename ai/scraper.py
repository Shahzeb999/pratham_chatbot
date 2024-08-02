
import requests
from bs4 import BeautifulSoup
import pandas as pd

class PrathamScraper:
    def __init__(self, base_url):
        self.base_url = base_url

    def scrape(self):
        # Example function to scrape data
        response = requests.get(self.base_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Example: Extract headings and paragraphs
        headings = [h.text.strip() for h in soup.find_all('h1')]
        paragraphs = [p.text.strip() for p in soup.find_all('p')]
        
        # Combine into a DataFrame
        data = pd.DataFrame({
            'heading': headings,
            'paragraph': paragraphs
        })
        
        return data

def create_knowledge_base(scraper):
    # Scrape and process the data
    data = scraper.scrape()
    
    # Example processing: concatenate headings and paragraphs
    data['content'] = data['heading'] + '. ' + data['paragraph']
    
    # Return as a dictionary
    knowledge_base = data['content'].to_dict()
    return knowledge_base

# Example usage:
# scraper = PrathamScraper('https://www.pratham.org/')
# knowledge_base = create_knowledge_base(scraper)
# print(knowledge_base)
