# RE → NFA → DFA Converter

A Python 3 command-line project that converts regular expressions over the fixed
alphabet `{0, 1}` into an NFA using **Thompson's Construction**, then converts
that NFA into a DFA using **Subset Construction**.

## Requirements
- Python 3.8 or newer
- No third-party packages (Python standard library only)

## Run
Open a terminal in this folder and run:

```bash
python regex_converter.py "(0|1)*011"
```

Or run without an argument and type the expression when prompted:

```bash
python regex_converter.py
```

The program prints the NFA and DFA 5-tuples, all transitions, the DFA subset
mapping, and its dead-state convention.

## Supported syntax
| Syntax | Meaning | Example |
|---|---|---|
| `0`, `1` | Binary symbols | `0` |
| `RS` | Concatenation | `01` |
| `R|S` | Union | `0|1` |
| `R*` | Zero or more | `0*` |
| `R+` | One or more | `1+` |
| `(R)` | Grouping | `(0|1)` |

Precedence: unary `*` and `+`, then concatenation, then `|`.
Only `0` and `1` are allowed as input symbols. Invalid symbols and malformed
expressions produce an error with a useful position/message.

## Run tests
From this folder:

```bash
python -m unittest discover -s tests -v
```

The tests cover all suggested expressions, invalid alphabet/syntax, `+`
semantics, and the requirement that each DFA state has transitions for both
`0` and `1`.

## Project files
- `regex_converter.py` — parser, Thompson NFA builder, subset construction,
  output formatting, and simulators.
- `tests/test_converter.py` — automated tests.
- `REPORT.md` — short project report with three complete example outputs.
- `sample_runs.txt` — sample successful and rejected runs.
- `CHECKLIST.md` — submission and run checklist.
