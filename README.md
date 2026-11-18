# Regular-Expression-to-NFA-DFA-Converter
A Python implementation of Thompson's Construction and Subset Construction to convert Regular Expressions into NFA and DFA.
# Regular Expression to NFA and DFA Converter

## Project Overview
This project implements a Regular Expression Converter using Python. It converts regular expressions into Non-deterministic Finite Automata (NFA) using Thompson's Construction, then converts the NFA into a Deterministic Finite Automaton (DFA) using the Subset Construction algorithm.

## Features
- Supports the binary alphabet `{0, 1}`.
- Supports Union (`|`), Kleene Star (`*`), Plus (`+`), and Parentheses.
- Supports implicit concatenation.
- Applies operator precedence correctly.
- Constructs NFA using Thompson's Construction.
- Converts NFA into DFA using Subset Construction.
- Calculates epsilon-closure and move operations.
- Displays NFA and DFA 5-tuples.
- Displays DFA state mapping.
- Handles invalid expressions and unsupported symbols.
- Includes automated unit tests.

## Technologies
- Python 3
- Python Standard Library
- Regular Expressions
- Finite Automata Theory

## Supported Operators

| Operator | Meaning | Example |
|---|---|---|
| `|` | Union | `0|1` |
| `*` | Zero or more | `0*` |
| `+` | One or more | `1+` |
| Concatenation | Sequence | `01` |
| `( )` | Grouping | `(0|1)*` |

## Algorithms
1. Recursive Descent Parsing.
2. Thompson's Construction (Regex to NFA).
3. Epsilon Closure and Move.
4. Subset Construction (NFA to DFA).

## How to Run

Make sure Python 3.8 or later is installed.

Run a regular expression:

```bash
python regex_converter.py "(0|1)*011"
```

Or start interactive mode:

```bash
python regex_converter.py
```

## Run Tests

```bash
python -m unittest discover -s tests -v
```

## Example Input

```text
(0|1)*011
```

The program displays:
- NFA 5-tuple.
- DFA 5-tuple.
- DFA state mapping.
- Dead state convention.

## Testing
The project includes the nine suggested regular expressions and tests for invalid inputs such as `a`, `012`, and `0|`.

## Error Handling
The program rejects unsupported symbols and invalid regular-expression syntax with clear error messages.

## Dead State Convention
An empty subset is included as a dead/trap state whenever it is reachable. It loops on both input symbols `0` and `1`.

## Project Structure

```text
RE_NFA_DFA_Converter/
│
├── regex_converter.py
├── tests/
│   └── test_converter.py
├── README.md
├── REPORT.md
├── sample_runs.txt
├── CHECKLIST.md
└── VERIFICATION.txt
```

## Author
**Negma Abderhman**

## License
This project is available for educational purposes.
