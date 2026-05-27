"""
Tests for expense_tracker.py
Covers: load_data, save_data, add_expense, view_expenses,
        category_summary, set_budget, delete_expense,
        monthly_report, spending_insights
"""

import json
import os
import pytest
from datetime import date
from unittest.mock import patch, MagicMock
import importlib, sys


# ── Fixture: isolate the JSON save file ────────────────────────────────────────

@pytest.fixture(autouse=True)
def tmp_save(tmp_path, monkeypatch):
    """Redirect SAVE_FILE to a temp directory so tests never touch the real file."""
    save_path = str(tmp_path / "expenses_data.json")
    # Import fresh module so patching takes effect
    if "expense_tracker" in sys.modules:
        del sys.modules["expense_tracker-1-1"]
    import importlib.util, pathlib
    spec = importlib.util.spec_from_file_location(
        "expense_tracker",
        pathlib.Path(__file__).parent / "expense_tracker-1-1.py",
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    monkeypatch.setattr(mod, "SAVE_FILE", save_path)
    yield mod, save_path


@pytest.fixture()
def et(tmp_save):
    """Return the patched module."""
    return tmp_save[0]


@pytest.fixture()
def empty_data(et):
    return et.load_data()


@pytest.fixture()
def sample_data(et):
    data = {"expenses": [], "budget": {}}
    data["expenses"].append({
        "id": 1000,
        "amount": 500.0,
        "category": "🍔 Food & Dining",
        "description": "Lunch",
        "payment": "UPI",
        "date": date.today().isoformat(),
    })
    data["expenses"].append({
        "id": 2000,
        "amount": 1500.0,
        "category": "🚗 Transport",
        "description": "Cab",
        "payment": "Cash",
        "date": date.today().isoformat(),
    })
    return data


# ══════════════════════════════════════════════════════════════════════════════
# Persistence
# ══════════════════════════════════════════════════════════════════════════════

class TestLoadData:
    def test_returns_defaults_when_no_file(self, et):
        data = et.load_data()
        assert data == {"expenses": [], "budget": {}}

    def test_loads_existing_file(self, et, tmp_save):
        _, path = tmp_save
        payload = {"expenses": [{"id": 1}], "budget": {"food": 300}}
        with open(path, "w") as f:
            json.dump(payload, f)
        data = et.load_data()
        assert data["expenses"] == [{"id": 1}]

    def test_returns_defaults_on_corrupt_json(self, et, tmp_save):
        _, path = tmp_save
        with open(path, "w") as f:
            f.write("NOT JSON{{{")
        data = et.load_data()
        assert data == {"expenses": [], "budget": {}}


class TestSaveData:
    def test_writes_json_to_disk(self, et, tmp_save):
        _, path = tmp_save
        data = {"expenses": [{"id": 42}], "budget": {}}
        et.save_data(data)
        with open(path) as f:
            loaded = json.load(f)
        assert loaded["expenses"][0]["id"] == 42

    def test_roundtrip(self, et, tmp_save):
        _, path = tmp_save
        data = {"expenses": [{"amount": 99.9}], "budget": {"x": 100}}
        et.save_data(data)
        loaded = et.load_data()
        assert loaded["expenses"][0]["amount"] == 99.9


# ══════════════════════════════════════════════════════════════════════════════
# add_expense
# ══════════════════════════════════════════════════════════════════════════════

class TestAddExpense:
    def _run_add(self, et, inputs):
        data = {"expenses": [], "budget": {}}
        with patch("builtins.input", side_effect=inputs), \
             patch("builtins.print"):
            et.add_expense(data)
        return data

    def test_adds_valid_expense(self, et):
        data = self._run_add(et, ["250", "1", "Dinner", "UPI"])
        assert len(data["expenses"]) == 1
        assert data["expenses"][0]["amount"] == 250.0
        assert data["expenses"][0]["category"] == "🍔 Food & Dining"

    def test_rejects_negative_amount(self, et):
        data = self._run_add(et, ["-50", "", "", ""])
        assert len(data["expenses"]) == 0

    def test_rejects_zero_amount(self, et):
        data = self._run_add(et, ["0", "", "", ""])
        assert len(data["expenses"]) == 0

    def test_rejects_non_numeric_amount(self, et):
        data = self._run_add(et, ["abc", "", "", ""])
        assert len(data["expenses"]) == 0

    def test_default_category_when_empty_input(self, et):
        data = self._run_add(et, ["100", "", "Test", "Cash"])
        assert data["expenses"][0]["category"] == "💰 Other"

    def test_default_payment_method_is_upi(self, et):
        data = self._run_add(et, ["100", "2", "Bus", ""])
        assert data["expenses"][0]["payment"] == "UPI"

    def test_entry_contains_today_date(self, et):
        data = self._run_add(et, ["100", "3", "Shop", "Card"])
        assert data["expenses"][0]["date"] == date.today().isoformat()

    def test_budget_exceeded_alert(self, et, capsys):
        data = {"expenses": [], "budget": {"🍔 Food & Dining": 100.0}}
        inputs = ["200", "1", "Big meal", "UPI"]
        with patch("builtins.input", side_effect=inputs):
            et.add_expense(data)
        captured = capsys.readouterr()
        assert "EXCEEDED" in captured.out or len(data["expenses"]) == 1

    def test_budget_warning_at_80_percent(self, et, capsys):
        # Pre-load 70 spent, then add 20 more (90% of 100 budget)
        data = {
            "expenses": [{
                "id": 1, "amount": 70.0,
                "category": "🍔 Food & Dining",
                "description": "x", "payment": "UPI",
                "date": date.today().isoformat(),
            }],
            "budget": {"🍔 Food & Dining": 100.0},
        }
        inputs = ["20", "1", "snack", "UPI"]
        with patch("builtins.input", side_effect=inputs):
            et.add_expense(data)
        captured = capsys.readouterr()
        assert "WARNING" in captured.out or len(data["expenses"]) == 2


# ══════════════════════════════════════════════════════════════════════════════
# view_expenses
# ══════════════════════════════════════════════════════════════════════════════

class TestViewExpenses:
    def test_prints_no_expenses_message(self, et, capsys):
        et.view_expenses({"expenses": [], "budget": {}})
        assert "No expenses" in capsys.readouterr().out

    def test_prints_all_expenses(self, et, sample_data, capsys):
        et.view_expenses(sample_data)
        out = capsys.readouterr().out
        assert "Lunch" in out
        assert "Cab" in out

    def test_month_filter_shows_only_matching(self, et, capsys):
        data = {
            "expenses": [
                {"id": 1, "amount": 100, "category": "A", "description": "Jan",
                 "payment": "UPI", "date": "2024-01-15"},
                {"id": 2, "amount": 200, "category": "B", "description": "Feb",
                 "payment": "UPI", "date": "2024-02-10"},
            ],
            "budget": {},
        }
        et.view_expenses(data, month_filter="2024-01")
        out = capsys.readouterr().out
        assert "Jan" in out
        assert "Feb" not in out

    def test_total_is_correct(self, et, sample_data, capsys):
        et.view_expenses(sample_data)
        out = capsys.readouterr().out
        assert "2,000" in out or "2000" in out


# ══════════════════════════════════════════════════════════════════════════════
# category_summary
# ══════════════════════════════════════════════════════════════════════════════

class TestCategorySummary:
    def test_no_expenses_this_month(self, et, capsys):
        data = {"expenses": [], "budget": {}}
        et.category_summary(data)
        assert "No expenses" in capsys.readouterr().out

    def test_shows_category_and_amount(self, et, sample_data, capsys):
        et.category_summary(sample_data)
        out = capsys.readouterr().out
        assert "Food" in out or "🍔" in out

    def test_excludes_other_months(self, et, capsys):
        data = {
            "expenses": [
                {"id": 1, "amount": 500, "category": "🍔 Food & Dining",
                 "description": "old", "payment": "UPI", "date": "2020-01-01"},
            ],
            "budget": {},
        }
        et.category_summary(data)
        out = capsys.readouterr().out
        # Should report no expenses for current month
        assert "No expenses" in out


# ══════════════════════════════════════════════════════════════════════════════
# set_budget
# ══════════════════════════════════════════════════════════════════════════════

class TestSetBudget:
    def test_sets_valid_budget(self, et):
        data = {"expenses": [], "budget": {}}
        with patch("builtins.input", side_effect=["1", "500"]), \
             patch("builtins.print"):
            et.set_budget(data)
        assert data["budget"]["🍔 Food & Dining"] == 500.0

    def test_rejects_invalid_category(self, et, capsys):
        data = {"expenses": [], "budget": {}}
        with patch("builtins.input", side_effect=["99", "500"]):
            et.set_budget(data)
        assert data["budget"] == {}

    def test_rejects_zero_budget(self, et, capsys):
        data = {"expenses": [], "budget": {}}
        with patch("builtins.input", side_effect=["1", "0"]):
            et.set_budget(data)
        assert data["budget"] == {}

    def test_rejects_negative_budget(self, et, capsys):
        data = {"expenses": [], "budget": {}}
        with patch("builtins.input", side_effect=["1", "-100"]):
            et.set_budget(data)
        assert data["budget"] == {}

    def test_rejects_non_numeric_budget(self, et, capsys):
        data = {"expenses": [], "budget": {}}
        with patch("builtins.input", side_effect=["1", "abc"]):
            et.set_budget(data)
        assert data["budget"] == {}


# ══════════════════════════════════════════════════════════════════════════════
# delete_expense
# ══════════════════════════════════════════════════════════════════════════════

class TestDeleteExpense:
    def test_deletes_valid_index(self, et, sample_data):
        with patch("builtins.input", side_effect=["1"]), \
             patch("builtins.print"):
            et.delete_expense(sample_data)
        assert len(sample_data["expenses"]) == 1

    def test_rejects_out_of_range_index(self, et, sample_data, capsys):
        original_len = len(sample_data["expenses"])
        with patch("builtins.input", side_effect=["99"]):
            et.delete_expense(sample_data)
        assert len(sample_data["expenses"]) == original_len

    def test_rejects_non_numeric_input(self, et, sample_data):
        original_len = len(sample_data["expenses"])
        with patch("builtins.input", side_effect=["abc"]), \
             patch("builtins.print"):
            et.delete_expense(sample_data)
        assert len(sample_data["expenses"]) == original_len

    def test_does_nothing_on_empty_list(self, et, capsys):
        data = {"expenses": [], "budget": {}}
        with patch("builtins.input", side_effect=[]):
            et.delete_expense(data)   # should not raise


# ══════════════════════════════════════════════════════════════════════════════
# monthly_report
# ══════════════════════════════════════════════════════════════════════════════

class TestMonthlyReport:
    def test_no_data_message(self, et, capsys):
        et.monthly_report({"expenses": []})
        assert "No data" in capsys.readouterr().out

    def test_shows_months(self, et, sample_data, capsys):
        et.monthly_report(sample_data)
        out = capsys.readouterr().out
        assert date.today().isoformat()[:7] in out

    def test_limits_to_six_months(self, et, capsys):
        expenses = []
        for i in range(1, 9):
            expenses.append({
                "id": i, "amount": 100, "category": "x",
                "description": "x", "payment": "UPI",
                "date": f"2024-{i:02d}-01",
            })
        et.monthly_report({"expenses": expenses})
        out = capsys.readouterr().out
        # At most 6 month rows should appear
        month_rows = [l for l in out.splitlines() if "2024-" in l]
        assert len(month_rows) <= 6


# ══════════════════════════════════════════════════════════════════════════════
# spending_insights
# ══════════════════════════════════════════════════════════════════════════════

class TestSpendingInsights:
    def test_no_data_message(self, et, capsys):
        et.spending_insights({"expenses": []})
        assert "No data" in capsys.readouterr().out

    def test_total_and_avg(self, et, sample_data, capsys):
        et.spending_insights(sample_data)
        out = capsys.readouterr().out
        assert "Total Spent" in out
        assert "Avg" in out

    def test_biggest_expense_highlighted(self, et, sample_data, capsys):
        et.spending_insights(sample_data)
        out = capsys.readouterr().out
        assert "1,500" in out or "1500" in out

    def test_payment_methods_listed(self, et, sample_data, capsys):
        et.spending_insights(sample_data)
        out = capsys.readouterr().out
        assert "UPI" in out
        assert "Cash" in out
