import os
import re
from tqdm import tqdm

def extract_article_text(file_path):
    """Extracts and returns all text between <doc ...> and </doc> tags in a WikiExtractor .txt file."""
    with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
        in_doc = False
        lines = []
        for line in f:
            if line.startswith('<doc '):
                in_doc = True
                continue
            if line.startswith('</doc>'):
                in_doc = False
                continue
            if in_doc:
                lines.append(line.strip())
        return ' '.join(lines)

def regex_tokenize(text):
    """Tokenize text using regex (only alphabetic words, min length 2)."""
    return re.findall(r'\\b[a-z]{2,}\\b', text.lower())

def prepare_corpus(extracted_dir='extracted', output_file='corpus.txt'):
    all_words = []
    file_count = 0
    for dirpath, _, filenames in os.walk(extracted_dir):
        for filename in filenames:
            if filename.endswith('.txt'):
                file_path = os.path.join(dirpath, filename)
                file_count += 1
                article_text = extract_article_text(file_path)
                words = regex_tokenize(article_text)
                if words:
                    print(f"{file_path}: {len(words)} words found.")
                all_words.extend(words)
    print(f"Processed {file_count} .txt files.")
    print(f"Writing {len(all_words)} words to {output_file} ...")
    with open(output_file, 'w', encoding='utf-8', errors='replace') as out:
        out.write(' '.join(all_words))
    print(f"Done! corpus.txt created with {len(all_words)} words.")

if __name__ == '__main__':
    prepare_corpus('extracted', 'corpus.txt') 