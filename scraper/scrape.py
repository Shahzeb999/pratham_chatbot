import requests
from bs4 import BeautifulSoup

def scrape_pratham():
    # URLs to scrape
    sections_to_scrape = {
        "About Us": "https://pratham.org/about/",
        "Programs": "https://pratham.org/programs/",
        "Get Involved": "https://pratham.org/get-involved/"
    }

    # Initialize a dictionary to store section content
    content = {}

    # Scrape each section
    for section_name, section_url in sections_to_scrape.items():
        print(f"Scraping section: {section_name}")
        section_response = requests.get(section_url)
        if section_response.status_code == 200:
            section_soup = BeautifulSoup(section_response.content, 'html.parser')
            # Extract the main content area (adjust class as needed)
            main_content = section_soup.find('div', {'class': 'entry-content'})
            if main_content:
                section_text = main_content.get_text(separator=' ', strip=True)
                content[section_name] = section_text
            else:
                print(f"Main content not found for {section_name}.")
        else:
            print(f"Failed to access section {section_name}. Status code: {section_response.status_code}")
    
    return content

if __name__ == '__main__':
    # Run scraper standalone for testing
    content = scrape_pratham()
    for section, text in content.items():
        print(f"\n{section}:\n{text[:500]}...")  # Print first 500 characters for brevity
