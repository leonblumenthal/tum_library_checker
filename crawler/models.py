import datetime
from dataclasses import dataclass


@dataclass
class Booking:
    """
    Dataclass representing a single booking for specific library, date, and period
    including a reservation link that is None if library is fully booked
    """

    library: str
    day: datetime.date
    period: tuple[datetime.time, datetime.time]
    link: str
