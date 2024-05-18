import urllib.request
from bs4 import BeautifulSoup
import json

class webScraper():
    def __init__(self, website):
        self.website = website
    
    def webScrape(self, output_file):
        article_count = 0
        results = []
        
        readSite = urllib.request.urlopen(self.website)
        html = readSite.read()
        parser = 'html.parser'
        sp = BeautifulSoup(html, parser)

        for tag in sp.find_all('a'):
            url = tag.get('href')
            if url is None:
                continue
            elif 'knicks' in url or 'jalen' in url:
                if url not in results:
                    results.append(url)
                    article_count += 1
                    if article_count >= 5:
                        break
        
        # Save results to JSON file
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=4)

# Define the output file path
output_file_path = 'scraped_results.json'

# Scrape the website and save results to JSON file
news = "https://www.nba.com/news"
webScraper(news).webScrape(output_file_path)
