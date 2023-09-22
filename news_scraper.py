import argparse
import logging
import os
from abc import ABC, abstractmethod
from enum import Enum

import pandas as pd
from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from urllib3.exceptions import ProtocolError
from webdriver_manager.chrome import ChromeDriverManager


# Base exception class
class BaseException(Exception):
    pass


# Custom exception for article title not found
class NoArticleTitleFound(BaseException):
    pass


# Custom exception for article date not found
class NoArticleDateFound(BaseException):
    pass


# Custom exception for article author not found
class NoArticleAuthorFound(BaseException):
    pass


# Custom exception for article content not found
class NoArticleContentFound(BaseException):
    pass


# Custom exception for no matching article source
class NoArticleSourceMatched(BaseException):
    pass


# Enum for article sources
class ArticleSource(Enum):
    TECH_CRUNCH = "techcrunch"


# Abstract Base Class for articles
class BaseArticles(ABC):
    def __init__(self):
        """
        Initialize the BaseArticle class.
        """

    def fetch_articles(self, scraper, html_content, source: ArticleSource):
        """
        Fetches and extracts articles from the web page.

        :param scraper: The scraper object to retrieve article pages.
        :param html_content: The HTML content of the page.
        :param source: The source of the articles.
        :return: A list of dictionaries, each containing article information.
        """
        soup = BeautifulSoup(html_content, "html.parser")
        article_urls = self.extract_article_urls(soup)

        articles_data = []

        # Loop through each article URL and extract article information
        for article_url in article_urls:
            # Retrieve the content of the individual article page using the existing get_page function
            article_page = scraper.get_page(article_url, headless=True)
            article_soup = BeautifulSoup(article_page, "html.parser")

            # exctract article element and add it to dictionary
            article = {}
            article["title"] = self.extract_article_title(article_soup, article_url)
            article["article_id"] = self.extract_article_id(article_url)
            article["content"] = self.extract_article_content_text(
                article_soup, article_url
            )
            article["url"] = article_url
            article["author"] = self.extract_article_author(article_soup, article_url)
            article["date_published"] = self.extract_article_date(
                article_soup, article_url
            )
            article["source"] = source.value

            if article:
                articles_data.append(article)

        return articles_data

    @abstractmethod
    def extract_article_title(self, article_soup, article_url):
        """
        Extracts the title of the article from the web page.

        :param article_soup: BeautifulSoup object of the web page content.
        :param article_url: URL of the article.
        :return: Title of the article.
        """
        pass

    @abstractmethod
    def extract_article_date(self, article_soup, article_url):
        """
        Extracts the date of the article from the web page.

        :param article_soup: BeautifulSoup object of the web page content.
        :param article_url: URL of the article.
        :return: Date of the article.
        """
        pass

    @abstractmethod
    def extract_article_author(self, article_soup, article_url):
        """
        Extracts the author of the article from the web page.

        :param article_soup: BeautifulSoup object of the web page content.
        :param article_url: URL of the article.
        :return: Author of the article.
        """
        pass

    @abstractmethod
    def extract_article_id(self, article_url):
        """
        Extracts the ID of the article from the article URL.

        :param article_url: URL of the article.
        :return: ID of the article.
        """
        pass

    @abstractmethod
    def extract_article_content_text(self, article_soup, article_url):
        """
        Extracts the content of the article from the web page.

        :param article_soup: BeautifulSoup object of the web page content.
        :param article_url: URL of the article.
        :return: Content of the article.
        """
        pass

    @abstractmethod
    def extract_article_urls(self, soup):
        """
        Extracts a list of article URLs from the web page.

        :param soup: BeautifulSoup object of the web page content.
        :return: List of article URLs.
        """
        pass


