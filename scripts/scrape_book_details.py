"""Code to scrape book details for a list of links."""

from os import environ
from time import sleep
import re

from dotenv import load_dotenv
import requests as req
from bs4 import BeautifulSoup
import pandas as pd


def scrape_book_page(link: str, headers: dict) -> dict:
    """Returns a dict of scraped details for a specific book."""

    res = req.get(link, headers=headers, timeout=5)
    soup = BeautifulSoup(res.content, features="html.parser")
    fact_sheet = soup.find("p", class_="product-description")
    description = soup.find("section", class_="book--description")

    # Remove the image section inside the description
    image_section = description.find("section")
    if image_section:
        image_section.extract()

    book = {
        "title": soup.find("h1", class_="book--title"),
        "series": soup.find("h3", class_="book--series"),
        "description": description
    }

    book = {k:v.decode_contents().strip() if v else None for k,v in book.items()}

    pages = re.search(r"(\d+) Pages", fact_sheet.text) if fact_sheet else None
    book["pages"] = pages.group(1) if pages else None
    published = re.search(r"\d{2}\/\d{2}\/\d{4}", fact_sheet.text)
    book["publication_date"] = published.group(0) if published else None
    formats = soup.find_all("h3", class_="product-format")
    book["formats"] = [x.text.strip()
                       for x in formats] if formats else None
    contributors = soup.find("h2", class_="book--contributor")
    book["contributors"] = [x.text.strip()
                            for x in
                            contributors.find_all("a")] if contributors else None
    book["link"] = link

    return book


def scrape_book_pages(links: list[str], headers: dict, delay: int) -> list[dict]:
    """Returns a list of dicts of scraped book details."""
    details = []

    for i, l in enumerate(links):
        print(f"Scraping link {i + 1}/{len(links)}.", end="\r")
        details.append(scrape_book_page(l, headers))
        sleep(delay)

    print("Scraping process complete.")
    return details


if __name__ == "__main__":

    load_dotenv()

    HEADERS = {
        "User-Agent": environ["USER_AGENT"]
    }

    with open(environ["LINK_FILEPATH"], 'r', encoding="utf-8") as f:
        book_links = [environ["BASE_URL"] + l.strip() for l in f.readlines()]

    book_details = scrape_book_pages(book_links, HEADERS, int(environ["SCRAPE_DELAY"]))

    pd.DataFrame(book_details).to_csv(environ["BOOK_FILEPATH"], index=False)
