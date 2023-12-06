"""Functions to scrape book details from https://publishing.tor.com/."""

from os import environ
from time import sleep

from dotenv import load_dotenv
import requests as req
from bs4 import BeautifulSoup


def scrape_book_listing_page(body: str) -> list[str]:
    """Returns a list of book links from a listing page."""

    soup = BeautifulSoup(body, features="html.parser")
    articles = soup.find("div", class_="books-wrapper").find_all("article")

    return [a.find("a")["href"] for a in articles]


def scrape_all_book_listings(base_url: str, headers: dict,
                             scrape_delay: int = 2, max_pages: int = 5) -> None:
    """Returns a list of relative links to books scraped from Tor."""

    page = 1
    books_on_page = True

    book_links = []

    while books_on_page and page <= max_pages:
        sleep(scrape_delay)
        print(f'Scraping page {page}...', end="\r")

        url = f"{base_url}/books/?page_number={page}"

        res = req.get(url, timeout=5, headers=headers)

        if "No books found..." in res.text:
            books_on_page = False
        else:
            book_links.extend(scrape_book_listing_page(res.content))
            page += 1

    print(f"Scraping complete ({page}/{page} pages).")

    return book_links


if __name__ == "__main__":

    load_dotenv()

    HEADERS = {
        "User-Agent": environ["USER_AGENT"]
    }

    links = scrape_all_book_listings(environ["BASE_URL"], headers=HEADERS,
                                     scrape_delay=int(environ["SCRAPE_DELAY"]),
                                     max_pages=int(environ["MAX_PAGES"]))

    with open(environ["LINK_FILEPATH"], "w", encoding="utf-8") as f:
        f.write("\n".join(links))
