# ---------------- IMPORTS ----------------
import sys
import json
import os
from datetime import datetime
import argparse


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(SCRIPT_DIR, "expenses.json")

# ---------------- CONSTANTS ----------------

DATE_FORMAT = "%Y-%m-%d"

# ---------------- FILE FUNCTIONS ----------------

def load_expenses():
    try:
        with open(FILE_PATH, "r") as file:
            return json.load(file)

    except FileNotFoundError:
        return []

    except json.JSONDecodeError:
        return []

def save_expenses(expenses):
    with open(FILE_PATH, "w") as file:
        json.dump(expenses, file, indent=4)


# ---------------- GENERIC HELPERS ----------------

def fail(message):
    print(message)
    sys.exit()

def get_current_time():
    return datetime.now().strftime(DATE_FORMAT)


# ---------------- VALIDATORS ----------------

def positive_float(number):
    try:
        value = float(number)
        if value > 0:
            return value
        raise argparse.ArgumentTypeError(f"Amount must be greater than 0. Got: {number}")
    except ValueError:
        raise argparse.ArgumentTypeError(f"Amount must be a valid number. Got: '{number}'")
    

def positive_int(number):
    try:
        value = int(number)
        if value > 0:
            return value
        raise argparse.ArgumentTypeError(f"ID must be greater than 0. Got: {number}")
    except ValueError:
        raise argparse.ArgumentTypeError(f"ID must be a valid number. Got: '{number}'")

def month_number(number):
    try:
        value = int(number)
        if 1 <= value <= 12:
            return value
        raise argparse.ArgumentTypeError(f"Month must be between 1 and 12 Got: {number}")
    except ValueError:
        raise argparse.ArgumentTypeError(f"Month must be a valid number. Got: '{number}'")
    

# ---------------- ARGUMENT PARSER ----------------

def build_parser():
    parser = argparse.ArgumentParser(
        prog="expense-tracker",
        description="Track your expenses"
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True
    )

    add_parser = subparsers.add_parser("add")
    add_parser.add_argument(
        "--description",
        required=True
    )
    add_parser.add_argument(
        "--amount",
        type=positive_float,
        required=True
    )

    update_parser = subparsers.add_parser("update")
    update_parser.add_argument(
        "--id",
        type=positive_int,
        required=True
    )
    update_parser.add_argument(
        "--amount",
        type=positive_float,
        required=True
    )
    update_parser.add_argument(
        "--description",
        required=True
    )
    
    delete_parser = subparsers.add_parser("delete")
    delete_parser.add_argument(
        "--id",
        type=positive_int,
        required=True
    )


    list_parser = subparsers.add_parser("list")

    summary_parser = subparsers.add_parser("summary")
    summary_parser.add_argument(
        "--month",
        type=month_number
    )

    return parser

# ---------------- EXPENSE HELPERS ----------------

def find_expense_by_id(id_text, expenses):
    message = f"Expense with ID {id_text} not found."

    for expense in expenses:
        if expense["id"] == id_text:
            return expense

    fail(message)

def get_next_expense_id(expenses):
    if not expenses:
        new_id = 1
    else:
        new_id = max(expense["id"] for expense in expenses) + 1
    return new_id

# ---------------- COMMANDS ----------------

def add_expense(description, amount):
    expenses = load_expenses()
    
    new_id = get_next_expense_id(expenses)
    created_at = get_current_time()

    new_expense = {
        "id": new_id,
        "description": description,
        "amount": amount,
        "createdAt": created_at,
        "updatedAt": created_at
    }

    print(f"# Expense added successfully (ID: {new_id})")
    expenses.append(new_expense)
    save_expenses(expenses)

def update_expense(id, description, amount):
    expenses = load_expenses()
    updated_expense = find_expense_by_id(id, expenses)
    updated_at = get_current_time()

    updated_expense["description"] = description
    updated_expense["amount"] = amount
    updated_expense["updatedAt"] = updated_at
    print(f"# Expense updated successfully (ID: {id})")

    save_expenses(expenses)


def delete_expense(expense_id):
    expenses = load_expenses()
    deleted_expense = find_expense_by_id(expense_id, expenses)

    expenses[:] = [expense for expense in expenses if expense["id"] != deleted_expense["id"]]

    print("# Expense deleted successfully")
    save_expenses(expenses)

def list_expenses():
    expenses = load_expenses()
    if not expenses:
        fail("No expenses found")
    
    print(f"{'#':<2}{'ID':<4}{'Date':<12}{'Description':<20}{'Amount'}")
    for expense in expenses:
        exp_id = expense["id"]
        date = expense["createdAt"]
        desc = expense["description"]
        amt = expense["amount"]

        print(f"# {exp_id:<4}{date:<12}{desc:<20}${amt:.2f}")


def summary(month=None):
    expenses = load_expenses()
    total_expenses = 0
    if not month:
        for expense in expenses:
            total_expenses += expense["amount"]
    else:
        for expense in expenses:
            if int(expense["createdAt"][5:7]) == month:
                total_expenses += expense["amount"]
    return total_expenses


# ---------------- MAIN ----------------

def main():
    parser = build_parser()
    args = parser.parse_args()


    if args.command == "add":
        add_expense(args.description, args.amount)

    elif args.command == "update":
        update_expense(args.id, args.description, args.amount)

    elif args.command == "delete":
        delete_expense(args.id)

    elif args.command == "list":
        list_expenses()

    elif args.command == "summary":
        total = summary(args.month)

        if args.month is None:
            print(f"# Total expenses: ${total:.2f}")
        else:
            
            months = ["", "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"]
            month_name = months[args.month]
            print(f"# Total expenses for {month_name}: ${total:.2f}")

    else:
        print("Unknown command.")


if __name__ == "__main__":
    main()

