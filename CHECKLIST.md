# Final Checklist

## A. Before running
- [ ] Python 3.8+ is installed.
- [ ] The ZIP file has been extracted.
- [ ] A terminal is opened inside the extracted `RE_NFA_DFA_Converter` folder.

## B. Run the project
- [ ] Run `python regex_converter.py "(0|1)*011"`.
- [ ] Confirm that both **NFA 5-tuple** and **DFA 5-tuple** appear.
- [ ] Confirm NFA output includes `Q`, `Σ`, `δ`, `q0`, and `F`.
- [ ] Confirm DFA output includes `Q`, `Σ`, `δ`, `q0`, and `F`.
- [ ] Confirm the DFA state mapping (`D0 = {...}` etc.) appears.
- [ ] Confirm every DFA state has exactly one `0` transition and one `1` transition.
- [ ] Confirm the dead/trap-state convention is printed.

## C. Test required expressions
Run each command and check that it completes without an error:

- [ ] `python regex_converter.py "0"`
- [ ] `python regex_converter.py "01"`
- [ ] `python regex_converter.py "0|1"`
- [ ] `python regex_converter.py "0*"`
- [ ] `python regex_converter.py "1+"`
- [ ] `python regex_converter.py "(0|1)*011"`
- [ ] `python regex_converter.py "0(0|1)*1"`
- [ ] `python regex_converter.py "(0|1)*"`
- [ ] `python regex_converter.py "(01)+"`

## D. Test error handling
- [ ] `python regex_converter.py "a"` → invalid symbol error.
- [ ] `python regex_converter.py "012"` → invalid symbol `2`.
- [ ] `python regex_converter.py "0|"` → missing-expression error.
- [ ] `python regex_converter.py "*0"` → operator-without-operand error.

## E. Automated tests
- [ ] Run `python -m unittest discover -s tests -v`.
- [ ] Confirm all tests pass (`OK`).
- [ ] Keep a screenshot of the successful test output for submission if required.

## F. Submission contents
- [ ] `regex_converter.py` source code is included.
- [ ] `tests/test_converter.py` is included.
- [ ] `REPORT.md` contains parsing approach and algorithm descriptions.
- [ ] Report includes three NFA/DFA 5-tuple examples.
- [ ] Report includes NFA vs DFA state-count table.
- [ ] Report states the undefined-transition/dead-state convention.
- [ ] Report includes assumptions and limitations.
- [ ] `sample_runs.txt` demonstrates successful conversions and a rejected input.
- [ ] Add your name, ID, course, and instructor to the report if your instructor requires them.
- [ ] Capture your own terminal screenshots if the instructor specifically asks for screenshots rather than text logs.
