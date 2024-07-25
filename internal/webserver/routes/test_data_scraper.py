from flask import Blueprint, jsonify, request
import internal.resources.datascraper as ds

endpoint = 'data-scraper'
data_scraper_bp = Blueprint(endpoint, __name__)


@data_scraper_bp.route('/' + endpoint, methods=['GET'])
def data_scraper():
    parameter_data = request.args
    scraper = ds.new_data_scraper()

    links = [
        "https://news.google.com/rss/articles/CBMikAFBVV95cUxNZzZTczdUdERnWWNlR0E3eWo2WEhXaXRCQUZVTzJGQ3hzY2VCdDhNZTI4RVJSSUZmaWZRdlhiSnBoX21ZNDl5YVdTMnR5M0kyN3JrWjdwUG5oSXRFYzI3Q1piUVRFVHZseUZSbm14U0JTMlZNVVVoVV93elA0em5lVW1sSklXYl82TkFmSl9YVTA?oc=5",
        "https://news.google.com/rss/articles/CBMisAFBVV95cUxQMUxGR2ZnZURCR3YxbERTZzdFLWVhb1dCSThvZ3VuYl92cmhDWEpDOFBVU3RLcTJRaERXWEtIU1R5dWVLdjBLZFZKaXpvNG5yNWdzbC0tbGRqMG1mUm1HeXRoLXpURG55V1NRcFRIWXdLT0VndWoxWnFzYVhqUHl6c0p0VFlJUlNsZFhfdEJsNUYzT1dPVWEtU2ZnQVJoNE1ETUtyX2Ffa3Fxdk94MWpycdIBtgFBVV95cUxPdFVyODNFZkE2dmxhdHB5UjV1QjJmdFR4TXRLN25jMjZReE96a3RGaUdfNFVRcXNtOFA4RlVTOVZwempyVWYyOGxsMVo5ZVU1c241aUJueG5fZW5kWTFsQmp5dWhWN3FDSWZDUUNaLVpXSUg1NHE2NkZUSXFTSDJaTTcycjA5aHhxNXpWZXNIaUpiR1A0M0xKWHkxVlEzRVdfLWd2a085MW9zbHJLUDR6bDA3X2ExZw?oc=5",
        "https://news.google.com/rss/articles/CBMixwFBVV95cUxOQldUdGQ0QU9uZEw4RElHV0huaC1PcENnMzJQLU5FMHdmTlBIVV90V2VuZEhlUXF3SUFuSDBDVl85MEh0TDJCTEM5Q21xRG5yQzVXbkY4ZDZRU0dHc2h6NXhNQVpnSFloN0NiUXU0bFBqTWFGWkEydFFkSWRxcUEyZ1c0RnB6LUxLdmdkdjFwZjVnX1phQWs4dkJTZktkdGVQaUwzZEcxQlJXNkpDeDVKWmx4N25NU1BJUEJYN0RLbjNwT2hvX1Zj?oc=5"
    ]

    ids = [
        "1",
        "2",
        "3"
    ]
    data = scraper.fetch_data(links, ids)
    if data:
        return jsonify({"status": "success","data": data,"count": len(data)}), 200
    else:
        return jsonify({"status": "error","data": {},"message": "No Records Found"}), 404
