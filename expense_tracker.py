# ============================================================
#  DecodeLabs Industrial Training Kit — Project 2
#  Expense Tracker | Batch 2026
#  Author : [Your Name]
# ============================================================

def main():
    print("=" * 45)
    print("   💰  DecodeLabs Expense Tracker  💰")
    print("=" * 45)
    print("  Enter expense amounts one by one.")
    print("  Type 'quit' to finish and see total.")
    print("=" * 45)

    total = 0          # Accumulator — initialized OUTSIDE the loop

    while True:
        user_input = input("\nEnter expense amount (or 'quit'): ").strip()

        # Kill switch / sentinel value
        if user_input.lower() == "quit":
            break

        # Defensive coding — Poka-Yoke / type-safety gate
        try:
            expense = float(user_input)
            if expense < 0:
                print("⚠️  Negative values not allowed. Try again.")
                continue
        except ValueError:
            print("❌  Invalid input. Please enter a number.")
            continue

        # Accumulator pattern: State(new) = State(old) + Input
        total += expense
        print(f"✅  Added: ${expense:,.2f}  |  Running Total: ${total:,.2f}")

    # Phase 3: Output — decouple logic from display
    print("\n" + "=" * 45)
    print(f"   FINAL TOTAL SPENT:  ${total:,.2f}")
    print("=" * 45)


if __name__ == "__main__":
    main()
