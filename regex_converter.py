#!/usr/bin/env python3
"""
Regular Expression -> NFA (Thompson) -> DFA (Subset Construction)
Supported alphabet: {0, 1}; operators: |, *, +, and parentheses.
Python standard library only.
"""

from dataclasses import dataclass
from collections import defaultdict, deque
import argparse
import sys


ALPHABET = ("0", "1")
EPSILON = "ε"
VALID_CHARS = set("01()|*+")


class RegexError(ValueError):
    """Raised when a regular expression is invalid."""


@dataclass(frozen=True)
class Node:
    kind: str
    value: str = ""
    left: object = None
    right: object = None


class Parser:
    """Recursive-descent parser: unary (*,+) > concatenation > union."""

    def __init__(self, pattern):
        self.pattern = pattern
        self.pos = 0

    def parse(self):
        if not self.pattern:
            raise RegexError("Error: regular expression is empty.")
        for i, ch in enumerate(self.pattern):
            if ch not in VALID_CHARS:
                raise RegexError(
                    f"Error: invalid symbol {ch!r} at position {i + 1}; "
                    "alphabet is restricted to {0, 1}."
                )
        node = self.parse_union()
        if self.pos != len(self.pattern):
            ch = self.pattern[self.pos]
            raise RegexError(
                f"Error: unexpected character {ch!r} at position {self.pos + 1}."
            )
        return node

    def peek(self):
        return self.pattern[self.pos] if self.pos < len(self.pattern) else None

    def parse_union(self):
        node = self.parse_concat()
        while self.peek() == "|":
            self.pos += 1
            if self.peek() in (None, ")", "|", "*", "+"):
                raise RegexError(f"Error: missing expression after '|' at position {self.pos}.")
            right = self.parse_concat()
            node = Node("union", left=node, right=right)
        return node

    def parse_concat(self):
        if self.peek() is None or self.peek() in (")", "|"):
            raise RegexError(f"Error: expected an expression at position {self.pos + 1}.")
        node = self.parse_unary()
        while self.peek() is not None and self.peek() not in (")", "|"):
            node = Node("concat", left=node, right=self.parse_unary())
        return node

    def parse_unary(self):
        node = self.parse_atom()
        while self.peek() in ("*", "+"):
            op = self.peek()
            self.pos += 1
            node = Node("star" if op == "*" else "plus", left=node)
        return node

    def parse_atom(self):
        ch = self.peek()
        if ch in ("0", "1"):
            self.pos += 1
            return Node("symbol", value=ch)
        if ch == "(":
            self.pos += 1
            if self.peek() == ")":
                raise RegexError(f"Error: empty parentheses at position {self.pos}.")
            node = self.parse_union()
            if self.peek() != ")":
                raise RegexError(f"Error: missing ')' for '(' at position {self.pos}.")
            self.pos += 1
            return node
        if ch == ")":
            raise RegexError(f"Error: unexpected ')' at position {self.pos + 1}.")
        if ch in ("*", "+"):
            raise RegexError(f"Error: operator {ch!r} has no preceding expression at position {self.pos + 1}.")
        if ch == "|":
            raise RegexError(f"Error: missing expression before '|' at position {self.pos + 1}.")
        raise RegexError(f"Error: expected 0, 1, or '(' at position {self.pos + 1}.")


class NFA:
    def __init__(self):
        self.states = set()
        self.transitions = defaultdict(lambda: defaultdict(set))
        self.start = None
        self.accept = None

    def new_state(self):
        state = len(self.states)
        self.states.add(state)
        return state

    def add(self, source, symbol, target):
        self.transitions[source][symbol].add(target)


def thompson(node, nfa):
    """Return (start, accept) for an AST node."""
    if node.kind == "symbol":
        start, accept = nfa.new_state(), nfa.new_state()
        nfa.add(start, node.value, accept)
        return start, accept

    if node.kind == "concat":
        s1, f1 = thompson(node.left, nfa)
        s2, f2 = thompson(node.right, nfa)
        nfa.add(f1, EPSILON, s2)
        return s1, f2

    if node.kind == "union":
        start, accept = nfa.new_state(), nfa.new_state()
        s1, f1 = thompson(node.left, nfa)
        s2, f2 = thompson(node.right, nfa)
        nfa.add(start, EPSILON, s1)
        nfa.add(start, EPSILON, s2)
        nfa.add(f1, EPSILON, accept)
        nfa.add(f2, EPSILON, accept)
        return start, accept

    if node.kind == "star":
        start, accept = nfa.new_state(), nfa.new_state()
        sub_start, sub_accept = thompson(node.left, nfa)
        nfa.add(start, EPSILON, sub_start)
        nfa.add(start, EPSILON, accept)
        nfa.add(sub_accept, EPSILON, sub_start)
        nfa.add(sub_accept, EPSILON, accept)
        return start, accept

    if node.kind == "plus":
        # R+ = RR*: the first copy guarantees at least one occurrence.
        first_start, first_accept = thompson(node.left, nfa)
        star_start, star_accept = thompson(Node("star", left=node.left), nfa)
        nfa.add(first_accept, EPSILON, star_start)
        return first_start, star_accept

    raise ValueError(f"Unknown AST node kind: {node.kind}")


