"""Functions to scrape book details from https://publishing.tor.com/."""

from os import environ
from time import sleep

from dotenv import load_dotenv
import requests as req


def scrape_book_listing_page(body: str) -> list[str]:
    """Returns a list of book links from a listing page."""

    pass


def scrape_all_book_listings(base_url: str, headers: dict, scrape_delay: int = 2) -> None:
    """Loops through all book listing pages until it runs out pages."""

    page = 1
    books_on_page = True

    while books_on_page:
        sleep(scrape_delay)
        print(f'Scraping page {page}...', end="\r")

        url = f"{base_url}/books/?page_number={page}"

        res = req.get(url, timeout=5, headers=headers)

        if "No books found..." in res.text:
            books_on_page = False
        else:
            page += 1


if __name__ == "__main__":

    load_dotenv()

    HEADERS = {
        "User-Agent": environ["USER_AGENT"]
    }

    # scrape_all_book_listings(URL, scrape_delay=SCRAPE_DELAY)
