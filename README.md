# Tech News Scraper and Article Summarizer

## Table of Contents
- [Description](#description)
- [Installation](#installation)
- [Packages and Tools](#packages-and-tools)
- [Usage](#usage)
- [Roadmap](#roadmap)

## Description
This repository contains Python scripts for scraping the latest tech news articles from TechCrunch and summarizing article content. This will be especially useful for busy individuals who don't have the time to read through lengthy articles but still need to stay informed on the latest tech news. The project consists of two main components:

1. **Tech News Scraper (`news_scraper.py`):**
   - A script that scrapes the latest tech news articles from the TechCrunch website.
   - The scraped data includes article titles, ids, content, urls, authors, and publication dates.
   - The scraped data is stored in a CSV file for further analysis or reference.

2. **Article Summarizer (`site_summarizer.py`):**
   - A script that reads a CSV file containing article information and summarizes each article using the LexRank algorithm.
   - The summarized articles are saved to another CSV file, providing concise summaries of lengthy articles.

## Installation
To use the Tech News Scraper and Article Summarizer, follow these steps:

1. Clone the repository to your local machine:
   ```shell
   git clone <repository-url>
   ```

2. Navigate to the project directory, create a virtual environment (optional but recommended), activate the virtual environment, and install the required packages from `requirements.txt`:

   a. On Windows:

      ```shell
      cd tech-news-scraper-and-summarizer
      python -m venv venv
      venv\Scripts\activate
      pip install -r requirements.txt
      ```

   b. On macOS and Linux:

      ```shell
      cd tech-news-scraper-and-summarizer
      python -m venv venv
      source venv/bin/activate
      pip install -r requirements.txt
      ```

## Packages and Tools
This project makes use of the following Python packages and tools to achieve its functionality:

#### [Beautiful Soup 4](https://www.crummy.com/software/BeautifulSoup/)
- **Description:** Beautiful Soup is a Python library for web scraping purposes. It allows you to parse HTML and XML documents, navigate their elements, and extract data from web pages.
- **Usage:** Beautiful Soup is used to parse the HTML content of web pages, extract article data, and navigate through the webpage structure to locate article titles, dates, authors, and content.

#### [Selenium](https://www.selenium.dev/)
- **Description:** Selenium is a web testing framework that provides a way to automate web browsers for tasks like web scraping and testing web applications.
- **Usage:** Selenium is utilized to automate web browsing, load web pages, and extract HTML content, especially for websites that require JavaScript execution, such as TechCrunch.

#### [Sumy](https://github.com/miso-belica/sumy)
- **Description:** Sumy is a Python library for text summarization. It provides various algorithms, including LexRank, to generate extractive summaries from textual content.
- **Usage:** Sumy's LexRank algorithm is employed to summarize the lengthy article content scraped from TechCrunch, creating concise summaries for each article.

#### [Pandas](https://pandas.pydata.org/)
- **Description:** Pandas is a powerful data manipulation and analysis library for Python. It provides data structures and functions for working with structured data.
- **Usage:** Pandas is used to store, manipulate, and analyze the scraped article data, allowing for easy storage and export of the data to CSV files.


#### [WebDriver Manager](https://pypi.org/project/webdriver-manager/)
- **Description:** WebDriver Manager is a Python library for managing web driver executables automatically. It ensures that the correct driver version is used for Selenium.
- **Usage:** WebDriver Manager is used to automatically download and manage the Chrome driver executable, ensuring compatibility with the installed Chrome browser.

These packages and tools work together to scrape, parse, and summarize tech news articles from TechCrunch effectively.


## Usage
This project consists of two main components: the **Tech News Scraper** and the **Article Summarizer**. Below, you'll find instructions on how to use each component.

### Tech News Scraper (news_scraper.py)

#### Scraping TechCrunch Articles
To scrape the latest tech news articles from TechCrunch, follow these steps:

1. Open your terminal.

2. Navigate to the project directory:

   ```shell
   cd tech-news-scraper-and-summarizer
3. Create a virtual environment (optional but recommended):
   
   a. On Windows:

      ```shell
     source venv\Scripts\activate
      ```

   b. On macOS and Linux:

      ```shell
      source venv/bin/activate
      ```

4. Run the Tech News Scraper to scrape the latest articles from TechCrunch:
    ```shell
      python news_scraper.py
      ```
5. The scraped data will be stored in a CSV file named **TechCrunch_latest_news.csv** for further analysis or reference.

### Article Summarizer (site_summarizer.py)

#### Summarizing Articles
To summarize articles from a CSV file, follow these steps:
1. Open your terminal.

2. Navigate to the project directory

3. Run the Article Summarizer with the following command, specifying the input and output CSV file paths:
    ```shell
      python site_summarizer.py input_articles.csv summarized_articles.csv
      ```
    Replace input_articles.csv with the path to your input CSV file containing article information and summarized_articles.csv with the desired output CSV file name.   
    Example: 
    ```shell
      python site_summarizer.py TechCrunch_latest_news.csv TechCrunch_summaries.csv
      ```
4. The summarized articles will be saved to the specified output CSV file.

## Roadmap

As this project evolves, there are plans for future developments, features, and improvements. Here's an overview of the planned developments and enhancements:

### Future Enhancements
1. **Integration with Django:**
    - Incorporate the Django framework to create a user-friendly web interface for the project.
    - Utilize Django's powerful features for building interactive web applications.
    
2. **PostgreSQL Database:**
    - Implement a PostgreSQL database to store and manage scraped article data.
    - PostgreSQL offers robust data handling capabilities, making it suitable for this purpose.

3. **Celery for Task Scheduling:**
    - Integrate Celery, a distributed task queue, to manage background jobs efficiently.
    - Configure three Celery worker processes for different tasks:
        1. **Worker 1 - Data Scraper:** Utilize Celery Scheduler to scrape data from TechCrunch and store it in the PostgreSQL database.
        2. **Worker 2 - Content Summarizer:** Employ Celery Scheduler to summarize article content and update the database.
        3. **Worker 3 - Celery Flower:** Integrate Celery Flower to maintain detailed logs of Celery runs, providing insights into active, failed, and pending Celery processes.


### APIs (Planned)
Once the project is integrated with Django, the following APIs will be available:

1. **List Articles API**
   - **Method:** GET
   - **Description:** Retrieves a list of articles sorted by publication date (newest to oldest) with pagination.

2. **Article API**
   - **Method:** GET
   - **Description:** Retrieves a specific article by its ID.

These APIs will provide programmatic access to the project's functionalities, allowing for easy integration with other applications or services.

Stay tuned for these exciting developments as the project evolves!
