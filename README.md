# 🧠 NLP Spelling Correction System (Assignment Task A - CT052-3-M-NLP)

This project is a spelling correction system developed as part of **Task A** in the **CT052-3-M-NLP (Natural Language Processing)** module at **Asia Pacific University**. It demonstrates classical NLP techniques applied to detect and correct both **non-word** and **real-word spelling errors** using edit distance and bigram-based context modeling.

## 🎓 Assignment Context
This system was implemented as the **Group Report Component (Task A)** for the NLP assignment. It fulfills the following deliverables as per the assignment brief:
- Corpus-based spelling correction engine
- Detection of non-words and real-word errors
- Suggestions with edit distance values
- Interactive GUI with correction features
- Dictionary explorer and word frequency statistics

## 🛠️ Features
- Supports correction of **non-words** (e.g., "graffe" → "giraffe")
- Handles **real-word context errors** using bigram probability
- GUI shows spelling errors with suggested corrections
- Allows user to apply corrections interactively
- Side panel for dictionary browsing, searching, and top 10 most frequent words
- Fast corpus loading with regex-based tokenization (no external NLP libraries used)

## ⚙️ How to Run

### 1. Clone the repository
```bash
git clone https://github.com/sabiqsabry/Spelling-Correction-System.git
cd Spelling-Correction-System
```

### 2. Create a virtual environment (optional but recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # on Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add or generate your corpus

The file `corpus.txt` is excluded from the repo due to size limits. You can:

* Use `preprocessing.py` to extract 1M+ words from Wikipedia or any large `.txt` file
* Or generate a lightweight test corpus manually

### 5. Launch the app

```bash
streamlit run app.py
```

---

## 💡 How It Works

* Loads a corpus and builds a vocabulary with word frequencies and bigrams
* Uses regex tokenization (no NLTK or spaCy required)
* Computes Levenshtein distance to suggest alternative words
* GUI highlights incorrect words and offers dropdown-based corrections
* Optionally shows corrected version of sentence after user applies a fix

---

## 📁 File Overview

| File               | Purpose                                   |
| ------------------ | ----------------------------------------- |
| `app.py`           | Streamlit app UI and control flow         |
| `preprocessing.py` | Tokenizes and loads corpus + bigrams      |
| `spell_checker.py` | Edit distance logic and correction engine |
| `corpus.txt`       | Large text file with 1M+ words (excluded) |
| `requirements.txt` | Python dependencies                       |
| `.gitignore`       | Ensures no heavy files are pushed         |

---

## 🔎 Academic Notes

This system satisfies **Task A requirements** of the assignment, including:

* Formulation of a classical NLP solution
* Proper GUI design for interaction
* Integration of corpus analysis, correction logic, and user feedback
* Modular, testable, and efficient implementation

---

## ⚠️ Limitations

* Large corpus must be generated or downloaded manually
* Doesn't use advanced ML (as per assignment rules – classical NLP only)
* Real-word error correction is limited to local bigram context

---

## 👤 Author

[Sabiq Sabry](https://github.com/sabiqsabry)

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details. 