# 💰 Smart Expense Tracker — Project 2

> **DecodeLabs Industrial Training Kit | Batch 2026**
> Author: Divya Bharti | Python Programming Intern

---

## 📌 Project Overview

A comprehensive command-line expense tracking application built as Project 2 of the DecodeLabs Python Programming Industrial Training Kit. This project goes well beyond simple accumulation — it delivers real financial intelligence through budget alerts, category breakdowns, monthly reports, and spending insights.

Users can **log expenses, set budgets, analyse spending patterns, and track trends over time** — all persisted to a local JSON file between sessions.

---

## ✨ Features

| Feature | Description |
|---|---|
| ➕ Add Expense | Amount, category, description, and payment method |
| 🗂️ 9 Categories | Food, Transport, Shopping, Utilities, Health, Entertainment, Education, Rent, Other |
| 🚨 Budget Alerts | Real-time warnings at 80% and 100% of monthly budget |
| 📊 Category Breakdown | Visual bar chart of spending by category for current month |
| 📅 Monthly Report | Last 6 months spending history with trend bars |
| 💡 Spending Insights | All-time total, average per transaction, biggest expense, payment method split |
| 🎯 Set Budgets | Per-category monthly budget limits |
| 🗑️ Delete Expense | Remove any logged transaction |
| 💾 JSON Persistence | All data saved to `expenses_data.json` — survives restarts |
| 💱 Currency Config | Single-line change to switch between ₹ / $ / € |

---

## 🎯 Key Concepts Demonstrated

| Concept | Implementation |
|---|---|
| IPO Model | Input → Process → Output pipeline throughout |
| Accumulator Pattern | `total += expense` — state preserved across iterations |
| Type Safety (Gatekeeper) | `float(input())` converts raw string to number |
| Defensive Coding (Poka-Yoke) | `try / except ValueError` blocks invalid input |
| Kill Switch / Sentinel Value | `'9'` exits the menu gracefully |
| State Anatomy | `data = {"expenses": [], "budget": {}}` — structured from the start |
| File I/O | `json.load()` / `json.dump()` for persistent storage |
| Date Handling | `date.today().isoformat()` for timestamping and monthly filtering |
| Dictionary Aggregation | Category totals built with `.get()` pattern |

---

## 🏗️ Architecture

```
Phase 1 — Load        : Read JSON file or initialise empty store
Phase 2 — Menu Loop   : Display menu, capture choice, dispatch action
Phase 3 — Action      : Validate input → mutate data → check budget
Phase 4 — Persist     : Write updated data back to JSON
Phase 5 — Feedback    : Print confirmation or alert to user
```

---

## 🚀 How to Run

### Prerequisites
- Python **3.x** installed
- No external libraries — uses stdlib only (`json`, `os`, `datetime`)

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/divyadhankhar2008-byte/decodelabs-expense-tracker.git

# 2. Navigate into the folder
cd decodelabs-expense-tracker

# 3. Run the script
python expense_tracker.py
```

---

## 🖥️ Sample Output

```
==================================================
   💰  DecodeLabs Smart Expense Tracker  💰
      Powered by DecodeLabs | Batch 2026
==================================================

── Menu ──────────────────────────────────
  1. ➕ Add expense
  2. 📋 View all expenses
  3. 📆 View this month's expenses
  4. 📊 Category breakdown (this month)
  5. 📅 Monthly report
  6. 💡 Spending insights
  7. 🎯 Set monthly budget
  8. 🗑️  Delete an expense
  9. 🚪 Exit
──────────────────────────────────────────
```

**Category Breakdown Example:**
```
📊 Category Breakdown — 2026-05
───────────────────────────────────────────────────────
  🍔 Food & Dining
    ₹  3,250.00  [████████████░░░░░░░░] 42.3% | Budget: ₹5,000 (65%)
  🚗 Transport
    ₹  1,800.00  [███████░░░░░░░░░░░░░] 23.4%
  🛒 Shopping
    ₹  2,630.00  [██████████░░░░░░░░░░] 34.2%
───────────────────────────────────────────────────────
  GRAND TOTAL: ₹7,680.00
```

**Budget Alert Example:**
```
⚠️  WARNING: 80% of your 🍔 Food & Dining budget used this month.
✅ Added: ₹350.00  |  🍔 Food & Dining  |  Lunch
```

---

## 📁 File Structure

```
decodelabs-expense-tracker/
├── expense_tracker.py    # Main application
├── expenses_data.json    # Auto-generated on first run (gitignored)
├── LICENSE
└── README.md
```

---

## 💡 What I Learned

By building this project I practised:

- **Accumulator pattern** — maintaining running totals across loop iterations
- **Nested data structures** — expenses as a list of dicts inside a parent dict
- **Date-based filtering** — slicing `YYYY-MM-DD` strings for monthly grouping
- **Budget logic** — percentage-based threshold alerts on every transaction
- **Financial aggregation** — grouping, summing, and sorting by category

---

## 👩‍💻 Author

**Divya Bharti**
Python Programming Intern | DecodeLabs Batch 2026
