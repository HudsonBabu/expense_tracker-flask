from flask import Flask, render_template, request, redirect,url_for
import json
import os
from datetime import datetime


app = Flask(__name__) 

FILE_NAME = "expenses.json"

def load_data():
    if not os.path.exists(FILE_NAME):
        return []
    try:
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return []

def save_data(expenses):
    with open(FILE_NAME, "w") as file:
        json.dump(expenses, file, indent=4)

@app.route("/add",methods = ["GET","POST"])
def add_expense():
    if request.method == "POST":
        try:
            amount = float(request.form["amount"])
        except ValueError:
            return "Invalide amount"
        category = request.form["category"]
        date_input = request.form["date"]
        try:
            date_obj = datetime.strptime(date_input, "%Y-%m-%d")
            date = date_obj.strftime("%Y-%m-%d")
        except ValueError:
            return "Invalid date format!"

        expenses = load_data()

        expense = {
            "amount": amount,
            "category": category,
            "date": date
        }

        expenses.append(expense)
        save_data(expenses)

        return redirect(url_for("view_expenses"))

    return render_template("add.html", show_benefits=False)


# Filter by Category

def filter_expenses():
    category = request.form["category"]
    expenses = load_data()

    filtered = [
        exp for exp in expenses
        if exp["category"].lower() == category.lower()
    ]

    total = sum(exp["amount"] for exp in filtered)

    return render_template("view.html",
                           expenses=filtered,
                           total=total,
                           show_benefits=False)

@app.route("/")
#def index():
#    expenses = load_data()
#   total = sum(exp["amount"] for exp in expenses)
#    return render_template("index.html", expenses=expenses, total=total)
def home():
    return render_template("home.html", show_benefits=True)
    
    
@app.route("/view")
def view_expenses():
    category = request.args.get("category")   # GET parameter
    expenses = load_data()

    if category and category.strip() != "":
        expenses = [
            exp for exp in expenses
            if exp["category"].lower() == category.lower()
        ]

    total = sum(exp["amount"] for exp in expenses)

    return render_template("view.html",
                           expenses=expenses,
                           total=total,
                           show_benefits=False)


if __name__ == "__main__":
    app.run(debug=True)












