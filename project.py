from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from passlib.hash import sha256_crypt
from datetime import datetime
import json

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Dummy database (SQLite for simplicity)
users_db = {
    "user1": {
        "username": "user1",
        "password": sha256_crypt.hash("password1"),
        "cash": 1000000.00,
    }
}

# Dummy transaction history
transaction_history = {}

stocks_db = {
    "AAPL": {"name": "Apple Inc.", "price": 150.0},
    "GOOGL": {"name": "Alphabet Inc.", "price": 2500.0},
    "MSFT": {"name": "Microsoft Corporation", "price": 300.0},
    "AMZN": {"name": "Amazon.com Inc.", "price": 3500.0},
    "TSLA": {"name": "Tesla Inc.", "price": 800.0},
    "FB": {"name": "Meta Platforms Inc. (Facebook)", "price": 330.0},
    "NVDA": {"name": "NVIDIA Corporation", "price": 750.0},
    "NFLX": {"name": "Netflix Inc.", "price": 600.0},
    "PYPL": {"name": "PayPal Holdings Inc.", "price": 200.0},
    "V": {"name": "Visa Inc.", "price": 220.0},
}

# User portfolios (dummy data for now)
user_portfolios = {
    "user1": {"AAPL": 0, "GOOGL": 0},
    # Add more users and portfolios as needed
}

# load stock data from json file
with open("stock_data.json") as json_file:
    stock_data = json.load(json_file)


def main():
    app.run(debug=True)


# Route for the home page
@app.route("/home")
def home():
    """
    Route for the home page.

    Returns:
        render_template: The rendered home page.
    """
    if "username" not in session:
        return redirect(url_for("login"))

    username = session["username"]
    user_portfolio_data = user_portfolios.get(username, {})
    cash_balance = user_cash(username)
    user_history = transaction_history.get(username, [])

    for symbol in stocks_db.keys():
        stock_info = get_stock_info(symbol)
        if stock_info:
            stocks_db[symbol]["price"] = stock_info

    return render_template(
        "home.html",
        username=username,
        user_portfolio=user_portfolio_data,
        user_cash=cash_balance,
        stocks_db=stocks_db,
        transaction_history=user_history,
    )


# Route for user registration
@app.route("/register", methods=["GET", "POST"])
def register():
    """
    Route for user registration.

    Returns:
        render_template or redirect: The registration form or redirect to login.
    """
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users_db:
            return "Username already exists. Please choose another username."

        hashed_password = sha256_crypt.hash(password)

        users_db[username] = {
            "username": username,
            "password": hashed_password,
            "cash": 1000000.0,
        }

        return redirect(url_for("login"))

    return render_template("register.html")


