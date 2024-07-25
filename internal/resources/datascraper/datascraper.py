import requests
from bs4 import BeautifulSoup
import time
import re
import random
from lxml.html.clean import Cleaner
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from readability import Document

class DataScraper:
    def __init__(self):
        pass

    def fetch_data(self, links, ids):
        """
        Fetch data from the given links and map them to the corresponding ids.

        :param links: List of URLs to fetch data from.
        :param ids: List of IDs corresponding to each link.
        :return: Dictionary with ids as keys and fetched data as values.
        """
        data = {}
        for i, link in enumerate(links):
            try:
                url, content= self.get_original_content(link)
                data[ids[i]] = self.clean_data(content)
                time.sleep(5)
            except requests.RequestException as e:
                print(f"Error fetching data from {link}: {e}")
                data[ids[i]] = None
        return data

    def clean_data(self, raw_data):
        """
        Clean the fetched data by removing unnecessary parts such as header, footer, ads, HTML tags,
        special characters, and unwanted text using BeautifulSoup and readability.

        :param raw_data: Raw HTML data as a string.
        :return: Cleaned text data.
        """
        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(raw_data, 'html.parser')

        # Remove unwanted tags
        for element in soup(['script', 'style', 'header', 'footer', 'nav', 'aside', 'form', 'iframe']):
            element.decompose()

        # Remove elements with certain classes or ids (common for ads, pop-ups, etc.)
        for element in soup.find_all(class_=re.compile('ad|banner|popup|footer|header|donations', re.IGNORECASE)):
            element.decompose()
        for element in soup.find_all(id=re.compile('ad|banner|popup|footer|header|donations', re.IGNORECASE)):
            element.decompose()

        # Extract the main content by targeting specific tags
        main_content = []
        for tag in soup.find_all(['p', 'div', 'article']):
            main_content.append(str(tag))

        cleaned_html_org = str(soup)
        # Combine the extracted tags into a single HTML string
        cleaned_html = ' '.join(main_content)
        cleaned_html = cleaned_html_org + ' '
        # Use readability to extract the main content from the cleaned HTML
        doc = Document(cleaned_html)
        content = doc.summary()

        # Parse the extracted content with BeautifulSoup for final cleanup
        soup = BeautifulSoup(content, 'html.parser')
        cleantext = soup.get_text(separator=' ')

        # Remove special characters and extra spaces
        cleantext = re.sub(r'\s+', ' ', cleantext)  # Replace multiple spaces with a single space
        cleantext = re.sub(r'[^A-Za-z0-9 .,;?!-]', '',
                           cleantext)  # Remove non-alphanumeric characters except punctuation

        # Remove duplicate sentences
        sentences = cleantext.split('.')
        unique_sentences = []
        seen_sentences = set()
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence and sentence not in seen_sentences:
                unique_sentences.append(sentence)
                seen_sentences.add(sentence)
        cleantext = '. '.join(unique_sentences) + '.'

        return cleantext.strip()


    def get_original_content(self, rss_url, timeout=2, headless=True):
        # Random User-Agent
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        ]
        user_agent = random.choice(user_agents)

        # Set up Chrome options
        chrome_options = Options()
        chrome_options.add_argument(f"user-agent={user_agent}")
        if headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        # Initialize the WebDriver
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

        try:
            # Access the RSS URL
            driver.get(rss_url)

            # Wait for the redirect by checking if the URL changes
            time.sleep(timeout)
            # Wait for an element that indicates the page has fully loaded
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.TAG_NAME, 'body'))
            )
            # Fetch the final URL
            current_url = driver.current_url

            content = driver.page_source
        finally:
            # Close the driver
            driver.quit()

        return current_url, content