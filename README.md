# 💰 DecodeLabs Expense Tracker

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-success)

**A comprehensive Python expense tracking application demonstrating the accumulator pattern, input validation, and defensive coding practices.**

## 📋 Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [Learning Outcomes](#learning-outcomes)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

- ✅ **Add Expenses**: Track expenses by category and amount
- ✅ **View Expenses**: Display all recorded expenses in a structured format
- ✅ **Calculate Totals**: Automatically sum expenses by category or overall
- ✅ **Input Validation**: Robust error handling for user inputs
- ✅ **Data Persistence**: Save/load expenses from file storage
- ✅ **Menu-Driven Interface**: Easy-to-use CLI navigation
- ✅ **Budget Tracking**: Monitor spending against budget limits

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/divyadhankhar2008-byte/decodelabs-expense-tracker.git
   cd decodelabs-expense-tracker
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 💻 Usage

### Running the Application

```bash
python main.py
```

### Menu Options

```
=== Expense Tracker Menu ===
1. Add Expense
2. View All Expenses
3. View Expenses by Category
4. Calculate Total Expenses
5. Set Budget Limit
6. View Budget Status
7. Exit
```

### Example Workflow

```python
# Start application
$ python main.py

# Add expenses
Enter expense amount: 50.00
Enter category: Food
Expense added successfully!

# View summary
Total Expenses: $150.00
Food: $50.00
Transport: $30.00
```

## 📁 Project Structure

```
decodelabs-expense-tracker/
├── main.py                 # Main application entry point
├── expense_tracker.py      # Core expense tracking logic
├── utils/
│   ├── __init__.py
│   └── validators.py       # Input validation functions
├── data/
│   └── expenses.json       # Stored expense records
├── tests/
│   ├── __init__.py
│   ├── test_expense_tracker.py
│   └── test_validators.py
├── requirements.txt        # Project dependencies
├── .gitignore
├── README.md
└── LICENSE
```

## 🛠 Technologies Used

- **Python 3.8+**: Core language
- **JSON**: Data persistence
- **pytest**: Unit testing framework
- **flake8**: Code linting
- **black**: Code formatting
- **mypy**: Static type checking
- **GitHub Actions**: CI/CD automation

## 📚 Learning Outcomes

This project demonstrates:

1. **Accumulator Pattern**
   - Using variables to collect and aggregate data
   - Implementing running totals and sums

2. **Input Validation**
   - Type checking and error handling
   - User-friendly error messages
   - Try-except blocks for exception handling

3. **Defensive Coding**
   - Validating data before processing
   - Edge case handling
   - Secure file operations

4. **Code Organization**
   - Module separation
   - Function decomposition
   - Clear naming conventions

5. **Data Management**
   - File I/O operations
   - JSON serialization
   - Data structure design

## 🧪 Testing

### Run All Tests

```bash
pytest
```

### Run with Coverage Report

```bash
pytest --cov=. --cov-report=html
```

### Run Specific Test

```bash
pytest tests/test_expense_tracker.py::test_add_expense -v
```

## 🔍 Code Quality

### Lint Code

```bash
flake8 .
pylint *.py
```

### Format Code

```bash
black .
```

### Type Check

```bash
mypy .
```

## 📈 Future Enhancements

- [ ] Add data visualization (charts/graphs)
- [ ] Implement recurring expense categories
- [ ] Add monthly/yearly reports
- [ ] Database integration (SQLite)
- [ ] Web interface (Flask/Django)
- [ ] Mobile app support

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## 👤 Author

**Divya Bharti**
- GitHub: [@divyadhankhar2008-byte](https://github.com/divyadhankhar2008-byte)
- DecodeLabs Industrial Training Kit - Project 2, Batch 2026

## 📞 Support

If you encounter any issues or have questions:

1. Check existing [GitHub Issues](https://github.com/divyadhankhar2008-byte/decodelabs-expense-tracker/issues)
2. Create a new issue with detailed description
3. Include error messages and steps to reproduce

---

**Made with ❤️ during DecodeLabs Internship 2026**
