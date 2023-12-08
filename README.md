# Stock Market Simulator

## Introduction

The Stock Market Simulator is a Python-based web application that simulates stock trading. Users can register, log in, view their cash balance, buy and sell stocks, and check their transaction history. The project is structured with clarity, utilizing Flask for the backend, Alpha Vantage API for real-time stock data, and a simple SQLite database for user information.

## Project Structure

The project consists of the following files:

### 1. API.py

#### Description

The `API.py` file interacts with the Alpha Vantage API to fetch recent stock data, stores the information in a dictionary, and saves it to a local JSON file. Additionally, it utilizes Flask to create an API endpoint for buying and selling stocks.

#### Usage

1. Replace `"YOUR_ALPHA_VANTAGE_API_KEY"` with a valid Alpha Vantage API key.
2. Ensure that the required libraries are installed (`requests`, `json`, `time`).
3. Run the script using `python API.py`.

### 2. project.py

#### Description

The `project.py` file is the main application file, utilizing Flask for creating a web-based stock market simulator. It handles user registration, login, buying and selling stocks, and transaction history. The script interacts with an SQLite dummy database for user information and utilizes passlib for password hashing.

#### Usage

1. Ensure that the required libraries are installed (`Flask`, `passlib`, `datetime`, `json`).
2. Run the script using `python project.py`.
3. Access the application in a web browser at `http://127.0.0.1:5000/home`.

### 3. templates/home.html

#### Description

The `home.html` file is the main HTML template for the user interface. It includes sections for displaying the cash balance, buying and selling stocks, user portfolio, available stocks, and transaction history. The script utilizes JavaScript to handle stock transactions and dynamically update the page content.

### 4. static/styles.css

#### Description

The `styles.css` file contains the styles for the HTML templates, ensuring a clean and responsive design. Feel free to customize the styles to match your preferences.

## How to Run

1. Start the Flask application by running `project.py`.
2. Open a web browser and go to `http://127.0.0.1:5000/home`.
3. Register a new user or log in with existing credentials.
4. Explore the features, buy and sell stocks, and check the transaction history.

## Dependencies

- Flask
- passlib
- Alpha Vantage API key (replace with your key in `API.py`)

## Notes

- Ensure that all required dependencies are installed before running the scripts.
- The Alpha Vantage API key is necessary for fetching stock data in real-time.
