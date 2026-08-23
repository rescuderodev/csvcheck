import csv
import re
from dataclasses import dataclass
from datetime import date


def _is_int(v):
    try:
        int(v)
        return True
    except ValueError:
        return False


def _is_float(v):
    try:
        float(v)
        return True
    except ValueError:
        return False


def _is_date(v):
    try:
        date.fromisoformat(v)
        return True
    except ValueError:
        return False


TYPES = {"str": lambda v: True, "int": _is_int, "float": _is_float, "date": _is_date}


@dataclass
class Problem:
    row: int
    column: str
    message: str

    def __str__(self):
        return f"row {self.row}, {self.column}: {self.message}"


def check(fh, schema):
    """Returns the list of problems found in the CSV."""
    columns = schema.get("columns", {})
    reader = csv.DictReader(fh)
    problems = []
    header = reader.fieldnames or []
    for name, rules in columns.items():
        if name not in header and rules.get("required", True):
            problems.append(Problem(1, name, "missing column"))
    for i, row in enumerate(reader, start=2):
        for name, rules in columns.items():
            if name not in row:
                continue
            value = (row[name] or "").strip()
            if not value:
                if rules.get("required", True):
                    problems.append(Problem(i, name, "empty"))
                continue
            t = rules.get("type", "str")
            if not TYPES[t](value):
                problems.append(Problem(i, name, f"not a valid {t}: {value!r}"))
                continue
            if "allowed" in rules and value not in rules["allowed"]:
                problems.append(Problem(i, name, f"{value!r} not in {rules['allowed']}"))
            if "regex" in rules and not re.fullmatch(rules["regex"], value):
                problems.append(Problem(i, name, f"{value!r} does not match {rules['regex']}"))
    return problems
