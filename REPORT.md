# Project Report: Regular Expression → NFA → DFA Converter

## 1. Overview
This project accepts a regular expression over the fixed binary alphabet
`Σ = {0, 1}`. It builds an NFA using Thompson's Construction and converts the
result into a DFA using the Subset Construction algorithm.

## 2. Parsing approach
A recursive-descent parser builds an abstract syntax tree (AST). Operator
precedence is:
1. `*` and `+` (highest)
2. Implicit concatenation
3. `|` (lowest)

Parentheses override precedence. The parser validates every character before
parsing. Any character outside `0`, `1`, `(`, `)`, `|`, `*`, and `+` is rejected.
Malformed expressions such as `0|`, `*0`, or unmatched parentheses are also
rejected.

## 3. NFA construction
Each AST node is converted bottom-up into a fragment with one start state and
one accepting state:
- Symbol: two states and one symbol transition.
- Concatenation: epsilon transition from the first fragment's accept state to
  the second fragment's start state.
- Union: new start and accept states with epsilon branches/joins.
- Kleene star: new start and accept states, including the skip and repeat
  epsilon transitions.
- Plus: implemented as `R R*`, ensuring at least one occurrence.

The final fragment's start is `q0`; its sole accept state forms `F`.

## 4. NFA to DFA
The implementation computes `ε-closure(T)` and `move(T, a)`. Starting from
`ε-closure({q0})`, it discovers reachable subsets in a worklist. DFA states
are labelled `D0`, `D1`, etc. A DFA subset is accepting if it contains the NFA
accepting state.

**Undefined-transition convention:** an explicit empty subset `∅` is added as
a dead/trap state whenever it is reachable. It loops to itself on both `0`
and `1`. Therefore every printed DFA state has exactly two outgoing
transitions.

## 5. Example 5-tuples

The following are complete program outputs for three sample expressions.
State numbering is deterministic for this implementation.

### Example A — `0`

```text
NFA 5-tuple:
Q = {0, 1}
Σ = {0, 1}
δ:
  0 --0--> {1}
q0 = 0
F = {1}

DFA 5-tuple:
Q = {D0, D1, D2}
Σ = {0, 1}
δ:
  D0 --0--> D1
  D0 --1--> D2
  D1 --0--> D2
  D1 --1--> D2
  D2 --0--> D2
  D2 --1--> D2
q0 = D0
F = {D1}
State mapping:
  D0 = {0}
  D1 = {1}
  D2 = {}
Convention: the empty subset ∅ is included as a dead/trap state when reachable.
```

### Example B — `0|1`

```text
NFA 5-tuple:
Q = {0, 1, 2, 3, 4, 5}
Σ = {0, 1}
δ:
  0 --ε--> {2, 4}
  2 --0--> {3}
  3 --ε--> {1}
  4 --1--> {5}
  5 --ε--> {1}
q0 = 0
F = {1}

DFA 5-tuple:
Q = {D0, D1, D2, D3}
Σ = {0, 1}
δ:
  D0 --0--> D1
  D0 --1--> D2
  D1 --0--> D3
  D1 --1--> D3
  D2 --0--> D3
  D2 --1--> D3
  D3 --0--> D3
  D3 --1--> D3
q0 = D0
F = {D1, D2}
State mapping:
  D0 = {0, 2, 4}
  D1 = {1, 3}
  D2 = {1, 5}
  D3 = {}
Convention: the empty subset ∅ is included as a dead/trap state when reachable.
```

### Example C — `1+`

```text
NFA 5-tuple:
Q = {0, 1, 2, 3, 4, 5}
Σ = {0, 1}
δ:
  0 --1--> {1}
  1 --ε--> {2}
  2 --ε--> {3, 4}
  4 --1--> {5}
  5 --ε--> {3, 4}
q0 = 0
F = {3}

DFA 5-tuple:
Q = {D0, D1, D2, D3}
Σ = {0, 1}
δ:
  D0 --0--> D1
  D0 --1--> D2
  D1 --0--> D1
  D1 --1--> D1
  D2 --0--> D1
  D2 --1--> D3
  D3 --0--> D1
  D3 --1--> D3
q0 = D0
F = {D2, D3}
State mapping:
  D0 = {0}
  D1 = {}
  D2 = {1, 2, 3, 4}
  D3 = {3, 4, 5}
Convention: the empty subset ∅ is included as a dead/trap state when reachable.
```

## 6. NFA vs DFA state-count comparison

| Regular expression | NFA states | DFA states |
|---|---:|---:|
| `0` | 2 | 3 |
| `0|1` | 6 | 4 |
| `1+` | 6 | 4 |

The DFA count includes the explicit dead state if it is reachable.

## 7. Testing
Automated tests compare NFA and DFA acceptance for all binary strings of
length 0 through 5 for the nine expressions suggested in the assignment.
Additional tests cover invalid symbols (`a`, `012`), malformed syntax
(`0|`, `|0`, `*0`, unmatched parentheses), plus semantics, and total DFA
transitions.

## 8. Assumptions and limitations
- The alphabet is fixed to `{0, 1}`.
- Empty regular expressions and empty groups `()` are not supported.
- No escape syntax or other regex features (such as `?`, `.`, character
  classes, or `{m,n}`) are supported.
- `*` and `+` may be repeated syntactically; the parser applies them in order.
- DFA states are reachable subsets only; the empty subset is included only
  when a transition reaches it.
