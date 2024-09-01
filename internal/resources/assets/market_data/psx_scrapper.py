import requests
from bs4 import BeautifulSoup


class PSXScrapper:
    def __init__(self, url):
        self.page = requests.get(url)
        self.soup = BeautifulSoup(self.page.content, 'html.parser')

    def check_response(self, status_code=200):
        """Check if the response is successful."""
        if self.page.status_code != status_code:
            return False
        return True

    def extract_tag(self, tag_name, item=None):
        """Helper method to extract text from a given tag within an item."""
        if item:
            tag = item.find(tag_name)
        else:
            tag = self.soup.find(tag_name)
        return tag.text.strip() if tag else None

    def extract_element(self, tag_name, class_name=None, item=None):
        """Extract an element from a BeautifulSoup object."""
        extract = self.soup
        if item:
            extract = item

        if class_name:
            element = extract.find(tag_name, class_=class_name)
        else:
            element = extract.find(tag_name)

        return element

    @staticmethod
    def parse_key_people(item):
        """Helper method to parse the key people table."""
        key_people_data = []
        key_people_table = item.find('table', class_='tbl')

        if key_people_table:
            key_people_rows = key_people_table.find('tbody', class_='tbl__body').find_all('tr')
            for row in key_people_rows:
                row_data = row.findAll('td')
                if len(row_data) < 2:
                    continue
                name = row_data[0].text.strip()
                designation = row_data[1].text.strip()
                key_people_data.append({
                    'name': name,
                    'designation': designation
                })

        return key_people_data

    @staticmethod
    def extract_fiscal_year_end(item):
        """Helper method to extract the fiscal year end information."""
        fiscal_year_end = item.find('div', class_='item__head').find_next_sibling('p')
        return fiscal_year_end.text.strip() if fiscal_year_end else None

    def extract_text(self, item, tag_name, class_name=None):
        """Extract text from a given tag within a BeautifulSoup object."""
        if class_name:
            element = item.find(tag_name, class_=class_name)
        else:
            element = item.find(tag_name)
        return element.text.strip() if element else None

    def extract_stats(self):
        """Helper function to extract stats from a BeautifulSoup object."""
        stats = {}
        stats_divs = self.soup.find_all('div', class_='stats_item')
        for stat in stats_divs:
            label = stat.find('div', class_='stats_label')
            value = stat.find('div', class_='stats_value')
            if label and value:
                stats[label.text.strip()] = value.text.strip()
        return stats

    def extract_stat_value(self, label_text):
        """Helper function to extract specific stat value based on the label text."""
        stat_item = self.soup.find('div', text=label_text)
        if stat_item:
            value = stat_item.find_next_sibling('div', class_='stats_value')
            return value.text.strip() if value else None
        return None
