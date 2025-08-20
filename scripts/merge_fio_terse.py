"""
merge_fio_terse.py

Scan one directory for *.csv files, skip any
"clock setaffinity failed: Invalid argument" lines, and
extract the single fio terse data line from each file based on
the fio terse v3 format.
Writes a merged CSV with the official fio terse v3 header.

Usage:
  python merge_fio_terse.py -p <path> -h <terse-header> -o <output>.csv
"""

import argparse
import glob
import os
import re
import sys
import pandas as pd


def iter_csv_files(paths, recursive, pattern):
    flags = "**/" + pattern if recursive else pattern
    for p in paths:
        if os.path.isdir(p):
            for f in glob.glob(os.path.join(p, flags), recursive=recursive):
                if os.path.isfile(f):
                    yield f
        elif os.path.isfile(p) and p.endswith(".csv"):
            yield p

def extract_fio_terse_line(filepath):
    """
    Return the first line that looks like a fio terse v3 data row,
    ignoring any 'clock setaffinity failed: Invalid argument' noise lines.
    """
    data_line = None
    pattern = re.compile(r"^\d+;fio-\d")  # e.g., "3;fio-3.23;..."
    with open(filepath, "r", encoding="utf-8", errors="replace") as fh:
        for raw in fh:
            line = raw.strip()
            if not line or line.startswith("clock setaffinity failed:"):
                continue
            if pattern.match(line):
                data_line = line
                break
    return data_line

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="merge_fio_terse.py",
        description="Scan a directory for *.csv, " \
            "skip noisy lines, and merge fio terse v3 rows with a standard header.",
    )
    p.add_argument(
        "-p", "--path",
        required=True,
        help="Directory containing the input *.csv files."
    )
    p.add_argument(
        "-H", "--header",
        required=True,
        help="Terse v3 header: either a path to a header file OR the header string itself."
    )
    p.add_argument(
        "-o", "--output",
        required=True,
        default="merge.csv",
        help="Output CSV file path (e.g., merged.csv)."
    )
    p.add_argument(
        "--pattern",
        default="*.csv",
        help="Filename pattern to scan inside the directory (default: *.csv)."
    )
    return p


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--path", help="The directory contains CSV files to scan")
    ap.add_argument("-H", "--header", default="fio_terse_header.csv",
                    help="The CSV file contains the header")
    ap.add_argument("-o", "--output", default="merged.csv", help="Output CSV file")
    args = ap.parse_args()


if __name__ == "__main__":
    main()
