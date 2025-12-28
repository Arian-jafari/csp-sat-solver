# CSP-based SAT Solver

This project implements a SAT (Boolean Satisfiability) solver using **Constraint Satisfaction Problem (CSP)** techniques in Python. It supports **hard and soft clauses** with optional heuristics to improve solving efficiency. A **PyQt6 GUI** is provided for interactive testing of CNF formulas.

## Features

- Handles CNF formulas with **hard and soft clauses**.
- Implements CSP heuristics:
  - **MRV** (Minimum Remaining Value)
  - **MCV** (Most Constraining Variable)
  - **LCV** (Least Constraining Value)
- Solves problems using **backtracking** and **branch-and-bound**.
- GUI interface for:
  - Loading CNF files
  - Selecting heuristics
  - Displaying results and execution time

## Installation

1. Clone the repository:
```bash
git clone https://github.com/<your-username>/csp-sat-solver.git
cd csp-sat-solver
```

2. Install dependencies:
```bash
pip install PyQt6
```
## Usage
1. Run the GUI application:
```bash
python main.py
```
2. Use the interface to:
- Select a CNF test file.
- Choose which heuristics to apply (MRV, MCV, LCV).
- Solve the SAT problem and view results.

## File Structure

- cnf.py – Handles CNF formula evaluation and clause weights.
- csp.py – Implements the CSP solver with heuristics and branch-and-bound.
- ui.py – PyQt6 GUI interface.
- main.py – Entry point for running the GUI.
- tests/ – Contains CNF test cases to try with the solver.

## Tests

The tests folder contains example CNF files that can be loaded directly in the GUI or used for automated testing. The files follow the format:

- First line: <num_vars> <num_hard_clauses> <num_soft_clauses>
- Hard clauses: one clause per line
- Soft clauses: start with SOFT_CLAUSE, followed by literals, ending with weight
- Literals can be variables (e.g., x1) or negations (e.g., ~x2)
