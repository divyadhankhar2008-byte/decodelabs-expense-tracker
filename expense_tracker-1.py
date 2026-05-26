# ============================================================
#  DecodeLabs Industrial Training Kit — Project 2
#  Expense Tracker | Batch 2026
#  Author : [Your Name]
# ============================================================

import json
import os
from datetime import date, datetime

SAVE_FILE = "expenses_data.json"

CATEGORIES = {
    "1": "🍔 Food & Dining",
    "2": "🚗 Transport",
    "3": "🛒 Shopping",
    "4": "💡 Utilities",
    "5": "🏥 Health",
    "6": "🎮 Entertainment",
    "7": "📚 Education",
    "8": "🏠 Rent / EMI",
    "9": "💰 Other",
}

CURRENCY = "₹"   # Change to "$" or "€" if needed


# ── Persistence ───────────────────────────────────────────────────────────────

def load_data():
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return {"expenses": [], "budget": {}}

def save_data(data):
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f, indent=2)


# ── Core Operations ───────────────────────────────────────────────────────────

def add_expense(data):
    print("\n── Add New Expense ───────────────────────")
    raw = input("Amount: ").strip()
    try:
        amount = float(raw)
        if amount <= 0:
            print("⚠️  Amount must be positive.")
            return
    except ValueError:
        print("❌ Invalid amount.")
        return

    print("Category:")
    for k, v in CATEGORIES.items():
        print(f"  {k}) {v}")
    cat_choice = input("Choose category (1-9) [default 9]: ").strip() or "9"
    category = CATEGORIES.get(cat_choice, "💰 Other")

    desc = input("Description (optional): ").strip() or "—"
    pay_method = input("Payment method (Cash/UPI/Card/Other) [default UPI]: ").strip() or "UPI"

    entry = {
        "id": int(datetime.now().timestamp() * 1000),
        "amount": amount,
        "category": category,
        "description": desc,
        "payment": pay_method,
        "date": date.today().isoformat(),
    }
    data["expenses"].append(entry)
    save_data(data)

    # Budget warning
    budget = data["budget"].get(category)
    if budget:
        spent = sum(e["amount"] for e in data["expenses"]
                    if e["category"] == category and e["date"][:7] == date.today().isoformat()[:7])
        pct = spent / budget * 100
        if pct >= 100:
            print(f"🚨 ALERT: You've EXCEEDED your {category} budget! ({pct:.0f}%)")
        elif pct >= 80:
            print(f"⚠️  WARNING: {pct:.0f}% of your {category} budget used this month.")

    print(f"✅ Added: {CURRENCY}{amount:,.2f}  |  {category}  |  {desc}")


def view_expenses(data, month_filter=None):
    expenses = data["expenses"]
    if month_filter:
        expenses = [e for e in expenses if e["date"][:7] == month_filter]

    if not expenses:
        print("\n📝 No expenses recorded yet.")
        return

    print(f"\n{'─'*65}")
    print(f"  {'#':<4} {'Date':<12} {'Category':<22} {'Amount':>10}  {'Desc'}")
    print(f"{'─'*65}")
    for i, e in enumerate(expenses, 1):
        print(f"  {i:<4} {e['date']:<12} {e['category']:<22} {CURRENCY}{e['amount']:>9,.2f}  {e['description']}")
    print(f"{'─'*65}")
    total = sum(e["amount"] for e in expenses)
    print(f"  TOTAL: {CURRENCY}{total:,.2f}  ({len(expenses)} transactions)")


