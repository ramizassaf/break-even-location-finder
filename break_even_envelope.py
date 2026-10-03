"""
Locational break-even analysis without plotting.

Input : list of (name, FC, VC) for each alternative.
Output: the alternatives on the minimal (lower) total cost envelope for Q >= 0,
        the break-even quantities Q* between them, and the range each one wins.

Total cost of alternative i: TC_i(Q) = FC_i + VC_i * Q
Break-even between i and j:  Q*(i, j) = (FC_j - FC_i) / (VC_i - VC_j)
Complexity: O(n log n) for the sort, O(n) for the scan.

Usage:
    python break_even_envelope.py                  # runs the Fall-Line example
    python break_even_envelope.py example.csv      # CSV columns: name,fc,vc
    python break_even_envelope.py data.csv --unit gallons
"""

import argparse
import csv


def break_even(a, b):
    """Q where TC_a = TC_b. a has the higher VC."""
    return (b[1] - a[1]) / (a[2] - b[2])


def minimal_envelope(alternatives):
    # Step 1: sort by VC descending. For equal VC, lower FC first.
    alts = sorted(alternatives, key=lambda x: (-x[2], x[1]))

    stack = []
    for alt in alts:
        # Step 2: equal VC with the top -> the new one has higher FC, skip it.
        if stack and alt[2] == stack[-1][2]:
            continue
        # Step 3: new alt has lower VC. If FC is not higher, the top is
        # dominated (worse or equal on both costs). Remove the top.
        while stack and alt[1] <= stack[-1][1]:
            stack.pop()
        # Step 4: hull test. Top j sits between i (below it) and new k.
        # If k overtakes i at or before j overtakes i, j never wins. Remove j.
        while len(stack) >= 2:
            i, j = stack[-2], stack[-1]
            if break_even(i, alt) <= break_even(i, j):
                stack.pop()
            else:
                break
        stack.append(alt)

    # Step 5: break-even points between consecutive survivors.
    q_star = [break_even(stack[t], stack[t + 1]) for t in range(len(stack) - 1)]
    return stack, q_star


def report(alternatives, unit="units"):
    lines, q_star = minimal_envelope(alternatives)
    winners = {a[0] for a in lines}

    print("Total cost equations")
    for name, fc, vc in alternatives:
        print(f"  {name:<12} TC = {fc:,.0f} + {vc:,.2f} Q")

    print("\nMinimal lines (in order of increasing volume)")
    bounds = [0.0] + q_star + [float("inf")]
    for t, (name, fc, vc) in enumerate(lines):
        lo, hi = bounds[t], bounds[t + 1]
        hi_txt = "and above" if hi == float("inf") else f"to {hi:,.2f}"
        print(f"  {name:<12} best from {lo:,.2f} {hi_txt} {unit}")

    print("\nBreak-even quantities Q*")
    for t, q in enumerate(q_star):
        a, b = lines[t], lines[t + 1]
        cost = a[1] + a[2] * q
        print(f"  {a[0]} -> {b[0]}: Q* = {q:,.2f}  (TC = {cost:,.2f})")

    dropped = [a[0] for a in alternatives if a[0] not in winners]
    print("\nNever best:", ", ".join(dropped) if dropped else "none")
    return lines, q_star


def brute_force_check(alternatives, lines, q_star):
    """Confirm the winner at a test point inside each range."""
    bounds = [0.0] + q_star + [q_star[-1] * 2 + 1 if q_star else 1.0]
    for t, line in enumerate(lines):
        q = (bounds[t] + bounds[t + 1]) / 2
        best = min(alternatives, key=lambda a: a[1] + a[2] * q)
        assert best[0] == line[0], (q, best, line)


def read_csv(path):
    """Read alternatives from a CSV file with header: name,fc,vc."""
    data = []
    with open(path, newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            name = row["name"].strip()
            fc = float(row["fc"].replace(",", ""))
            vc = float(row["vc"].replace(",", ""))
            if fc < 0 or vc < 0:
                raise ValueError(f"{name}: costs must be zero or positive")
            data.append((name, fc, vc))
    if not data:
        raise ValueError("The CSV file has no alternatives")
    return data


EXAMPLE = [
    ("Aspen",      8_000_000, 250),
    ("Boyne City", 2_400_000, 130),
    ("Portland",   3_400_000,  90),
    ("Lake Tahoe", 4_500_000,  65),
]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Locational break-even analysis")
    parser.add_argument("csv", nargs="?", help="CSV file with columns name,fc,vc")
    parser.add_argument("--unit", default=None, help="volume unit label, e.g. pairs")
    args = parser.parse_args()

    if args.csv:
        data, unit = read_csv(args.csv), args.unit or "units"
    else:
        data, unit = EXAMPLE, args.unit or "pairs"

    lines, q = report(data, unit=unit)
    brute_force_check(data, lines, q)
    print("\nCheck against brute force: passed")
