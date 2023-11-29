import scrapy
from urllib.parse import urlsplit
from urllib.parse import quote

class TextScraperSpider(scrapy.Spider):
    name = 'cohere'
    # Define the allowed website domains to scrape
    allowed_domains = ['uwaterloo.ca', 'cs.uwaterloo.ca']
    #, 'uwaterloo.atlassian.net'
    start_urls = ['https://uwaterloo.ca/quest/', 'https://cs.uwaterloo.ca/cscf/']
    #, 'https://uwaterloo.atlassian.net/wiki/spaces/ISTKB/', 'https://uwaterloo.atlassian.net/wiki/spaces/ISTSERV/'
    # Define the allowed relative paths
    allowed_paths = ['/quest', '/cscf']
    #, '/wiki/spaces/ISTKB/', '/wiki/spaces/ISTSERV/'

    def parse(self, response):
        # Check if the current URL path is allowed
        parsed_url = urlsplit(response.url)
        if any(parsed_url.path.startswith(path) for path in self.allowed_paths):
            # Extract text and save it to a file
            #filename = f'crawl.txt'
            sanitized_url = quote(response.url, safe='')
            filename = ''.join(char for char in sanitized_url if char.isalnum() or char in ('-', '_'))
            with open(filename, 'a', encoding='utf-8') as file:
                # Extracting text from the webpage
                text = response.css('body ::text').extract()
                text = ' '.join(text)
                #text=response.url+'\n'
                # Writing the extracted text to a file
                file.write(text)

            self.log(f'Saved file {filename}')

            # Follow links within the allowed paths
            for next_page in response.css('a::attr(href)').extract():
                next_page_parsed_url = urlsplit(next_page)
                if any(next_page_parsed_url.path.startswith(path) for path in self.allowed_paths):
                    yield scrapy.Request(response.urljoin(next_page), callback=self.parse)
        else:
            self.log(f'Skipping URL {response.url} as it is not in the allowed paths')