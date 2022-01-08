import os

from dotenv import load_dotenv

from crawler.crawler import Crawler


def run():
    """Run crawler"""

    load_dotenv()

    url = os.getenv('URL', 'https://www.ub.tum.de/en/reserve-study-desks')
    data_path = os.getenv('DATA_PATH', 'data')

    crawler = Crawler(url, data_path)

    crawler.run()


if __name__ == '__main__':
    run()
