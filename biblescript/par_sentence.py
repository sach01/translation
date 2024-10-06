import csv

# Dictionary to map Borana book names to their English equivalents
book_name_mapping = {
    'Uumama': 'Genesis',  # Example for Genesis
    # Add more mappings for other books
}

# Function to read aligned verses from the file
def read_aligned_bible(file_path):
    bible_data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            bible_data.append(row)
    return bible_data

# Function to align and save only matching verses
def align_matching_verses(bible_data):
    parallel_sentences = []
    
    for i in range(0, len(bible_data), 2):
        borana = bible_data[i]
        english = bible_data[i + 1]
        
        # Map Borana book name to English if available
        borana_book = book_name_mapping.get(borana['Book'], borana['Book'])
        
        # Debug output to check the values being compared
        print(f"Comparing Borana -> Book: {borana_book}, Chapter: {borana['Chapter']}, Verse: {borana['Verse']}")
        print(f"Comparing English -> Book: {english['Book']}, Chapter: {english['Chapter']}, Verse: {english['Verse']}")
        
        # Ensure they have the same book, chapter, and verse
        if (borana_book.strip() == english['Book'].strip() and 
            borana['Chapter'].strip() == english['Chapter'].strip() and 
            borana['Verse'].strip() == english['Verse'].strip()):
            
            print("Match found! Adding to parallel sentences.")
            parallel_sentences.append({
                'Book': borana_book,
                'Chapter': borana['Chapter'],
                'Verse': borana['Verse'],
                'Borana_Text': borana['Text'],
                'English_Text': english['Text']
            })
        else:
            print("No match found between these rows. Skipping...")

    return parallel_sentences

# Save the aligned verses into a new CSV file
def save_aligned_verses(file_path, aligned_verses):
    with open(file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['Book', 'Chapter', 'Verse', 'Borana_Text', 'English_Text'])
        writer.writeheader()
        for row in aligned_verses:
            writer.writerow(row)

# Paths to the input aligned CSV and the output CSV for aligned verses
input_file = '/home/kature/Videos/language/translation3/core/biblescript/aligned_bible_verses.csv'
output_file = '/home/kature/Videos/language/translation3/core/biblescript/parallel_sentence.csv'

# Read the aligned verses
aligned_bible_data = read_aligned_bible(input_file)

# Align and save only the matching verses
aligned_verses = align_matching_verses(aligned_bible_data)

# Save the aligned verses to a new CSV
save_aligned_verses(output_file, aligned_verses)

print(f"Saved {len(aligned_verses)} aligned verses to '{output_file}'")
