"""Literal numerical-cipher decoder: caller supplies permitted inputs.

No AI, network, inferred digit corrections, or accepted number splits.
Python 3.9+; standard library only. Prints JSON without modifying inputs.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re

STOP = "## IMG_R4284_I25751_P_hi.jpeg right"


def read_key(path):
    key = json.loads(path.read_text(encoding="utf-8-sig"))["alphabet"]
    if not isinstance(key, dict) or not key:
        raise ValueError("alphabet must be a nonempty object")
    for value, letter in key.items():
        if not re.fullmatch(r"[1-9][0-9]*", value) or not 1 <= int(value) <= 108:
            raise ValueError("Alphabet values must be canonical numbers from 1 to 108")
        if not isinstance(letter, str) or not letter:
            raise ValueError("Alphabet labels must be nonempty strings")
    return key


def partitions(digits, key):
    if not digits:
        return [[]]
    return [
        [digits[:size]] + rest
        for size in range(1, min(3, len(digits)) + 1)
        if digits[:size] in key
        for rest in partitions(digits[size:], key)
    ]


def render(token, key):
    if token.startswith("["):
        return " " + token + " "
    return key.get(token, "<" + token + ">") if "?" not in token else "<" + token + ">"


def decode(text, key):
    counts = Counter()
    lines = []
    unresolved = []
    for number, raw in enumerate(text.splitlines(), 1):
        if raw.startswith(STOP):
            break
        if not raw.strip() or raw.startswith("#"):
            continue
        cleaned = re.sub(r"\([^)]*\)", "", raw)
        tokens = re.findall(r"\[[^]]*\]|\d+\?*|\?+", cleaned)
        residue = re.sub(r"\[[^]]*\]|\d+\?*|\?+", "", cleaned)
        if re.sub(r"[\s,;.:]", "", residue):
            raise ValueError("Unsupported notation on input line " + str(number))
        for position, token in enumerate(tokens, 1):
            if token.startswith("["):
                category = "clear_spans"
            elif "?" in token:
                category = "uncertain_numeric"
            elif token in key:
                category = "assigned_numeric"
            else:
                category = "unresolved_numeric"
            counts[category] += 1
            if category in ("uncertain_numeric", "unresolved_numeric"):
                # Long or damaged inputs are not recursively partitioned.
                candidates = partitions(token, key) if token.isdigit() and len(token) <= 8 else []
                unresolved.append({
                    "line": number, "position_including_clear_spans": position,
                    "raw": token, "classification": "unresolved",
                    "exact_partitions": [parts for parts in candidates if len(parts) > 1],
                    "note": "Alternatives only; not applied. Uncertain or >8-digit tokens not partitioned.",
                })
        lines.append({
            "line": number, "tokens": tokens,
            "literal": "".join(render(token, key) for token in tokens),
        })
    denominator = sum(n for category, n in counts.items() if category != "clear_spans")
    return {
        "counts": dict(counts),
        "numeric_denominator": denominator,
        "alphabet_coverage": counts["assigned_numeric"] / denominator if denominator else None,
        "accuracy": None,
        "note": "Coverage is not accuracy. This tool does not reproduce the retrospective shuffled controls.",
        "lines": lines, "unresolved": unresolved,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--transcription", type=Path, required=True)
    parser.add_argument("--key", type=Path, required=True)
    args = parser.parse_args()
    report = decode(args.transcription.read_text(encoding="utf-8-sig"), read_key(args.key))
    report["input_sha256"] = {
        label: hashlib.sha256(path.read_bytes()).hexdigest()
        for label, path in (("transcription", args.transcription), ("key", args.key))
    }
    print(json.dumps(report, indent=2, ensure_ascii=True))


if __name__ == "__main__":
    main()
