import os
import re
import random
import time
from collections import Counter
from typing import List, Dict, Tuple
from pathlib import Path
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CorpusPreprocessor:
    def __init__(self, corpus_file_path: str = "corpus.txt"):
        """
        Initialize the preprocessor with the path to the plain text corpus file.
        Args:
            corpus_file_path (str): Path to the plain text corpus file
        """
        self.corpus_file_path = corpus_file_path
        self.word_frequencies = Counter()
        self.bigram_frequencies = Counter()
        self.vocabulary = set()

    @staticmethod
    def regex_tokenize(text: str) -> List[str]:
        """Tokenize text using regex (only alphabetic words, min length 2)."""
        return re.findall(r'\b[a-z]{2,}\b', text.lower())

    @staticmethod
    def build_limited_corpus(extracted_dir: str = './extracted', output_path: str = 'corpus.txt', max_words: int = 1_000_000):
        import itertools
        start_time = time.time()
        words = []
        file_count = 0
        done = False
        with open(output_path, 'w', encoding='utf-8', errors='replace') as out:
            for dirpath, _, filenames in os.walk(extracted_dir):
                for filename in filenames:
                    file_path = os.path.join(dirpath, filename)
                    if os.path.isfile(file_path):
                        file_count += 1
                        try:
                            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                                text = f.read().lower()
                                new_words = re.findall(r'\b[a-z]{2,}\b', text)
                                needed = max_words - len(words)
                                if needed > 0:
                                    words.extend(new_words[:needed])
                                print(f"After file {file_count} ({file_path}): total words so far = {len(words)}")
                                if len(words) >= max_words:
                                    out.write(' '.join(words[:max_words]))
                                    done = True
                                    break
                        except Exception as e:
                            logger.warning(f"Skipping {file_path}: {e}")
                if done:
                    break
        elapsed = time.time() - start_time
        print(f"Processed {file_count} files.")
        print(f"Wrote {min(len(words), max_words)} words to {output_path}.")
        print(f"Time taken: {elapsed:.2f} seconds.")

    def build_corpus_from_extracted(self, extracted_dir: str = './extracted') -> Tuple[Counter, Counter]:
        """
        Traverse all files in extracted_dir, clean and tokenize, write to corpus.txt, and build frequency stats.
        Returns:
            word_frequencies (Counter), bigram_frequencies (Counter)
        """
        logger.info(f"Building corpus.txt from all files in {extracted_dir} ...")
        file_count = 0
        skipped_files = 0
        total_words = 0
        word_frequencies = Counter()
        bigram_frequencies = Counter()
        last_word = None

        with open(self.corpus_file_path, 'w', encoding='utf-8', errors='replace') as out:
            for file_path in Path(extracted_dir).rglob('*'):
                if file_path.is_file():
                    file_count += 1
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                            text = f.read().lower()
                            words = self.regex_tokenize(text)
                            logger.info(f"{file_path}: {len(words)} words found.")
                            if words:
                                out.write(' '.join(words) + ' ')
                                total_words += len(words)
                                word_frequencies.update(words)
                                # Bigram update (across files)
                                if last_word:
                                    bigram_frequencies[(last_word, words[0])] += 1
                                bigram_frequencies.update(zip(words[:-1], words[1:]))
                                last_word = words[-1]
                    except Exception as e:
                        logger.warning(f"Skipping {file_path}: {e}")
                        skipped_files += 1

        self.word_frequencies = word_frequencies
        self.bigram_frequencies = bigram_frequencies
        self.vocabulary = set(word_frequencies.keys())
        logger.info(f"✅ Loaded {file_count} files from {extracted_dir} (skipped {skipped_files} files)")
        logger.info(f"✅ Found {total_words} total words and {len(self.vocabulary)} unique words")
        logger.info(f"Done! corpus.txt created with {total_words} words.")
        return self.word_frequencies, self.bigram_frequencies

    def read_corpus_file(self) -> List[str]:
        """
        Read the plain text corpus file.
        Returns:
            List[str]: List of lines/text segments from the corpus
        """
        if not os.path.exists(self.corpus_file_path):
            logger.error(f"Corpus file '{self.corpus_file_path}' not found. Please build it from extracted files.")
            raise FileNotFoundError(f"Corpus file '{self.corpus_file_path}' not found.")
        texts = []
        with open(self.corpus_file_path, 'r', encoding='utf-8', errors='replace') as f:
            for i, line in enumerate(f):
                try:
                    if line.strip():
                        texts.append(line.strip())
                except Exception as e:
                    logger.warning(f"Skipping problematic line {i}: {e}")
                    continue
        logger.info(f"Read {len(texts)} lines from corpus file.")
        return texts

    def clean_text(self, text: str) -> str:
        """
        Clean the extracted text by removing markup, non-English characters, etc.
        Args:
            text (str): Raw text to clean
        Returns:
            str: Cleaned text
        """
        # Remove Wikipedia markup
        text = re.sub(r'\[\[.*?\]\]', '', text)  # Remove links
        text = re.sub(r'{{.*?}}', '', text)      # Remove templates
        text = re.sub(r'<.*?>', '', text)        # Remove HTML tags
        # Remove non-English characters and punctuation
        text = re.sub(r'[^a-zA-Z\s]', ' ', text)
        # Convert to lowercase and remove extra whitespace
        text = text.lower()
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def build_corpus(self, min_words: int = 100000) -> Tuple[Counter, Counter]:
        logger.info("Building corpus from plain text file (regex tokenization)...")
        texts = self.read_corpus_file()
        all_words = []
        for text in texts:
            words = self.regex_tokenize(text)
            all_words.extend(words)
            if len(all_words) >= min_words:
                break
        self.word_frequencies = Counter(all_words)
        self.bigram_frequencies = Counter(zip(all_words[:-1], all_words[1:]))
        self.vocabulary = set(self.word_frequencies.keys())
        logger.info(f"Corpus built: {len(all_words)} words, {len(self.vocabulary)} unique words.")
        return self.word_frequencies, self.bigram_frequencies

    def get_vocabulary(self) -> set:
        return self.vocabulary

    def get_word_frequencies(self) -> Counter:
        return self.word_frequencies

    def get_bigram_frequencies(self) -> Counter:
        return self.bigram_frequencies

if __name__ == "__main__":
    # Build corpus.txt from extracted/ if needed
    preprocessor = CorpusPreprocessor("corpus.txt")
    preprocessor.build_corpus_from_extracted('./extracted')
    word_freqs, bigram_freqs = preprocessor.build_corpus()
    print(f"Vocabulary size: {len(preprocessor.get_vocabulary())}")
    print(f"Most common words: {word_freqs.most_common(5)}")
    print(f"Most common bigrams: {bigram_freqs.most_common(5)}")
    # Build corpus.txt by collecting up to 1,000,000 words from extracted/ and its subfolders, stopping early for speed
    CorpusPreprocessor.build_limited_corpus('./extracted', 'corpus.txt', 1_000_000) 