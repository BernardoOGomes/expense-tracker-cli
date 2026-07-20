# Expense Tracker CLI

A simple command-line expense tracker built with Python. This project allows users to manage their expenses by adding, updating, deleting, listing, and summarizing them. Expense data is stored locally in a JSON file.

This project was built as part of the Roadmap.sh Python Projects.

## Features

* Add new expenses
* Update existing expenses
* Delete expenses
* List all expenses
* View total expenses
* View expenses for a specific month
* Input validation using `argparse`
* Persistent JSON storage

## Requirements

* Python 3.10 or newer

## Installation

Clone the repository:

```bash
git clone https://github.com/<your-username>/expense-tracker-cli.git
```

Move into the project directory:

```bash
cd expense-tracker-cli
```

## Usage

### Add an expense

```bash
python expense-tracker.py add --description "Lunch" --amount 20
```

### Update an expense

```bash
python expense-tracker.py update --id 1 --description "Business Lunch" --amount 25
```

### Delete an expense

```bash
python expense-tracker.py delete --id 1
```

### List expenses

```bash
python expense-tracker.py list
```

Example output:

```text
# ID  Date        Description         Amount
# 1   2026-07-20  Lunch               $20.00
# 2   2026-07-20  Coffee              $5.50
```

### Show total expenses

```bash
python expense-tracker.py summary
```

### Show expenses for a specific month

```bash
python expense-tracker.py summary --month 7
```

## Data Storage

Expenses are stored in the local `expenses.json` file.

Each expense contains:

* ID
* Description
* Amount
* Creation date
* Last updated date

## Technologies Used

* Python
* argparse
* JSON
* datetime

## Skills Demonstrated

- Python
- Command-line applications (CLI)
- Argument parsing with argparse
- File handling
- JSON data persistence
- CRUD operations
- Input validation
- Modular programming

## Project Structure

```
expense-tracker-cli/
│
├── expense-tracker.py
├── expenses.json
├── README.md
└── .gitignore
```

## License

This project is licensed under the MIT License.
