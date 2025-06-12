# 🔠 NLP Spelling Correction System (Task A – CT052-3-M-NLP)

![Screenshot of the NLP Spelling Correction System Streamlit App](NLP%20Spelling%20Correction%20System.png)

This project is part of **Task A (Spelling Correction Component)** for the **CT052-3-M-NLP** module at **Asia Pacific University**. The system detects and corrects both **non-word** and **real-word** spelling errors using classical NLP techniques, including **Levenshtein Edit Distance** and **Bigram Probability Models**.

---

## 📌 Features

- Handles:
  - Non-word errors (e.g., "graffe" → "giraffe")
  - Real-word errors based on context (e.g., "He no the answer" → "He knows the answer")
- Uses a corpus of 1 million+ words
- Calculates:
  - Minimum edit distance for candidate corrections
  - Bigram probability for contextual disambiguation
- Highlights errors and suggests corrections
- Includes:
  - Dictionary browser
  - Top 10 most frequent words in the corpus
  - Streamlit GUI with live correction view

---

## 🧠 Technologies Used

- Python
- Streamlit
- `editdistance` / `difflib`
- Regular expressions (`re`)
- `collections.Counter`
- Custom corpus from Wikipedia (`corpus.txt`)

---

## 📁 Project Structure

| File                | Description                                       |
|---------------------|---------------------------------------------------|
| `app.py`            | Main Streamlit GUI                                |
| `preprocessing.py`  | Loads and tokenizes corpus                        |
| `spell_checker.py`  | Spell checking logic using edit distance & bigram |
| `corpus.txt`        | Large text corpus (1M+ words, excluded from Git)  |
| `requirements.txt`  | All dependencies                                  |
| `.gitignore`        | Excludes large files and cache                    |

---

## 🚀 How to Run

### 1. Clone the Repo
```bash
git clone https://github.com/sabiqsabry/Spelling-Correction-System.git
cd Spelling-Correction-System
```

### 2. Set Up Environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Launch the App

```bash
streamlit run app.py
```

### 4. Use the Interface

* Type text (max 500 characters)
* Click **Check Spelling**
* View highlighted errors and suggestions
* Click on a suggestion to apply
* Corrected sentence appears on the right

---

## 📂 Corpus

Due to file size, `corpus.txt` is excluded from the repository.

You can:

* Generate it using `preprocessing.py`
* Extract up to 1 million words from a Wikipedia dump or `.txt` books

---

## 📊 Screenshots (Sample Placeholders)

> _Add screenshots here if available for GUI, suggestions, and dictionary browser._

- **GUI Interface:** Input box + highlighted error
- **Dropdown:** Edit distance suggestions
- **Dictionary Browser:** Word frequency table

---

## ✅ Assignment Context

This system fulfills the **Spelling Correction System** requirement under **Task A** of the CT052-3-M-NLP module:

* Demonstrates classical NLP formulation
* Implements GUI with interaction features
* Highlights model design, tokenization, error detection, and suggestion generation

---

## ✍️ Author

[Sabiq Sabry](https://github.com/sabiqsabry)  
*Asia Pacific University – CT052-3-M-NLP*

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details. 