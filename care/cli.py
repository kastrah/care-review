"""CLI for C.A.R.E. messaging review."""

import argparse
import json
import sys
from pathlib import Path

from care.care import CAREReview


def main():
    parser = argparse.ArgumentParser(
        description="C.A.R.E. — evaluate customer-facing messages for quality",
    )
    parser.add_argument(
        "--input",
        "-i",
        type=str,
        default="-",
        help="Input file path (use '-' or omit for stdin)",
    )
    parser.add_argument(
        "--stdin",
        action="store_true",
        help="Read input from stdin (alternative to --input -)",
    )
    parser.add_argument(
        "--output",
        "-o",
        choices=["json", "md"],
        default="md",
        help="Output format",
    )

    args = parser.parse_args()

    if args.stdin or args.input == "-":
        text = sys.stdin.read()
    else:
        text = Path(args.input).read_text(encoding="utf-8")

    if not text.strip():
        print("Error: empty input", file=sys.stderr)
        sys.exit(1)

    review = CAREReview()
    result = review.evaluate(text)

    if args.output == "json":
        print(json.dumps(result, indent=2))
    else:
        _print_care_md(result)


def _print_care_md(result: dict):  # pragma: no cover
    print("# C.A.R.E. Message Review\n")
    principles_labels = {
        "C": "Conversational (Warm & Personal)",
        "A": "Actionable (Timelines & Next Steps)",
        "R": "Richer than Asked (Value-Added)",
        "E": "Engaging Dialogue (Open Closing)",
    }
    for principle in ["C", "A", "R", "E"]:
        p = result[principle]
        status = "PASS" if p["pass"] else "FAIL"
        icon = "\u2705" if p["pass"] else "\u274c"
        label = principles_labels[principle]
        print(f"## {label} \u2014 {icon} {status}\n")
        if p["issues"]:
            for issue in p["issues"]:
                print(f"- {issue}")
            print(f"\n**Fix lever:** {p['fix']}\n")
        else:
            print("No issues found.\n")
    print(f"**Verdict:** {result['verdict']}")


if __name__ == "__main__":
    main()