def build_nfa(pattern):
    ast = Parser(pattern).parse()
    nfa = NFA()
    nfa.start, nfa.accept = thompson(ast, nfa)
    return nfa


def epsilon_closure(nfa, states):
    closure = set(states)
    stack = list(states)
    while stack:
        state = stack.pop()
        for target in nfa.transitions[state].get(EPSILON, ()):
            if target not in closure:
                closure.add(target)
                stack.append(target)
    return frozenset(closure)


def move(nfa, states, symbol):
    result = set()
    for state in states:
        result.update(nfa.transitions[state].get(symbol, ()))
    return result


def build_dfa(nfa):
    """Subset construction with an explicit dead state (empty subset)."""
    start = epsilon_closure(nfa, {nfa.start})
    dfa_states = [start]
    labels = {start: "D0"}
    transitions = {}
    queue = deque([start])

    while queue:
        current = queue.popleft()
        for symbol in ALPHABET:
            target = epsilon_closure(nfa, move(nfa, current, symbol))
            if target not in labels:
                labels[target] = f"D{len(labels)}"
                dfa_states.append(target)
                queue.append(target)
            transitions[(current, symbol)] = target

    accepting = {state for state in dfa_states if nfa.accept in state}
    return {
        "states": dfa_states,
        "labels": labels,
        "transitions": transitions,
        "start": start,
        "accepting": accepting,
    }


def format_nfa(nfa):
    lines = [
        "NFA 5-tuple:",
        f"Q = {{{', '.join(map(str, sorted(nfa.states)))}}}",
        "Σ = {0, 1}",
        "δ:",
    ]
    entries = []
    for source in sorted(nfa.states):
        for symbol in (EPSILON, "0", "1"):
            targets = nfa.transitions[source].get(symbol, set())
            if targets:
                entries.append(
                    f"  {source} --{symbol}--> {{{', '.join(map(str, sorted(targets)))}}}"
                )
    lines.extend(entries or ["  (no transitions)"])
    lines.extend([f"q0 = {nfa.start}", f"F = {{{nfa.accept}}}"])
    return "\n".join(lines)


def format_dfa(dfa):
    states = dfa["states"]
    labels = dfa["labels"]
    lines = [
        "DFA 5-tuple:",
        f"Q = {{{', '.join(labels[s] for s in states)}}}",
        "Σ = {0, 1}",
        "δ:",
    ]
    for state in states:
        for symbol in ALPHABET:
            target = dfa["transitions"][(state, symbol)]
            lines.append(f"  {labels[state]} --{symbol}--> {labels[target]}")
    accepting = [labels[s] for s in states if s in dfa["accepting"]]
    lines.extend([
        f"q0 = {labels[dfa['start']]}",
        f"F = {{{', '.join(accepting)}}}",
        "State mapping:",
    ])
    for state in states:
        members = ", ".join(map(str, sorted(state)))
        lines.append(f"  {labels[state]} = {{{members}}}")
    lines.append("Convention: the empty subset ∅ is included as a dead/trap state when reachable.")
    return "\n".join(lines)


def nfa_accepts(nfa, word):
    current = epsilon_closure(nfa, {nfa.start})
    for symbol in word:
        current = epsilon_closure(nfa, move(nfa, current, symbol))
    return nfa.accept in current


def dfa_accepts(dfa, word):
    current = dfa["start"]
    for symbol in word:
        current = dfa["transitions"][(current, symbol)]
    return current in dfa["accepting"]


def convert(pattern):
    nfa = build_nfa(pattern)
    dfa = build_dfa(nfa)
    return nfa, dfa


def main():
    parser = argparse.ArgumentParser(
        description="Convert a binary regular expression to an NFA and then a DFA."
    )
    parser.add_argument("regex", nargs="?", help="regular expression over {0, 1}")
    args = parser.parse_args()
    pattern = args.regex
    if pattern is None:
        try:
            pattern = input("Enter regular expression: ").strip()
        except EOFError:
            print("Error: no regular expression was provided.", file=sys.stderr)
            return 2
    try:
        nfa, dfa = convert(pattern)
    except RegexError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(format_nfa(nfa))
    print()
    print(format_dfa(dfa))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