# Class for TechCrunch articles, inheriting from BaseArticles
class TechCrunchArticles(BaseArticles):
    def extract_article_title(self, article_soup, article_url):
        """
        Extracts the title of the article from the web page.

        :param article_soup: BeautifulSoup object of the web page content.
        :param article_url: URL of the article.
        :return: Title of the article.
        :raises NoArticleTitleFound: when an article's title wasn't found.
        """
        tag_title = article_soup.find("h1", class_="article__title")
        if not tag_title:
            logging.warning("Article title element not found.")
            raise NoArticleTitleFound(
                "No title found for article: {}".format(article_url)
            )

        return tag_title.get_text().strip()

    def extract_article_date(self, article_soup, article_url):
        """
        Extracts the date of the article from the web page.

        :param article_soup: BeautifulSoup object of the web page content.
        :param article_url: URL of the article.
        :return: Date of the article.
        :raises NoArticleDateFound: when an article's date wasn't found.
        """
        tag_date = article_soup.find("time", class_="full-date-time")
        if not tag_date:
            logging.warning("Article date element not found.")
            raise NoArticleDateFound(
                "No date found for article: {}".format(article_url)
            )

        date_text = tag_date.get_text(strip=True)

        try:
            # Split the date_text using the '•' character
            date_parts = date_text.split("•")

            # Get the last item from the split result and remove any leading/trailing whitespace
            date_text = date_parts[-1].strip()

        except IndexError:
            # Handle the case where the split result is empty
            date_text = None
            logging.warning(
                "date format is invalid for article: {}".format(article_url)
            )

        return date_text

    def extract_article_author(self, article_soup, article_url):
        """
        Extracts the author of the article from the web page.

         :param article_soup: BeautifulSoup object of the web page content.
         :param article_url: URL of the article.
         :return: Author of the article.
         :raises NoArticleAuthorFound: when an article's author wasn't found.
        """
        tag_author = article_soup.find("span", class_="river-byline__authors")
        if not tag_author:
            raise NoArticleAuthorFound(
                "No author found for article: {}".format(article_url)
            )

        return tag_author.get_text().strip()

    def extract_article_content_text(self, article_soup, article_url):
        """
        Extracts the content of the article from the web page.

        :param article_soup: BeautifulSoup object of the web page content.
        :param article_url: URL of the article.
        :return: Content of the article.
        :raises NoArticleContentFound: when an article's content wasn't found.
        """
        article_content = article_soup.find("div", class_="article-content")
        if not article_content:
            logging.warning("Article content element not found.")
            raise NoArticleContentFound(
                "No content found for article: {}".format(article_url)
            )

        # Extract only individual text paragraphs and concatenate them as the article text
        article_paragraphs = article_content.find_all("p")
        article_text = "\n".join(
            paragraph.get_text() for paragraph in article_paragraphs
        )
        return article_text

    def extract_article_id(self, article_url):
        """
        Extracts the ID of the article from the article URL.

        :param article_url: URL of the article.
        :return: ID of the article.
        """
        try:
            url_parts = article_url.split("/")
            article_id = url_parts[-2]

        except IndexError:
            article_id = None
            logging.warning("url format is invalid")

        return article_id

    def extract_article_urls(self, soup):
        """
        Extracts a list of article URLs from the web page.

        :param soup: BeautifulSoup object of the web page content.
        :return: List of article URLs.
        """
        article_urls = []

        articles = soup.find_all("a", class_="post-block__title__link")
        article_urls = []

        # Extract article URLs and add them to the list
        for article in articles:
            article_url = article.get("data-mrf-link")
            if article_url:
                article_urls.append(article_url)
            else:
                logging.warning("Article url not found")

        return article_urls


