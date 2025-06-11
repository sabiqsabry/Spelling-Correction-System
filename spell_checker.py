import difflib
from typing import List, Dict, Tuple, Set
from collections import Counter
import numpy as np

# Try to import editdistance, fall back to difflib if not available
try:
    import editdistance
    USE_EDITDISTANCE = True
except ImportError:
    USE_EDITDISTANCE = False

class SpellChecker:
    def __init__(self, vocabulary: Set[str], word_frequencies: Dict[str, int], 
                 bigram_frequencies: Dict[Tuple[str, str], int]):
        """
        Initialize the spell checker with vocabulary and frequency information.
        
        Args:
            vocabulary (Set[str]): Set of valid words
            word_frequencies (Dict[str, int]): Word frequency dictionary
            bigram_frequencies (Dict[Tuple[str, str], int]): Bigram frequency dictionary
        """
        self.vocabulary = vocabulary
        self.word_frequencies = word_frequencies
        self.bigram_frequencies = bigram_frequencies
        
        # Calculate total word count for probability calculations
        self.total_words = sum(word_frequencies.values())
        
    def get_edit_distance(self, word1: str, word2: str) -> int:
        """
        Calculate the Levenshtein distance between two words.
        Uses editdistance package if available, otherwise falls back to difflib.
        
        Args:
            word1 (str): First word
            word2 (str): Second word
            
        Returns:
            int: Levenshtein distance
        """
        if USE_EDITDISTANCE:
            return editdistance.eval(word1, word2)
        else:
            # Fallback to difflib's SequenceMatcher
            return int((1 - difflib.SequenceMatcher(None, word1, word2).ratio()) * max(len(word1), len(word2)))
    
    def get_candidates(self, word: str, max_distance: int = 2) -> List[Tuple[str, int]]:
        """
        Get candidate corrections for a word based on edit distance.
        
        Args:
            word (str): Word to find candidates for
            max_distance (int): Maximum edit distance to consider
            
        Returns:
            List[Tuple[str, int]]: List of (candidate, distance) tuples
        """
        candidates = []
        
        # If word is in vocabulary, it's a valid word
        if word in self.vocabulary:
            return [(word, 0)]
        
        # Find words within max_distance
        for vocab_word in self.vocabulary:
            distance = self.get_edit_distance(word, vocab_word)
            if distance <= max_distance:
                candidates.append((vocab_word, distance))
        
        return candidates
    
    def get_word_probability(self, word: str) -> float:
        """
        Calculate the probability of a word based on its frequency.
        
        Args:
            word (str): Word to calculate probability for
            
        Returns:
            float: Word probability
        """
        return self.word_frequencies.get(word, 0) / self.total_words
    
    def get_bigram_probability(self, word1: str, word2: str) -> float:
        """
        Calculate the probability of a bigram.
        
        Args:
            word1 (str): First word
            word2 (str): Second word
            
        Returns:
            float: Bigram probability
        """
        bigram = (word1, word2)
        if bigram in self.bigram_frequencies:
            return self.bigram_frequencies[bigram] / self.word_frequencies.get(word1, 1)
        return 0.0
    
    def rank_candidates(self, word: str, candidates: List[Tuple[str, int]], 
                       context: Tuple[str, str] = None) -> List[Tuple[str, float]]:
        """
        Rank candidate corrections using both edit distance and context.
        
        Args:
            word (str): Original word
            candidates (List[Tuple[str, int]]): List of (candidate, distance) tuples
            context (Tuple[str, str]): Previous and next word for context
            
        Returns:
            List[Tuple[str, float]]: Ranked list of (candidate, score) tuples
        """
        ranked_candidates = []
        
        for candidate, distance in candidates:
            # Base score from edit distance (lower is better)
            distance_score = 1.0 / (1.0 + distance)
            
            # Word frequency score
            freq_score = self.get_word_probability(candidate)
            
            # Context score if context is provided
            context_score = 0.0
            if context:
                prev_word, next_word = context
                if prev_word:
                    context_score += self.get_bigram_probability(prev_word, candidate)
                if next_word:
                    context_score += self.get_bigram_probability(candidate, next_word)
            
            # Combine scores (you can adjust weights)
            final_score = (0.4 * distance_score + 
                          0.4 * freq_score + 
                          0.2 * context_score)
            
            ranked_candidates.append((candidate, final_score))
        
        # Sort by score in descending order
        return sorted(ranked_candidates, key=lambda x: x[1], reverse=True)
    
    def check_text(self, text: str) -> List[Dict]:
        """
        Check a text for spelling errors and suggest corrections.
        
        Args:
            text (str): Text to check
            
        Returns:
            List[Dict]: List of error information dictionaries
        """
        words = text.lower().split()
        errors = []
        
        for i, word in enumerate(words):
            # Get context (previous and next word)
            prev_word = words[i-1] if i > 0 else None
            next_word = words[i+1] if i < len(words)-1 else None
            context = (prev_word, next_word)
            
            # Get candidates
            candidates = self.get_candidates(word)
            
            # If no candidates found or word is valid, skip
            if not candidates or candidates[0][1] == 0:
                continue
            
            # Rank candidates
            ranked_candidates = self.rank_candidates(word, candidates, context)
            
            # Add error information
            errors.append({
                'word': word,
                'position': i,
                'suggestions': [(cand, score) for cand, score in ranked_candidates[:5]]
            })
        
        return errors

if __name__ == "__main__":
    # Test the spell checker
    from preprocessing import CorpusPreprocessor
    
    # Initialize preprocessor and build corpus
    preprocessor = CorpusPreprocessor("enwiki-20250601-pages-articles-multistream.xml.bz2")
    word_freqs, bigram_freqs = preprocessor.build_corpus()
    
    # Initialize spell checker
    spell_checker = SpellChecker(
        preprocessor.get_vocabulary(),
        word_freqs,
        bigram_freqs
    )
    
    # Test some examples
    test_text = "The graffe is a tall animal that lives in Africa"
    errors = spell_checker.check_text(test_text)
    
    print("Test text:", test_text)
    print("\nErrors found:")
    for error in errors:
        print(f"\nWord: {error['word']}")
        print("Suggestions:")
        for suggestion, score in error['suggestions']:
            print(f"  - {suggestion} (score: {score:.4f})") 