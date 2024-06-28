import datetime

import requests
from bs4 import BeautifulSoup

marketSummaryURL = "https://www.psx.com.pk/market-summary/"


def get_market_summary_data():
    response = requests.get(marketSummaryURL)
    # Check if the request was successful
    if response.status_code != 200:
        print(
            f"Failed to retrieve the page. Status code: {response.status_code}"
        )
        return None
    return response


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


def get_market_summary():
    response = get_market_summary_data()
    if response:
        parsed_stock_data = parse_all_stock_data(response)
        # Respond with current time
        final_resp = {
            "success": True,
            "date": datetime.datetime.now().timestamp(),
            "data": parsed_stock_data
        }
        return final_resp
    else:
        return None
