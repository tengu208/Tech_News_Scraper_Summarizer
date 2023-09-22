import argparse

import pandas as pd
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.lex_rank import LexRankSummarizer

"""
Article Summarizer

This script reads a CSV file containing article info, summarizes each article using the LexRank algorithm, and saves the summarized articles to another CSV file. 

Example Usage:
$ python site_summarizer.py TechCrunch_latest_news.csv TechCrunch_summaries.csv
"""


# Custom exception for csv file not found
class NoCSVFound(BaseException):
    pass


def read_csv(csv_file_path):
    """
    Read a CSV file and return its contents as a pandas DataFrame.

    :param csv_file_path: Path to the CSV file.
    :return: A pandas DataFrame containing the CSV data.
    """
    return pd.read_csv(csv_file_path)


def summarize_article(article_text, tokenizer, summarizer, num_sentences=3):
    """
    Summarize an article using LexRank algorithm.

    :param article_text: The text of the article to be summarized.
    :param num_sentences: Number of sentences for the summary.
    :return: A summary of the article as a string.
    """
    parser = PlaintextParser.from_string(article_text, tokenizer)
    summary_sentences = summarizer(parser.document, num_sentences)
    summary = " ".join([str(sentence) for sentence in summary_sentences])
    return summary


def main(input_csv_file, output_csv_file):
    """
    Read articles from an input CSV file, summarize them, and save the results to an output CSV file.

    :param input_csv_file: Path to the input CSV file containing articles.
    :param output_csv_file: Path to the output CSV file for saving summarized articles.
    """
    try:
        df = pd.read_csv(input_csv_file)
    except FileNotFoundError:
        raise NoCSVFound(f"CSV file not found at path: {input_csv_file}")

    df_copy = df.copy()  # Create a copy of the DataFrame

    tokenzier = Tokenizer("english")

    try:
        summarizer = LexRankSummarizer()
    except:
        print(f"An error occurred: {str(e)}")

    summary_column = []
    for article_text in df_copy["content"]:
        summary = summarize_article(article_text, tokenzier, summarizer)
        summary_column.append(summary)

    df_copy["summary"] = summary_column

    df_copy.to_csv(output_csv_file, index=False, encoding="utf-8-sig")


if __name__ == "__main__":
    # Create an argument parser for command-line inputs
    parser = argparse.ArgumentParser(
        description="Summarize articles in a CSV file and save as a new CSV."
    )
    parser.add_argument(
        "input_csv_file",
        help="Path to the input CSV file (e.g., TechCrunch_latest_news.csv)",
    )
    parser.add_argument(
        "output_csv_file", help="Path to the output CSV file for saving the new data"
    )
    args = parser.parse_args()

    # Call the main function with the provided input and output CSV paths
    main(args.input_csv_file, args.output_csv_file)