def category_summary(data):
    month = date.today().isoformat()[:7]
    expenses = [e for e in data["expenses"] if e["date"][:7] == month]
    if not expenses:
        print(f"\n📝 No expenses for {month}.")
        return

    totals = {}
    for e in expenses:
        totals[e["category"]] = totals.get(e["category"], 0) + e["amount"]

    grand = sum(totals.values())
    budgets = data.get("budget", {})

    print(f"\n📊 Category Breakdown — {month}")
    print(f"{'─'*55}")
    for cat, amt in sorted(totals.items(), key=lambda x: -x[1]):
        pct_total = amt / grand * 100
        budget = budgets.get(cat)
        budget_str = f" | Budget: {CURRENCY}{budget:,.0f} ({amt/budget*100:.0f}%)" if budget else ""
        bar = "█" * int(pct_total // 5) + "░" * (20 - int(pct_total // 5))
        print(f"  {cat}")
        print(f"    {CURRENCY}{amt:>9,.2f}  [{bar}] {pct_total:.1f}%{budget_str}")
    print(f"{'─'*55}")
    print(f"  GRAND TOTAL: {CURRENCY}{grand:,.2f}")


def set_budget(data):
    print("\n── Set Monthly Budget ────────────────────")
    for k, v in CATEGORIES.items():
        print(f"  {k}) {v}")
    cat_choice = input("Choose category (1-9): ").strip()
    category = CATEGORIES.get(cat_choice)
    if not category:
        print("❌ Invalid choice.")
        return
    try:
        amount = float(input(f"Monthly budget for {category}: {CURRENCY}").strip())
        if amount <= 0:
            print("⚠️  Budget must be positive.")
            return
    except ValueError:
        print("❌ Invalid amount.")
        return

    data["budget"][category] = amount
    save_data(data)
    print(f"✅ Budget set: {category} → {CURRENCY}{amount:,.2f}/month")


def delete_expense(data):
    view_expenses(data)
    if not data["expenses"]:
        return
    try:
        idx = int(input("\nEnter # to delete: ")) - 1
        if 0 <= idx < len(data["expenses"]):
            removed = data["expenses"].pop(idx)
            save_data(data)
            print(f"🗑️  Deleted: {CURRENCY}{removed['amount']:,.2f} — {removed['category']}")
        else:
            print("❌ Invalid number.")
    except ValueError:
        print("❌ Please enter a valid number.")


def monthly_report(data):
    months = sorted({e["date"][:7] for e in data["expenses"]}, reverse=True)
    if not months:
        print("\n📝 No data available.")
        return

    print("\n📅 Monthly Spending Report")
    print(f"{'─'*40}")
    for m in months[:6]:
        total = sum(e["amount"] for e in data["expenses"] if e["date"][:7] == m)
        count = sum(1 for e in data["expenses"] if e["date"][:7] == m)
        bar = "█" * min(int(total // 1000), 20)
        print(f"  {m}  {CURRENCY}{total:>10,.2f}  ({count} txns)  {bar}")
    print(f"{'─'*40}")


def spending_insights(data):
    expenses = data["expenses"]
    if not expenses:
        print("\n📝 No data yet.")
        return

    total = sum(e["amount"] for e in expenses)
    avg = total / len(expenses)
    biggest = max(expenses, key=lambda e: e["amount"])
    by_method = {}
    for e in expenses:
        by_method[e["payment"]] = by_method.get(e["payment"], 0) + e["amount"]

    print("\n💡 Spending Insights")
    print(f"{'─'*45}")
    print(f"  Total Spent (all time) : {CURRENCY}{total:,.2f}")
    print(f"  Avg per transaction    : {CURRENCY}{avg:,.2f}")
    print(f"  Biggest expense        : {CURRENCY}{biggest['amount']:,.2f} ({biggest['category']} on {biggest['date']})")
    print(f"\n  Payment Methods:")
    for method, amt in sorted(by_method.items(), key=lambda x: -x[1]):
        print(f"    {method}: {CURRENCY}{amt:,.2f} ({amt/total*100:.1f}%)")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    data = load_data()
    print("=" * 50)
    print("   💰  DecodeLabs Smart Expense Tracker  💰")
    print(f"      Powered by DecodeLabs | Batch 2026")
    print("=" * 50)

    menu = {
        "1": ("➕ Add expense",                   lambda: add_expense(data)),
        "2": ("📋 View all expenses",              lambda: view_expenses(data)),
        "3": ("📆 View this month's expenses",     lambda: view_expenses(data, date.today().isoformat()[:7])),
        "4": ("📊 Category breakdown (this month)",lambda: category_summary(data)),
        "5": ("📅 Monthly report",                 lambda: monthly_report(data)),
        "6": ("💡 Spending insights",              lambda: spending_insights(data)),
        "7": ("🎯 Set monthly budget",             lambda: set_budget(data)),
        "8": ("🗑️  Delete an expense",              lambda: delete_expense(data)),
        "9": ("🚪 Exit",                           None),
    }

    while True:
        print("\n── Menu ──────────────────────────────────")
        for key, (label, _) in menu.items():
            print(f"  {key}. {label}")
        print("──────────────────────────────────────────")
        choice = input("Enter choice: ").strip()

        if choice == "9":
            print("\n👋 Goodbye! Track smart, spend smarter! 💪")
            break
        elif choice in menu:
            _, action = menu[choice]
            action()
        else:
            print("⚠️  Invalid choice. Please enter 1–9.")

if __name__ == "__main__":
    main()
