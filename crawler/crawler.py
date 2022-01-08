import datetime
import os
import time

import requests
from bs4 import BeautifulSoup
from bs4.element import Tag

from .models import Booking
from .short import LibraryShortener


class Crawler:
    """Crawler for bookings from url"""

    def __init__(self, url: str, data_path: str) -> None:
        self.url = url
        self.data_path = data_path
        self.csv_path = os.path.join(data_path, 'bookings.csv')
        self.shortener = LibraryShortener(path=os.path.join(data_path, 'shorts.txt'))

    def run(self):
        """Crawl bookings and save them in csv."""

        bookings = self._crawl_bookings()

        # Create data path directory before using
        # the shortener and creating the csv file.
        os.makedirs(self.data_path, exist_ok=True)

        # Create rows for each booking (and header row for new file).
        current_time = time.time()
        csv_rows = [
            self._booking_to_csv_row(booking, current_time) for booking in bookings
        ]
        if not os.path.exists(self.csv_path):
            csv_rows.insert(0, 'timestamp;library;day;period_start;period_end;bookable')

        # Write rows.
        with open(self.csv_path, 'a') as f:
            for row in csv_rows:
                f.write(row + '\n')

    def _crawl_bookings(self) -> list[Booking]:
        html = requests.get(self.url).content

        # Parse reservation table rows from html.
        soup = BeautifulSoup(html, 'html.parser')
        view = soup.find(class_='view-resevierungen-lesesaal')
        table_body = view.find(class_='view-content').find('tbody')
        rows = table_body.find_all('tr')

        bookings = [self._table_row_to_booking(row) for row in rows]

        return bookings

    @staticmethod
    def _table_row_to_booking(row: Tag) -> Booking:
        cols = row.find_all('td')

        library, date, period = (c.text.strip() for c in cols[:3])
        link = cols[-1].find('a')
        day = datetime.datetime.strptime(date.split(',')[1], ' %d. %B %Y').date()
        start, _, end = period.split()
        period = datetime.time.fromisoformat(start), datetime.time.fromisoformat(end)

        booking = Booking(library, day, period, link)

        return booking

    def _booking_to_csv_row(self, booking: Booking, current_time: int) -> str:
        library = self.shortener.shorten(booking.library)
        period_start = str(booking.period[0])[:-3]
        period_end = str(booking.period[1])[:-3]
        bookable = int(booking.link is not None)

        row = f'{current_time:.0f};{library};{booking.day};{period_start};{period_end};{bookable}'

        return row
