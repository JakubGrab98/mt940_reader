"""Module responsible for communication with NBP api"""

from datetime import datetime
import requests
from dateutil.relativedelta import relativedelta

BASE_URL = "http://api.nbp.pl/api/exchangerates/rates/a/"
DATE_FORMAT = "%Y-%m-%d"


class Rates:
    """Class for retrievieng currency rate based on transaction date"""

    def __init__(self, rate_date: str, currency_code: str) -> float:
        self.rate_date = datetime.strptime(rate_date, DATE_FORMAT).date()
        self.currency_code = currency_code.lower()
        self.rate = 1

    def get_rate(self) -> None:
        """Getting average rate on specific date for specific currency"""
        rate_assign = False
        while not rate_assign:
            date_string = str(self.rate_date)
            try:
                response = requests.get(
                    url=f"{BASE_URL}/{self.currency_code}/{date_string}/?format=json",
                    timeout=10,
                )
                data = response.json()
                self.rate = data["rates"][0]["mid"]
                rate_assign = True
                return float(self.rate)
            except ValueError as e:
                e.add_note(f"Lack of data for date equal to {date_string}")
                self.rate_date = self.rate_date - relativedelta(days=1)
