# Press ⌃R to execute it or replace it with your code.
import os
import json
from nordpool import elspot, elbas
from pprint import pprint
from datetime import date, datetime, timedelta
from pymongo import MongoClient


class DateTimeAwareEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()

        return json.JSONEncoder.default(self, o)


def get_tomorrow(area_in, end_date):
    # Initialize class for fetching Elspot prices
    prices_spot = elspot.Prices()

    # Fetch hourly Elspot prices for area and print the resulting dictionary
    return prices_spot.hourly(areas=[area_in], end_date=end_date)


def get_today(area_in, end_date):
    # Initialize class for fetching Elbas prices
    prices_bas = elbas.Prices()

    # Fetch hourly Elbas prices for area and print the resulting dictionary
    return prices_bas.hourly(areas=[area_in], end_date=end_date)


def print_prices(today_data, tomorrow_data):
    pprint(tomorrow_data)
    pprint(today_data)


if __name__ == '__main__':
    area = os.getenv('SCRAPE_AREA', 'LV')
    mongo_server = os.getenv('MONGO_SERVER', 'mongo')
    mongo_port = os.getenv('MONGO_PORT', '27017')
    mongo_database_name = os.getenv('MONGO_DATABASE', 'nordpool')
    now = datetime.now().time()

    mongo_client = MongoClient(f"mongodb://{mongo_server}:{mongo_port}/")
    mongo_db = mongo_client[mongo_database_name]

    if now.hour > 14 and now.minute > 59:
        today = date.today()
        tomorrow = today + timedelta(days=1)
    else:
        tomorrow = date.today()
        today = tomorrow - timedelta(days=1)

    day_ahead = get_tomorrow(area, tomorrow)
    day_ahead_json = json.dumps(day_ahead, cls=DateTimeAwareEncoder)
    history = get_today(area, today)
    history_json = json.dumps(history, cls=DateTimeAwareEncoder)

    print_prices(day_ahead, history)
