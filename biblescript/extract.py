import re
import csv
import json
import unicodedata
from fuzzywuzzy import fuzz

# Function to read text from a file
def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.readlines()

# Function to normalize book names by stripping accents and converting to lowercase
def normalize_name(name):
    # Remove accents and convert to lowercase
    return unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode('ascii').lower()

# Function to parse Bible text into structured data
def parse_bible(lines, language):
    bible_data = []
    book = None
    chapter = None

    for line in lines:
        line = line.strip()
        # Check if the line is a book name and chapter heading (e.g., "Genesis 1")
        chapter_match = re.match(r"([A-Za-z]+)\s+(\d+)", line)
        if chapter_match:
            book = chapter_match.group(1)
            chapter = chapter_match.group(2)
            print(f"Found Chapter: {book} {chapter}")  # Debugging output
        else:
            # Assume this is a verse, modify to handle no space after verse number (e.g., "1When God...")
            verse_match = re.match(r"^(\d+)(.*)", line)
            if verse_match:
                verse_number = verse_match.group(1)
                verse_text = verse_match.group(2).strip()  # Strip leading/trailing spaces in text
                # Store the parsed verse with book, chapter, verse, and language
                bible_data.append({
                    'language': language,
                    'book': book,
                    'chapter': chapter,
                    'verse': verse_number,
                    'text': verse_text
                })
                print(f"Parsed verse {verse_number} in {book} {chapter}")  # Debugging output
    return bible_data

# Function to match book names dynamically using fuzzy matching
def match_book_names(borana_book, english_books):
    best_match = None
    highest_ratio = 0

    # Normalize Borana book name
    normalized_borana_book = normalize_name(borana_book)

    # Loop through all English book names and find the best match
    for english_book in english_books:
        normalized_english_book = normalize_name(english_book)
        ratio = fuzz.ratio(normalized_borana_book, normalized_english_book)
        print(f"Matching {normalized_borana_book} with {normalized_english_book}: Similarity = {ratio}")  # Debugging
        if ratio > highest_ratio:
            highest_ratio = ratio
            best_match = english_book

    print(f"Best match for {borana_book} is {best_match} with ratio {highest_ratio}\n")  # Debugging
    return best_match

