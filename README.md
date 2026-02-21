# S&P 500 App

A web application built with Python and Streamlit that displays the **S&P 500** company list and their **stock closing prices** (year-to-date). Data is scraped from Wikipedia and stock prices are retrieved via Yahoo Finance.

## Features

- **Sector filtering** — Filter companies by GICS sector (Information Technology, Healthcare, Finance, etc.)
- **Stock price charts** — View closing price charts for selected companies
- **Company search** — Search for specific companies by name (e.g., IBM, Oracle, Intel)
- **CSV download** — Export filtered data as CSV
- **Responsive layout** — Wide layout for better data visualization

## Data Sources

- **Company list:** [Wikipedia - List of S&P 500 companies](https://en.wikipedia.org/wiki/List_of_S%26P_500_companies)
- **Stock prices:** [Yahoo Finance](https://finance.yahoo.com/) (via yfinance)

## Tech Stack

- **Python**
- **Streamlit** — Web framework
- **pandas** — Data manipulation
- **matplotlib** — Charting
- **yfinance** — Stock data

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/JosueDS21/sp500app.git
   cd sp500app
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the app locally:

```bash
streamlit run sp500-appy.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

## Live Demo

The app is deployed on Streamlit Community Cloud:

[**sp500-appypy.streamlit.app**](https://sp500-appypy-dbqcczub6j9irmghjt3siw.streamlit.app/)

## Project Structure

```
sp500app/
├── sp500-appy.py    # Main application
├── requirements.txt # Python dependencies
└── README.md
```

## Author

[Josue Holguin](http://www.linkedin.com/in/josue-holguin-13694324b)
