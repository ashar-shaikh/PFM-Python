import datetime
import requests
from bs4 import BeautifulSoup

from .psx_scrapper import PSXScrapper

# Constants
psxHost = "https://www.psx.com.pk"
dpsHost = "https://dps.psx.com.pk/company/"
marketSummaryEndpoint = "/market-summary"


class PSXData:
    def __init__(self):
        self.PSXScrapper = None

    def get_company_data(self, symbol):
        # Call get Company Page
        is_true, error = self.get_company_page(symbol)
        if not is_true:
            return None, error

        # Parse the company profile
        company_data, error = self.parse_company_profile()
        if error:
            return None, error
        # Extract company info
        company_info, error = self.extract_company_info()
        if error:
            return None, error
        # Combine the data
        company_data.update(company_info)
        return company_data, None

    def get_company_page(self, symbol):
        self.PSXScrapper = PSXScrapper(dpsHost + symbol)
        if not self.PSXScrapper.check_response():
            return False, "Failed to retrieve the page"
        return True, None

    def extract_company_info(self):
        """Extract company data from HTML content."""
        try:
            data = self.PSXScrapper.extract_element('div', 'company__quote')
            # Extracting company data using helper function
            company_info = {
                'Company Name': self.PSXScrapper.extract_text(data, 'div', 'quote__name'),
                'Sector': self.PSXScrapper.extract_text(data, 'div', 'quote__sector'),
                'Price': self.PSXScrapper.extract_text(data, 'div', 'quote__close'),
                'Price Change Value': self.PSXScrapper.extract_text(data, 'div', 'change__value'),
                'Price Change Percent': self.PSXScrapper.extract_text(data, 'div', 'change__percent'),
                'Quote Date': self.PSXScrapper.extract_text(data, 'div', 'quote__date'),
                'Stats': self.PSXScrapper.extract_stats()
            }

            # Check for missing data
            missing_data = [key for key, value in company_info.items() if value is None]
            if missing_data:
                return company_info, f"Missing data for: {', '.join(missing_data)}"

            return company_info, None
        except Exception as e:
            return None, str(e)

    def parse_company_profile(self):
        """Parse the company profile page and extract the company data."""
        try:
            company_data = {}

            # Find the company profile section
            company_profile = self.PSXScrapper.soup.find('div', class_='company__profile')
            if not company_profile:
                return None, "Company profile section not found"

            # Find all profile items
            profile_items = company_profile.find_all('div', class_='profile__item')
            if not profile_items:
                return None, "No profile items found in the company profile section"

            # Parse each profile item
            for item in profile_items:
                item_head = self.PSXScrapper.extract_text(item, 'div', 'item__head')

                if item_head == "BUSINESS DESCRIPTION":
                    company_data['description'] = self.PSXScrapper.extract_text(item, 'p')

                elif item_head == "KEY PEOPLE":
                    company_data['key_people'] = self.PSXScrapper.parse_key_people(item)

                elif item_head == "ADDRESS":
                    company_data['address'] = self.PSXScrapper.extract_text(item, 'p')

                elif item_head == "WEBSITE":
                    company_data['website'] = self.PSXScrapper.extract_text(item, 'a')

                elif item_head == "REGISTRAR":
                    company_data['registrar'] = self.PSXScrapper.extract_text(item, 'p')

                elif item_head == "AUDITOR":
                    company_data['auditor'] = self.PSXScrapper.extract_text(item, 'p')
                    company_data['fiscal_year_end'] = self.PSXScrapper.extract_fiscal_year_end(item)

            return company_data, None

        except Exception as e:
            return None, str(e)

    @staticmethod
    def get_market_summary_data():
        response = requests.get(psxHost + marketSummaryEndpoint)
        # Check if the request was successful
        if response.status_code != 200:
            print(
                f"Failed to retrieve the page. Status code: {response.status_code}"
            )
            return None
        return response

    @staticmethod
    def parse_all_stock_data(response):
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the table elements with the class "table-responsive"
        tables = soup.findAll('table')

        # Stock Data
        stock_data = {}
        # Loop through the tables and extract the data
        for table in tables:
            # Find all the rows in the table
            rows = table.findAll('tr')
            for row in rows:
                # Find all the cells in the row
                cells = row.findAll('td')
                # Check if there are at least eight cells
                if len(cells) >= 8:
                    # Extract the stock symbol from the attribute of the first cell
                    stock_symbol = cells[0].get('data-srip', '').strip()
                    # Extract the other data fields
                    ldcp = cells[1].text.strip()
                    open_price = cells[2].text.strip()
                    high = cells[3].text.strip()
                    low = cells[4].text.strip()
                    current = cells[5].text.strip()
                    change = cells[6].text.strip()
                    volume = cells[7].text.strip()

                    if stock_symbol:
                        # Add the Stock Data to the dictionary
                        stock_data[stock_symbol] = {
                            'LDCP': ldcp,
                            'OPEN': open_price,
                            'HIGH': high,
                            'LOW': low,
                            'CURRENT': current,
                            'CHANGE': change,
                            'VOLUME': volume
                        }

        return stock_data

    def get_market_summary(self):
        response = self.get_market_summary_data()
        if response:
            parsed_stock_data = self.parse_all_stock_data(response)
            # Respond with current time
            final_resp = {
                "date": datetime.datetime.now().timestamp(),
                "data": parsed_stock_data
            }
            return final_resp
        else:
            return None
