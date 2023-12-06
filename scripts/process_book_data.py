"""Code to clean and process a dataframe of book detals."""

from dotenv import load_dotenv
import pandas as pd

if __name__ == "__main__":

    load_dotenv()    

    books = pd.read_csv("./data/books.csv")

    print(books.head())