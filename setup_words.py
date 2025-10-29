"""
Setup script to download and prepare the word list for Stackle
"""
import nltk
import json
import os

def setup_word_list():
    """Download NLTK words corpus and create filtered word list"""
    print("Downloading NLTK words corpus...")
    nltk.download('words', quiet=True)
    
    from nltk.corpus import words
    
    # Get all words
    all_words = set(words.words())
    
    # Filter words: only lowercase, alphabetic, length 1-15
    filtered_words = {
        word.lower() 
        for word in all_words 
        if word.isalpha() and 1 <= len(word) <= 15
    }
    
    # Remove offensive words (basic filter - expand this list)
    offensive_words = {'damn', 'hell', 'crap'}  # Add more as needed
    filtered_words = filtered_words - offensive_words
    
    print(f"Total valid words: {len(filtered_words)}")
    
    # Save to JSON file
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    word_file = os.path.join(data_dir, 'words.json')
    with open(word_file, 'w') as f:
        json.dump({
            'words': sorted(list(filtered_words)),
            'count': len(filtered_words)
        }, f)
    
    print(f"Word list saved to {word_file}")
    
    # Create word length index for faster lookups
    words_by_length = {}
    for word in filtered_words:
        length = len(word)
        if length not in words_by_length:
            words_by_length[length] = []
        words_by_length[length].append(word)
    
    index_file = os.path.join(data_dir, 'words_by_length.json')
    with open(index_file, 'w') as f:
        json.dump(words_by_length, f)
    
    print(f"Word index saved to {index_file}")
    print("\nWord count by length:")
    for length in sorted(words_by_length.keys())[:10]:
        print(f"  {length} letters: {len(words_by_length[length])} words")

if __name__ == "__main__":
    setup_word_list()