# Web page scraper class using Selenium
class Scraper:
    def __init__(self):
        """
        Initialize the BaseScraper class.
        """
        self.retry_count = 3

        # Set up the Chrome driver service
        self.service = Service(ChromeDriverManager().install())

    def get_page(self, url, headless=True):
        """
        Retrieves the web page content using Selenium.

        :param url: The URL of the web page to scrape.
        :return: HTML content of the web page.
        """
        # Set up Selenium options
        options = Options()
        if headless:
            options.add_argument("--headless")  # Run Chrome in headless mode

        # Choose Chrome Browser
        driver = webdriver.Chrome(service=self.service, options=options)

        # Retry mechanism to handle connection errors, code will try to connect 3 times
        for _ in range(self.retry_count):
            try:
                driver.get(url)

                # Extract the HTML content after JavaScript execution
                html_content = driver.page_source

                return html_content

            except (ConnectionError, ProtocolError):
                logging.warning("Connection error occurred. Retrying...")

        logging.error(
            f"Failed to establish connection to news homepage after {self.retry_count} attempts."
        )
        driver.quit()  # Close the driver to clean up resources if the connection fails

    def scrape(self, url, source):
        """
        Scrape articles from a given URL based on the source.

        :param url: The URL of the web page
        :param source: the source of the articles
        :return: List of dictionaries, each containing article information.
        """

        # Get the HTML content of the web page using the get_page method
        html_content = self.get_page(url, headless=True)
        # Check if the HTML content is None (indicating failure to retrieve the web page)
        if html_content is None:
            # If there's no content, return empty list indicating no articles were scraped
            return []

        # If source is TECH_CRUNCH, create a TechCrunchArticles object and scrape the articles
        if source == ArticleSource.TECH_CRUNCH:
            articles = TechCrunchArticles()

            return articles.fetch_articles(
                self, html_content, ArticleSource.TECH_CRUNCH
            )

        # If there is no source match, log a warning and raise a custom exception
        logging.warning("No articles source matched for source: {}".format(source))
        raise NoArticleSourceMatched(
            "No articles source matched for source: {}".format(source)
        )


class DataStorage:
    def __init__(self, filename):
        """
        Initialize the DataStorage class.

        :param filename: Name of the CSV file to store the data.
        """
        self.filename = filename

    def load_existing_data(self):
        """
        Loads existing data from the CSV file.

        :return: DataFrame containing the existing data.
        """
        if os.path.exists(self.filename):
            return pd.read_csv(self.filename)
        else:
            return pd.DataFrame(
                columns=[
                    "title",
                    "article_id",
                    "content",
                    "url",
                    "author",
                    "date_published",
                    "source",
                ]
            )

    def save_to_csv(self, df):
        """
        Saves a DataFrame to a CSV file.

        :param dataframe: The DataFrame to be saved to CSV.
        :return: None
        """
        df.to_csv(self.filename, index=False, encoding="utf-8-sig")

    def update_csv_file(self, article_data: list):
        """
        Compares new data with existing data and updates the CSV file.

        :return: None
        """

        # Load existing data from the CSV file into a DataFrame
        existing_data = self.load_existing_data()

        # Convert the scraped article data (list of dictionaries) into a new DataFrame
        new_data = pd.DataFrame(article_data)

        # Filter out articles that already exist in the CSV based on their 'article_id'
        new_data = new_data[~new_data["article_id"].isin(existing_data["article_id"])]

        # Concatenate the existing data DataFrame and the new data DataFrame to update the data
        updated_data = pd.concat([existing_data, new_data], ignore_index=True)

        # Save the updated DataFrame to the CSV file
        self.save_to_csv(updated_data)


if __name__ == "__main__":

    # Use argparse to handle command-line arguments
    parser = argparse.ArgumentParser(description="Script with debug mode.")
    parser.add_argument("-v", action="store_true", help="Enable debug mode.")
    args = parser.parse_args()

    # Set the log level based on the command-line argument
    log_level = logging.DEBUG if args.v else logging.INFO
    logging.basicConfig(level=log_level)

    # Create an instance of the Scraper class
    scraper = Scraper()
    # Scrape articles from the TechCrunch website
    techcrunch_articles_data = scraper.scrape(
        "https://techcrunch.com/", ArticleSource.TECH_CRUNCH
    )

    # Create an instance of the DataStorage class with the specified CSV file name
    data_storage = DataStorage("TechCrunch_latest_news.csv")

    # Call the update_csv_file() method to update the CSV file
    data_storage.update_csv_file(techcrunch_articles_data)
