# Candy Daily Pulse

A small command-line tool written in pure Python (standard library only), built for my own daily use — recording business income/expense and tracking my annual goal.

## 1. What this tool is

Candy Daily Pulse is a **bilingual (中文 / English) command-line bookkeeping tool** for my company **CANDY & FRANK LTD**.
It records the daily income and expense of 4 businesses and automatically works out how far the company is from the **AU$200,000 after-tax net income goal for 2026**.

On startup the program first asks for a language:

- `1 = 中文`
- `2 = English`

After you choose, all menus and prompts are shown in the selected language.

## 2. The real problem it solves for me

I have 4 real businesses, each with scattered income and expenses every day. Relying on memory alone, it is hard to know whether each business is making money, or whether the AU$200,000 after-tax net income goal for the year is on track.

This tool solves:

- Quickly recording the income and expense of each business every day
- Viewing today's records at any time
- Seeing total income, total expense and net profit per business
- Seeing how far the whole company is from the AU$200,000 goal
- Seeing the days left and the required after-tax net per day

The 4 businesses:

| Code | 中文名 | English |
|------|--------|---------|
| `camp` | 青少年创业营 | Youth Entrepreneurship Camp |
| `clothing` | 童装店 | Kids Clothing Store |
| `youtube` | YouTube 频道 | YouTube Channel |
| `secondhand` | 二手书玩具店 | Secondhand Toy & Book Store |

## 3. How to run

Run inside the project folder:

```bash
python3 main.py
```

Requirements:

- Requires Python 3
- No third-party libraries needed
- Uses only the Python standard library: `json`, `os`, `datetime`
- Data is stored in `data/pulse_data.json`
- Close the program and reopen it — your history is loaded back automatically

Main menu options:

1. Add an income record
2. Add an expense record
3. View today's records
4. View full summary
5. View AU$200,000 goal progress
6. Exit

## 4. How the goal progress is calculated

Calculation rules:

- Total income = sum of all `income` record amounts
- Total expense = sum of all `expense` record amounts
- Pre-tax net = total income - total expense
- After-tax net = pre-tax net x (1 - 0.25)
- Distance to goal = 200000 - after-tax net
- Days left = 2026-12-31 - today
- Required after-tax net per day = distance / days left
- Progress percentage = after-tax net / 200000 x 100

Progress is shown with a simple text bar, for example:

```text
[#####-----] 50.0%
```

## 5. Where the 6 technical elements live in the code

For the live walkthrough, you can follow this table:

| Technical element | Code location |
|----------|----------|
| 1. At least 3 custom functions | `load_data()`, `save_data(data)`, `add_record(data, lang, kind=None)`, `show_summary(data, lang)`, `show_goal_progress(data, lang)`, plus `choose_language()`, `show_today()`, `make_bar()`, `main()` |
| 2. Loop + conditional | The `while True` main-menu loop in `main()`, and `if / elif / else` to handle the user's choice; `for` loops over records in `show_summary()` and `show_goal_progress()` |
| 3. Dictionaries | Every record is a dict; `BUSINESSES` holds the 4 businesses; `TEXT` holds the bilingual UI strings |
| 4. try / except | `load_data()` handles a missing file and broken JSON; `add_record()` handles the case where the amount input is not a number |
| 5. JSON file read/write | `load_data()` reads `data/pulse_data.json` with `json.load`; `save_data(data)` saves with `json.dump` |
| 6. Git branch development + merge | Developed and committed on the `feature/cli-tracker` branch, then merged back into `main` |

## 6. What a stored record looks like

`data/pulse_data.json` holds a list, and each record is a dictionary:

```json
[
  {
    "date": "2026-05-30",
    "type": "income",
    "business": "camp",
    "amount": 500.0,
    "note": "summer camp signup"
  }
]
```
