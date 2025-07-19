# 📄 PaperFetcher

**PaperFetcher** is a Python CLI tool that fetches PubMed research papers authored by **non-academic (industry) contributors**.  
It uses the [NCBI Entrez API](https://www.ncbi.nlm.nih.gov/books/NBK25500/) to search PubMed and extract detailed metadata.

---

## 🔧 Features

- 🔍 Search any topic on PubMed
- 🧪 Filters out purely academic authors
- 💾 Save results to CSV
- 🐍 Built with Python + Poetry

---

## 📦 Requirements

- Python 3.9 or above
- [Poetry](https://python-poetry.org/) installed

---

## 🚀 Installation

Clone the repo and install dependencies:

Basic query:
```bash
git clone https://github.com/Meenaramamoorthi/paperfetcher.git
cd paperfetcher
poetry install

poetry run get-papers-list "cancer treatment"


Save to CSV:
bash
Copy
Edit
poetry run get-papers-list "covid vaccine" -f results.csv
Enable debug logging:
bash
Copy
Edit
poetry run get-papers-list "diabetes" --debug
📁 Project Structure
bash
Copy
Edit
paperfetcher/
├── pyproject.toml        # Project metadata and dependencies
├── README.md             # This file
├── src/
│   └── paperfetcher/
│       ├── cli.py        # Command-line interface
│       ├── fetch.py      # PubMed search and parsing logic
│       └── __init__.py
🛠 How It Works
cli.py: Handles command-line arguments

fetch.py: Calls PubMed API, filters authors, builds result data

Output: Printed in terminal or saved to CSV

📜 License
This project is for educational and demonstration purposes.







