# Candy Daily Pulse

A small command-line tool written in pure Python (standard library only), built for my own daily use.

## 1. What this tool is

Candy Daily Pulse is a **bilingual (中文 / English) command-line bookkeeping tool** for my company
**CANDY & FRANK LTD**. It lets me quickly record the daily **income** and **expense** of each business,
and automatically works out how far the company is from the **AU$200,000 after-tax net income goal for 2026**.

On startup it first asks for a language (`1 = 中文`, `2 = English`); after that, all menus and prompts
are shown in the chosen language.

## 2. The real problem it solves for me

My company has **4 real businesses**, each with scattered income and expenses every day, but I never had a
clear picture in my head, nor any idea whether the AU$200,000 after-tax goal for the year was on track.
This tool records the daily flow and lets me see, at any moment with a single key:

- The total income, total expense and net profit of each business
- How far the whole company is from the AU$200,000 goal, how many days are left, and how much net I still need per day

The 4 businesses:

| Code | 中文名 | English |
|------|--------|---------|
| `camp` | 青少年创业营 | Youth Entrepreneurship Camp |
| `clothing` | 童装店 | Kids Clothing Store |
| `youtube` | YouTube 频道 | YouTube Channel |
| `secondhand` | 二手书玩具店 | Secondhand Toy & Book Store |

## 3. How to run

```bash
python3 main.py
```

- Requires **Python 3** (uses `.format()` and the standard library; Python 3.6+ is enough). No third-party packages needed.
- Data is stored in **`data/pulse_data.json`**. Close and reopen the program and your records are still there — they are loaded back automatically.
- On the first run there is no data file yet; the tool creates the `data/` folder and the JSON file for you.

Main menu options:

1. Add an income record
2. Add an expense record
3. View today's records
4. View full summary (total income, expense and net profit per business)
5. View AU$200,000 goal progress
6. Exit

## 4. How the goal progress is calculated

- Total income = sum of all `income` record amounts
- Total expense = sum of all `expense` record amounts
- Pre-tax net = total income − total expense
- After-tax net = pre-tax net × (1 − 0.25)　← 25% tax rate
- Distance to goal = 200000 − after-tax net
- Days left = 2026-12-31 − today (computed with `datetime`)
- Required after-tax net per day = distance ÷ days left (shows "Goal achieved!" once reached)
- Progress percentage = after-tax net ÷ 200000 × 100, shown with a text progress bar `[#####-----]`

## 5. Where the 6 technical elements live (walkthrough cheat sheet)

> Line numbers refer to `main.py`; if they shift slightly, search by function name instead.

| Technical element | Where it lives |
|----------|----------|
| **1. At least 3 custom functions** | `load_data()`, `save_data(data)`, `add_record(data, lang, kind)`, `show_summary(data, lang)`, `show_goal_progress(data, lang)`, plus `choose_language()`, `show_today()`, `make_bar()`, `main()` |
| **2. Loop + conditional** | The `while True` main-menu loop in `main()` + `if / elif / else` dispatch; `for` loops over all records to accumulate totals in `show_summary()` and `show_goal_progress()` |
| **3. Storing data with dictionaries** | Each record is a dict `{"date":..., "type":..., "business":..., "amount":..., "note":...}` (see `add_record()`); the UI text dict `TEXT`; the business config dict `BUSINESSES` |
| **4. try / except error handling** | In `add_record()`, the amount input uses `try/except ValueError` to catch non-numbers and re-prompt; in `load_data()`, `try/except` handles `FileNotFoundError` and `json.JSONDecodeError` |
| **5. Saving data to a local JSON file** | `save_data()` writes to `data/pulse_data.json` with `json.dump`; `load_data()` reads it back with `json.load` |
| **6. Git branch development + merge back to main** | Developed on the `feature/cli-tracker` branch with several commits, then `git merge` back into `main` (see `git log --oneline` and `git branch`) |

## 6. What a stored record looks like

`data/pulse_data.json` is simply a list of records, each one a dictionary:

```json
[
  {"date": "2026-05-30", "type": "income", "business": "camp", "amount": 500.0, "note": "summer camp signup"}
]
```
