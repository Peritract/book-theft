"""Functions to scrape book details from https://publishing.tor.com/."""

from time import sleep

import requests as req


def scrape_all_book_listings(base_url: str, scrape_delay: int=2) -> None:
    """Loops through all book listing pages until it runs out pages."""

    page = 1
    books_on_page = True

    while books_on_page:
        sleep(scrape_delay)
        print(f'Scraping page {page}...', end="\r")

        url = f"{base_url}/books/?page_number={page}"

        res = req.get(url, timeout=5)

        if "No books found..." in res.text:
            books_on_page = False
        else:
            page += 1


if __name__ == "__main__":

    URL = "https://publishing.tor.com"
    SCRAPE_DELAY = 2

    scrape_all_book_listings(URL, scrape_delay=SCRAPE_DELAY)