# Route for user login
@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Route for user login.

    Returns:
        render_template or redirect: The login form or redirect to home.
    """
    if request.method == "POST":
        username = request.form["username"]
        password_candidate = request.form["password"]

        if username not in users_db:
            return "Invalid username."

        if sha256_crypt.verify(password_candidate, users_db[username]["password"]):
            session["username"] = username
            return redirect(url_for("home"))
        else:
            return "Invalid password."

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))


# Route for buying stocks
@app.route("/buy", methods=["POST"])
def buy():
    """
    Route for buying stocks.

    Returns:
        str: A message indicating the success or failure of the buy operation.
    """
    if "username" not in session:
        return "Please log in to buy stocks."

    data = request.get_json()
    stock_symbol = data.get("symbol")
    quantity_str = data.get("quantity")

    if stock_symbol not in stocks_db:
        return "Invalid stock symbol."

    try:
        quantity = int(quantity_str)
    except ValueError:
        return "Invalid quantity."

    stock_price = stocks_db[stock_symbol]["price"]

    try:
        total_cost = quantity * float(stock_price)
    except ValueError:
        return "Invalid stock price."

    user_balance = user_cash(session["username"])

    if total_cost > user_balance:
        return "Insufficient funds."

    update_portfolio(session["username"], stock_symbol, quantity)
    update_cash(session["username"], -total_cost)

    record_transaction(
        session["username"], "buy", stock_symbol, quantity, float(stock_price)
    )

    return f"Successfully bought {quantity} shares of {stock_symbol}."


# Route for selling stocks
@app.route("/sell", methods=["POST"])
def sell():
    """
    Helper function to record transactions.

    Args:
        username (str): The username.
        transaction_type (str): Type of transaction (buy/sell).
        stock_symbol (str): The stock symbol.
        quantity (int): The quantity of stocks.
        price (float): The price per stock.

    Returns:
        None
    """
    if "username" not in session:
        return "Please log in to sell stocks."

    data = request.get_json()
    stock_symbol = data.get("symbol")
    quantity_str = data.get("quantity")

    if stock_symbol not in stocks_db:
        return "Invalid stock symbol."

    try:
        quantity = int(quantity_str)
    except ValueError:
        return "Invalid quantity."

    user_portfolio_quantity = user_portfolio(session["username"], stock_symbol)

    if quantity > user_portfolio_quantity:
        return "Not enough shares to sell."

    stock_price = stocks_db[stock_symbol]["price"]

    update_portfolio(session["username"], stock_symbol, -quantity)
    update_cash(session["username"], quantity * float(stock_price))

    record_transaction(
        session["username"], "sell", stock_symbol, quantity, float(stock_price)
    )

    return f"Successfully sold {quantity} shares of {stock_symbol}."


# Route for viewing transaction history
@app.route("/history")
def history():
    """
    Route for viewing transaction history.

    Returns:
        render_template: The rendered transaction history page.
    """
    if "username" not in session:
        return "Please log in to view transaction history."

    username = session["username"]
    user_history = transaction_history.get(username, [])

    return render_template(
        "history.html", username=username, transaction_history=user_history
    )


# Route for getting user data
@app.route("/get_user_data", methods=["GET"])
def get_user_data():
    """
    Route for getting user data.

    Returns:
        jsonify: JSON response containing user data.
    """
    if "username" not in session:
        return jsonify({"error": "User not logged in"})

    username = session["username"]
    user_data = {
        "user_cash": user_cash(username),
        "user_portfolio": user_portfolios.get(username, {}),
        "transaction_history": transaction_history.get(username, []),
        "stocks_db": stocks_db,
    }

    return jsonify(user_data)


# Route for redirecting to the home page
@app.route("/")
def redirect_to_home():
    """
    Route for redirecting to the home page.

    Returns:
        redirect: Redirect to the home page.
    """
    return redirect(url_for("home"))


def get_stock_info(symbol):
    """
    Get stock information for the given symbol from the stock_data.

    Args:
        symbol (str): The stock symbol.

    Returns:
        dict or None: The stock information if available, else None.
    """
    if symbol in stock_data:
        stock_info = stock_data[symbol]["price"]
        return stock_info
    else:
        return None


def create_user(username, password):
    """
    Create a new user and add it to the users_db.

    Args:
        username (str): The username.
        password (str): The user's password.

    Returns:
        bool: True if user creation is successful, False if the user already exists.
    """
    if username not in users_db:
        users_db[username] = {"password": password, "cash": 100000.0, "portfolio": {}}
        return True
    else:
        return False


def record_transaction(username, transaction_type, stock_symbol, quantity, price):
    if username not in transaction_history:
        transaction_history[username] = []

    transaction_history[username].append(
        {
            "type": transaction_type,
            "symbol": stock_symbol,
            "quantity": quantity,
            "price": price,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
    )


def user_portfolio(username, stock_symbol):
    """
    Get the quantity of a specific stock in the user's portfolio.

    Args:
        username (str): The username.
        stock_symbol (str): The stock symbol.

    Returns:
        int: The quantity of the specified stock in the user's portfolio.
    """
    return user_portfolios.get(username, {}).get(stock_symbol, 0)


def user_cash(username):
    """
    Get the cash balance of the user.

    Args:
        username (str): The username.

    Returns:
        float: The cash balance of the user.
    """
    if username in users_db and "cash" in users_db[username]:
        return users_db[username]["cash"]
    else:
        return 0.0


def update_portfolio(username, stock_symbol, quantity):
    """
    Update the user's portfolio with the given stock and quantity.

    Args:
        username (str): The username.
        stock_symbol (str): The stock symbol.
        quantity (int): The quantity of the stock to be updated.

    Returns:
        None
    """
    if username not in user_portfolios:
        user_portfolios[username] = {}

    current_quantity = user_portfolios[username].get(stock_symbol, 0)
    user_portfolios[username][stock_symbol] = current_quantity + quantity


def update_cash(username, amount):
    """
    Update the user's cash balance.

    Args:
        username (str): The username.
        amount (float): The amount to be added or subtracted from the user's cash.

    Returns:
        None
    """
    if username not in users_db:
        users_db[username] = {"password": "", "cash": 0, "portfolio": {}}

    if "cash" not in users_db[username]:
        users_db[username]["cash"] = 0

    users_db[username]["cash"] += amount


if __name__ == "__main__":
    main()
