"""Code to clean and process a dataframe of book detals."""

from os import environ

from dotenv import load_dotenv
import pandas as pd

if __name__ == "__main__":

    load_dotenv()

    books = pd.read_csv("./data/books.csv", parse_dates=True)

    # Remove HTML tags
    books["description"] = books["description"].str.replace(r'(<\/?[\w\s=""-]+\/?>)',
                                                            " ", regex=True)

    # Replace em dashes with " -- "
    books["description"] = books["description"].str.replace(r"\u2014", " — ", regex=True)

    # Collapse multiple spaces (left by removing adjacent HTML tags)
    books["description"] = books["description"].str.replace(r"\s+",
                                                        " ", regex=True)

    # Split the series number from the name
    books["series_number"] = books["series"].str.extract(r"#(\d+)", expand=False)
    books["series"] = books["series"].str.replace(r"#(\d+)", "", regex=True)


    books = books[["title", "description", "series", "series_number",
                   "pages", "publication_date", "formats", "contributors"]]
    books.to_csv(environ["FINAL_BOOK_FILEPATH"], index=False)
