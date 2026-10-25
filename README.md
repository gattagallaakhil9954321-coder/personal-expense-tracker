# Personal Expense Tracker

A responsive, beginner-friendly expense tracking web app built with Python, Flask, SQLite, HTML and CSS.

## Features
- Add expenses with title, amount, category, date and optional note
- View total spending, today's spending and transaction count
- View spending grouped by category
- Search by title/note and filter by category or date range
- Delete an expense after confirmation
- Export saved records to CSV
- SQLite database is created automatically on first run

## Requirements
- Python 3.10 or newer
- pip

## Run locally
1. Download or clone this repository.
2. Open a terminal in the project folder.
3. Create and activate a virtual environment (recommended):
   - Windows: `py -m venv .venv` then `.venv\\Scripts\\activate`
   - macOS/Linux: `python3 -m venv .venv` then `source .venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Start the app: `python app.py`
6. Open `http://127.0.0.1:5000` in your browser.

The app stores data in `expenses.db` on the same computer. This local database is ignored by Git so your personal transactions are not accidentally uploaded.

## GitHub: make the repository belong to your account
I cannot create or claim a repository in your account from this chat. To make it yours, sign in to your own GitHub account and follow these steps:
1. Create a new repository named `personal-expense-tracker` at https://github.com/new.
2. Choose **Public** if your faculty needs to view the code, or **Private** if you want to keep it private. Do not initialize it with a README because this folder already has one.
3. Install Git if needed, open a terminal in this folder, and run:

```bash
git init
git add .
git commit -m "Initial commit: Personal Expense Tracker"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/personal-expense-tracker.git
git push -u origin main
```

Replace `YOUR-USERNAME` with your actual GitHub username. The repository will be under your account because you created it while signed in and pushed the code to it. Use your own GitHub credentials; never share your password or token in chat. You should understand and be able to explain the code before submitting it for assessment.

## Notes
- Change `app.secret_key` in `app.py` before deploying publicly.
- This is intended as a local/student project. It has no login or multi-user access control, so do not deploy it with real sensitive financial data as-is.
- For a hosted demo, use a platform that supports Python web apps and persistent storage; local SQLite files may not persist on some free hosting platforms.

## Suggested future improvements
- User login and separate accounts
- Monthly budget limits and alerts
- Edit existing expenses
- Charts and monthly reports
- Automated tests and cloud database support
