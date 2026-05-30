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
        "pick_business": "请选择业务:",
        "business_prompt": "输入业务代号: ",
        "bad_business": "无效的业务代号,请重新输入。",
        "amount_prompt": "请输入金额 (AU$): ",
        "bad_amount": "请输入数字!",
        "amount_positive": "金额必须大于 0,请重新输入。",
        "note_prompt": "备注 (可留空,直接回车): ",
        "saved_income": "已记录一笔收入。",
        "saved_expense": "已记录一笔支出。",
        "summary_title": "\n===== 全部汇总(按业务) =====",
        "total_income": "总收入",
        "total_expense": "总支出",
        "net": "净利",
        "company_total": "公司合计",
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
        "pick_business": "Choose a business:",
        "business_prompt": "Enter business code: ",
        "bad_business": "Invalid business code, please try again.",
        "amount_prompt": "Enter amount (AU$): ",
        "bad_amount": "Please enter a number!",
        "amount_positive": "Amount must be greater than 0, please try again.",
        "note_prompt": "Note (optional, press Enter to skip): ",
        "saved_income": "Income record saved.",
        "saved_expense": "Expense record saved.",
        "summary_title": "\n===== Full Summary (by business) =====",
        "total_income": "Total income",
        "total_expense": "Total expense",
        "net": "Net profit",
        "company_total": "Company total",
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
# Feature: add a record (income or expense)
# ----------------------------------------------------------------------

def add_record(data, lang, kind):
    """Ask the user for one income/expense record and append it to data.

    'kind' is either "income" or "expense" (decided by the menu).
    Demonstrates: dictionary (the record), try/except (amount input).
    """
    t = TEXT[lang]

    # 1) Choose which business this record belongs to.
    print(t["pick_business"])
    for code in BUSINESSES:
        print("  {} = {}".format(code, BUSINESSES[code][lang]))
    while True:
        business = input(t["business_prompt"]).strip()
        if business in BUSINESSES:
            break
        print(t["bad_business"])

    # 2) Ask for the amount. try/except catches non-numbers so we
    #    never crash; the loop repeats until a valid positive number.
    while True:
        raw = input(t["amount_prompt"]).strip()
        try:
            amount = float(raw)
        except ValueError:
            print(t["bad_amount"])
            continue
        if amount <= 0:
            print(t["amount_positive"])
            continue
        break

    # 3) Optional note.
    note = input(t["note_prompt"]).strip()

    # 4) Build the record as a dictionary and store it.
    record = {
        "date": date.today().isoformat(),
        "type": kind,
        "business": business,
        "amount": amount,
        "note": note,
    }
    data.append(record)
    save_data(data)

    print(t["saved_income"] if kind == "income" else t["saved_expense"])


# ----------------------------------------------------------------------
# Feature: summary by business
# ----------------------------------------------------------------------

def show_summary(data, lang):
    """Print total income, expense and net profit for each business."""
    t = TEXT[lang]
    print(t["summary_title"])

    # Build a dictionary of running totals, one entry per business.
    totals = {}
    for code in BUSINESSES:
        totals[code] = {"income": 0.0, "expense": 0.0}

    # Loop over every record and add its amount to the right bucket.
    for record in data:
        code = record["business"]
        totals[code][record["type"]] += record["amount"]

    company_income = 0.0
    company_expense = 0.0

    # Print one block per business.
    for code in BUSINESSES:
        inc = totals[code]["income"]
        exp = totals[code]["expense"]
        net = inc - exp
        company_income += inc
        company_expense += exp
        print("\n{}".format(BUSINESSES[code][lang]))
        print("  {}: {:.2f}".format(t["total_income"], inc))
        print("  {}: {:.2f}".format(t["total_expense"], exp))
        print("  {}: {:.2f}".format(t["net"], net))

    # Company-wide totals.
    print("\n{}".format(t["company_total"]))
    print("  {}: {:.2f}".format(t["total_income"], company_income))
    print("  {}: {:.2f}".format(t["total_expense"], company_expense))
    print("  {}: {:.2f}".format(t["net"], company_income - company_expense))


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
        if choice == "1":
            add_record(data, lang, "income")
        elif choice == "2":
            add_record(data, lang, "expense")
        elif choice == "3":
            show_today(data, lang)
        elif choice == "4":
            show_summary(data, lang)
        elif choice == "6":
            save_data(data)
            print(t["goodbye"])
            break
        else:
            print(t["bad_choice"])


if __name__ == "__main__":
    main()
