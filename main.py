"""
Candy Daily Pulse - 每日业务脉搏
A simple bilingual command-line tool for CANDY & FRANK LTD.
Record daily income / expense for 4 businesses and track the
AU$200,000 after-tax net income goal for 2026.

Standard library only: json, os, datetime. No classes, no frameworks.
"""

import json
import os
from datetime import date


# ----------------------------------------------------------------------
# Constants / business config
# ----------------------------------------------------------------------

# Where all records are stored on disk (a JSON file inside data/).
DATA_FILE = os.path.join("data", "pulse_data.json")

# Goal logic settings.
GOAL = 200000.0          # after-tax net income target (AU$)
TAX_RATE = 0.25          # 25% tax
FY_END = date(2026, 12, 31)   # financial year end date

# The 4 businesses: code -> bilingual names.
# Using a dictionary keeps the codes and display names together.
BUSINESSES = {
    "camp":       {"zh": "青少年创业营",   "en": "Youth Entrepreneurship Camp"},
    "clothing":   {"zh": "童装店",         "en": "Kids Clothing Store"},
    "youtube":    {"zh": "YouTube 频道",   "en": "YouTube Channel"},
    "secondhand": {"zh": "二手书玩具店",   "en": "Secondhand Toy & Book Store"},
}

# All on-screen text stored in a dictionary, two languages: "zh" and "en".
# This is one of the dictionary uses required by the spec.
TEXT = {
    "zh": {
        "menu_title": "\n===== 每日业务脉搏 主菜单 =====",
        "menu_1": "1. 记一笔收入",
        "menu_2": "2. 记一笔支出",
        "menu_3": "3. 查看今天的收支",
        "menu_4": "4. 查看全部汇总",
        "menu_5": "5. 查看 AU$200,000 目标进度",
        "menu_6": "6. 退出",
        "choose": "请输入选项编号: ",
        "bad_choice": "无效选项,请重新输入。",
        "goodbye": "再见!数据已保存。",
        "today_title": "----- 今天的收支 -----",
        "no_today": "今天还没有任何记录。",
        "income_word": "收入",
        "expense_word": "支出",
        "note_word": "备注",
    },
    "en": {
        "menu_title": "\n===== Daily Pulse - Main Menu =====",
        "menu_1": "1. Add an income record",
        "menu_2": "2. Add an expense record",
        "menu_3": "3. View today's records",
        "menu_4": "4. View full summary",
        "menu_5": "5. View AU$200,000 goal progress",
        "menu_6": "6. Exit",
        "choose": "Enter option number: ",
        "bad_choice": "Invalid option, please try again.",
        "goodbye": "Goodbye! Your data is saved.",
        "today_title": "----- Today's records -----",
        "no_today": "No records for today yet.",
        "income_word": "Income",
        "expense_word": "Expense",
        "note_word": "Note",
    },
}


# ----------------------------------------------------------------------
# Data layer: load / save JSON
# ----------------------------------------------------------------------

def load_data():
    """Read records from the JSON file and return a list of records.

    Uses try/except to handle two problems gracefully:
      - the file does not exist yet (first run)
      - the file is corrupted / not valid JSON
    In both cases we just start with an empty list instead of crashing.
    """
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        # First time running: no file yet, so start fresh.
        return []
    except json.JSONDecodeError:
        # File exists but is broken: warn and start fresh.
        print("Warning: data file is corrupted, starting with empty data.")
        return []


def save_data(data):
    """Write the list of records back to the JSON file.

    Makes sure the data/ folder exists first, then dumps the list
    as nicely formatted JSON so it survives between program runs.
    """
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ----------------------------------------------------------------------
# Language selection
# ----------------------------------------------------------------------

def choose_language():
    """Ask the user to pick a language at startup. Returns 'zh' or 'en'."""
    while True:
        choice = input("选择语言 / Choose language (1=中文, 2=English): ").strip()
        if choice == "1":
            return "zh"
        elif choice == "2":
            return "en"
        else:
            print("请输入 1 或 2 / Please enter 1 or 2.")


# ----------------------------------------------------------------------
# Feature: view today's records
# ----------------------------------------------------------------------

def show_today(data, lang):
    """Print every record whose date is today."""
    t = TEXT[lang]
    today = date.today().isoformat()   # e.g. "2026-05-30"
    print(t["today_title"])

    found = False
    # Loop over all records and pick out today's ones.
    for record in data:
        if record["date"] == today:
            found = True
            kind = t["income_word"] if record["type"] == "income" else t["expense_word"]
            biz = BUSINESSES[record["business"]][lang]
            print("  [{}] {} {}: {:.2f}  {}: {}".format(
                kind, biz, "AU$", record["amount"], t["note_word"], record["note"]))

    if not found:
        print("  " + t["no_today"])


# ----------------------------------------------------------------------
# Main menu loop
# ----------------------------------------------------------------------

def main():
    """Program entry point: pick language, then loop the main menu."""
    lang = choose_language()
    data = load_data()
    t = TEXT[lang]

    # while loop keeps showing the menu until the user chooses to exit.
    while True:
        print(t["menu_title"])
        print(t["menu_1"])
        print(t["menu_2"])
        print(t["menu_3"])
        print(t["menu_4"])
        print(t["menu_5"])
        print(t["menu_6"])

        choice = input(t["choose"]).strip()

        # if / elif / else routes the user's choice to the right action.
        if choice == "3":
            show_today(data, lang)
        elif choice == "6":
            save_data(data)
            print(t["goodbye"])
            break
        else:
            print(t["bad_choice"])


if __name__ == "__main__":
    main()
