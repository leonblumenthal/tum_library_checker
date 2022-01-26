import os
import time

from . import scraping
from .models import Booking
from .short import LibraryShortener


class Crawler:
    """Crawler for bookings from url"""

    def __init__(self, url: str, data_path: str) -> None:
        self.url = url
        self.data_path = data_path
        self.csv_path = os.path.join(data_path, 'bookings.csv')
        self.shortener = LibraryShortener(path=os.path.join(data_path, 'shorts.txt'))

    def run(self, timespan: float = 0.1, cooldown: float = 0):
        """
        Crawl bookings and save them in csv.
        Run for timespan seconds and sleep cooldown seconds after each run.
        """

        start_time = time.time()
        while time.time() <= start_time + timespan:
            self._run_once()
            time.sleep(cooldown)

    def _run_once(self):
        try:
            bookings = scraping.scrape_bookings(self.url)
        except Exception as e:
            print(e)
            return

        if not bookings:
            return

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

        print(current_time)

    def _booking_to_csv_row(self, booking: Booking, current_time: int) -> str:
        library = self.shortener.shorten(booking.library)
        period_start = str(booking.period[0])[:-3]
        period_end = str(booking.period[1])[:-3]
        bookable = int(booking.link is not None)

        row = f'{current_time:.0f};{library};{booking.day};{period_start};{period_end};{bookable}'

        return row
