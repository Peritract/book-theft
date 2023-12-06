# Book theft

This project scrapes a bunch of books and does not-technically-illegal stuff with them.

## Installation

- `pip3 install -r requirements.txt`

## Setup

This project expects a `.env` file with the following keys:

```sh
BASE_URL=https://publishing.tor.com
SCRAPE_DELAY=2
USER_AGENT="Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/119.0"
MAX_PAGES=60
LINK_FILEPATH=./data/book_links.txt
BOOK_FILEPATH=./data/books.csv
```

The values provided above are reasonable-ish defaults.

Additionally, the scripts expect the existence of a `data` folder at the project root.

## Data collection process

This repository contains a number of scripts that should be run in order to scrape and process the resultant data. Run them using the below commands:

1. `python3 ./scripts/scrape_book_links.py`
2. `python3 ./scripts/scrape_book_details.py`
3. `python3 ./scripts/process_book_data.py`

The end result of running the above scripts is a clean dataframe in the `data` folder named `tor_books.csv`.