import streamlit as st
import pandas as pd
from preprocessing import CorpusPreprocessor
from spell_checker import SpellChecker
import time
import re

# Set page config
st.set_page_config(
    page_title="NLP Spelling Correction System",
    page_icon="✍️",
    layout="wide"
)

# Initialize session state for storing corpus data and corrections
if 'corpus_loaded' not in st.session_state:
    st.session_state.corpus_loaded = False
    st.session_state.spell_checker = None
    st.session_state.vocabulary = None
    st.session_state.word_frequencies = None
    st.session_state.bigram_frequencies = None
    st.session_state.corrections = None
    st.session_state.corrected_sentence = None

# Helper to load and process the corpus
@st.cache_resource(show_spinner=False)
def load_corpus():
    st.info("Building corpus from corpus.txt... This may take a few minutes.")
    preprocessor = CorpusPreprocessor("corpus.txt")
    word_freqs, bigram_freqs = preprocessor.build_corpus()
    spell_checker = SpellChecker(
        preprocessor.get_vocabulary(),
        word_freqs,
        bigram_freqs
    )
    return spell_checker, preprocessor.get_vocabulary(), word_freqs, bigram_freqs

# Sidebar
st.sidebar.title("Corpus Dictionary Explorer")
st.sidebar.write("Browse and search the vocabulary from the corpus.")

# Load corpus button
if not st.session_state.corpus_loaded:
    if st.sidebar.button("Load Corpus"):
        spell_checker, vocab, word_freqs, bigram_freqs = load_corpus()
        st.session_state.spell_checker = spell_checker
        st.session_state.vocabulary = vocab
        st.session_state.word_frequencies = word_freqs
        st.session_state.bigram_frequencies = bigram_freqs
        st.session_state.corpus_loaded = True
        st.success("Corpus loaded and processed!")

# Corpus explorer
if st.session_state.corpus_loaded:
    # Sorting and search
    sort_option = st.sidebar.radio("Sort dictionary by:", ("Alphabetical", "Frequency"))
    search_query = st.sidebar.text_input("Search word:")
    vocab_list = list(st.session_state.vocabulary)
    if sort_option == "Alphabetical":
        vocab_list = sorted(vocab_list)
    else:
        vocab_list = sorted(vocab_list, key=lambda w: st.session_state.word_frequencies[w], reverse=True)
    if search_query:
        vocab_list = [w for w in vocab_list if search_query.lower() in w.lower()]
    st.sidebar.write(f"{len(vocab_list)} words found.")
    st.sidebar.dataframe(pd.DataFrame({"Word": vocab_list[:100]}))
    st.sidebar.subheader("Top 10 Most Common Words")
    most_common = pd.DataFrame(
        st.session_state.word_frequencies.most_common(10),
        columns=['Word', 'Frequency']
    )
    st.sidebar.dataframe(most_common)

# Main content
st.title("✍️ NLP Spelling Correction System")
st.write("""
This system uses NLP techniques to detect and correct both non-word errors (e.g., "graffe" → "giraffe") and real-word errors (e.g., "He no the answer" → "He knows the answer").
""")

# Text input
text_input = st.text_area(
    "Enter text to check (max 500 characters):",
    max_chars=500,
    height=150
)

# Use regex to split text into words and keep punctuation for reconstruction
word_pattern = re.compile(r'\b[a-zA-Z]+\b|[^a-zA-Z\s]')

def split_text_with_punct(text):
    # Returns a list of tokens (words and punctuation)
    return re.findall(r'\b[a-zA-Z]+\b|[^a-zA-Z\s]', text)

def reconstruct_text(tokens):
    # Reconstructs text from tokens, preserving spacing and punctuation
    out = ''
    for i, tok in enumerate(tokens):
        if i > 0 and re.match(r'^[a-zA-Z]+$', tok) and re.match(r'^[a-zA-Z]+$', tokens[i-1]):
            out += ' '
        out += tok
    return out

# Two columns: left for original, right for corrected
col1, col2 = st.columns(2)

with col1:
    st.subheader("Original Input & Suggestions")
    if st.button("Check Spelling"):
        if not st.session_state.corpus_loaded:
            st.warning("Please load the corpus first using the button in the sidebar.")
        elif not text_input:
            st.warning("Please enter some text to check.")
        else:
            with st.spinner("Checking spelling..."):
                tokens = split_text_with_punct(text_input)
                words_only = [tok for tok in tokens if re.match(r'^[a-zA-Z]+$', tok)]
                errors = st.session_state.spell_checker.check_text(' '.join(words_only))
                st.session_state.corrections = {}
                # Highlight errors in red
                highlighted = []
                word_idx = 0
                for i, tok in enumerate(tokens):
                    if re.match(r'^[a-zA-Z]+$', tok):
                        err = next((e for e in errors if e['position'] == word_idx), None)
                        if err:
                            highlighted.append(f'<span style="color:red;font-weight:bold">{tok}</span>')
                        else:
                            highlighted.append(tok)
                        word_idx += 1
                    else:
                        highlighted.append(tok)
                st.markdown(" ".join(highlighted), unsafe_allow_html=True)
                st.session_state.tokens = tokens
                st.session_state.errors = errors
                st.session_state.corrected_sentence = None
    # Show suggestions and allow user to select corrections
    if 'errors' in st.session_state and st.session_state.errors:
        tokens = st.session_state.tokens
        words_only = [tok for tok in tokens if re.match(r'^[a-zA-Z]+$', tok)]
        corrections = st.session_state.corrections or {}
        for error in st.session_state.errors:
            idx = error['position']
            orig_word = words_only[idx]
            suggestions = error['suggestions']
            suggestion_options = [f"{s[0]} (edit distance: {st.session_state.spell_checker.get_edit_distance(orig_word, s[0])})" for s in suggestions]
            default = 0
            selected = st.selectbox(
                f"Suggestions for '{orig_word}' (position {idx+1}):",
                options=[orig_word] + suggestion_options,
                index=0,
                key=f"suggestion_{idx}"
            )
            if selected != orig_word:
                new_word = selected.split(' (edit distance:')[0]
                corrections[idx] = new_word
            else:
                corrections.pop(idx, None)
        st.session_state.corrections = corrections
        # Build corrected tokens
        corrected_tokens = []
        word_idx = 0
        for i, tok in enumerate(tokens):
            if re.match(r'^[a-zA-Z]+$', tok):
                if word_idx in corrections:
                    # Highlight corrected word in green
                    corrected_tokens.append(f'<span style="color:green;font-weight:bold">{corrections[word_idx]}</span>')
                else:
                    corrected_tokens.append(tok)
                word_idx += 1
            else:
                corrected_tokens.append(tok)
        st.session_state.corrected_sentence = reconstruct_text([re.sub('<.*?>', '', t) for t in corrected_tokens])

with col2:
    st.subheader("Corrected Sentence")
    if st.session_state.get('corrected_sentence'):
        # Show with highlights
        st.markdown(' '.join(corrected_tokens), unsafe_allow_html=True)
    else:
        st.info("No corrections applied yet. Select a suggestion to see the corrected sentence.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>Built by Sabiq Sabry (TP085636) for NLP (Task A)</p>
</div>
""", unsafe_allow_html=True) 