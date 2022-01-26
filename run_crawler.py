import os
from argparse import ArgumentParser

from dotenv import load_dotenv

from crawler.crawler import Crawler


def run(timespan: float, cooldown: float):
    """Run crawler"""

    load_dotenv()

    url = os.getenv('URL', 'https://www.ub.tum.de/en/reserve-study-desks')
    data_path = os.getenv('DATA_PATH', 'data')

    crawler = Crawler(url, data_path)

    crawler.run(timespan, cooldown)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('timespan', type=float)
    parser.add_argument('cooldown', type=float)
    args = parser.parse_args()
    run(args.timespan, args.cooldown)
