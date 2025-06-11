# 📝 NLP Spelling Correction System

This project is a spelling correction system built using classical NLP techniques like edit distance and bigram modeling. It detects both non-word and real-word errors and suggests corrections in an interactive Streamlit GUI.

## 📌 Features
- Spellcheck non-word and real-word errors
- Suggest multiple corrections using Levenshtein distance
- Displays word frequency and bigrams from a large corpus
- Built-in Streamlit GUI with error highlighting and interactive correction
- Dictionary explorer with search and top 10 common words
- Option to correct and display modified sentence live

## 🚀 How to Run

1. Clone the repository:
```bash
git clone https://github.com/sabiqsabry/Spelling-Correction-System.git
cd Spelling-Correction-System
```

2. Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # or use venv\Scripts\activate on Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the app:

```bash
streamlit run app.py
```

## 📂 Corpus

> Note: The `corpus.txt` file is too large to upload to GitHub.
> Please generate it locally using your own Wikipedia data or Project Gutenberg books using the tools provided in `preprocessing.py`.

## 🛠️ Technologies Used

* Python
* Streamlit
* Edit Distance (editdistance / difflib)
* Regular Expressions
* Collections / Counter
* Wikipedia corpus via WikiExtractor

## ✍️ Author

[Sabiq Sabry](https://github.com/sabiqsabry)

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details. 