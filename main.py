# Press ⌃R to execute it or replace it with your code.
# Import library for fetching Elspot data
from nordpool import elspot, elbas
from pprint import pprint
from datetime import date, datetime, timedelta
import json
from pymongo import MongoClient


class DateTimeAwareEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()

        return json.JSONEncoder.default(self, o)


def get_tomorrow(area, date):
    # Initialize class for fetching Elspot prices
    prices_spot = elspot.Prices()

    # Fetch hourly Elspot prices for area and print the resulting dictionary
    return prices_spot.hourly(areas=[area], end_date=date)


def get_today(area, date):
    # Initialize class for fetching Elsbas prices
    prices_bas = elbas.Prices()

    # Fetch hourly Elbas prices for area and print the resulting dictionary
    return prices_bas.hourly(areas=[area], end_date=date)


def print_prices(today_data, tomorrow_data):
    pprint(tomorrow_data)
    pprint(today_data)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    area = 'LV'
    now = datetime.now().time()
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
