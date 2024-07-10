import sys
import nltk
import pandas as pd
import string
import re
import csv
from typing import List
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from profanity import profanity

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

def preprocess_lyrics(lyrics: str) -> str:
    """Preprocesses the lyrics by converting to lowercase, removing punctuation, non-English characters, and stopwords.

    Args:
        lyrics (str): The lyrics to be preprocessed.

    Returns:
        str: The preprocessed lyrics.
    """
    tokens = word_tokenize(lyrics.lower())  # Convert text to lowercase
    tokens = [token for token in tokens if token not in string.punctuation]  # Remove punctuation
    tokens = [token for token in tokens if re.match(r'^[a-zA-Z]+$', token)]  # Remove non-English characters
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]  # Remove stopwords
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]
    preprocessed_lyrics = ' '.join(lemmatized_tokens)
    return preprocessed_lyrics

def remove_profanity(text: str) -> str:
    """Removes profanity from the given text.

    Args:
        text (str): The text to remove profanity from.

    Returns:
        str: The text with profanity removed.
    """
    return profanity.censor(text)

def clean_csv(input_file: str, output_file: str, flag_remove_profanity: bool = False) -> List[List[str]]:
    """Cleans the lyrics column in the CSV file and writes the cleaned data to a new CSV file.

    Args:
        input_file (str): The path to the input CSV file.
        output_file (str): The path to the output CSV file.
        flag_remove_profanity (bool): Whether to remove profanity from the lyrics (default: False).

    Returns:
        List[List[str]]: The cleaned rows of the CSV file.
    """
    cleaned_rows = []
    header = None  # Initialize header variable

    with open(input_file, 'r', encoding="utf-8", newline='') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)  # Read the header row

        for row in reader:
            # Clean the lyrics column
            lyrics = row[3]
            if flag_remove_profanity:
                lyrics = remove_profanity(lyrics)
            lyrics = preprocess_lyrics(lyrics)

            # Modify the row in-place
            row[3] = lyrics
            cleaned_rows.append(row)

    # Write the cleaned data
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)  # Write the header row
        writer.writerows(cleaned_rows)  # Write the cleaned data rows

    return cleaned_rows

# Check if the correct number of command-line arguments is provided
if len(sys.argv) != 2 and len(sys.argv) != 3:
    print('Usage: python3 preprocessing.py <input_file> [--remove-profanity]')
    sys.exit(1)

# Get the input file path from the command-line argument
input_file = sys.argv[1]

# Check if the "--remove-profanity" option is provided
flag_remove_profanity = False
if len(sys.argv) == 3 and sys.argv[2] == "--remove-profanity":
    flag_remove_profanity = True

# Create the output file name
output_file = 'Preprocessed_' + input_file

# Clean the CSV file and get the cleaned rows
cleaned_rows = clean_csv(input_file, output_file, flag_remove_profanity)

print('Preprocessing completed. Output file:', output_file)
