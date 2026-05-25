# 💰 Expense Tracker — Project 2

> **DecodeLabs Industrial Training Kit | Batch 2026**

---

## 📌 Project Overview

A command-line Python script that continuously accepts expense amounts from the user, accumulates them in real-time, and displays the **Total Spent** when the user quits. This project demonstrates the core backend engineering concept of **stateful data accumulation**.

---

## 🎯 Key Concepts Demonstrated

| Concept | Implementation |
|---|---|
| **IPO Model** | Input → Process → Output pipeline |
| **Accumulator Pattern** | `total += expense` — state preserved across iterations |
| **Type Safety (Gatekeeper)** | `float(input())` converts raw string to number |
| **Defensive Coding (Poka-Yoke)** | `try / except ValueError` blocks invalid input |
| **Kill Switch / Sentinel Value** | `'quit'` command breaks the loop gracefully |
| **State Anatomy** | `total = 0` initialized **outside** the loop |

---

## 🚀 How to Run

### Prerequisites
- Python 3.x installed

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/decodelabs-expense-tracker.git

# 2. Navigate into the folder
cd decodelabs-expense-tracker

# 3. Run the script
python expense_tracker.py
```

---

## 🖥️ Sample Output

```
=============================================
   💰  DecodeLabs Expense Tracker  💰
=============================================
  Enter expense amounts one by one.
  Type 'quit' to finish and see total.
=============================================

Enter expense amount (or 'quit'): 100
✅  Added: $100.00  |  Running Total: $100.00

Enter expense amount (or 'quit'): 50
✅  Added: $50.00   |  Running Total: $150.00

Enter expense amount (or 'quit'): 20
✅  Added: $20.00   |  Running Total: $170.00

Enter expense amount (or 'quit'): ten
❌  Invalid input. Please enter a number.

Enter expense amount (or 'quit'): quit

=============================================
   FINAL TOTAL SPENT:  $170.00
=============================================
```

---

## ✅ Quality Checklist (Audit Standard)

- [x] **Stability** — Handles 5+ transactions without crashing
- [x] **State** — `total` initialized **outside** the loop
- [x] **Defense** — Catches `ValueError` on invalid input
- [x] **Control** — Kill switch (`quit`) prints final total on exit
- [x] **Negative Guard** — Rejects negative expense values

---

## 📁 Project Structure

```
decodelabs-expense-tracker/
│
├── expense_tracker.py   # Main script
└── README.md            # Project documentation
```

---

## 🏢 About DecodeLabs

**DecodeLabs** is an industrial training platform based in Greater Lucknow, India, focused on building real-world Python and backend development skills.

- 🌐 [www.decodelabs.tech](http://www.decodelabs.tech)
- 📧 decodelabs.tech@gmail.com
- 📞 +91 89330 06408

---

*Built with 💻 as part of the DecodeLabs Python Programming Industrial Training — Batch 2026*