# Function to create parallel sentences for Borana and English based on book, chapter, and verse
def create_parallel_sentences(borana_bible_data, english_bible_data):
    parallel_sentences = []

    # Extract unique book names from the English Bible
    english_books = set([verse['book'] for verse in english_bible_data])

    # Loop through the Borana verses and find the best match in English verses
    for borana in borana_bible_data:
        # Find the best match for the Borana book name in the English book names
        matched_english_book = match_book_names(borana['book'], english_books)

        # Debugging: Print Borana and English book name match
        print(f"Matching Borana book: {borana['book']} with English book: {matched_english_book}")

        # Loop through the English verses to find matches by chapter and verse
        for english in english_bible_data:
            if (matched_english_book == english['book'] and
                borana['chapter'] == english['chapter'] and
                borana['verse'] == english['verse']):
                # Add matched sentences to parallel data
                parallel_sentences.append({
                    'book': borana['book'],  # Use Borana book name
                    'chapter': borana['chapter'],
                    'verse': borana['verse'],
                    'borana_language': borana['text'],
                    'english_language': english['text']
                })
                print(f"Match found: {borana['book']} {borana['chapter']}:{borana['verse']}")  # Debugging output

    # Save the parallel sentences to a CSV file
    with open('parallel_sentence.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['book', 'chapter', 'verse', 'borana_language', 'english_language'])
        writer.writeheader()
        writer.writerows(parallel_sentences)

    print(f"Saved {len(parallel_sentences)} parallel sentences.")  # Debugging output

# File paths for the Borana and English files
borana_file = '/home/kature/Videos/language/translation3/core/biblescript/bible_borana.txt'
english_file = '/home/kature/Videos/language/translation3/core/biblescript/bible_english.txt'

# Read the Borana and English verses from the text files
borana_verses = read_file(borana_file)
english_verses = read_file(english_file)

# Parse the data for Borana and English
borana_bible_data = parse_bible(borana_verses, 'Borana')
english_bible_data = parse_bible(english_verses, 'English')

# Check if data is parsed correctly
print(f"Borana Data: {len(borana_bible_data)} verses")
print(f"English Data: {len(english_bible_data)} verses")

# Create parallel sentences based on dynamically matched book names
create_parallel_sentences(borana_bible_data, english_bible_data)



'''
import re
import csv
import json

# Function to read text from a file
def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.readlines()

# Function to parse Bible text into structured data
def parse_bible(lines, language):
    bible_data = []
    book = None
    chapter = None

    for line in lines:
        line = line.strip()
        # Check if the line is a book name and chapter heading (e.g., "Genesis 1")
        chapter_match = re.match(r"([A-Za-z]+)\s+(\d+)", line)
        if chapter_match:
            book = chapter_match.group(1)
            chapter = chapter_match.group(2)
            print(f"Found Chapter: {book} {chapter}")  # Debugging output
        else:
            # Assume this is a verse, modify to handle no space after verse number (e.g., "1When God...")
            verse_match = re.match(r"^(\d+)(.*)", line)
            if verse_match:
                verse_number = verse_match.group(1)
                verse_text = verse_match.group(2).strip()  # Strip leading/trailing spaces in text
                # Store the parsed verse with book, chapter, verse, and language
                bible_data.append({
                    'language': language,
                    'book': book,
                    'chapter': chapter,
                    'verse': verse_number,
                    'text': verse_text
                })
                print(f"Parsed verse {verse_number} in {book} {chapter}")  # Debugging output
    return bible_data

# File paths for the Borana and English files
borana_file = '/home/kature/Videos/language/translation3/core/biblescript/bible_borana.txt'
english_file = '/home/kature/Videos/language/translation3/core/biblescript/bible_english.txt'

# Read the Borana and English verses from the text files
borana_verses = read_file(borana_file)
english_verses = read_file(english_file)

# Parse the data for Borana and English
borana_bible_data = parse_bible(borana_verses, 'Borana')
english_bible_data = parse_bible(english_verses, 'English')

# Check if data is parsed correctly
print(f"Borana Data: {len(borana_bible_data)} verses")
print(f"English Data: {len(english_bible_data)} verses")

# Combine the parsed data for Borana and English based on verse alignment
combined_data = list(zip(borana_bible_data, english_bible_data))

# Print example output for verification
for borana, english in combined_data[:10]:  # Print the first 10 aligned verses
    print(f"Borana: {borana['book']} {borana['chapter']}:{borana['verse']} - {borana['text']}")
    print(f"English: {english['book']} {english['chapter']}:{english['verse']} - {english['text']}")
    print()

# Save aligned verses into a CSV file
with open('aligned_bible_verses.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Language', 'Book', 'Chapter', 'Verse', 'Text'])  # Header row
    for borana, english in combined_data:
        writer.writerow([borana['language'], borana['book'], borana['chapter'], borana['verse'], borana['text']])
        writer.writerow([english['language'], english['book'], english['chapter'], english['verse'], english['text']])

# Save aligned verses into a JSON file
with open('aligned_bible_verses.json', 'w', encoding='utf-8') as file:
    json.dump(combined_data, file, indent=4, ensure_ascii=False)



import re
import csv
import json

# Function to read text from a file
def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.readlines()

# Function to parse Bible text into structured data
def parse_bible(lines, language):
    bible_data = []
    book = None
    chapter = None

    for line in lines:
        line = line.strip()
        # Check if the line is a book name and chapter heading (e.g., "Genesis 1")
        chapter_match = re.match(r"([A-Za-z]+)\s+(\d+)", line)
        if chapter_match:
            book = chapter_match.group(1)
            chapter = chapter_match.group(2)
            print(f"Found Chapter: {book} {chapter}")  # Debugging output
        else:
            # Assume this is a verse, modify to handle no space after verse number (e.g., "1When God...")
            verse_match = re.match(r"^(\d+)(.*)", line)
            if verse_match:
                verse_number = verse_match.group(1)
                verse_text = verse_match.group(2).strip()  # Strip leading/trailing spaces in text
                # Store the parsed verse with book, chapter, verse, and language
                bible_data.append({
                    'language': language,
                    'book': book,
                    'chapter': chapter,
                    'verse': verse_number,
                    'text': verse_text
                })
                print(f"Parsed verse {verse_number} in {book} {chapter}")  # Debugging output
    return bible_data

# File paths for the Borana and English files
borana_file = '/mnt/data/bible_borana.txt'
english_file = '/mnt/data/bible_english.txt'

# Read the Borana and English verses from the text files
borana_verses = read_file(borana_file)
english_verses = read_file(english_file)

# Parse the data for Borana and English
borana_bible_data = parse_bible(borana_verses, 'Borana')
english_bible_data = parse_bible(english_verses, 'English')

# Check if data is parsed correctly
print(f"Borana Data: {len(borana_bible_data)} verses")
print(f"English Data: {len(english_bible_data)} verses")

# Combine the parsed data for Borana and English based on verse alignment
combined_data = list(zip(borana_bible_data, english_bible_data))

# Print example output for verification
for borana, english in combined_data[:10]:  # Print the first 10 aligned verses
    print(f"Borana: {borana['book']} {borana['chapter']}:{borana['verse']} - {borana['text']}")
    print(f"English: {english['book']} {english['chapter']}:{english['verse']} - {english['text']}")
    print()

# Save aligned verses into a CSV file
with open('aligned_bible_verses.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Language', 'Book', 'Chapter', 'Verse', 'Text'])  # Header row
    for borana, english in combined_data:
        writer.writerow([borana['language'], borana['book'], borana['chapter'], borana['verse'], borana['text']])
        writer.writerow([english['language'], english['book'], english['chapter'], english['verse'], english['text']])

# Save aligned verses into a JSON file
with open('aligned_bible_verses.json', 'w', encoding='utf-8') as file:
    json.dump(combined_data, file, indent=4, ensure_ascii=False)

'''