import argparse
import sys
import tomllib

from .check import check


def main(argv=None):
    parser = argparse.ArgumentParser(prog="csvcheck", description="Check a CSV file against a schema")
    parser.add_argument("csv")
    parser.add_argument("-s", "--schema", required=True, help="TOML file with the columns")
    args = parser.parse_args(argv)

    with open(args.schema, "rb") as f:
        schema = tomllib.load(f)
    with open(args.csv, newline="", encoding="utf-8-sig") as f:
        problems = check(f, schema)
    for p in problems:
        print(p)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
