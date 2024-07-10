import csv
import re
import sys
from typing import List

def clean_lyrics(lyrics: str) -> str:
    """Removes characters within square brackets and content before 'Lyrics' in the lyrics.

    Args:
        lyrics (str): The lyrics to be cleaned.

    Returns:
        str: The cleaned lyrics.
    """
    lyrics = re.sub(r'\[.*?\]', '', lyrics)  # Remove characters within square brackets
    start_index = lyrics.find('Lyrics')
    if start_index != -1:
        lyrics = lyrics[start_index + len('Lyrics'):]  # Remove content before 'Lyrics'
    return lyrics.strip()  # Remove leading/trailing spaces

def clean_csv(input_file: str, output_file: str) -> None:
    """Cleans the lyrics column in the CSV file and writes the cleaned data to a new CSV file.

    Args:
        input_file (str): The path to the input CSV file.
        output_file (str): The path to the output CSV file.
    """
    with open(input_file, 'r', encoding="utf-8", newline='') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)  # Read the header row

        cleaned_rows: List[List[str]] = []
        for row in reader:
            # Clean the lyrics column
            lyrics = clean_lyrics(row[3])

            # Append cleaned row to the list
            cleaned_row = [row[0], row[1], row[2], lyrics]
            cleaned_rows.append(cleaned_row)

    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)  # Write the header row
        writer.writerows(cleaned_rows)  # Write the cleaned data rows

# Example usage
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 formatting.py <input_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = 'Cleaned_' + input_file + ".csv"
    clean_csv(input_file, output_file)

