import datetime

import requests
from bs4 import BeautifulSoup, Tag

from .models import Booking


def _table_row_to_booking(row: Tag) -> Booking:
    cols = row.find_all('td')

    library, date, period = (c.text.strip() for c in cols[:3])
    link = cols[-1].find('a')
    day = datetime.datetime.strptime(date.split(',')[1], ' %d. %B %Y').date()
    start, _, end = period.split()
    period = datetime.time.fromisoformat(start), datetime.time.fromisoformat(end)

    booking = Booking(library, day, period, link)

    return booking


def scrape_bookings(url: str) -> list[Booking]:
    """Scrape bookings from url."""

    html = requests.get(url).content

    # Parse reservation table rows from html.
    soup = BeautifulSoup(html, 'html.parser')
    content = soup.find(class_='view-resevierungen-lesesaal').find(
        class_='view-content'
    )
    if content is None:
        return []
    table_body = content.find('tbody')
    rows = table_body.find_all('tr')

    bookings = [_table_row_to_booking(row) for row in rows]

    return bookings
